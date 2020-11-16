import boto3
import yaml
from time import sleep
import logging
import argparse
import re

def run(aws_region):
    logformat = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level='INFO', format=logformat)
    logger = logging.getLogger('ami_create')

    with open ('amis/ami_orig.yml','r') as f:
        ami_dict = yaml.safe_load(f)

    obj_list = []

    for ami in ami_dict.keys():
        logger.info(f"Creating EC2 image ami_create_tmp-{ami_dict[ami]['name']}")
        # Creating temporary EC2 instance
        ec2_ohio = boto3.resource('ec2', region_name='us-east-2')
        instances = ec2_ohio.create_instances(
            ImageId=ami_dict[ami]['id'], 
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            Placement={'AvailabilityZone': 'us-east-2a'},
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': f"ami_create_tmp-{ami_dict[ami]['name']}"
                        },
                    ]
                },
            ]

        )

        logger.info(f"Waiting for ami_create_tmp-{ami_dict[ami]['name']} to start")
        # Wait for instance to move to running state
        instances[0].wait_until_running()

        # Creating AMI from the temporary EC2 instance
        for instance in instances:
            
            if aws_region == 'us-east-2':
                logger.info(f"Creating AMI {ami_dict[ami]['name']}")
                image_obj = instance.create_image(
                Description=ami_dict[ami]['name'],
                Name=ami_dict[ami]['name']
                )
            else:
                logger.info(f"Creating AMI ami_create_tmp-{ami_dict[ami]['name']}")
                image_obj = instance.create_image(
                Description=f"ami_create_tmp-{ami_dict[ami]['name']}",
                Name=f"ami_create_tmp-{ami_dict[ami]['name']}"
                )

            obj_list.append((instances[0], image_obj))
            ami_dict[ami]['new_id'] = image_obj.id

    # Loop through list of instances and associated images
    # Wait for the image to be 'available' state and then
    # terminate the instance
    for inst_obj, image_obj in obj_list:
        logger.info(f"Waiting for image {image_obj.name} to become available")
        while image_obj.state == 'pending':
            image_obj.load()
            logger.info(f"{image_obj.name}: {image_obj.state}")
            sleep(5)
        logger.info(f"{image_obj.name}: {image_obj.state}")
        inst_name = inst_obj.tags[0]['Value']
        logger.info(f"Terminating instance {inst_name}")
        inst_obj.terminate()

    # If using other region besides us-east-2, copy to dest region then delete from us-east-2
    if aws_region != 'us-east-2':
        ohio_amis = []
        dest_region_amis = []
        # copy newly created AMIs to destination region
        for key in ami_dict.keys():
            logger.info(f"Copying AMI {ami_dict[key]['name']} to region {aws_region}")
            dest_region = boto3.client('ec2', region_name=aws_region)
            copy_response = dest_region.copy_image(
                Name=ami_dict[key]['name'],
                Description='Tetration Virtual Bootcamp Lab',
                SourceImageId=ami_dict[key]['new_id'],
                SourceRegion='us-east-2'
            )
            image = ec2_ohio.Image(ami_dict[key]['new_id'])
            ohio_amis.append(image)
            ami_dict[key]['new_id'] = copy_response['ImageId']
            dest_region_amis.append(copy_response['ImageId'])

        # wait for images to be successfully copied in dest region
        for image_id in dest_region_amis:
            ec2_dest_region = boto3.resource('ec2', region_name=aws_region)
            image = ec2_dest_region.Image(image_id)
            logger.info(f"Checking state of AMI {image.name} in region {aws_region}")
            while image.state == 'pending':
                image.load()
                logger.info(f"{image.name}: {image.state}")
                sleep(5)
        
        # deregistering and deleting snapshots in Ohio
        for image_obj in ohio_amis:
            logger.info(f"Deregistering AMI {image_obj.name} from region us-east-2")
            image_obj.load()
            snapshot_id = image_obj.block_device_mappings[0]['Ebs']['SnapshotId']
            image_obj.deregister()
            logger.info(f"Deleting snapshot {snapshot_id} from region us-east-2" )
            snapshot = ec2_ohio.Snapshot(snapshot_id)
            snapshot.delete()     
        
    ami_dict['employee_ubuntu_ami'] = dict(new_id=ami_dict['employee_sysadmin_ubuntu_ami']['new_id'])
    ami_dict['sysadmin_ubuntu_ami'] = dict(new_id=ami_dict['employee_sysadmin_ubuntu_ami']['new_id'])
    ami_dict.pop('employee_sysadmin_ubuntu_ami')

    # Parse YAML file of valid EKS worker nodes and update parameters.yml
    def ami_lookup(yaml_file):
        with open(yaml_file, 'r') as f:
            amis = yaml.safe_load(f)
        return amis.get(aws_region)

    ami_dict['eks_worker_ami'] = dict(new_id=ami_lookup('amis/eks_worker_amis.yml'))
    ami_dict['asav_ami'] = dict(new_id=ami_lookup('amis/asav_amis.yml'))

        
    logger.info(f"Creating file {aws_region}-ami-ids.yml")

    with open(f"{aws_region}-ami-ids.yml", 'w') as f:  
        for ami_key in ami_dict.keys():
            f.write(f"{ami_key}: {ami_dict[ami_key]['new_id']}\n")
       
    # for ami_key in ami_dict.keys():
    #     replaced = False
    #     for x, line in enumerate(params_file):
    #         if ami_key in line:
    #             params_file[x] = f"{ami_key}: {ami_dict[ami_key]['new_id']}\n"
    #             replaced = True
    #         if 'aws_region' in line:
    #             params_file[x] = f"aws_region: {aws_region}\n"
    #         if x == len(params_file) - 1 and not replaced:
    #             params_file.append(f"{ami_key}: {ami_dict[ami_key]['new_id']}\n")


    logger.info(f"New AMIs written to {aws_region}-ami-ids.yml")
    for ami in ami_dict.keys():
        print(f"{ami}: {ami_dict[ami]['new_id']}")

    s3 = boto3.resource('s3', region_name=aws_region)
    arn = boto3.resource('iam').CurrentUser().arn
    ACCT_ID = re.search('[0-9]+', arn).group()
    S3_BUCKET = f"n0work-{ACCT_ID}"
    logger.info(f"Uploading AMI file {aws_region}-ami-ids.yml to S3 bucket {S3_BUCKET}")
    s3.meta.client.upload_file(f"{aws_region}-ami-ids.yml", S3_BUCKET, f"{aws_region}-ami-ids.yml")

    logger.info("AMI create finished successfully!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create AMIs and copy to destination region")

    parser.add_argument('--region', '-r', required=True, help="AWS Region")
    args = parser.parse_args()

    aws_region = args.region
    run(aws_region)
