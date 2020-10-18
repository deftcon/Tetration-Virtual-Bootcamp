# This script will create a scheduler and class schedule separate from launch.py if needed
# It might be used for example if a class is already scheduled but you want to make a change
# to the run time.  In that case, delete the existing class-schedule from DynamoDB and then
# run this script.  
# The instances must be separately tagged with Schedule=class-schedule for this to
# take affect.  The tag is configured on all instances when launch.py is run. 
import os
import boto3
import re
import yaml
from datetime import datetime
from time import sleep

REGION='us-east-2'
ACCESS_KEY=os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)

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
                    print(f"End time {t} is before start time {begin_time}, please try again!")
            else:
                return m.group()
        else:
            print(f"Invalid time {t} entered, please enter the time using 24hr format XX:XX")

def get_tz(prompt):
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
            print("Invalid timezone selection, please try again")

print("In order to reduce AWS costs, instances should be run only during class hours.")
print("Schedule the lab at least 30 minutes prior to class start in order to give the instances time to boot up.")
BEGIN_TIME = validate_time("Please enter the start time in 24-hour format (00:00-23:59): ")
END_TIME = validate_time("Please enter the end time in 24-hour format (00:00-23:59): ", BEGIN_TIME)
TIMEZONE = get_tz("Enter the number corresponding to your timezone in the above list: ")

cloudformation = session.client('cloudformation')

stacks = cloudformation.describe_stacks()['Stacks']
stack = [True for item in stacks if item['StackName'] == 'tethol-instance-scheduler']

if not stack:    

    with open ('cisco-hol-scheduler-cft-template.yml', 'r') as f:
        cft = f.read()

    aws_parameters = [{'ParameterKey': 'Regions', 'ParameterValue': 'us-east-2'},
    {'ParameterKey': 'StartedTags', 'ParameterValue': r"SchedulerMessage=Started on {year}/{month}/{day} at {hour}:{minute} {timezone}"},
    {'ParameterKey': 'StoppedTags', 'ParameterValue':  r"SchedulerMessage=Stopped on {year}/{month}/{day} at {hour}:{minute} {timezone}"},
    {'ParameterKey': 'CrossAccountRoles', 'ParameterValue': ""}
    ]

    print('Creating stack tethol-instance-scheduler')
    result = cloudformation.create_stack(
        StackName="tethol-instance-scheduler",
        TemplateBody=cft,
        Parameters=aws_parameters,
        Capabilities=[
                    'CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM',
                ])
else:
    print("Cloudformation stack tethol-instance-scheduler already exists in this region, skipping!")
# Wait for scheduler creation
    while True:
        status = cloudformation.describe_stacks(
            StackName='tethol-instance-scheduler')['Stacks'][0]['StackStatus']
        if status == 'CREATE_COMPLETE':
            print(f"Creating cloudformation stack tethol-instance-scheduler. Status={status}")
            break
        else:
            print(f"Creating cloudformation stack tethol-instance-scheduler. Status={status}")
            sleep(5)

# Get the ServiceAccountToken
outputs = cloudformation.describe_stacks(
          StackName='tethol-instance-scheduler'
       )['Stacks'][0]['Outputs']

servicetoken = [item['OutputValue'] for item in outputs if item['OutputKey'] == 'ServiceInstanceScheduleServiceToken'][0]

aws_parameters = [
{'ParameterKey': 'TimeZone', 'ParameterValue': TIMEZONE},
{'ParameterKey': 'BeginTime', 'ParameterValue': BEGIN_TIME},
{'ParameterKey': 'EndTime', 'ParameterValue':  END_TIME},
{'ParameterKey': 'ServiceToken', 'ParameterValue': servicetoken}
]

with open ('cisco-hol-class-schedule-cft-template.yml', 'r') as f:
     cft = f.read()

print('Creating schedule tethol-class-schedule')
result = cloudformation.create_stack(
    StackName="tethol-class-schedule",
    TemplateBody=cft,
    Parameters=aws_parameters,
    Capabilities=[
                'CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM',
            ])

# Wait for class-schedule creation
while True:
    status = cloudformation.describe_stacks(
        StackName='tethol-class-schedule')['Stacks'][0]['StackStatus']
    if status == 'CREATE_COMPLETE':
        print(f"Creating cloudformation stack tethol-class-schedule. Status={status}")
        break
    else:
        print(f"Creating cloudformation stack tethol-class-schedule. Status={status}")
        sleep(5)

print('Finished!')