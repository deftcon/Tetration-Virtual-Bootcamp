import boto3

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
new_vpc_id = vpc['Vpc']['VpcId']

# Create Secondary CIDR
sec_cidr = client.associate_vpc_cidr_block(CidrBlock=SUBNET_RANGE_SECONDARY, VpcId=new_vpc_id)

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
inet_gateway_id = inet_gateway['InternetGateway']['InternetGatewayId']

# Associate Internet Gateway with VPC
ec2 = boto3.resource('ec2', region_name=REGION)
ig = ec2.InternetGateway(inet_gateway_id)
ig_associate = ig.attach_to_vpc(VpcId=new_vpc_id)
