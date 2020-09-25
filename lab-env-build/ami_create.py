import boto3
import yaml
from time import sleep
import logging
import argparse

parser = argparse.ArgumentParser(description="Create AMIs and copy to destination region")

parser.add_argument('--region', '-r', required=True, help="AWS Region")
args = parser.parse_args()

aws_region = args.region


logformat = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level='INFO', format=logformat)
logger = logging.getLogger('ami_create')

with open ('ami_orig.yml','r') as f:
    ami_dict = yaml.safe_load(f)

obj_list = []

for ami in ami_dict.keys():
    logger.info(f"Creating EC2 image {ami_dict[ami]['name']}")
    # Creating temporary EC2 instance
    ec2 = boto3.resource('ec2')
    instances = ec2.create_instances(
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
                        'Value': f"tmp-{ami_dict[ami]['name']}"
                    },
                ]
            },
        ]

    )

    logger.info(f"Waiting for {ami_dict[ami]['name']} to start")
    # Wait for instance to move to running state
    instances[0].wait_until_running()

    # Creating AMI from the temporary EC2 instance
    for instance in instances:
        logger.info(f"Creating AMI {ami_dict[ami]['name']}")
        image_obj = instance.create_image(
            Description=ami_dict[ami]['name'],
            Name=ami_dict[ami]['name']
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
    inst_name = inst_obj.tags[0]['Value']
    logger.info(f"Terminating instance {inst_name}")
    inst_obj.terminate()

# If using other region besides us-east-2, copy to dest region then delete from us-east-2
if aws_region != 'us-east-2':
    # copy newly created AMIs to destination region
    for key in ami_dict.keys():
        logger.info(f"Copying AMI {ami_dict[key]['id']} to region {aws_region}")
        dest_region = boto3.client('ec2', region_name=aws_region)
        copy_response = dest_region.copy_image(
            Name=ami_dict[key]['name'],
            Description='Tetration Virtual Bootcamp Lab',
            SourceImageId=ami_dict[key]['new_id'],
            SourceRegion='us-east-2'
        )
        ec2 = boto3.resource('ec2')
        image = ec2.Image(ami_dict[key]['new_id'])
        image.deregister()
        logger.info(f"Deregistering AMI {ami_dict[key]['id']} from region us-east-2")
        ami_dict[key]['new_id'] = copy_response['ImageId']


ami_dict['employee_ubuntu_ami'] = dict(new_id=ami_dict['employee_sysadmin_ubuntu_ami']['new_id'])
ami_dict['sysadmin_ubuntu_ami'] = dict(new_id=ami_dict['employee_sysadmin_ubuntu_ami']['new_id'])
ami_dict.pop('employee_sysadmin_ubuntu_ami')


logger.info("AMIs to be updated in parameters.yml")
for ami in ami_dict.keys():
    print(f"{ami}: {ami_dict[ami]['new_id']}")
      
logger.info("Updating parameters.yml")

with open('parameters.yml', 'r') as f:
    params_file = f.readlines()

for ami_key in ami_dict.keys():
    replaced = False
    for x, line in enumerate(params_file):
        if ami_key in line:
            params_file[x] = f"{ami_key}: {ami_dict[ami_key]['new_id']}\n"
            replaced = True
        if 'aws_region' in line:
            params_file[x] = f"aws_region: {aws_region}\n"
        if x == len(params_file) - 1 and not replaced:
            params_file.append(f"{ami_key}: {ami_dict[ami_key]['new_id']}\n")

# Parse list of valid EKS worker nodes and update parameters.yml
with open ('eks_worker_amis.yml', 'r') as f:
    eks_amis = yaml.safe_load(f)

params_file.append(f"{aws_region}: {eks_amis.get(aws_region)}")
logger.info(f"EKS image for region {aws_region} is {eks_amis.get(aws_region)}")




with open('parameters.yml', 'w') as f:
    f.writelines(params_file)

logger.info("Finished!")