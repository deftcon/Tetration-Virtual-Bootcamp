import yaml
import boto3
import ipaddress
import string
import random
import time
import re
import collections
import csv
import os
import json
import urllib
import sys
from datetime import datetime

PARAMETERS_FILE = './parameters.yml'

params = yaml.load(open(PARAMETERS_FILE), Loader=yaml.Loader)

ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

if ACCESS_KEY == None or ACCESS_KEY == '':
    ACCESS_KEY = params['aws_access_key']

if SECRET_KEY == None or SECRET_KEY == '':
    SECRET_KEY = params['aws_secret_key']

REGION = params['aws_region']
# VPC_ID = params['vpc_id']
SUBNET_RANGE_PRIMARY = params['subnet_range_primary']
SUBNET_RANGE_SECONDARY = params['subnet_range_secondary']
STUDENT_COUNT = params['student_count']
STUDENT_PREFIX = params['student_prefix']

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)

STUDENTS_LIST = []
STACKS_LIST = []

#######################################################################
# Retrieve VPC_ID ##############################################
#######################################################################
try:
    print(f'INFO: Retrieving VPC_ID...')
    ec2 = session.resource('ec2', region_name=REGION)
#    vpc = ec2.Vpc(VPC_ID)
    vpcs = list(ec2.vpcs.all())
    VPC_ID = None
    for vpc in vpcs:
        if vpc.tags:
            for tag in vpc.tags:
                name = tag.get('Value')
                if name == 'Tetration HoL':
                    answer = input(f"Do you want to delete the lab environment for VPC {vpc.id} (Y/N)? ")
                    if answer.upper() == 'Y':
                        VPC_ID = vpc.id
                        break
        if VPC_ID:
            break
                        
    if not VPC_ID:
        print('ERROR: No VPCs selected for deletion')
        sys.exit(1)
                                       
    print(f'INFO: VPC ID: {VPC_ID}')
except Exception as e:
    print(f'ERROR: While retrieving VPC_ID {e}')
    sys.exit(1)

NAMING_SUFFIX = VPC_ID[-6:]
#######################################################################


#######################################################################
# Calculate & Verify Subnet Range #####################################
#######################################################################
try:
    print(f'INFO: Validating Subnet Range...')
    primary_ips = list(ipaddress.ip_network(SUBNET_RANGE_PRIMARY).hosts())
    secondary_ips = list(ipaddress.ip_network(SUBNET_RANGE_SECONDARY).hosts())

    primary_ips = list(set(list(map(lambda ip: str(re.sub(r'([0-9]+)$', '0', str(ip))), primary_ips))))
    secondary_ips = list(set(list(map(lambda ip: str(re.sub(r'([0-9]+)$', '0', str(ip))), secondary_ips))))

    print(f'INFO: {len(primary_ips)} Subnets Are Available...')

    if len(primary_ips) < (STUDENT_COUNT * 2):
        print(f'ERROR: Number Of Required Primary Subnets Are {STUDENT_COUNT * 2} But Only {len(primary_ips)} Are Available...')
        sys.exit(1)
    
    if len(secondary_ips) < STUDENT_COUNT:
        print(f'ERROR: Number Of Required Secondary Subnets Are {STUDENT_COUNT} But Only {len(secondary_ips)} Are Available...')
        sys.exit(1)

except:
    print(f'ERROR: Invalid Subnet! Please provide a valid subnet range...')
    sys.exit(1)
print(f'INFO: Subnet Range Validation Completed...')
#######################################################################


#######################################################################
# Discover Student Accounts ###########################################
#######################################################################
try:
    print(f'INFO: Creating Student Accounts Collection...')
    primary_ips = list(ipaddress.ip_network(SUBNET_RANGE_PRIMARY).hosts())
    secondary_ips = list(ipaddress.ip_network(SUBNET_RANGE_SECONDARY).hosts())

    primary_ips = list(collections.OrderedDict.fromkeys(list(map(lambda ip: str(re.sub(r'([0-9]+)$', '0', str(ip))), primary_ips))))
    secondary_ips = list(collections.OrderedDict.fromkeys(list(map(lambda ip: str(re.sub(r'([0-9]+)$', '0', str(ip))), secondary_ips))))

    public_subnet_01 = primary_ips[:len(primary_ips)//2]
    public_subnet_02 = primary_ips[len(primary_ips)//2:]

    for i in range(STUDENT_COUNT):
        STUDENTS_LIST.append({
            'account_name': f'{STUDENT_PREFIX}-0{i}',
            'public_subnet_01': f'{public_subnet_01[i]}',
            'public_subnet_02': f'{public_subnet_02[i]}',
            'private_subnet': f'{secondary_ips[i]}'
        })

    print(f'INFO: {STUDENTS_LIST}')

except:
    print(f'ERROR: Invalid Subnet! Please provide a valid subnet range...')
    sys.exit(1)
print(f'INFO: Student Accounts Collection Created...')
#######################################################################


#######################################################################
# Confirm Destroy Before Proceeding ###################################
#######################################################################
print(f'You are about to DESTROY all student pod(s) in {VPC_ID} in the {REGION} Region')
rusure_response1 = input('Are you sure you wish to destroy all of these pods (type "Y" to continue)? ')
if rusure_response1 == 'Y':
    rusure_response2 = input('ARE YOU ABSOLUTELY SURE (type "YES" to continue)? ')
    if rusure_response2 != 'YES':
        print('No pods were destroyed, sys.exiting now.')
        sys.exit(1)
else:
    print('No pods were destroyed, sys.exiting now.')
    sys.exit(1)

#######################################################################
# EIP de-association and un-allocation
#######################################################################
instance_ids = []
for student in STUDENTS_LIST:
# Look up Guac and Tet-ingest instance IDs
    ec2 = session.client('ec2',region_name=REGION)
    reservations = ec2.describe_instances()['Reservations']
    for reservation in reservations:
        instances = reservation['Instances']
        for instance in instances:
            if instance['VpcId'] == VPC_ID:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':                   
                        if student['account_name'] in tag['Value'] and 'guac' in tag['Value']:
                            instance_ids.append(instance['InstanceId'])
                        elif student['account_name'] in tag['Value'] and 'tet-data' in tag['Value']:
                            instance_ids.append(instance['InstanceId'])

# Loop through all EIPs and release the ones associated with the instance IDs 
addresses_dict = ec2.describe_addresses()
for address in addresses_dict['Addresses']:
    instance_id = address.get('InstanceId')
    if instance_id:
        if instance_id in instance_ids:
            print(f"INFO: Disassociating EIP {address['PublicIp']} from instance {address['InstanceId']}")
            ec2.disassociate_address(PublicIp=address['PublicIp'])
            print(f"INFO: Releasing EIP {address['PublicIp']}")
            ec2.release_address(AllocationId=address['AllocationId'])

#######################################################################
# Delete VPC Flow Logs S3 Buckets #####################################
#######################################################################
print(f'INFO: Initializing VPC Flow Logs S3 Bucket Deletion...')
for student in STUDENTS_LIST:

    bucket_name = ''

    try:

        cloudformation = session.client('cloudformation')

        result = cloudformation.describe_stacks(
            StackName=f"{student['account_name']}-{NAMING_SUFFIX}"
        )

        bucket_name = list(filter(lambda o: o['OutputKey'] == 'CiscoHOLVPCFlowLogBucket', result['Stacks'][0]['Outputs']))[0]['OutputValue']

        s3 = session.resource('s3')
        bucket = s3.Bucket(bucket_name)
        bucket.objects.all().delete()
        bucket.delete()

        print(f'INFO: S3 Bucket Deleted: {bucket_name}')

    except Exception as e:

        if 'does not exist' in str(e):
            print(f'INFO: S3 Bucket {bucket_name} Does Not Exist...')
        else:
            print('WARN: ', e)

print(f'INFO: S3 Bucket Deletion Complete...')
#######################################################################


#######################################################################
# Delete EKS Load Balancers ###########################################
#######################################################################
print('INFO: Initializing EKS Load Balancers Deletion...')
for student in STUDENTS_LIST:

    try:

        client = session.client('elb', region_name=REGION)

        eks_elbs = client.describe_load_balancers()['LoadBalancerDescriptions']

        if (len(eks_elbs) < 1):
            continue

        elb_tags = client.describe_tags(
            LoadBalancerNames=list(map(lambda e: e['LoadBalancerName'], eks_elbs))
        )

        for elb in elb_tags['TagDescriptions']:
            for tag in elb['Tags']:
                for key in tag:
                    if NAMING_SUFFIX in tag[key]:
                        elb_list = list(filter(lambda e: e['LoadBalancerName'] == elb['LoadBalancerName'], eks_elbs))
                        if (len(elb_list) > 0):
                            client.delete_load_balancer(
                                LoadBalancerName=elb_list[0]['LoadBalancerName']
                            )
                            print(f"INFO: ELB Deleted: {elb_list[0]['LoadBalancerName']}...")
                            break
        
    except Exception as e:
        print('WARN: ', e)
        
print(f'INFO: EKS Load Balancers Deletion Complete...')
#######################################################################
# Delete class schedule
#######################################################################
print(f'INFO: Deleting the class schedule')
try:
    cloudformation = session.client('cloudformation')

    result = cloudformation.delete_stack(
        StackName=f'tethol-class-schedule-{NAMING_SUFFIX}'
    )
except Exception as e:
    print('WARN: ', e)
print(f"INFO: Deleted class schedule tethol-class-schedule-{NAMING_SUFFIX}")

#######################################################################
# Delete Students POD In CloudFormation ###############################
#######################################################################
print('INFO: Commencing CloudFormation Stack Deletion...')
for student in STUDENTS_LIST:

    try:

        cloudformation = session.client('cloudformation')

        result = cloudformation.delete_stack(
            StackName=f"{student['account_name']}-{NAMING_SUFFIX}"
        )

        print(f"INFO: Stack deletion initiated for: {student['account_name']}-{NAMING_SUFFIX}...")

        STACKS_LIST.append(f"{student['account_name']}-{NAMING_SUFFIX}")

    except Exception as e:
        print('WARN: ', e)
print(f"INFO: CloudFormation deletion initiated for {student['account_name']}-{NAMING_SUFFIX}...")
#######################################################################


#######################################################################
# Wait For Stack Deletion #############################################
#######################################################################
deleted_stacks = []
while True:

    try:

        for stack_name in STACKS_LIST:

            if stack_name in deleted_stacks:
                continue

            cloudformation = session.client('cloudformation')

            status = {}

            try:
                status = cloudformation.describe_stacks(
                    StackName=stack_name
                )
            except:
                deleted_stacks.append(stack_name)
                print(f'WARN: {stack_name} Does Not Exist...')
                continue

            print(f"INFO: StackName: {stack_name}, Status: {status['Stacks'][0]['StackStatus']}")

        if len(STUDENTS_LIST) == len(deleted_stacks):
            print('INFO: CloudFormation Rollback Completed Successfully...')
            break

        time.sleep(10)

    except Exception as e:
        print('WARN: ', e)

#######################################################################
# Detach and Delete the Internet Gateway
#######################################################################
try:
    print(f'INFO: Retrieve Internet Gateways')
    ec2 = session.resource('ec2')
    igs = list(ec2.internet_gateways.all())
    for ig in igs:
        if ig.tags:
            for tag in ig.tags:
                if tag.get('Key') == 'Name':
                    name = tag.get('Value')
                    if name == 'Tetration HoL':
                        attached_vpc_id = ig.attachments[0]['VpcId']
                        if attached_vpc_id == VPC_ID:
                            print(f'INFO: Detaching Internet Gateway {ig.id} from {attached_vpc_id}')
                            ig.detach_from_vpc(VpcId=attached_vpc_id)
                            print(f'INFO: Deleting Internet Gateway {ig.id}')
                            ig.delete()
except Exception as e:
    print(f'ERROR: While deleting Internet Gateway {e}')
    sys.exit(1)



#######################################################################
# Delete the VPC (and any associated Security Groups)
#######################################################################
try:
    print(f'INFO: Retrieve VPCs')
    ec2 = session.resource('ec2')
    vpcs = list(ec2.vpcs.all())
    for vpc in vpcs:
        if vpc.id == VPC_ID:
            if vpc.tags:
                for tag in vpc.tags:
                    if tag.get('Key') == 'Name':
                        name = tag.get('Value')
                        if name == 'Tetration HoL':
                            sgs = vpc.security_groups.all()
                            for sg in sgs:
                                if not sg.group_name == 'default':
                                    print(f'INFO: Deleting security group {sg.id}')
                                    sg.delete()
                            print(f'INFO: Deleting vpc {vpc.id}')
                            vpc.delete()

except Exception as e:
    print(f'ERROR: While deleting VPC_ID {e}')
    sys.exit(1)

#######################################################################
# Empty and delete the S3 bucket
#######################################################################

try:
    s3 = session.resource('s3')
    bucket = s3.Bucket(f'tetration-hol-cft-template-{NAMING_SUFFIX}')
    bucket.objects.all().delete()
    bucket.delete()
    print(f'INFO: Deleted S3 bucket tetration-hol-cft-template-{NAMING_SUFFIX}')
except Exception as e:
    print(f'ERROR: While deleting S3 Bucket tetration-hol-cft-template-{NAMING_SUFFIX}:  {e}')
    sys.exit(1)

print('INFO: Rollback completed successfully!')