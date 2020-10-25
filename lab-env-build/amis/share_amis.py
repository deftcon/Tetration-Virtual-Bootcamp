import boto3
import yaml
import argparse
import logging
import sys

parser = argparse.ArgumentParser(description="Share or Un-Share AMIs in Ohio region with other accounts")

parser.add_argument('--account_id', '-a', required=True, help="AWS Account ID for sharing/unsharing")
parser.add_argument('--unshare', '-u', required=False, default=False, action='store_true')
args = parser.parse_args()

account_id = args.account_id
unshare = args.unshare

logformat = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level='INFO', format=logformat)
logger = logging.getLogger('ami_share')

with open ('ami_orig.yml','r') as f:
    ami_dict = yaml.safe_load(f)

if unshare:
    op_type = 'remove'
    operation = 'Removed'
else:
    op_type = 'add'
    operation = 'Added'

for ami in ami_dict.values():
    ec2 = boto3.resource('ec2', region_name="us-east-2")
    logger.info(f"Loading image {ami['id']}")
    source_ami = ec2.Image(ami['id'])
    source_ami.load()
    try:
        source_ami.modify_attribute(
            Attribute='launchPermission',
            OperationType=op_type,
            UserIds=[str(account_id)]
        )
    except Exception as e:
        logger.error(f"Error occurred while attempting to modify permissions: {e}")
        logger.error(f"Are you using the correct AWS API key/secret for the source account?")
        sys.exit(1)
    logger.info(f"{operation} launchPermission for account {account_id} on AMI {ami['id']}")
    source_snapshot = ec2.Snapshot(source_ami.block_device_mappings[0]['Ebs']['SnapshotId'])
    source_snapshot.load()
    logger.info(f"Found snapshot {source_snapshot.id}")
    try:
        source_snapshot.modify_attribute(
            Attribute='createVolumePermission',
            OperationType=op_type,
            UserIds=[str(account_id)]
        )
    except Exception as e:
        logger.error(f"Error occurred while attempting to modify permissions: {e}")
        logger.error(f"Are you using the correct AWS API key/secret for the source account?")
        sys.exit(1)
    logger.info(f"{operation} createVolumePermission for account {account_id} on snapshot {source_snapshot.id}")


logger.info('Finished!')



