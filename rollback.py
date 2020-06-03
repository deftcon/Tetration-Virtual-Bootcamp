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
VPC_ID = params['vpc_id']
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
# Verify VPC Id Provided ##############################################
#######################################################################
try:
    print(f'INFO: Checking VPC ID: {VPC_ID}...')
    ec2 = session.resource('ec2')
    vpc = ec2.Vpc(VPC_ID)
    print(f'INFO: VPC ID Verified: {vpc.vpc_id}...')
except:
    print(f'ERROR: VPC Check Failed! Please provide a valid VPC Id...')
    exit(1)
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
        exit(1)
    
    if len(secondary_ips) < STUDENT_COUNT:
        print(f'ERROR: Number Of Required Secondary Subnets Are {STUDENT_COUNT} But Only {len(secondary_ips)} Are Available...')
        exit(1)

except:
    print(f'ERROR: Invalid Subnet! Please provide a valid subnet range...')
    exit(1)
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
    exit(1)
print(f'INFO: Student Accounts Collection Created...')
#######################################################################


#######################################################################
# Confirm Destroy Before Proceeding ###################################
#######################################################################
print(f'You are about to DESTROY all student pod(s) in {VPC_ID} in the {REGION} Region')
rusure_response1 = input('Are you sure you wish to destory all of these pods (type "Y" to continue)? ')
if rusure_response1 == 'Y':
    rusure_response2 = input('ARE YOU ABSOLUTELY SURE (type "YES" to continue)? ')
    if rusure_response2 != 'YES':
        print('No pods were destroyed, exiting now.')
        exit(1)
else:
    print('No pods were destroyed, exiting now.')
    exit(1)
#######################################################################


#######################################################################
# Delete VPC Flow Logs S3 Bcukets #####################################
#######################################################################
print(f'INFO: Initializing VPC Flow Logs S3 Bucket Deletion...')
for student in STUDENTS_LIST:

    bucket_name = ''

    try:

        cloudformation = session.client('cloudformation')

        result = cloudformation.describe_stacks(
            StackName=student['account_name']
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

        client = session.client('elb')

        eks_elbs = client.describe_load_balancers()['LoadBalancerDescriptions']

        if (len(eks_elbs) < 1):
            continue

        elb_tags = client.describe_tags(
            LoadBalancerNames=list(map(lambda e: e['LoadBalancerName'], eks_elbs))
        )

        for elb in elb_tags['TagDescriptions']:
            for tag in elb['Tags']:
                for key in tag:
                    if student['account_name'] in tag[key]:
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


#######################################################################
# Delete Students POD In CloudFormation ###############################
#######################################################################
print('INFO: Commencing CloudFormation Stack Deletion...')
for student in STUDENTS_LIST:

    try:

        cloudformation = session.client('cloudformation')

        result = cloudformation.delete_stack(
            StackName=student['account_name']
        )

        print(f"INFO: Stack Deleted: {student['account_name']}...")

        STACKS_LIST.append(student['account_name'])

    except Exception as e:
        print('WARN: ', e)
print('INFO: CloudFormation Stacks Deletion Complete...')
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