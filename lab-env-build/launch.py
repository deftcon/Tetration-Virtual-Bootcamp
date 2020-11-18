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
import calendar
import sys
import requests
from datetime import datetime
from datetime import timedelta
from botocore.config import Config
from botocore.exceptions import ClientError

import ami_create


ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

if not ACCESS_KEY or not SECRET_KEY:
    print('ERROR: AWS_ACCESS_KEY_ID and/or AWS_SECRET_ACCESS_KEY not found in environment!')
    print('''Please run the following in your terminal:
    export AWS_ACCESS_KEY_ID=<YOUR AWS KEY>
    export AWS_SECRET_ACCESS_KEY=<YOUR AWS SECRET>
    ''')
    sys.exit(1)
API_GATEWAY_URL = "https://fh3aao7bri.execute-api.us-east-1.amazonaws.com/prod"
API_GATEWAY_KEY = "iBO39NUUc1401nMYkNWvM1jbA4YAHhKD1z4wpIlh"

def get_session_name(prompt):
    while True:
        pattern = re.compile(r'^([^~+&@!#$%_?/:\']*)$')
        answer = input(prompt)
        if ' ' in answer:
            print("Spaces are not allowed!")
            continue
        if '\\' in answer:
            print("Backslash is not permitted!")
            continue
        if len(answer) < 5:
            print("Length must be between 5 and 25 characters!")
        if len(answer) > 25:
            print("Length is limited to 25 characters!")
            continue
        m = re.match(pattern, answer)
        if m:
            return answer
        else:
            print("No special characters are allowed, except a dash (-)!")
print('A session name is required to uniquely identify your deployment')
print('The session name can be between 5 and 25 characters, with no special characters allowed except for a dash (-).')
SESSION_NAME = get_session_name("Please enter the session name: ")

CFT_POD_FILE = f'n0work-{SESSION_NAME}-pod-cft-template.yml'

def get_pod_count(prompt):
    while True:
        pattern = '^[0-9]+$'
        answer = input(prompt)
        m = re.match(pattern, answer)
        if m:
            return int(answer)

POD_COUNT = get_pod_count("How many pods are needed? ")

def get_region(prompt):
    region_dict = {
        '1': ('us-east-1','N. Virginia'),
        '2': ('us-east-2', 'Ohio'),
        '3': ('us-west-2', 'Oregon'),
        '4': ('af-south-1', 'Africa - Cape Town)'),
        '5': ('ap-east-1', 'Asia Pacific - Hong Kong'),
        '6': ('ap-south-1', 'Asia Pacific - Mumbai'),
        '7': ('ap-northeast-3', 'Asia Pacific - Osaka-Local'),
        '8': ('ap-northeast-2', 'Asia Pacific - Seoul'),
        '9': ('ap-southeast-1', 'Singapore'),
        '10': ('ap-southeast-2', 'Asia Pacific - Sydney'),
        '11': ('ap-northeast-1', 'Asia Pacific - Tokyo')
    }
    for key in region_dict:
        print(f"{key}: {region_dict[key][0]} ({region_dict[key][1]})")
    while True:
        answer = input(prompt)
        if int(answer) > 0 and int(answer) < 13:
            return region_dict[answer][0]

REGION = get_region('Please enter the AWS region you would like to deploy these pods in by entering the corresponding number: ')

def get_user_input(prompt, valid_pattern):
    while True:
      answer = input(prompt)
      m = re.match(valid_pattern, answer)
      if m:
          return answer

print(" ")
print("These lab environment pods can be deployed into an existing VPC, or a new VPC can be created for you.")
print("It is HIGHLY encouraged to allow this process to create the VPC and all components therein, for you.")
print("One reason to choose the option to use an existing VPC is if you require more than two (2) pods (which require a total of 4 EIPs),")
print("in which case you will need to make a request to AWS to increase the number of EIPs and have them allocated to a specific VPC-Id PRIOR to running this script.")
print("To deploy into an existing VPC, the VPC ID and the ID of the Internet Gateway in the existing VPC will be needed,")
print("as well as requiring the two (2) subnets chosen in the parameters.yml file to be associated to the VPC as attached CIDR Blocks.")
print(" ")
print("Again, unless you require more than 2 pods to be deployed, you should allow this script to create everything for you.")
print(" ")
vpc_answer = get_user_input("Do you require only 1 or 2 pods and wish to have everything, including the VPC, created for you? (Y/N) ", "^[YyNn]$")
if vpc_answer.upper() == 'N':
    VPC_ID = get_user_input("Enter your existing VPC ID: ", "^vpc-[0-9a-z]*")
    INTERNET_GATEWAY_ID = get_user_input("Enter the Internet Gateway ID: ", "^igw-[0-9a-z]*")
    use_existing_vpc = True
elif vpc_answer.upper() == 'Y':
    use_existing_vpc = False
print(" ")

#######################################################################
# Verify VPC Id Provided, if using existing ###########################
#######################################################################
session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)
if use_existing_vpc:
    try:
        print(f'INFO: Checking VPC ID: {VPC_ID} in region {REGION}')
        ec2 = session.resource('ec2', region_name=REGION)
        vpc = ec2.Vpc(VPC_ID)
        print(f'INFO: VPC ID Verified: {vpc.vpc_id}...')
    except ClientError as e:
        print(f'ERROR: VPC Check Failed with error {e}')
        sys.exit(1)

#######################################################################

print(" ")
print("Next, we require two (2) /16 CIDR blocks that will be used to create each pod's 'Inside' (or Corporate) and 'Outside' (or psuedo-Internet) subnet.")
print("Both CIDR blocks MUST end in /16. This is essentially due to the fact that we let you pick the first two octets, then use the third octet for each new pod #,")
print("and the fourth octet for the hosts in each pod.")
print(" ")
primary_cidr_answer = get_user_input("Please enter a CIDR block to be used for the 'INSIDE' subnet for each Pod (MUST be in the format x.x.0.0/16): ", "^[0-9]+\.[0-9]+\.[0]+\.[0]+\/16$")
secondary_cidr_answer = get_user_input("Please enter a CIDR block to be used for the 'OUTSIDE' subnet for each Pod (MUST be in the format x.x.0.0/16): ", "^[0-9]+\.[0-9]+\.[0]+\.[0]+\/16$")
print(" ")

SUBNET_RANGE_PRIMARY = primary_cidr_answer
SUBNET_RANGE_SECONDARY = secondary_cidr_answer
MANAGEMENT_CIDR = ''

STACKS_LIST = []
PODS_LIST = []

def password_generator(size=14, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Gets the public IP address of system running this script
# def get_public_ip():
#     result = json.load(urllib.request.urlopen('https://api.ipify.org/?format=json'))
#     return result['ip']


#######################################################################
# Get Management Cidr Block ###########################################
#######################################################################
# try:
#     print(f'INFO: Fetching Your Public IP for AWS SG Access "All Traffic" ...')
#     MANAGEMENT_CIDR = f"{get_public_ip()}/32"
#     print('INFO: Management Cidr:', MANAGEMENT_CIDR)
# except:
#     print(f'MINOR: Unable To Grab Your Public IP for the Management CIDR')
#     print(f'MINOR: Not a major issue, so continuing ...')
#     MANAGEMENT_CIDR = '1.1.1.1/32'
#     pass

# MANAGEMENT_CIDR = '1.1.1.1/32'

#######################################################################
# Check Existing Subnets if deploying into existing ###################
#######################################################################
if use_existing_vpc:
    print(f'INFO: Checking Existing Subnets...')
    filters = [{'Name':'vpcId', 'Values':[VPC_ID]}]

    ec2 = session.resource('ec2', region_name=REGION)
    subnets_count = len(list(ec2.subnets.filter(Filters=filters)))

    if subnets_count > 0:
        print(f'ERROR: {subnets_count} Subnets Found In Current VPC...')
        sys.exit(1)

    print(f'INFO: Subnet Check Completed...')

#######################################################################
# Check Available Elastic IPs #########################################
#######################################################################

print('INFO: Checking Available Elastic IPs...')

client = session.client('ec2', region_name=REGION)

addresses_dict = client.describe_addresses()

eips_allocated = len(addresses_dict['Addresses'])
eips_in_use = 0
ELASTIC_IPS = []

for eip_dict in addresses_dict['Addresses']:
    if 'NetworkInterfaceId' not in eip_dict:
        ELASTIC_IPS.append({
            'public_ip': eip_dict['PublicIp'],
            'allocation_id': eip_dict['AllocationId']
        })
    elif 'InstanceId' in eip_dict:
        eips_in_use += 1

allocated_and_available = eips_allocated - eips_in_use
print(f'INFO: Number of required Elastic IPs is {POD_COUNT * 2}, you currently have {allocated_and_available} available for use')
succeeded_count = 0
if allocated_and_available < (POD_COUNT * 2):   
    print(f'INFO: Attempting to allocate {(POD_COUNT * 2) - allocated_and_available} additional Elastic IPs...')
    for i in range(1,((POD_COUNT * 2) - allocated_and_available) + 1):
        try:
            eip = client.allocate_address()
            ELASTIC_IPS.append({
            'public_ip': eip['PublicIp'],
            'allocation_id': eip['AllocationId']})
            succeeded_count += 1
        except ClientError as e:
            if 'AddressLimitExceeded' in str(e):
                print(f'ERROR: Number of additional Elastic IPs is {(POD_COUNT * 2) - allocated_and_available} and {succeeded_count} were able to be allocated.')
                print(f'Please go to the AWS portal to request increase of EIP limit by {(POD_COUNT * 2) - allocated_and_available - succeeded_count} or more addresses:')
                print(f'https://console.aws.amazon.com/support/home?#/case/create?issueType=service-limit-increase&limitType=vpc')
                sys.exit(1)
        
    if succeeded_count > 0:
        print(f'INFO: Successfully allocated {succeeded_count} Elastic IPs')

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
# Create Pod Accounts #############################################
#######################################################################
try:
    print(f'INFO: Creating Pod Accounts Collection...')
    primary_ips = list(ipaddress.ip_network(SUBNET_RANGE_PRIMARY).hosts())
    secondary_ips = list(ipaddress.ip_network(SUBNET_RANGE_SECONDARY).hosts())

    primary_ips = list(collections.OrderedDict.fromkeys(list(map(lambda ip: str(re.sub(r'([0-9]+)$', '0', str(ip))), primary_ips))))
    secondary_ips = list(collections.OrderedDict.fromkeys(list(map(lambda ip: str(re.sub(r'([0-9]+)$', '0', str(ip))), secondary_ips))))

    public_subnet_01 = primary_ips[:len(primary_ips)//2]
    public_subnet_02 = primary_ips[len(primary_ips)//2:]

    eip_index = 0

    for i in range(POD_COUNT):
        PODS_LIST.append({
            'account_name': f'pod{i:04}',
            'account_password': password_generator(),
            'public_subnet_01': f'{public_subnet_01[i]}',
            'public_subnet_02': f'{public_subnet_02[i]}',
            'private_subnet': f'{secondary_ips[i]}',
            'eks_dns': '',
            'guacamole_elastic_ip': ELASTIC_IPS[eip_index]['public_ip'],
            'guacamole_elastic_ip_allocation_id': ELASTIC_IPS[eip_index]['allocation_id'],
            'tet_data_elastic_ip': ELASTIC_IPS[eip_index + 1]['public_ip'],
            'tet_data_elastic_ip_allocation_id': ELASTIC_IPS[eip_index + 1]['allocation_id']
        })

        eip_index = eip_index + 2

#    print(f'INFO: {PODS_LIST}')

except:
    print(f'ERROR: Invalid Subnet! Please provide a valid subnet range...')
    sys.exit(1)


print(f'INFO: Pod Accounts Collection Created...')
#######################################################################
# Collect scheduling information
#######################################################################
def validate_time(prompt, begin_time=None):
    while True:
        t = input(prompt)
        pattern = "[0-2][0-9]:[0-5][0-9]"
        m = re.match(pattern, t)
        if m:
            if begin_time:
                begin = datetime.strptime(begin_time, '%H:%M').time()
                end = datetime.strptime(t, '%H:%M').time()
                if end > begin:
                    return m.group()
                else:
                    print(f"ERROR: End time {t} is before start time {begin_time}, please try again!")
            else:
                return m.group()
        else:
            print(f"ERROR: Invalid time {t} entered, please enter the time using 24hr format XX:XX")

def validate_tz(prompt):
    with open('tz_info', 'r') as f:
        y = yaml.safe_load(f)
    print('Timezone Selections:')
    for key in y.keys():
        print(f"{key}: {y[key]}")
    while True:
        selection = input(prompt)
        if selection.isdigit() and int(selection) > 0 and int(selection) < 432:
            return y[selection]
        else:
            print("ERROR: Invalid timezone selection, please try again")

def validate_month(prompt):
    month_dict = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    for key in month_dict:
        print(f"{key}: {month_dict[key]}")
    while True:
        answer = input(prompt)
        if int(answer) in month_dict.keys():
            return answer

def validate_day(prompt):
    while True:
        answer = input(prompt)
        if int(answer) > 0 and int(answer) < 32:
            return answer
print(" ")
print("************************************************************************************************************************************************************")
print("The lab can run continuously or you can define a schedule which allows cost savings in AWS by powering off EC2 instances when not using the lab environment.")
print("When setting a schedule, the instances will be deployed now and will be running at first, then upon inspection of both the defined schedule and the state ")
print("of each EC2 instance, any running instances will be stopped (not terminated) and will spin up automatically when at the properly scheduled time.")
print("Note that there will still be some AWS billing incurred starting today for the resources associated with the stopped instances and other lab components.")
print("************************************************************************************************************************************************************")
print(" ")
answer = get_user_input("Would you like to define a schedule for the lab? (Y/N) ", "^[YyNn]$")
if answer.upper() == 'Y':
    use_schedule = True
    START_MONTH = validate_month("Please enter the Starting Month for this session: ")
    START_DAY = validate_day("Please enter the Starting Day of the month (1-31) for this session: ")
    BEGIN_TIME = validate_time("Please enter the Starting Time (EACH DAY) for this session using a 24-hour format (00:00 - 23:59): ")
    END_MONTH = validate_month("Please enter the Ending Month for this session: ")
    END_DAY = validate_day("Please enter the Ending Day of the month (1-31) for this session: ")
    END_TIME = validate_time("Please enter the Starting Time (EACH DAY) for this session using a 24-hour format (00:00 - 23:59): ", BEGIN_TIME)
    TIMEZONE = validate_tz("Please enter the timezone you would like this schedule to be run against using the number of the TZ from the above list: ")
else:
    use_schedule = False

if use_schedule:
    # Create a start time
    dt = datetime.strptime(BEGIN_TIME, '%H:%M')
    # option to add a delta to the starting time to allow things such as Tetration ADM runs (not needed for now so removing for cost)
    # t = timedelta(hours=6)
    # dt_start = dt - t
    dt_start = dt
    ADM_START_TIME = dt_start.strftime('%H:%M')
    # Handles case where class start and end are in same month
    if START_MONTH == END_MONTH:
        MONTHDAYS = f"{START_DAY}-{END_DAY}"
        ADM_MONTH = START_MONTH
        ADM_DAY = str(int(START_DAY) + 1)
    # Handles case where class starts end of month and overlaps into next month
    else:
        MONTHDAYS = f"{START_DAY}-L"
        date_obj = datetime(datetime.now().year, int(START_MONTH), int(START_DAY))
        days_in_month = calendar.monthrange(datetime.now().year,date_obj.month)[1]
        if int(START_DAY) == days_in_month:
            ADM_MONTH = END_MONTH
            ADM_DAY = "1"
        else:
            ADM_MONTH = START_MONTH
            ADM_DAY = str(int(START_DAY) + 1)

    month_dict = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    SCHEDULE_NAME = f"{month_dict[int(START_MONTH)]}{START_DAY}-to-{month_dict[int(END_MONTH)]}{END_DAY}-{BEGIN_TIME.replace(':','')}-{END_TIME.replace(':','')}"
else:
    SCHEDULE_NAME = "Always-On"


#######################################################################
# Confirm Deploy Before Proceeding ####################################
#######################################################################
if use_existing_vpc:
    print(f'You are about to deploy {POD_COUNT} pod(s) to {VPC_ID} in the {REGION} Region')
else:
    print(f'You are about to deploy {POD_COUNT} pod(s) to a new VPC in the {REGION} Region')
if use_schedule:
    print(f"The lab will start at {BEGIN_TIME} and stop each day at {END_TIME} in the {TIMEZONE} timezone")
rusure_response = input('Are you sure you wish to proceed with this deployment (y/Y to continue)? ')
if rusure_response.lower() != 'y':
    print('No pods were created, exiting now.')
    sys.exit(1)

######################################################################
# Create S3 bucket    ################################################
######################################################################
def create_bucket(bucket_name, config, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3', config=config)
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region, config=config)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        if 'BucketAlreadyOwnedByYou' in e.response['Error']['Code']:
            print(f"INFO: Bucket {bucket_name} already exists, skipping")
        elif 'BucketAlreadyExists' in e.response['Error']['Code']:
            print(f"INFO: Bucket {bucket_name} already exists, skipping")
        else:
            print(f"ERROR: Error while creating S3 bucket {e}")
            sys.exit(1)
        return False
    return True

arn = boto3.resource('iam').CurrentUser().arn
ACCT_ID = re.search('[0-9]+', arn).group()
ACCT_USER = arn[arn.find('/')+1:]
S3_BUCKET = f"n0work-{ACCT_ID}"
# Create S3 bucket if not already existing
print(f"INFO: Creating S3 Bucket {S3_BUCKET}")
boto_config = Config(region_name=REGION)
if REGION == 'us-east-1':
    result = create_bucket(S3_BUCKET, boto_config)
else:
    result = create_bucket(S3_BUCKET, boto_config, region=REGION)

if result:
    print(f"INFO: Created S3 bucket {S3_BUCKET}")

#######################################################################
# Check for existing AMIs in S3 bucket for destination region
# If no AMI file found, launch ami_create
######################################################################
def read_s3_contents(bucket_name, key):
    response = s3.Object(bucket_name, key).get()
    return response['Body'].read()

s3 = boto3.resource('s3', region_name=REGION)
AMI_FILE = f"{REGION}-ami-ids.yml"
print(f"INFO: Checking bucket {S3_BUCKET} for AMI file {AMI_FILE} ")
bucket = s3.Bucket(name=S3_BUCKET)
objects = [x.key for x in list(bucket.objects.iterator())]
if AMI_FILE in objects:
    print(f"INFO: Loading AMI IDs from {AMI_FILE} in S3 bucket {S3_BUCKET}")
    params = yaml.safe_load(read_s3_contents(S3_BUCKET, AMI_FILE)) 
else:
    print(f"INFO: No AMI file {AMI_FILE} in S3 bucket {S3_BUCKET}")
    print(f"INFO: Launching AMI Creation! This will take a while.")
    # Launch AMI Create
    ami_create.run(REGION)
    params = yaml.safe_load(read_s3_contents(S3_BUCKET, AMI_FILE))



#######################################################################
# CREATE VPC IF NOT SPECIFIED IN PARAMETERS FILE
#######################################################################
if not use_existing_vpc:
    # Create VPC
    client = boto3.client('ec2', region_name=REGION)
    vpc = client.create_vpc(
        CidrBlock=SUBNET_RANGE_PRIMARY,
        TagSpecifications=[
            {
                'ResourceType': 'vpc',
                'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'n0work'
                },
                ]
            },
        ]
    )
    VPC_ID = vpc['Vpc']['VpcId']
    print(f"INFO: Created VPC with ID {VPC_ID} and CIDR block {SUBNET_RANGE_PRIMARY}")
    #SESSION_NAME = VPC_ID[-6:]

    # Create Secondary CIDR
    sec_cidr = client.associate_vpc_cidr_block(CidrBlock=SUBNET_RANGE_SECONDARY, VpcId=VPC_ID)
    print(f"INFO: Created Secondary CIDR block {SUBNET_RANGE_SECONDARY} on VPC {VPC_ID}")

    # Create Internet Gateway
    inet_gateway = client.create_internet_gateway(
        TagSpecifications=[
            {
                'ResourceType': 'internet-gateway',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'n0work '
                    },
                ]
            },
        ],
    )
    INTERNET_GATEWAY_ID = inet_gateway['InternetGateway']['InternetGatewayId']
    print(f"INFO: Created Internet Gateway with ID {INTERNET_GATEWAY_ID}")

    # Associate Internet Gateway with VPC
    ec2 = boto3.resource('ec2', region_name=REGION)
    ig = ec2.InternetGateway(INTERNET_GATEWAY_ID)
    ig_associate = ig.attach_to_vpc(VpcId=VPC_ID)
    print(f"INFO: Associated Internet Gateway with ID {INTERNET_GATEWAY_ID} to VPC {VPC_ID}")

#######################################################################
# Create state file for rollback
######################################################################

STATE_FILE = f'n0work-{SESSION_NAME}-{REGION}-state.yml'

with open(f"/tmp/{STATE_FILE}", 'w') as f:
    f.write(f"session_name: {SESSION_NAME}\n")
    f.write(f"aws_region: {REGION}\n")
    f.write(f"pod_count: {POD_COUNT}\n")
    f.write(f"vpc_id: {VPC_ID}\n")
    f.write(f"subnet_range_primary: {SUBNET_RANGE_PRIMARY}\n")
    f.write(f"subnet_range_secondary: {SUBNET_RANGE_SECONDARY}\n")

CREATED_DATE = datetime.now().strftime('%h-%d-%Y %H:%M')

metadata = {'session_name': SESSION_NAME, 'created_date':CREATED_DATE, 'created_by':ACCT_USER, 'schedule':SCHEDULE_NAME, 'region': REGION, 'vpcid': VPC_ID}

print(f"INFO: Uploading state file {STATE_FILE} To S3 bucket {S3_BUCKET}...")
s3.meta.client.upload_file(f"/tmp/{STATE_FILE}", S3_BUCKET, STATE_FILE, ExtraArgs={"Metadata":metadata})
print(f"INFO: Uploaded state file {STATE_FILE} to bucket {S3_BUCKET}...")
os.remove(f"/tmp/{STATE_FILE}")


#######################################################################
# Upload CFT TO S3 Bucket #############################################
#######################################################################
print(f'INFO: Uploading CFT Template {CFT_POD_FILE} To S3...')
s3 = boto3.resource('s3', region_name=REGION)
s3.meta.client.upload_file('n0work-pod-cft-template.yml', S3_BUCKET, CFT_POD_FILE)
print(f'INFO: CFT Template {CFT_POD_FILE} Uploaded To S3...')

#######################################################################
# Upload DNS Updater Lambda Function TO S3 Bucket #####################
#######################################################################
print(f'INFO: Uploading lambda_function/tvb-dyndns.zip To S3 bucket {S3_BUCKET}')
DNS_UPDATER_FILE = os.path.join(os.getcwd(),'lambda_function','tvb-dyndns.zip')
DNS_UPDATER_NAME = 'tvb-dyndns.zip'
s3 = boto3.resource('s3', region_name=REGION)
s3.meta.client.upload_file(DNS_UPDATER_FILE, S3_BUCKET, DNS_UPDATER_NAME)
print(f'INFO: lambda_function/tvb-dyndns.zip Uploaded To S3 bucket {S3_BUCKET}')

#######################################################################
# Run POD Cloud Formation #############################################
#######################################################################

# Previously this was in parameters.yml.  Hard-coding for now so CFT can work.  
params['ise_server_ip'] = '127.0.0.1'

for pod in PODS_LIST:

    try:

        outside_pod_ips = list(ipaddress.ip_network(f"{pod['private_subnet']}/24").hosts())

        cloudformation = session.client('cloudformation', region_name=REGION)

        aws_parameters = [
            {'ParameterKey': 'AccessKey', 'ParameterValue': ACCESS_KEY},
            {'ParameterKey': 'SecretKey', 'ParameterValue': SECRET_KEY},

            {'ParameterKey': 'PodIndex', 'ParameterValue': str(PODS_LIST.index(pod))},
            {'ParameterKey': 'PodName', 'ParameterValue': pod['account_name']},
            {'ParameterKey': 'PodPassword', 'ParameterValue': pod['account_password']},
            # {'ParameterKey': 'ManagementCidrBlock', 'ParameterValue': MANAGEMENT_CIDR},

            {'ParameterKey': 'Subnet01CidrBlock', 'ParameterValue': f"{pod['public_subnet_01']}/24"},
            {'ParameterKey': 'Subnet02CidrBlock', 'ParameterValue': f"{pod['public_subnet_02']}/24"},
            {'ParameterKey': 'Subnet03CidrBlock', 'ParameterValue': f"{pod['private_subnet']}/24"},

            {'ParameterKey': 'ASAvInsideSubnet', 'ParameterValue': pod['public_subnet_01']},
            {'ParameterKey': 'ASAvOutsideSubnet', 'ParameterValue': pod['private_subnet']},

            {'ParameterKey': 'GuacamoleElasticIp', 'ParameterValue': pod['guacamole_elastic_ip']},
            {'ParameterKey': 'GuacamoleElasticIpAllocationId', 'ParameterValue': pod['guacamole_elastic_ip_allocation_id']},

            {'ParameterKey': 'TetDataElasticIp', 'ParameterValue': pod['tet_data_elastic_ip']},
            {'ParameterKey': 'TetDataElasticIpAllocationId', 'ParameterValue': pod['tet_data_elastic_ip_allocation_id']},

            {'ParameterKey': 'Region', 'ParameterValue': REGION},
            {'ParameterKey': 'Subnet01AvailabilityZone', 'ParameterValue': 'a'},
            {'ParameterKey': 'Subnet02AvailabilityZone', 'ParameterValue': 'b'},
            {'ParameterKey': 'Subnet03AvailabilityZone', 'ParameterValue': 'a'},

            {'ParameterKey': 'ISEIPAddress', 'ParameterValue': params['ise_server_ip']},

            {'ParameterKey': 'AttackerPrivateIp', 'ParameterValue': str(outside_pod_ips[13])},
            {'ParameterKey': 'IISOutsidePrivateIp', 'ParameterValue': str(outside_pod_ips[14])},
            {'ParameterKey': 'ApacheOutsidePrivateIp', 'ParameterValue': str(outside_pod_ips[15])},
            {'ParameterKey': 'ASAvOutsidePrivateIp01', 'ParameterValue': str(outside_pod_ips[16])},
            {'ParameterKey': 'ASAvOutsidePrivateIp02', 'ParameterValue': str(outside_pod_ips[17])},
            {'ParameterKey': 'Ubuntu1804EmployeePrivateIp', 'ParameterValue': str(outside_pod_ips[18])},
            {'ParameterKey': 'Ubuntu1804SysAdminPrivateIp', 'ParameterValue': str(outside_pod_ips[19])},
            {'ParameterKey': 'GuacamoleOutsidePrivateIp', 'ParameterValue': str(outside_pod_ips[20])},

            {'ParameterKey': 'ASAvImageID', 'ParameterValue': params['asav_ami']},
            {'ParameterKey': 'LDAPImageID', 'ParameterValue': params['ldap_ami']},
            {'ParameterKey': 'MSSQLImageID', 'ParameterValue': params['mssql_ami']},
            {'ParameterKey': 'IISImageID', 'ParameterValue': params['iis_ami']},
            {'ParameterKey': 'MySQLImageID', 'ParameterValue': params['mysql_ami']},
            {'ParameterKey': 'ApacheImageID', 'ParameterValue': params['apache_ami']},
            {'ParameterKey': 'AnsibleImageID', 'ParameterValue': params['ansible_ami']},
            {'ParameterKey': 'TetrationDataIngestImageID', 'ParameterValue': params['tet_data_ami']},
            {'ParameterKey': 'TetrationEdgeImageID', 'ParameterValue': params['tet_edge_ami']},
            {'ParameterKey': 'Ubuntu1804EmployeeImageID', 'ParameterValue': params['employee_ubuntu_ami']},
            {'ParameterKey': 'Ubuntu1804SysAdminImageID', 'ParameterValue': params['sysadmin_ubuntu_ami']},
            {'ParameterKey': 'AttackerImageID', 'ParameterValue': params['attack_server_ami']},
            {'ParameterKey': 'GuacamoleImageID', 'ParameterValue': params['guacamole_ami']},
            {'ParameterKey': 'EKSWorkerImageID', 'ParameterValue': params['eks_worker_ami']},
            {'ParameterKey': 'VpcID', 'ParameterValue': VPC_ID},
            {'ParameterKey': 'InternetGatewayId', 'ParameterValue': INTERNET_GATEWAY_ID},
            {'ParameterKey': 'ScheduleName', 'ParameterValue': SCHEDULE_NAME},
            {'ParameterKey': 'SessionName', 'ParameterValue': SESSION_NAME}
            ]
        
        # aws_params_json_formatted_str = json.dumps(aws_parameters, indent=2)
        # print('INFO:', aws_params_json_formatted_str)

        templateURL = f"https://{S3_BUCKET}.s3.amazonaws.com/{CFT_POD_FILE}"
        print(templateURL)
        result = cloudformation.create_stack(
            StackName=f"n0work-{SESSION_NAME}-{pod['account_name']}",
            TemplateURL=templateURL,
            Parameters=aws_parameters,
            Capabilities=[
                'CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM',
            ]
        )

        STACKS_LIST.append(f"n0work-{SESSION_NAME}-{pod['account_name']}")
        
    except Exception as e:
        print(e)
        sys.exit(1)


#######################################################################
# Wait For Stack Creation #############################################
#######################################################################
completed_stacks = []
while True:

    try:

        for stack_name in STACKS_LIST:

            if stack_name in completed_stacks:
                continue

            cloudformation = session.client('cloudformation', region_name=REGION)

            status = cloudformation.describe_stacks(
                StackName=stack_name
            )

            if status['Stacks'][0]['StackStatus'] == 'CREATE_COMPLETE':
                completed_stacks.append(stack_name)

            if status['Stacks'][0]['StackStatus'] == 'ROLLBACK_IN_PROGRESS' or  status['Stacks'][0]['StackStatus'] == 'ROLLBACK_COMPLETE':
                print(f"ERROR: Stack Failed => {stack_name}")
                print('ERROR: Unable To Complete CloudFormation Deployment.')
                sys.exit(1)

            print(f"INFO: StackName: {stack_name}, Status: {status['Stacks'][0]['StackStatus']}")

        if len(STACKS_LIST) == len(completed_stacks):
            print('INFO: CloudFormation Completed Successfully...')
            break

        time.sleep(10)


    except Exception as e:
        print(e)
        sys.exit(1)

print(f'INFO: Deleting CFT file {CFT_POD_FILE} from S3 bucket {S3_BUCKET}')
s3.meta.client.delete_object(Bucket=S3_BUCKET, Key=CFT_POD_FILE)

#######################################################################
# Assemble EKS ELB DNS Records ########################################
#######################################################################
print('INFO: Preparing to initialize the EKS DNS Assembly...')
# time.sleep(5)
# print('INFO: Preparing to initialize the EKS DNS Assembly...')
# time.sleep(5)
# print('INFO: Preparing to initialize the EKS DNS Assembly...')
# time.sleep(5)
try:

    # print('INFO: Initializing EKS DNS Assembly...')

    # time.sleep(120)

    for pod in PODS_LIST:

        client = session.client('elb', region_name=REGION)
        # Check for ELB creation, retry until we get a response
        eks_elbs = None
        elb_name = None
        retries = 0
        while not eks_elbs or not elb_name:
            print(f"INFO Initializing EKS DNS Assembly for pod {pod['account_name']}...")
            eks_elbs = client.describe_load_balancers()['LoadBalancerDescriptions']

            loadbalancer_list = [e['LoadBalancerName'] for e in eks_elbs if e['VPCId'] == VPC_ID]
            print(f"INFO: List of ELBs in VPC {VPC_ID}: {loadbalancer_list}")

            if loadbalancer_list:    
                elb_tags = client.describe_tags(LoadBalancerNames=loadbalancer_list)

                for elb in elb_tags['TagDescriptions']:
                    for tag in elb['Tags']:
                        for key in tag:
                            if pod['account_name'] in tag[key]:
                                pod['eks_dns'] = list(filter(lambda e: e['LoadBalancerName'] == elb['LoadBalancerName'], eks_elbs))[0]['DNSName']
                                elb_name = elb['LoadBalancerName']
                                print(f"INFO: elb {elb_name} for pod {pod['account_name']} was found!")
                                break
            else:
                print("INFO: Waiting for ELB initialization, retry in 15 seconds")
            retries += 1
            if retries == 20:
                print(f"ERROR: ELB was not found for pod {pod['account_name']} after 20 retries!")
                break
            time.sleep(15)

#######################################################################################
# Attach EKS worker node to ELB - workaround for instance not getting attached to ELB 
#######################################################################################
        if elb_name:
            ec2 = session.client('ec2',region_name=REGION)
            waiter = ec2.get_waiter('instance_status_ok')
            reservations = ec2.describe_instances()['Reservations']
            for reservation in reservations:
                instances = reservation['Instances']
                for instance in instances:
                    if not instance['State']['Name'] == 'terminated':
                        for tag in instance['Tags']:
                            if tag['Key'] == 'Name':
                                if pod['account_name'] in tag['Value'] and 'eks' in tag['Value'] and SESSION_NAME in tag['Value']:
                                    instance_id = instance['InstanceId']
                                    print(f'Waiting for EKS worker node {instance_id} to pass health checks')
                                    waiter.wait(InstanceIds=[instance_id])
                                    print(f"EKS worker node {instance_id} now has status of 'ok'!")
                                    while True:
                                        print(f"INFO: Registering instance {tag['Value']} with elb {elb_name}")
                                        client.register_instances_with_load_balancer(LoadBalancerName=elb_name, Instances=[{'InstanceId': instance_id}])
                                        print(f"INFO: Checking to see if the instance attached to the ELB")
                                        client = session.client('elb', region_name=REGION)
                                        elb = client.describe_load_balancers(LoadBalancerNames=[elb_name])
                                        if elb['LoadBalancerDescriptions'][0]['Instances']:
                                            if elb['LoadBalancerDescriptions'][0]['Instances'][0]['InstanceId'] == instance_id:
                                                print(f"INFO: Instance {instance_id} is attached to elb {elb_name}")
                                                health = client.describe_instance_health(LoadBalancerName=elb_name)
                                                if health:
                                                    if instance_id in health['InstanceStates'][0]['InstanceId']:
                                                        print(f"INFO: Instance status: {health['InstanceStates'][0]['State']}")
                                                        if health['InstanceStates'][0]['State'] == 'InService':
                                                            break
                                                        else:
                                                            print(f"INFO: Instance not in service yet. Retry in 15 seconds")
                                                            time.sleep(15)
                                        else:
                                            print(f"INFO: Instance {instance_id} not attached to the ELB {elb_name}, trying again")
                                    break
        else:
            print(f"WARN: No ELB was found for pod {pod['account_name']}")                
    print(f"INFO: EKS DNS Assembly Completed...")

except Exception as e:
    print(e)
    sys.exit(1)


#######################################################################
# Gather the list of Instance IDs to track and create DNS Updater stack
#######################################################################
def update_dns(public_ip, hostname):
    '''Performs the initial DNS update during instance creation'''
    # api_key = os.environ.get('API_GATEWAY_KEY')
    # api_url = os.environ.get('API_GATEWAY_URL')
    api_key = API_GATEWAY_KEY
    api_url = API_GATEWAY_URL
    headers = {'x-api-key': api_key }
    query_params = {'mode':'set', 'hostname': hostname, 'ipv4_address': public_ip}
    response = requests.get(api_url, headers=headers, params=query_params)
    return response

print("INFO: Beginning deployment of DNS updater stack")
try:
    instance_ids = []
    ec2 = session.client('ec2',region_name=REGION)
    print("INFO: Retrieving the instance IDs of the EC2 instances to track (Apache and IIS servers)")
    reservations = ec2.describe_instances()['Reservations']
    for reservation in reservations:
        instances = reservation['Instances']
        for instance in instances:
            if instance['State']['Name'] == 'running':
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        if 'apache' in tag['Value'] or 'iis' in tag['Value']:
                            instance_ids.append(instance['InstanceId'])
                    # Perform initial DNS update, reading hostname from the tag and getting Public IP from the instance
                    if tag['Key'] == 'DNS':
                        public_ip = instance['PublicIpAddress']
                        hostname = tag['Value']
                        print(f'INFO: Updating DNS for hostname: {hostname} IP Address: {public_ip}')
                        response = update_dns(public_ip, hostname)
                        if response.status_code == 200:
                            print(f'INFO: DNS update successful')
                        else:
                            print(f'ERROR: DNS update failed for hostname {hostname} IP Address: {public_ip}')
                            print(f'ERROR: Status code: {response.status_code}, Reason: {response.reason}')
    
    cloudformation = session.client('cloudformation', region_name=REGION)
    
    INSTANCE_IDS = ''
    for x, instance in enumerate(instance_ids):
        INSTANCE_IDS += instance
        if not x == len(instance_ids)-1:
            INSTANCE_IDS += ','     

    aws_parameters = [
        {'ParameterKey': 'S3Bucket', 'ParameterValue': S3_BUCKET},
        {'ParameterKey': 'APIGatewayURL', 'ParameterValue': API_GATEWAY_URL},
        {'ParameterKey': 'APIGatewayKey', 'ParameterValue': API_GATEWAY_KEY},
        {'ParameterKey': 'InstanceList', 'ParameterValue': INSTANCE_IDS},
        {'ParameterKey': 'SessionName', 'ParameterValue': SESSION_NAME}
    ]
    
    with open('n0work-dns-updater-cft-template.yml', 'r') as f:
        dns_updater_cft = f.read()

    print(f'INFO: Creating stack n0work-{SESSION_NAME}-dns-updater')
    result = cloudformation.create_stack(
        StackName=f"n0work-{SESSION_NAME}-dns-updater",
        TemplateBody=dns_updater_cft,
        Parameters=aws_parameters,
        Capabilities=[
                    'CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM',
                ])

    # Wait for DNS updater creation
    while True:
        status = cloudformation.describe_stacks(
            StackName=f'n0work-{SESSION_NAME}-dns-updater')['Stacks'][0]['StackStatus']
        if status == 'CREATE_COMPLETE':
            print(f"INFO: Creating cloudformation stack n0work-{SESSION_NAME}-dns-updater. Status={status}")
            break
        if "ROLLBACK" in status:
            print(f"WARN: Error during creation of cloudformation stack n0work-{SESSION_NAME}-dns-updater. Status={status}")
            break
        else:
            print(f"INFO: Creating cloudformation stack n0work-{SESSION_NAME}-dns-updater. Status={status}")
            time.sleep(5)

except Exception as e:
    print(e)
    sys.exit(1)



#######################################################################
# Generate CSV Reports ################################################
######################################################################

try:

    records = []
    print(f"STACKS_LIST: {STACKS_LIST}")
    for stack_name in STACKS_LIST:
        print(f"INFO: StackName: {stack_name}, Status: Generating CSV Report...")

        cloudformation = session.client('cloudformation', region_name=REGION)

        stack = cloudformation.describe_stacks(
            StackName=stack_name
        )

        pod = list(filter(lambda pod: f"n0work-{SESSION_NAME}-{pod['account_name']}" == stack_name, PODS_LIST))[0]

        output = {}

        for o in stack['Stacks'][0]['Outputs']:
            output[o['OutputKey']] = o['OutputValue']

        eks_endpoint = output['EKSClusterEndpoint']
        eks_endpoint_fqdn_only = (eks_endpoint.split('//'))[1]

        records.append([
            f"https://{output['n0workGuacamolePublic']}",
            output['n0workPodName'],
            output['n0workPodPassword'],
            f"http://{output['n0workIISDNS']}",
            f"http://{output['n0workApacheDNS']}",
            f"http://{pod['eks_dns']}",
            output['n0workPublicSubnet01'],
            output['n0workPrivateSubnet'],
            output['n0workActiveDirectory'],
            output['n0workISE'],
            output['n0workIISPrivate'],
            output['n0workIISOutsidePrivate'],
            output['n0workMSSQL'],
            output['n0workApachePrivate'],
            output['n0workApacheOutsidePrivate'],
            output['n0workMySql'],
            output['n0workAnsible'],
            output['n0workTetrationEdge'],
            output['TetNetworkInterfaces01Data'],
            output['TetNetworkInterfaces02Data'],
            output['TetNetworkInterfaces03Data'],
            output['n0workASAvPrivate03'],
            output['n0workASAvPrivate02'],
            output['n0workAttacker'],
            output['n0workUbuntu1804Employee'],
            output['n0workUbuntu1804SysAdmin'],
            output['PodAccessKey'],
            output['PodSecretKey'],
            output['n0workAWSRegion'],
            output['n0workVPCFlowLogBucket'],
            f"{eks_endpoint_fqdn_only}",
            output['EKSClusterCertificate'],
            # output['n0work-cisco-pod-00-public-subnet-01-us-east-2a'],
            # n0work-cisco-pod-00-vpc-flow-logs-us-east-2a
            # aws key will need perms to read this log

        ])

        header = [
            'Pod Lab Access (Guac) Web Console URL',
            'Pod Lab Access (Guac) Username',   
            'Pod Lab Access (Guac) Password', 
            'nopCommerce Windows App URL',
            'OpenCart Linux App URL',
            'EKS SockShop App URL',
            'Pod Internal/Inside Corporate Subnet',
            'Pod External/Outside "Internet" Subnet',
            'MS Active Directory IP',
            'ISE Server IP',
            'MS IIS nopCommerce Inside IP',
            'MS IIS nopCommerce Outside IP',
            'MS SQL Private IP',
            'Apache OpenCart Inside IP',
            'Apache OpenCart Outside IP',
            'MySQL Private IP',
            'Ansible IP',
            'Tetration Edge IP',
            'Tetration Data Ingest IP 1',
            'Tetration Data Ingest IP 2',
            'Tetration Data Ingest IP 3',
            'ASAv Inside IP',
            'ASAv Outside IP',
            'Metasploit Attacker IP',
            'Ubuntu18.04 Employee IP',
            'Ubuntu18.04 SysAdmin IP',
            'Pod AWS External Orchestrator Access Key',
            'Pod AWS External Orchestrator Secret Key',
            'Pod AWS Region',
            'Pod VPC Flow Log S3 Bucket',
            'EKS Cluster API Endpoint (use for external orchestrator)',
            'EKS Cluster CA Cert (should not need)'
        ]

        columnar_output = [
            f"Pod Lab Access (Guac) Web Console URL,https://{output['n0workGuacamolePublic']}\n",
            f"Pod Lab Access (Guac) Username,{output['n0workPodName']}\n",
            f"Pod Lab Access (Guac) Password,{output['n0workPodPassword']}\n",
            f"nopCommerce Windows App URL,http://{output['n0workIISDNS']}\n",
            f"OpenCart Linux App URL,http://{output['n0workApacheDNS']}\n",
            f"EKS SockShop App URL,http://{pod['eks_dns']}\n",
            f"Pod Internal/Inside Corporate Subnet,{output['n0workPublicSubnet01']}\n",
            f"Pod External/Outside Internet Subnet,{output['n0workPrivateSubnet']}\n",
            f"MS Active Directory IP,{output['n0workActiveDirectory']}\n",
            f"ISE Server IP,{output['n0workISE']}\n",
            f"MS IIS nopCommerce Inside IP,{output['n0workIISPrivate']}\n",
            f"MS IIS nopCommerce Outside IP,{output['n0workIISOutsidePrivate']}\n",
            f"MS SQL Private IP,{output['n0workMSSQL']}\n",
            f"Apache OpenCart Inside IP,{output['n0workApachePrivate']}\n",
            f"Apache OpenCart Outside IP,{output['n0workApacheOutsidePrivate']}\n"
            f"MySQL Private IP,{output['n0workMySql']}\n",
            f"Ansible IP,{output['n0workAnsible']}\n",
            f"Tetration Edge IP,{output['n0workTetrationEdge']}\n",
            f"Tetration Data Ingest IP 1,{output['TetNetworkInterfaces01Data']}\n",
            f"Tetration Data Ingest IP 2,{output['TetNetworkInterfaces02Data']}\n",
            f"Tetration Data Ingest IP 3,{output['TetNetworkInterfaces03Data']}\n",
            f"ASAv Inside IP,{output['n0workASAvPrivate03']}\n",
            f"ASAv Outside IP,{output['n0workASAvPrivate02']}\n",
            f"Metasploit Attacker IP,{output['n0workAttacker']}\n",
            f"Ubuntu18.04 Employee IP,{output['n0workUbuntu1804Employee']}\n",
            f"Ubuntu18.04 SysAdmin IP,{output['n0workUbuntu1804SysAdmin']}\n",
            f"Pod AWS External Orchestrator Access Key,{output['PodAccessKey']}\n",
            f"Pod AWS External Orchestrator Secret Key,{output['PodSecretKey']}\n",
            f"Pod AWS Region,{output['n0workAWSRegion']}\n",
            f"Pod VPC Flow Log S3 Bucket,{output['n0workVPCFlowLogBucket']}\n",
            f"EKS Cluster API Endpoint (use for external orchestrator),{eks_endpoint_fqdn_only}\n",
            f"EKS Cluster CA Cert (should not need),{output['EKSClusterCertificate']}"
        ]
        
        filename = 'reports/' + f'n0work-{SESSION_NAME}-' + output['n0workPodName'] + '-report.csv'

        if not os.path.exists('reports'):
            os.makedirs('reports')
        
        print(f"INFO: Writing file: {filename} to reports/.")
        with open(filename, 'w') as file:
            file.writelines(columnar_output)
    
    # the old way
    # with open(filename, 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(header)
    #     writer.writerows(records)

except Exception as e:
    print(e)
    sys.exit(1)

#######################################################################
# Creating Scheduler
#######################################################################
if use_schedule:
    try:
        cloudformation = session.client('cloudformation', region_name=REGION)

        # Check to see if stack already exists in this region
        stacks = cloudformation.describe_stacks()['Stacks']
        stack = [True for item in stacks if item['StackName'] == 'n0work-instance-scheduler']

        if not stack:    
            with open ('n0work-scheduler-cft-template.yml', 'r') as f:
                cft = f.read()

            aws_parameters = [{'ParameterKey': 'Regions', 'ParameterValue': REGION},
            {'ParameterKey': 'StartedTags', 'ParameterValue': r"SchedulerMessage=Started on {year}/{month}/{day} at {hour}:{minute} {timezone}"},
            {'ParameterKey': 'StoppedTags', 'ParameterValue':  r"SchedulerMessage=Stopped on {year}/{month}/{day} at {hour}:{minute} {timezone}"},
            {'ParameterKey': 'CrossAccountRoles', 'ParameterValue': ""}
            ]

            print('INFO: Creating stack n0work-instance-scheduler')
            result = cloudformation.create_stack(
                StackName="n0work-instance-scheduler",
                TemplateBody=cft,
                Parameters=aws_parameters,
                Capabilities=[
                            'CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM',
                        ])
            # Wait for cloudformation stack to be created
            while True:
                status = cloudformation.describe_stacks(
                    StackName='n0work-instance-scheduler')['Stacks'][0]['StackStatus']
                if status == 'CREATE_COMPLETE':
                    print(f"INFO: Creating cloudformation stack n0work-instance-scheduler. Status={status}")
                    break
                elif 'ROLLBACK' in status:
                    print(f"ERROR: Creating cloudformation stack n0work-instance-scheduler. Status={status}")
                    print(f"ERROR: Check cloudformation events in the AWS dashboard")
                    sys.exit(1)
                else:
                    print(f"INFO: Creating cloudformation stack n0work-instance-scheduler. Status={status}")
                    time.sleep(5)
        else:
            print("INFO: Cloudformation stack n0work-instance-scheduler already exists in this region, skipping!")

        # Get the ServiceAccountToken
        outputs = cloudformation.describe_stacks(
                StackName='n0work-instance-scheduler'
            )['Stacks'][0]['Outputs']

        servicetoken = [item['OutputValue'] for item in outputs if item['OutputKey'] == 'ServiceInstanceScheduleServiceToken'][0]
        


    #######################################################################
    # Creating Class Schedule
    #######################################################################

        stack_payload = {
        "Resources": {
            "n0workHours": {
                "Type": "Custom::ServiceInstanceSchedule",
                "Properties": {
                    "Name": SCHEDULE_NAME,
                    "NoStackPrefix": "True",
                    "Description": "n0work Class Schedule",
                    "ServiceToken": servicetoken,
                    "Enforced": "True",
                    "Timezone": TIMEZONE,
                    "Periods": [
                        {
                            "Description": "n0work Period 01",
                            "BeginTime": BEGIN_TIME,
                            "EndTime": END_TIME,
                            "Months": START_MONTH,
                            "MonthDays": MONTHDAYS
                        },
                        {
                            "Description": "n0work Period 02 - 6hrs early for ADM run on day 2",
                            "BeginTime": ADM_START_TIME,
                            "EndTime": BEGIN_TIME,
                            "Months": ADM_MONTH,
                            "MonthDays": ADM_DAY

                        }
                    ]
                }
            }
        }
    }

        # Add a second period in the case the class falls on a month boundary.
        if START_MONTH != END_MONTH:
            MONTHDAYS = f"1-{END_DAY}"
            stack_payload['Resources']['n0workHours']['Properties']['Periods'].append({
                "Description": "n0work Period 03",
                "BeginTime": BEGIN_TIME,
                "EndTime": END_TIME,
                "Months": END_MONTH,
                "MonthDays": MONTHDAYS
            })

        print(f'INFO: Creating schedule {SCHEDULE_NAME}')
        result = cloudformation.create_stack(
            StackName=f"n0work-{SESSION_NAME}-class-schedule",
            TemplateBody=json.dumps(stack_payload),
            Capabilities=[
                        'CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM',
                    ])

        # Wait for class-schedule creation
        while True:
            status = cloudformation.describe_stacks(
                StackName=f'n0work-{SESSION_NAME}-class-schedule')['Stacks'][0]['StackStatus']
            if status == 'CREATE_COMPLETE':
                print(f"INFO: Creating cloudformation stack n0work-{SESSION_NAME}-class-schedule. Status={status}")
                break
            else:
                print(f"INFO: Creating cloudformation stack n0work-{SESSION_NAME}-class-schedule. Status={status}")
                time.sleep(5)

    except Exception as e:
        print(f"WARN: {e}")
#######################################################################
# Finishing up
#######################################################################

print(f'INFO: The report was written to: {filename}')
print('Exiting! All The Tasks Are Completed Successfully...')
sys.exit(0)