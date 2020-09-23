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

if 'vpc_id' in params:
    CFT_POD_FILE = './cisco-hol-pod-cft-template-existvpc.yml'
else:
    CFT_POD_FILE = './cisco-hol-pod-cft-template-newvpc.yml'


ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

if ACCESS_KEY == None or ACCESS_KEY == '':
    ACCESS_KEY = params['aws_access_key']


if SECRET_KEY == None or SECRET_KEY == '':
    SECRET_KEY = params['aws_secret_key']


REGION = params['aws_region']
if 'vpc_id' in params:
    VPC_ID = params['vpc_id']
    INTERNET_GATEWAY_ID = params['internet_gateway_id']
VPC_CIDR = params['vpc_cidr']
SUBNET_RANGE_PRIMARY = params['subnet_range_primary']
SUBNET_RANGE_SECONDARY = params['subnet_range_secondary']
STUDENT_COUNT = params['student_count']
STUDENT_PREFIX = params['student_prefix']

S3_BUCKET = params['s3_bucket']

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)

MANAGEMENT_CIDR = ''

STACKS_LIST = []
STUDENTS_LIST = []
ELASTIC_IPS = []

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
#######################################################################


#######################################################################
# Verify VPC Id Provided, if using existing ###########################
#######################################################################
if 'vpc_id' in params:
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
# Check Existing Subnets if deploying into existing ###################
#######################################################################
    print(f'INFO: Checking Existing Subnets...')
    filters = [{'Name':'vpcId', 'Values':[VPC_ID]}]

    ec2 = session.resource('ec2')
    subnets_count = len(list(ec2.subnets.filter(Filters=filters)))

    if subnets_count > 0:
        print(f'ERROR: {subnets_count} Subnets Found In Current VPC...')
        exit(1)


    print(f'INFO: Subnet Check Completed...')
#######################################################################


#######################################################################
# Check Available Elastic IPs #########################################
#######################################################################
try:
    print('INFO: Checking Available Elastic IPs...')

    client = session.client('ec2')

    addresses_dict = client.describe_addresses()

    for eip_dict in addresses_dict['Addresses']:
        if 'NetworkInterfaceId' not in eip_dict:
            ELASTIC_IPS.append({
                'public_ip': eip_dict['PublicIp'],
                'allocation_id': eip_dict['AllocationId']
            })

    if len(ELASTIC_IPS) < (STUDENT_COUNT * 2):
        print(f'ERROR: Number Of Required Elastic IPs Are {STUDENT_COUNT * 2} But Only {len(ELASTIC_IPS)} Are Available...')
        exit(1)

    print('INFO: Created Available Elastic IPs Collection...')
except:
    print('ERROR: Unable To Get Available Elastic IPs...')
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

    print(f'INFO: {STUDENTS_LIST}')

except:
    print(f'ERROR: Invalid Subnet! Please provide a valid subnet range...')
    exit(1)


print(f'INFO: Student Accounts Collection Created...')
#######################################################################


#######################################################################
# Confirm Deploy Before Proceeding ####################################
#######################################################################
if 'vpc_id' in params:
    print(f'You are about to deploy {STUDENT_COUNT} student pod(s) to {VPC_ID} in the {REGION} Region')
else:
    print(f'You are about to deploy {STUDENT_COUNT} student pod(s) to a new VPC in the {REGION} Region')
rusure_response = input('Are you sure you wish to proceed with this deployment (y/Y to continue)? ')
if rusure_response.lower() != 'y':
    print('No pods were created, exiting now.')
    exit(1)
#######################################################################


#######################################################################
# Upload CFT TO S3 Bucket #############################################
#######################################################################
print('INFO: Uploading Template To S3...')
s3 = boto3.resource('s3')
if 'vpc_id' in params:
    s3.meta.client.upload_file('cisco-hol-pod-cft-template-existvpc.yml', S3_BUCKET, 'cisco-hol-pod-cft-template-existvpc.yml')
else:
    s3.meta.client.upload_file('cisco-hol-pod-cft-template-newvpc.yml', S3_BUCKET, 'cisco-hol-pod-cft-template-newvpc.yml')
print('INFO: CFT Template Uploaded To S3...')
#######################################################################


#######################################################################
# Run POD Cloud Formation #############################################
#######################################################################
for student in STUDENTS_LIST:

    try:

        outside_pod_ips = list(ipaddress.ip_network(f"{student['private_subnet']}/24").hosts())

        cloudformation = session.client('cloudformation')
        cloudformation_template = open(CFT_POD_FILE, 'r').read()

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
            {'ParameterKey': 'EKSWorkerImageID', 'ParameterValue': params['eks_worker_ami']}
        ]
        if 'vpc_id' in params:
            aws_parameters.append(
                {'ParameterKey': 'VpcID', 'ParameterValue': VPC_ID},
                {'ParameterKey': 'InternetGatewayId', 'ParameterValue': INTERNET_GATEWAY_ID},
                {'ParameterKey': 'VpcCIDR', 'ParameterValue': VPC_CIDR})

        print('INFO:', aws_parameters)

        result = cloudformation.create_stack(
            StackName=student['account_name'],
            # TemplateBody=cloudformation_template,
            TemplateURL=f"https://{S3_BUCKET}.s3.{REGION}.amazonaws.com/{CFT_POD_FILE }",
            Parameters=aws_parameters,
            Capabilities=[
                'CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM',
            ]
        )

        STACKS_LIST.append(student['account_name'])

    except Exception as e:
        print(e)
        exit(1)
#######################################################################

#######################################################################
# Wait For Stack Creation #############################################
#######################################################################
completed_stacks = []
while True:

    try:

        for stack_name in STACKS_LIST:

            if stack_name in completed_stacks:
                continue

            cloudformation = session.client('cloudformation')

            status = cloudformation.describe_stacks(
                StackName=stack_name
            )

            if status['Stacks'][0]['StackStatus'] == 'CREATE_COMPLETE':
                completed_stacks.append(stack_name)

            if status['Stacks'][0]['StackStatus'] == 'ROLLBACK_IN_PROGRESS' or  status['Stacks'][0]['StackStatus'] == 'ROLLBACK_COMPLETE':
                print(f"ERROR: Stack Failed => {stack_name}")
                print('ERROR: Unable To Complete CloudFormation Deployment.')
                exit(1)

            print(f"INFO: StackName: {stack_name}, Status: {status['Stacks'][0]['StackStatus']}")

        if len(STACKS_LIST) == len(completed_stacks):
            print('INFO: CloudFormation Completed Successfully...')
            break

        time.sleep(10)

    except Exception as e:
        print(e)
        exit(1)
#######################################################################

#######################################################################
# Assemble EKS ELB DNS Records ########################################
#######################################################################
try:

    print('INFO: Initializing EKS DNS Assembly...')

    time.sleep(120)

    for student in STUDENTS_LIST:

        client = session.client('elb')

        eks_elbs = client.describe_load_balancers()['LoadBalancerDescriptions']

        elb_tags = client.describe_tags(
            LoadBalancerNames=list(map(lambda e: e['LoadBalancerName'], eks_elbs))
        )

        for elb in elb_tags['TagDescriptions']:
            for tag in elb['Tags']:
                for key in tag:
                    if student['account_name'] in tag[key]:
                        student['eks_dns'] = list(filter(lambda e: e['LoadBalancerName'] == elb['LoadBalancerName'], eks_elbs))[0]['DNSName']
                        break
    

    print('INFO: EKS DNS Assembly Completed...')

except Exception as e:
    print(e)
    exit(1)
#######################################################################

#######################################################################
# Generate CSV Reports ################################################
######################################################################

try:

    records = []

    for stack_name in STACKS_LIST:

        print(f"INFO: StackName: {stack_name}, Status: Generating CSV Report...")

        cloudformation = session.client('cloudformation')

        stack = cloudformation.describe_stacks(
            StackName=stack_name
        )

        student = list(filter(lambda student: student['account_name'] == stack_name, STUDENTS_LIST))[0]

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

    filename = 'reports/' + datetime.today().strftime('%H-%M-%S %Y-%m-%d') + '-report.csv'

    if not os.path.exists('reports'):
        os.makedirs('reports')

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(records)

except Exception as e:
    print(e)
    exit(1)

#######################################################################


print('Exiting! All The Tasks Are Completed Successfully...')
exit(0)
