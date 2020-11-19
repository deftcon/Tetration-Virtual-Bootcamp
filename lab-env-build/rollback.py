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
import requests
from datetime import datetime

ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

#######################################################################
# Rollback selection from state files on S3 ###########################
#######################################################################

arn = boto3.resource('iam').CurrentUser().arn
ACCT_ID = re.search('[0-9]+', arn).group()
S3_BUCKET = f"n0work-{ACCT_ID}"
s3 = boto3.resource('s3')
bucket = s3.Bucket(name=S3_BUCKET)
objects = list(bucket.objects.iterator())
object_dict = {}
count = 1
for obj in objects:
   if 'state' in obj.key:
        object_dict[str(count)] = {'filename': obj.key, 'metadata': obj.get()['Metadata']}
        count += 1
while True:
    print("{0:<10} {1:<25} {2:<15} {3:<25} {4:<25} {5:<20} {6:<25}".format('SELECTION', 'SESSION', 'REGION', 'VPC', 'SCHEDULE', 'CREATED', 'CREATED BY'))
    for key in object_dict.keys():
        session_name = object_dict[key]['metadata']['session_name']
        region = object_dict[key]['metadata']['region']
        vpc = object_dict[key]['metadata']['vpcid']
        schedule = object_dict[key]['metadata']['schedule']
        created = object_dict[key]['metadata']['created_date']
        created_by = object_dict[key]['metadata']['created_by']
        print(f"{key:<10} {session_name:<25} {region:<15} {vpc:<25} {schedule:<25} {created:<20} {created_by:<25}")
    print('\n')
    answer = input("Please select the number corresponding to the deployment you would like to roll back: ")
    if answer in object_dict.keys():
        STATE_FILE = object_dict[answer]['filename']
        break
   
def read_s3_contents(bucket_name, key):
    response = s3.Object(bucket_name, key).get()
    return response['Body'].read()

params = yaml.safe_load(read_s3_contents(S3_BUCKET, STATE_FILE))

if ACCESS_KEY == None or ACCESS_KEY == '':
    ACCESS_KEY = params['aws_access_key']

if SECRET_KEY == None or SECRET_KEY == '':
    SECRET_KEY = params['aws_secret_key']

API_GATEWAY_URL = "https://fh3aao7bri.execute-api.us-east-1.amazonaws.com/prod"
API_GATEWAY_KEY = "iBO39NUUc1401nMYkNWvM1jbA4YAHhKD1z4wpIlh"

# if not API_GATEWAY_URL:
#     print('ERROR: You must define the environment variable API_GATEWAY_URL. See the README.md for details')
#     sys.exit(1)
# if not API_GATEWAY_KEY:
#     print('ERROR: You must define the environment variable API_GATEWAY_KEY. See the README.md for details')
#     sys.exit(1)


REGION = params['aws_region']
VPC_ID = params['vpc_id']
SUBNET_RANGE_PRIMARY = params['subnet_range_primary']
SUBNET_RANGE_SECONDARY = params['subnet_range_secondary']
POD_COUNT = params['pod_count']
POD_PREFIX = 'pod'
SESSION_NAME = params['session_name']

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)

PODS_LIST = []
STACKS_LIST = []

#######################################################################
# Retrieve VPC_ID ##############################################
#######################################################################
# try:
#     print(f'INFO: Retrieving VPC_ID...')
#     ec2 = session.resource('ec2', region_name=REGION)
#     vpcs = list(ec2.vpcs.all())
#     VPC_ID = None
#     for vpc in vpcs:
#         if vpc.tags:
#             for tag in vpc.tags:
#                 name = tag.get('Value')
#                 if name == 'Tetration HoL':
#                     print(f"INFO: Found VPC {vpc.id} with tag 'Tetration HoL'")
#                     answer = input(f"Do you want to delete the lab environment for VPC {vpc.id} (Y/N)? ")
#                     if answer.upper() == 'Y':
#                         VPC_ID = vpc.id
#                         break
#         if VPC_ID:
#             break
                        
#     if not VPC_ID:
#         print('ERROR: No VPCs selected for deletion')
#         sys.exit(1)
                                       
#     print(f'INFO: VPC ID: {VPC_ID}')
# except Exception as e:
#     print(f'ERROR: While retrieving VPC_ID {e}')
#     sys.exit(1)

# SESSION_NAME = VPC_ID[-6:]
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

    if len(primary_ips) < (POD_COUNT * 2):
        print(f'ERROR: Number Of Required Primary Subnets Are {POD_COUNT * 2} But Only {len(primary_ips)} Are Available...')
        sys.exit(1)
    
    if len(secondary_ips) < POD_COUNT:
        print(f'ERROR: Number Of Required Secondary Subnets Are {POD_COUNT} But Only {len(secondary_ips)} Are Available...')
        sys.exit(1)

except:
    print(f'ERROR: Invalid Subnet! Please provide a valid subnet range...')
    sys.exit(1)
print(f'INFO: Subnet Range Validation Completed...')
#######################################################################


#######################################################################
# Discover Pod Accounts ###########################################
#######################################################################
try:
    print(f'INFO: Creating Pod Accounts Collection...')
    primary_ips = list(ipaddress.ip_network(SUBNET_RANGE_PRIMARY).hosts())
    secondary_ips = list(ipaddress.ip_network(SUBNET_RANGE_SECONDARY).hosts())

    primary_ips = list(collections.OrderedDict.fromkeys(list(map(lambda ip: str(re.sub(r'([0-9]+)$', '0', str(ip))), primary_ips))))
    secondary_ips = list(collections.OrderedDict.fromkeys(list(map(lambda ip: str(re.sub(r'([0-9]+)$', '0', str(ip))), secondary_ips))))

    public_subnet_01 = primary_ips[:len(primary_ips)//2]
    public_subnet_02 = primary_ips[len(primary_ips)//2:]

    for i in range(POD_COUNT):
        PODS_LIST.append({
            'account_name': f'pod{i:04}',
            'public_subnet_01': f'{public_subnet_01[i]}',
            'public_subnet_02': f'{public_subnet_02[i]}',
            'private_subnet': f'{secondary_ips[i]}'
        })

    print(f'INFO: {PODS_LIST}')

except:
    print(f'ERROR: Invalid Subnet! Please provide a valid subnet range...')
    sys.exit(1)
print(f'INFO: Pod Accounts Collection Created...')
#######################################################################


#######################################################################
# Confirm Destroy Before Proceeding ###################################
#######################################################################
print(f'You are about to DESTROY all pod pod(s) in {VPC_ID} in the {REGION} Region')
rusure_response1 = input('Are you sure you wish to destroy all of these pods (type "Y" to continue)? ')
if rusure_response1 == 'Y':
    rusure_response2 = input('ARE YOU ABSOLUTELY SURE (type "YES" to continue)? ')
    if rusure_response2 != 'YES':
        print('No pods were destroyed, sys.exiting now.')
        sys.exit(1)
else:
    print('No pods were destroyed, exiting now.')
    sys.exit(1)

#######################################################################
# EIP de-association and un-allocation + DynDNS deletion
#######################################################################
def update_dns(public_ip, hostname):
    '''Your friendly neighborhood DNS cleaner upper'''
    api_key = API_GATEWAY_KEY
    api_url = API_GATEWAY_URL
    headers = {'x-api-key': api_key }
    query_params = {'mode': 'del', 'hostname': hostname, 'ipv4_address': public_ip}
    response = requests.get(api_url, headers=headers, params=query_params)
    return response

def query_dns(hostname):
    '''Query route53 to retrieve current IP'''
    api_key = API_GATEWAY_KEY
    api_url = API_GATEWAY_URL
    headers = {'x-api-key': api_key }
    query_params = {'mode': 'get', 'hostname': hostname}
    response = requests.get(api_url, headers=headers, params=query_params)
    return response

instance_ids = []
for pod in PODS_LIST:
# Look up Guac and Tet-ingest instance IDs
    ec2 = session.client('ec2',region_name=REGION)
    reservations = ec2.describe_instances()['Reservations']
    for reservation in reservations:
        instances = reservation['Instances']
        for instance in instances:
            if 'VpcId' in instance:
                if instance['VpcId'] == VPC_ID:
                    for tag in instance['Tags']:
                        if tag['Key'] == 'Name':                   
                            if pod['account_name'] in tag['Value'] and 'guac' in tag['Value']:
                                instance_ids.append(instance['InstanceId'])
                            elif pod['account_name'] in tag['Value'] and 'tet-data' in tag['Value']:
                                instance_ids.append(instance['InstanceId'])
                        if tag['Key'] == 'DNS':
                            public_ip = None
                            if pod['account_name'] in tag['Value']:
                                print(f"INFO: Looking up current IP address for {tag['Value']}")
                                r = query_dns(tag['Value'])
                                if r.status_code == 200:
                                    content = json.loads(r.content)
                                    if content:
                                        if 'return_message' in content:
                                            print(f"INFO: found IP address {content['return_message']}")
                                            public_ip = content['return_message']
                                        else:
                                            print(f"WARN: did not find an IP address for host {tag['Value']}")
                                else:
                                    print(f"ERROR: DNS lookup failed for hostname {tag['Value']}")
                                hostname = tag['Value']
                                if public_ip:
                                    print(f'INFO: Deleting DNS entry for hostname: {hostname} IP Address: {public_ip}')
                                    response = update_dns(public_ip, hostname)
                                    if response.status_code == 200:
                                        print(f'INFO: DNS update successful')
                                    else:
                                        print(f'ERROR: DNS update failed for hostname {hostname} IP Address: {public_ip}')
                                        print(f'ERROR: Status code: {response.status_code}, Reason: {response.reason}')

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
for pod in PODS_LIST:

    bucket_name = ''

    try:

        cloudformation = session.client('cloudformation')

        result = cloudformation.describe_stacks(
            StackName=f"n0work-{SESSION_NAME}-{pod['account_name']}"
        )

        bucket_name = list(filter(lambda o: o['OutputKey'] == 'n0workVPCFlowLogBucket', result['Stacks'][0]['Outputs']))[0]['OutputValue']

        s3 = session.resource('s3')
        bucket = s3.Bucket(bucket_name)
        print(f"INFO: Emptying s3 bucket {bucket_name}")
        bucket.objects.delete()
        while len(list(bucket.objects.iterator())) > 0:
            print('INFO: Waiting for object deletion to complete')
        print(f"INFO: Deleting s3 bucket {bucket_name}")
        bucket.delete()
        print(f'INFO: S3 Bucket Deleted: {bucket_name}')

    except Exception as e:

        if 'does not exist' in str(e):
            print(f'INFO: S3 Bucket {bucket_name} Does Not Exist...')
        elif 'BucketNotEmpty' in str(e):
            print(f'ERROR: S3 Bucket {bucket_name} is not empty even though we already emptied it.')
            print(f'Exiting')
            sys.exit(1)
        else:
            print('WARN: ', e)

print(f'INFO: S3 Bucket Deletion Complete...')
#######################################################################


#######################################################################
# Delete EKS Load Balancers ###########################################
#######################################################################
print('INFO: Initializing EKS Load Balancers Deletion...')
for pod in PODS_LIST:

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
                    if SESSION_NAME in tag[key]:
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
        StackName=f"n0work-{SESSION_NAME}-class-schedule"
    )
except Exception as e:
    print('WARN: ', e)
print(f"INFO: Deleted class schedule n0work-{SESSION_NAME}-class-schedule")

#######################################################################
# Delete DynDNS Updater
#######################################################################
print(f'INFO: Deleting the DNS updater Lambda function n0work-{SESSION_NAME}-dns-updater')
try:
    cloudformation = session.client('cloudformation')

    result = cloudformation.delete_stack(
        StackName=f'n0work-{SESSION_NAME}-dns-updater'
    )
except Exception as e:
    print('WARN: ', e)
print(f"INFO: Deleted DNS updater Lambda function n0work-{SESSION_NAME}-dns-updater")

#######################################################################
# Delete Pods In CloudFormation ###############################
#######################################################################
print('INFO: Commencing CloudFormation Stack Deletion...')
for pod in PODS_LIST:

    try:

        cloudformation = session.client('cloudformation')

        result = cloudformation.delete_stack(
            StackName=f"n0work-{SESSION_NAME}-{pod['account_name']}"
        )

        print(f"INFO: Stack deletion initiated for: n0work-{SESSION_NAME}-{pod['account_name']}...")

        STACKS_LIST.append(f"n0work-{SESSION_NAME}-{pod['account_name']}")

    except Exception as e:
        print('WARN: ', e)
print(f"INFO: CloudFormation deletion initiated for n0work-{SESSION_NAME}-{pod['account_name']}...")
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
                print(f'WARN: {stack_name} does not exist or was deleted...')
                continue

            print(f"INFO: StackName: {stack_name}, Status: {status['Stacks'][0]['StackStatus']}")

            if "DELETE_FAILED" in status['Stacks'][0]['StackStatus']:
                print(f'ERROR: Deletion failed for stack {stack_name}, please check the CloudFormation dashboard on the AWS console')
                print('Exiting')
                sys.exit(1)

        if len(PODS_LIST) == len(deleted_stacks):
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
# Empty and delete the S3 bucket for the CFT
#######################################################################

# try:
#     s3 = session.resource('s3')
#     bucket = s3.Bucket(f'tetration-hol-cft-template-{SESSION_NAME}')
#     bucket.objects.delete()
#     while len(list(bucket.objects.iterator())) > 0:
#         print('INFO: Waiting for object deletion to complete')
#     bucket.delete()
#     print(f'INFO: Deleted S3 bucket tetration-hol-cft-template-{SESSION_NAME}')
# except Exception as e:
#     print(f'ERROR: While deleting S3 Bucket tetration-hol-cft-template-{SESSION_NAME}:  {e}')
#     sys.exit(1)

#######################################################################
# Delete the state file from S3
#######################################################################
try:
    s3 = session.resource('s3')
    print(f'INFO: Deleting state file {STATE_FILE} from S3 bucket {S3_BUCKET}')
    s3.Object(bucket_name=S3_BUCKET, key=STATE_FILE).delete()
    print(f"INFO: State file {STATE_FILE} deleted from S3 bucket {S3_BUCKET}")
except Exception as e:
    print(f'WARN: While deleting {STATE_FILE} from S3:  {e}')

########################################################################
# Delete the DNS record for the session from Route53
########################################################################
print(f"INFO: Deleting {SESSION_NAME}.lab.tetration.guru from Route53")
resp = update_dns("127.0.0.1", f"{SESSION_NAME}.lab.tetration.guru")
if resp.status_code == 200:
    content = json.loads(resp.content)
    if content:
        if "return_message" in content:
            print(f"INFO: Response from API - {content['return_message']}")
        else:
            print(f"WARN: {content['errorMessage']}")
    else:
        print(f"ERROR: Received HTTP {resp.status_code} {resp.reason}")

print('INFO: Rollback completed successfully!')