import json
import boto3
import requests
import os
import re

def get_hostname(instance_obj):
    for tag in instance_obj.tags:
        if tag['Key'] == 'DNS':
            hostname = tag['Value']
    return hostname

def update_dns(public_ip, hostname):
    api_key = os.environ.get('X_API_KEY')
    api_url = os.environ.get('API_URL')
    headers = {'x-api-key': api_key }
    query_params = {'mode':'set', 'hostname': hostname, 'ipv4_address': public_ip}
    response = requests.get(api_url, headers=headers, params=query_params)
    return response
    
def lambda_handler(event, context):
    region = event['region']
    instance_id = event['detail']['instance-id']
    print(instance_id)
    ec2 = boto3.resource('ec2', region_name=region)
    instance_obj = ec2.Instance(instance_id)
    public_ip = instance_obj.public_ip_address
    print(public_ip)
    hostname = get_hostname(instance_obj)
    print(hostname)
    result = update_dns(public_ip, hostname)
    return {
        'statusCode': result.status_code,
        'body': json.dumps(result.content)
    }
