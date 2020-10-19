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
from datetime import datetime
from datetime import timedelta
from botocore.config import Config
from botocore.exceptions import ClientError

PARAMETERS_FILE = './parameters.yml'

params = yaml.load(open(PARAMETERS_FILE), Loader=yaml.Loader)


CFT_POD_FILE = 'cisco-hol-pod-cft-template.yml'

ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

if ACCESS_KEY == None or ACCESS_KEY == '':
    ACCESS_KEY = params['aws_access_key']


if SECRET_KEY == None or SECRET_KEY == '':
    SECRET_KEY = params['aws_secret_key']

def get_student_count(prompt):
    while True:
        pattern = '^[0-9]+$'
        answer = input(prompt)
        m = re.match(pattern, answer)
        if m:
            return int(answer)

STUDENT_COUNT = get_student_count("How many students are needed? ")

def get_region(prompt):
    region_dict = {
        '1': ('us-east-1','N. Virginia'),
        '2': ('us-east-2', 'Ohio'),
        '3': ('us-west-1', 'N. California'),
        '4': ('us-west-2', 'Oregon'),
        '5': ('af-south-1', 'Africa - Cape Town)'),
        '6': ('ap-east-1', 'Asia Pacific - Hong Kong'),
        '7': ('ap-south-1', 'Asia Pacific - Mumbai'),
        '8': ('ap-northeast-3', 'Asia Pacific - Osaka-Local'),
        '9': ('ap-northeast-2', 'Asia Pacific - Seoul'),
        '10': ('ap-southeast-1', 'Singapore'),
        '11': ('ap-southeast-2', 'Asia Pacific - Sydney'),
        '12': ('ap-northeast-1', 'Asia Pacific - Tokyo')
    }
    for key in region_dict:
        print(f"{key}: {region_dict[key][0]} ({region_dict[key][1]})")
    while True:
        answer = input(prompt)
        if int(answer) > 0 and int(answer) < 13:
            return region_dict[answer][0]

REGION = get_region('Please enter the number corresponding to the AWS region to which you will be deploying: ')

def get_user_input(prompt, valid_pattern):
    while True:
      answer = input(prompt)
      m = re.match(valid_pattern, answer)
      if m:
          return answer
 
print("You may deploy into an existing AWS VPC, or a new VPC can be created.")
print("To deploy into an existing VPC, the VPC ID and the ID of the Internet Gateway in the existing VPC will be needed.")
print("If you do not choose to use an existing VPC, a new VPC and Internet Gateway will be created")
vpc_answer = get_user_input("Do you want to deploy into an existing VPC (Y/N)? ", "^[YyNn]$")
if vpc_answer.upper() == 'Y':
    VPC_ID = get_user_input("Enter the VPC ID: ", "^vpc-[0-9a-z]*")
    INTERNET_GATEWAY_ID = get_user_input("Enter the Internet Gateway ID: ", "^igw-[0-9a-z]*")
    use_existing_vpc = True
elif vpc_answer.upper() == 'N':
    use_existing_vpc = False


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

SUBNET_RANGE_PRIMARY = params['subnet_range_primary']
SUBNET_RANGE_SECONDARY = params['subnet_range_secondary']
# STUDENT_COUNT = params['student_count']
STUDENT_PREFIX = params['student_prefix']

S3_BUCKET = params['s3_bucket']

MANAGEMENT_CIDR = ''

STACKS_LIST = []
STUDENTS_LIST = []

def password_generator(size=14, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Gets the public IP address of system running this script
def get_public_ip():
    result = json.load(urllib.request.urlopen('https://api.ipify.org/?format=json'))
    return result['ip']


#######################################################################
# Get Management Cidr Block ###########################################
#######################################################################
try:
    print(f'INFO: Fetching Your Public IP for AWS SG Access "All Traffic" ...')
    MANAGEMENT_CIDR = f"{get_public_ip()}/32"
    print('INFO: Management Cidr:', MANAGEMENT_CIDR)
except:
    print(f'ERROR: Unable To Grab Your Public IP for the Management CIDR')
    sys.exit(1)



#######################################################################
# Check Existing Subnets if deploying into existing ###################
#######################################################################
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
print(f'INFO: Number of required Elastic IPs is {STUDENT_COUNT * 2}, you currently have {allocated_and_available} available for use')
succeeded_count = 0
if allocated_and_available < (STUDENT_COUNT * 2):   
    print(f'INFO: Attempting to allocate {(STUDENT_COUNT * 2) - allocated_and_available} additional Elastic IPs...')
    for i in range(1,((STUDENT_COUNT * 2) - allocated_and_available) + 1):
        try:
            eip = client.allocate_address()
            ELASTIC_IPS.append({
            'public_ip': eip['PublicIp'],
            'allocation_id': eip['AllocationId']})
            succeeded_count += 1
        except ClientError as e:
            if 'AddressLimitExceeded' in str(e):
                print(f'ERROR: Number of additional Elastic IPs is {(STUDENT_COUNT * 2) - allocated_and_available} and {succeeded_count} were able to be allocated.')
                print(f'Please go to the AWS portal to request increase of EIP limit by {(STUDENT_COUNT * 2) - allocated_and_available - succeeded_count} or more addresses:')
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
# Create Student Accounts #############################################
#######################################################################
try:
    print(f'INFO: Creating Student Accounts Collection...')
    primary_ips = list(ipaddress.ip_network(SUBNET_RANGE_PRIMARY).hosts())
    secondary_ips = list(ipaddress.ip_network(SUBNET_RANGE_SECONDARY).hosts())

    primary_ips = list(collections.OrderedDict.fromkeys(list(map(lambda ip: str(re.sub(r'([0-9]+)$', '0', str(ip))), primary_ips))))
    secondary_ips = list(collections.OrderedDict.fromkeys(list(map(lambda ip: str(re.sub(r'([0-9]+)$', '0', str(ip))), secondary_ips))))

    public_subnet_01 = primary_ips[:len(primary_ips)//2]
    public_subnet_02 = primary_ips[len(primary_ips)//2:]

    eip_index = 0

    for i in range(STUDENT_COUNT):
        STUDENTS_LIST.append({
            'account_name': f'{STUDENT_PREFIX}-0{i}',
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

#    print(f'INFO: {STUDENTS_LIST}')

except:
    print(f'ERROR: Invalid Subnet! Please provide a valid subnet range...')
    sys.exit(1)


print(f'INFO: Student Accounts Collection Created...')
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
    month_dict = {1:'jan',2:'feb',3:'mar',4:'apr',5:'may',6:'jun',7:'jul',8:'aug',9:'sep',10:'oct',11:'nov',12:'dec'}
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
print("***********************************************************************************************************************************")
print("The lab can begin running continuously now or you can set a schedule indicating when the lab should be active.")
print("Setting a schedule will help to manage the AWS cost, as the instances will only run during the time period specified.")
print("When setting a schedule, the instances will be deployed now and will be placed in a shut down state until the scheduled time slot.")
print("Note that there will still be some AWS billing incurred starting today for the resources associated with the stopped instances.")
print("In addition the lab will spin up 6 hours early on day 2 to allow agents enough time to stream telemetry in order to run ADM.")
print("This requires agents to be registered, annotations configured, and scopes to be created on day 1 of the training.")
print("***********************************************************************************************************************************")
answer = get_user_input("Would you like to set a schedule for the lab (Y/N) ", "^[YyNn]$")
if answer.upper() == 'Y':
    use_schedule = True
    START_MONTH = validate_month("Please enter the number corresponding to the month the class starts: ")
    START_DAY = validate_day("Please enter the numerical day of the month the class starts: ")
    END_MONTH = validate_month("Please enter the number corresponding to the month the class ends: ")
    END_DAY = validate_day("Please enter the numerical day of the month the class ends: ")
    BEGIN_TIME = validate_time("Please enter the start time in 24-hour format (00:00-23:59): ")
    END_TIME = validate_time("Please enter the end time in 24-hour format (00:00-23:59): ", BEGIN_TIME)
    TIMEZONE = validate_tz("Enter the number corresponding to your timezone in the above list: ")
else:
    use_schedule = False

# Create a start time 6 hours earlier than configured to allow flows for ADM 
dt = datetime.strptime(BEGIN_TIME, '%H:%M')
t = timedelta(hours=6)
dt_start = dt - t
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

month_dict = {1:'jan',2:'feb',3:'mar',4:'apr',5:'may',6:'jun',7:'jul',8:'aug',9:'sep',10:'oct',11:'nov',12:'dec'}
SCHEDULE_NAME = f"{month_dict[int(START_MONTH)]}{START_DAY}-to-{month_dict[int(END_MONTH)]}{END_DAY}-{BEGIN_TIME.replace(':','')}-{END_TIME.replace(':','')}"

#######################################################################
# Confirm Deploy Before Proceeding ####################################
#######################################################################
if use_existing_vpc:
    print(f'You are about to deploy {STUDENT_COUNT} student pod(s) to {VPC_ID} in the {REGION} Region')
else:
    print(f'You are about to deploy {STUDENT_COUNT} student pod(s) to a new VPC in the {REGION} Region')
if use_schedule:
    print(f"The lab will start at {BEGIN_TIME} and stop each day at {END_TIME} in the {TIMEZONE} timezone")
rusure_response = input('Are you sure you wish to proceed with this deployment (y/Y to continue)? ')
if rusure_response.lower() != 'y':
    print('No pods were created, sys.exiting now.')
    sys.exit(1)

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
                    'Value': 'Tetration HoL'
                },
                ]
            },
        ]
    )
    VPC_ID = vpc['Vpc']['VpcId']
    print(f"INFO: Created VPC with ID {VPC_ID} and CIDR block {SUBNET_RANGE_PRIMARY}")

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
                        'Value': 'Tetration HoL'
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
# CREATE THE S3 BUCKET FOR THE CFT TEMPLATE
#######################################################################

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
            print(f"INFO: Bucket {S3_BUCKET} already exists, skipping")
        elif 'BucketAlreadyExists' in e.response['Error']['Code']:
            print(f"INFO: Bucket {S3_BUCKET} already exists, skipping")
        else:
            print(f"ERROR: Error while creating S3 bucket {e}")
            sys.exit(1)
        return False
    return True

print(f"INFO: Creating S3 Bucket {S3_BUCKET}")
boto_config = Config(region_name = REGION)
if REGION == 'us-east-1':
    result = create_bucket(S3_BUCKET, boto_config)
else:
    result = create_bucket(S3_BUCKET, boto_config, region=REGION)

if result:
    print(f"INFO: Created S3 bucket {S3_BUCKET}")

#######################################################################
# Upload CFT TO S3 Bucket #############################################
#######################################################################
print('INFO: Uploading Template To S3...')
s3 = boto3.resource('s3', region_name=REGION)
s3.meta.client.upload_file(CFT_POD_FILE, S3_BUCKET, CFT_POD_FILE)
print('INFO: CFT Template Uploaded To S3...')


#######################################################################
# Run POD Cloud Formation #############################################
#######################################################################
for student in STUDENTS_LIST:

    try:

        outside_pod_ips = list(ipaddress.ip_network(f"{student['private_subnet']}/24").hosts())

        cloudformation = session.client('cloudformation', region_name=REGION)
        cloudformation_template = open(CFT_POD_FILE, 'r').read()

        NAMING_SUFFIX = VPC_ID[-6:]

        aws_parameters = [
            {'ParameterKey': 'AccessKey', 'ParameterValue': ACCESS_KEY},
            {'ParameterKey': 'SecretKey', 'ParameterValue': SECRET_KEY},

            {'ParameterKey': 'StudentIndex', 'ParameterValue': str(STUDENTS_LIST.index(student))},
            {'ParameterKey': 'StudentName', 'ParameterValue': student['account_name']},
            {'ParameterKey': 'StudentPassword', 'ParameterValue': student['account_password']},
            {'ParameterKey': 'ManagementCidrBlock', 'ParameterValue': MANAGEMENT_CIDR},

            {'ParameterKey': 'Subnet01CidrBlock', 'ParameterValue': f"{student['public_subnet_01']}/24"},
            {'ParameterKey': 'Subnet02CidrBlock', 'ParameterValue': f"{student['public_subnet_02']}/24"},
            {'ParameterKey': 'Subnet03CidrBlock', 'ParameterValue': f"{student['private_subnet']}/24"},

            {'ParameterKey': 'ASAvInsideSubnet', 'ParameterValue': student['public_subnet_01']},
            {'ParameterKey': 'ASAvOutsideSubnet', 'ParameterValue': student['private_subnet']},

            {'ParameterKey': 'GuacamoleElasticIp', 'ParameterValue': student['guacamole_elastic_ip']},
            {'ParameterKey': 'GuacamoleElasticIpAllocationId', 'ParameterValue': student['guacamole_elastic_ip_allocation_id']},

            {'ParameterKey': 'TetDataElasticIp', 'ParameterValue': student['tet_data_elastic_ip']},
            {'ParameterKey': 'TetDataElasticIpAllocationId', 'ParameterValue': student['tet_data_elastic_ip_allocation_id']},

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
            {'ParameterKey': 'NamingSuffix', 'ParameterValue': NAMING_SUFFIX}
            ]

        print('INFO:', aws_parameters)
        templateURL = f"https://{S3_BUCKET}.s3.{REGION}.amazonaws.com/{CFT_POD_FILE }"
        print(templateURL)
        result = cloudformation.create_stack(
            StackName=f"{student['account_name']}-{NAMING_SUFFIX}",
            # TemplateBody=cloudformation_template,
            TemplateURL=templateURL,
            Parameters=aws_parameters,
            Capabilities=[
                'CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM',
            ]
        )

        STACKS_LIST.append(f"{student['account_name']}-{NAMING_SUFFIX}")
        
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

#######################################################################
# Assemble EKS ELB DNS Records ########################################
#######################################################################
try:

    print('INFO: Initializing EKS DNS Assembly...')

    time.sleep(120)

    for student in STUDENTS_LIST:

        client = session.client('elb', region_name=REGION)

        eks_elbs = client.describe_load_balancers()['LoadBalancerDescriptions']

        elb_tags = client.describe_tags(
            LoadBalancerNames=list(map(lambda e: e['LoadBalancerName'], eks_elbs))
        )

        for elb in elb_tags['TagDescriptions']:
            for tag in elb['Tags']:
                for key in tag:
                    if student['account_name'] in tag[key]:
                        student['eks_dns'] = list(filter(lambda e: e['LoadBalancerName'] == elb['LoadBalancerName'], eks_elbs))[0]['DNSName']
                        elb_name = elb['LoadBalancerName']
                        break
    

    

#######################################################################################
# # Attach EKS worker node to ELB - workaround for instance not getting attached to ELB 
#######################################################################################
        ec2 = session.client('ec2',region_name=REGION)
        reservations = ec2.describe_instances()['Reservations']
        for reservation in reservations:
            instances = reservation['Instances']
            for instance in instances:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        if student['account_name'] in tag['Value'] and 'eks' in tag['Value'] and NAMING_SUFFIX in tag['Value']:
                            instance_id = instance['InstanceId']
                            print(f"INFO: Registering instance {tag['Value']} with elb {elb_name}")
                            client.register_instances_with_load_balancer(LoadBalancerName=elb_name, Instances=[{'InstanceId': instance_id}])
                            break
    
    print('INFO: EKS DNS Assembly Completed...')

except Exception as e:
    print(e)
    sys.exit(1)

#######################################################################
# Populate selected AWS region and student_count into parameters.yml for rollback
######################################################################

with open ('parameters.yml', 'r') as f:
    params_file = f.readlines()
for x, line in enumerate(params_file):
    if 'aws_region' in line:
        params_file[x] = f"aws_region: {REGION}\n"
    if 'student_count' in line:
        params_file[x] = f"student_count: {STUDENT_COUNT}\n"
with open('parameters.yml', 'w') as f:
    f.writelines(params_file)

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

        student = list(filter(lambda student: f"{student['account_name']}-{NAMING_SUFFIX}" == stack_name, STUDENTS_LIST))[0]

        output = {}

        for o in stack['Stacks'][0]['Outputs']:
            output[o['OutputKey']] = o['OutputValue']

        eks_endpoint = output['EKSClusterEndpoint']
        eks_endpoint_fqdn_only = (eks_endpoint.split('//'))[1]

        records.append([
            f"https://{output['CiscoHOLGuacamolePublic']}",
            output['CiscoHOLStudentName'],
            output['CiscoHOLStudentPassword'],
            f"http://{output['CiscoHOLIISPublic']}",
            f"http://{output['CiscoHOLApachePublic']}",
            f"http://{student['eks_dns']}",
            output['CiscoHOLPublicSubnet01'],
            output['CiscoHOLPrivateSubnet'],
            output['CiscoHOLActiveDirectory'],
            output['CiscoHOLISE'],
            output['CiscoHOLIISPrivate'],
            output['CiscoHOLIISOutsidePrivate'],
            output['CiscoHOLMSSQL'],
            output['CiscoHOLApachePrivate'],
            output['CiscoHOLApacheOutsidePrivate'],
            output['CiscoHOLMySql'],
            output['CiscoHOLAnsible'],
            output['CiscoHOLTetrationEdge'],
            output['TetNetworkInterfaces01Data'],
            output['TetNetworkInterfaces02Data'],
            output['TetNetworkInterfaces03Data'],
            output['CiscoHOLASAvPrivate03'],
            output['CiscoHOLASAvPrivate02'],
            output['CiscoHOLAttacker'],
            output['CiscoHOLUbuntu1804Employee'],
            output['CiscoHOLUbuntu1804SysAdmin'],
            output['StudentAccessKey'],
            output['StudentSecretKey'],
            output['CiscoHOLAWSRegion'],
            output['CiscoHOLVPCFlowLogBucket'],
            f"{eks_endpoint_fqdn_only}",
            output['EKSClusterCertificate'],
            # output['cisco-hol-cisco-student-00-public-subnet-01-us-east-2a'],
            # cisco-hol-cisco-student-00-vpc-flow-logs-us-east-2a
            # aws key will need perms to read this log

        ])

        header = [
            'Student Lab Access (Guac) Web Console URL',
            'Student Lab Access (Guac) Username',   
            'Student Lab Access (Guac) Password', 
            'nopCommerce Windows App URL',
            'OpenCart Linux App URL',
            'EKS SockShop App URL',
            'Student Internal/Inside Corporate Subnet',
            'Student External/Outside "Internet" Subnet',
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
            'Student AWS External Orchestrator Access Key',
            'Student AWS External Orchestrator Secret Key',
            'Student AWS Region',
            'Student VPC Flow Log S3 Bucket',
            'EKS Cluster API Endpoint (use for external orchestrator)',
            'EKS Cluster CA Cert (should not need)'
        ]

        columnar_output = [
            f"Student Lab Access (Guac) Web Console URL,https://{output['CiscoHOLGuacamolePublic']}\n",
            f"Student Lab Access (Guac) Username,{output['CiscoHOLStudentName']}\n",
            f"Student Lab Access (Guac) Password,{output['CiscoHOLStudentPassword']}\n",
            f"nopCommerce Windows App URL,http://{output['CiscoHOLIISPublic']}\n",
            f"OpenCart Linux App URL,http://{output['CiscoHOLApachePublic']}\n",
            f"EKS SockShop App URL,http://{student['eks_dns']}\n",
            f"Student Internal/Inside Corporate Subnet,{output['CiscoHOLPublicSubnet01']}\n",
            f"Student External/Outside Internet Subnet,{output['CiscoHOLPrivateSubnet']}\n",
            f"MS Active Directory IP,{output['CiscoHOLActiveDirectory']}\n",
            f"ISE Server IP,{output['CiscoHOLISE']}\n",
            f"MS IIS nopCommerce Inside IP,{output['CiscoHOLIISPrivate']}\n",
            f"MS IIS nopCommerce Outside IP,{output['CiscoHOLIISOutsidePrivate']}\n",
            f"MS SQL Private IP,{output['CiscoHOLMSSQL']}\n",
            f"Apache OpenCart Inside IP,{output['CiscoHOLApachePrivate']}\n",
            f"Apache OpenCart Outside IP,{output['CiscoHOLApacheOutsidePrivate']}\n"
            f"MySQL Private IP,{output['CiscoHOLMySql']}\n",
            f"Ansible IP,{output['CiscoHOLAnsible']}\n",
            f"Tetration Edge IP,{output['CiscoHOLTetrationEdge']}\n",
            f"Tetration Data Ingest IP 1,{output['TetNetworkInterfaces01Data']}\n",
            f"Tetration Data Ingest IP 2,{output['TetNetworkInterfaces02Data']}\n",
            f"Tetration Data Ingest IP 3,{output['TetNetworkInterfaces03Data']}\n",
            f"ASAv Inside IP,{output['CiscoHOLASAvPrivate03']}\n",
            f"ASAv Outside IP,{output['CiscoHOLASAvPrivate02']}\n",
            f"Metasploit Attacker IP,{output['CiscoHOLAttacker']}\n",
            f"Ubuntu18.04 Employee IP,{output['CiscoHOLUbuntu1804Employee']}\n",
            f"Ubuntu18.04 SysAdmin IP,{output['CiscoHOLUbuntu1804SysAdmin']}\n",
            f"Student AWS External Orchestrator Access Key,{output['StudentAccessKey']}\n",
            f"Student AWS External Orchestrator Secret Key,{output['StudentSecretKey']}\n",
            f"Student AWS Region,{output['CiscoHOLAWSRegion']}\n",
            f"Student VPC Flow Log S3 Bucket,{output['CiscoHOLVPCFlowLogBucket']}\n",
            f"EKS Cluster API Endpoint (use for external orchestrator),{eks_endpoint_fqdn_only}\n",
            f"EKS Cluster CA Cert (should not need),{output['EKSClusterCertificate']}"
        ]
        
        filename = 'reports/' + datetime.today().strftime('%Y-%m-%d-%H-%M-%S-') + output['CiscoHOLStudentName'] + '-report.csv'

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
        stack = [True for item in stacks if item['StackName'] == 'tethol-instance-scheduler']

        if not stack:    
            with open ('cisco-hol-scheduler-cft-template.yml', 'r') as f:
                cft = f.read()

            aws_parameters = [{'ParameterKey': 'Regions', 'ParameterValue': REGION},
            {'ParameterKey': 'StartedTags', 'ParameterValue': r"SchedulerMessage=Started on {year}/{month}/{day} at {hour}:{minute} {timezone}"},
            {'ParameterKey': 'StoppedTags', 'ParameterValue':  r"SchedulerMessage=Stopped on {year}/{month}/{day} at {hour}:{minute} {timezone}"},
            {'ParameterKey': 'CrossAccountRoles', 'ParameterValue': ""}
            ]

            print('INFO: Creating stack tethol-instance-scheduler')
            result = cloudformation.create_stack(
                StackName="tethol-instance-scheduler",
                TemplateBody=cft,
                Parameters=aws_parameters,
                Capabilities=[
                            'CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM',
                        ])
            # Wait for cloudformation stack to be created
            while True:
                status = cloudformation.describe_stacks(
                    StackName='tethol-instance-scheduler')['Stacks'][0]['StackStatus']
                if status == 'CREATE_COMPLETE':
                    print(f"INFO: Creating cloudformation stack tethol-instance-scheduler. Status={status}")
                    break
                else:
                    print(f"INFO: Creating cloudformation stack tethol-instance-scheduler. Status={status}")
                    time.sleep(5)
        else:
            print("INFO: Cloudformation stack tethol-instance-scheduler already exists in this region, skipping!")

        # Get the ServiceAccountToken
        outputs = cloudformation.describe_stacks(
                StackName='tethol-instance-scheduler'
            )['Stacks'][0]['Outputs']

        servicetoken = [item['OutputValue'] for item in outputs if item['OutputKey'] == 'ServiceInstanceScheduleServiceToken'][0]
        


    #######################################################################
    # Creating Class Schedule
    #######################################################################

        stack_payload = {
        "Resources": {
            "TetHoLHours": {
                "Type": "Custom::ServiceInstanceSchedule",
                "Properties": {
                    "Name": SCHEDULE_NAME,
                    "NoStackPrefix": "True",
                    "Description": "TetHol Class Schedule",
                    "ServiceToken": servicetoken,
                    "Enforced": "True",
                    "Timezone": TIMEZONE,
                    "Periods": [
                        {
                            "Description": "TetHol Period 01",
                            "BeginTime": BEGIN_TIME,
                            "EndTime": END_TIME,
                            "Months": START_MONTH,
                            "MonthDays": MONTHDAYS
                        },
                        {
                            "Description": "TetHol Period 02 - 6hrs early for ADM run on day 2",
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
            stack_payload['Resources']['TetHoLHours']['Properties']['Periods'].append({
                "Description": "TetHol Period 03",
                "BeginTime": BEGIN_TIME,
                "EndTime": END_TIME,
                "Months": END_MONTH,
                "MonthDays": MONTHDAYS
            })

        print(f'INFO: Creating schedule {SCHEDULE_NAME}')
        result = cloudformation.create_stack(
            StackName=f"tethol-class-schedule-{NAMING_SUFFIX}",
            TemplateBody=json.dumps(stack_payload),
            Capabilities=[
                        'CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM',
                    ])

        # Wait for class-schedule creation
        while True:
            status = cloudformation.describe_stacks(
                StackName=f'tethol-class-schedule-{NAMING_SUFFIX}')['Stacks'][0]['StackStatus']
            if status == 'CREATE_COMPLETE':
                print(f"INFO: Creating cloudformation stack tethol-class-schedule. Status={status}")
                break
            else:
                print(f"INFO: Creating cloudformation stack tethol-class-schedule-{NAMING_SUFFIX}. Status={status}")
                time.sleep(5)

    except Exception as e:
        print(f"WARN: {e}")
#######################################################################
# Finishing up
#######################################################################

print(f'INFO: The report was written to: {filename}')
print('sys.exiting! All The Tasks Are Completed Successfully...')
sys.exit(0)
