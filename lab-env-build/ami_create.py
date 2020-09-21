import boto3
import yaml
from time import sleep
import logging
import random

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
        if x == len(params_file) - 1 and not replaced:
            params_file.append(f"{ami_key}: {ami_dict[ami_key]['new_id']}\n")

with open('parameters.yml', 'w') as f:
    f.writelines(params_file)

logger.info("Finished!")        

