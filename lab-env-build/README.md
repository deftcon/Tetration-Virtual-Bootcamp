# Cisco Tetration Virtual Bootcamp
  
<a href="https://github.com/deftcon/Tetration-Virtual-Bootcamp/tree/master/lab-env-build" target="_blank">Click Here First to open this repo in GitHub</a>  
  
## Lab Environment Deployment

<a href="https://learningnetwork.cisco.com/s/learning-activity-detail-standard-lp?ltui__urlRecordId=a0t3i000004MRV4AAO&ltui__urlRedirect=learning-activity-detail-standard-lp&ltui__parentUrl=learning-plan-detail-standard" target="_blank" style="font-weight:bold"><img src="https://tetration.guru/bootcamp-w-vids/diagrams/images/video_icon_small.png">Lab Setup Walk-Through Video can be found here on CLN</a>

This automated deployment builds three fully functional ecommerce web apps in either an existing or new AWS VPC for use in a lab environment. One Windows-based, one Linux-based, and one container-based ecommerce app operating in a Kubernetes cluster. 

Live web traffic is sent to each app every sixty seconds ensuring Tetration can observe flows and map applications without the user having to generate their own and remember and run ADM against those small windows of observable traffic. It does this using Lambda, which adds at least a tiny part of very likely real-world customer 'serverless' environment scenarios and the observations cloud workloads running in AWS would see. It contains a functional AD server that authenticates calls against the MSSQL DB, which is sent via the MS-RPC protocol which uses the ephemeral ports 49152-65535, along with <a href="https://docs.microsoft.com/en-us/troubleshoot/windows-server/networking/service-overview-and-network-port-requirements" target="_blank">the many other ports an AD server (application, really) brings to an actual customer environment</a>. In fact, most organizations have Active Directory, and it is one of (if not **the**) largest applications every organization runs from the important perspective of nearly every other workload in an organization's comprehensive environment, and especially requires segmenting and securing with near realtime updates to dynamically changing surrounding applications and workloads. 

This lab environment deploys entirely to AWS with the exception of Cisco ISE, which, if utilized with this lab for user-based policy (it is optional), requires you to have deployed yourself in a vCenter environment with a VPN connection into the AWS VPC (once the automated deployment has fully completed), as well as the appropriate route table additions on both sides. We do go into a bit of detail as to how to configure ISE for integration with Cisco Tetration, however we do not cover the fundamentals of ISE installation and basic deployment.
  
  
---  

> NOTE: This lab build DOES NOT deploy any type of instance(s) for the Tetration cluster itself (TaaS/Tetration-V, ), and ONLY deploys that which you see below in the "Complete Lab Diagram" inside of the "AWS Cloud" box with the already noted exception of ISE, as well as the exception of the necessary AMIs, which must be copied from Deft's AWS account and is detailed below in the next sub-section. It is necessary that you have your own instance of Tetration, whether On-Prem, Tet-V, or TaaS makes no difference, only that you have one provisioned. 

---  
  
This lab environment can be provisioned any time, before or after provisioning your instance of Tetration. You may wish to deploy it just to become familiar with the environment, or you may perhaps find another use for this lab environment, in which case <a href="https://github.com/deftcon/Tetration-Virtual-Bootcamp/issues/new?template=use_case.md" target="_blank">we'd love to know what your use-case is</a>. If you have any feature requests, those go <a href="https://github.com/deftcon/Tetration-Virtual-Bootcamp/issues/new?template=feature_request.md" target="_blank">here</a>. Bugs go <a href="https://github.com/deftcon/Tetration-Virtual-Bootcamp/issues/new?template=bug_report.md" target="_blank">here</a>. 

## Interactive Lab Diagram
  
<a href="https://www.lucidchart.com/documents/view/425e1b97-194e-413a-b793-0df939a87501" target="_blank">Complete Lab Diagram<img src="https://lucid.app/publicSegments/view/c88b4faf-7135-48ba-8344-1a75d6dc8fbe/image.png" style="width:100%;height:100%;"></a>  
  
  

#### AMIs Required Prior to AWS Lab Environment Deployment

There are a number of custom-built AMI images that require copying before deploying this lab environment. These images reside in Deftcon's GitHub account, and require us to add _**your**_ AWS Account ID to each AMI and Snapshot, therefore <a href="https://github.com/deftcon/Tetration-Virtual-Bootcamp/issues/new?template=ami_copy.md" target="_blank">fill out this form specifying your AWS Account ID</a>. You should receive an email in 24 hours or less (often much faster) indicating the permissions have been added and that you are ready to proceed with the below instructions.  
  
---  
NOTE: You cannot move on and run `launch.py` as instructed below until _**after**_ you receive an email reply indicating the permissions have been added to allow you access to the necessary AMIs. Failure to follow this will result in the `launch.py` failing miserably.

---  

For a few of the images, you must Subscribe to use them in AWS Marketplace before they can be launched.  Please follow the links below and proceed to "Continue to Subscribe".   

<a href="https://aws.amazon.com/marketplace/pp?sku=89bab4k3h9x4rkojcm2tj8j4l" target="_blank">Kali Linux</a>  
<a href="https://aws.amazon.com/marketplace/pp?sku=aw0evgkw8e5c1q413zgy5pjce" target="_blank">CentOS 7</a>      
<a href="https://aws.amazon.com/marketplace/pp/B00WRGASUC" target="_blank">ASAv</a>  

Accept the terms for each product and after a few moments a date should appear under "Effective Date".  It is not necessary to proceed to "Continue to Configuration" as this would be used to manually deploy an instance,  and this will be accomplished by automation using the lab setup script. 

---

The lab environment launcher requires Python 3.7 or later as well as a few packages which can be installed by running a pip install on the provided requirements file. We highly recommend setting up a <a href="https://docs.python.org/3/library/venv.html" target="_blank">Python Virtual Environment (venv)</a> for each AWS account that you plan to work with. This will allow you to store your AWS account credentials inside the specific virtual environment you create for this lab launcher, which also will aid greatly by isolating any Python modules that must be installed to fullfil the requirements for Python here, while not allowing any specific versions required to adversely impact any other Python code you may have. 
  

To create a new Python venv on MacOS or Linux:
```
python3 -m venv ~/.venvs/<your_venv_env_name>
```
  
  
Next you must generate API keys for <a href="https://console.aws.amazon.com/iam/home" target="_blank">an IAM user in your AWS account</a> and either export them to your OS Environment Variables (and continue to do this anytime you start a new shell), or you may opt to store them in a shell startup file that triggers the export upon every new shell creation. 

> NOTE: Generating API keys can be accomplished by navigating to the Identity and Access Management (IAM) service in the AWS console.  Under Users, select your user account and click on the `Security credentials` tab. 

If you choose to export them upon each new shell creation, simply export your environment variables in your terminal session as shown below:  
```
export AWS_ACCESS_KEY_ID=<YOUR AWS ACCESS KEY>
export AWS_SECRET_ACCESS_KEY=<YOUR AWS SECRET KEY>
```  
  

However, for a much more scalable and easy to use approach, you may consider storing them in a shell startup file. 

> NOTE: This next task involves something that some consider to be a huge security no-no and something that may be quite risky, depending. If you are operating on a machine that may be outside your control at any time, this is a serious security risk and you should consider if you truly wish to store your AWS credentials in a plain text file. Beware. Your milage may vary. Enter at your own risk. There be dragons here. Yadda yadda. That being said - we use it, and it is wonderful, especially switching between different AWS Account IDs! You have been warned.

Edit your new venv activation file:
```
vi ~/.venvs/<your_venv_env_name>/bin/activate
```
  
  
> Note: If you happen to use an alternative shell such as the absolutely wonderful <a href="https://fishshell.com/" target="_blank">fishshell</a>, you will need to edit a slightly different activation file:
```
vi ~/.venvs/<your_venv_env_name>/bin/activate.fish
```
  
  
Store your AWS credentials in your new venv activation file:
(note I am using the fishshell here, thus you may see extra stuff such as "set -gx" that you would not otherwise see in the plain bash activate file)
```
... skip down to the section that begins with "# unset irrelevant variables":
  
# unset irrelevant variables
deactivate nondestructive

set -gx VIRTUAL_ENV "/Users/msnow/.venvs/aws-deftcon"

set -gx _OLD_VIRTUAL_PATH $PATH
set -gx PATH "$VIRTUAL_ENV/bin" $PATH


### And insert your own section that sets your AWS credentials.
### You may find it helpful to list the IAM account that you used to create your 
### API Access/Secret key pair, and list the date so that you can later delete that 
### API key and recreate new keys, in keeping with good AWS security practices.

### Insert your section below, perhaps similar to something like this:

# set Deft Consult AWS creds (user@email  20-Oct-20)
set -gx AWS_ACCESS_KEY_ID "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
set -gx AWS_SECRET_ACCESS_KEY "NOWIKNOWMYABCSNEXTTIMEWONTYOUSINGWITHME?"


### Save the file and quit:
ESC
:wq
```
  
  
Now enter into that virtual environment:
```
source ~/.venvs/<your_venv_env_name>/bin/activate
```
  
  
Or if you are using the alternative <a href="https://fishshell.com/" target="_blank">fishshell</a>:
```
source ~/.venvs/<your_venv_env_name>/bin/activate.fish
```
  
  
Now install the python module requirements:
```
pip install -r requirements.txt
```
  
  

And now you should be ready to begin executing the python scripts necessary to launch the lab environment. 
  
  
---  
  

#### Deploying Pods
  
Deployment of the environment is accomplished by running the `launch.py` script. The `launch.py` script first copies the AMI files that are shared by the Deft AWS account to your AWS account in the `us-east-2` (OH) region.  The AMIs will then be copied to the destination region that you choose in the interactive prompts when running the script.  Of course, if the destination region is `us-east-2` then no further copying is necessary.  

The `launch.py` then executes one entire deployment of `cisco-hol-pod-cft-template.yml` per number of pods which you specify in the interactive prompts.  The pod number begins with `0000` and thus we recommend designating the first pod for the lab admin/instructor as a pristine deployment for use in demoing or troubleshooting any issues an actual student might for some reason encounter, and allowing the first student to be the second pod `pod0001`.

#### AMI Considerations

Note that the AMIs that are copied to `us-east-2` as well as to other regions currently will not be deleted during rollback. This ensures that the AMIs are present in the account so that they do not need to be continually copied each time `launch.py` is run,  allowing faster performance and reducing the data transfer cost which is incurred when copying the AMIs between regions.  Note that there will be a minimal cost incurred for the images and associated snapshots on a per-region basis.  If desired, you may manually delete the AMIs from a region.  However, it is imperative that you also delete the AMI ID file associated with the region.  An AMI ID file for each region is stored in the S3 bucket named `n0work-{AWS_ACCOUNT_ID}`,  where AWS_ACCOUNT_ID is your 12-digit AWS Account ID.  If AMIs have been deleted,  delete the file `{REGION_ID}-ami-ids.yml` from the S3 bucket.  The `launch.py` script obtains the AMI IDs to use for a region from this file.  If the file is present but the AMIs are not, the script will fail.  

#### Requirements / Dependencies

Important items to note prior to running `launch.py`:
1. You may use an existing VPC and Internet Gateway. This VPC must have at least two CIDR blocks, one for `subnet_range_primary` and one for `subnet_range_secondary`. It is important that **no** subnets already exist in this VPC, else the script will error out. `launch.py` will create the subnets and we have a brief discussion about them below.  

2. S3 Bucket: Due to the size of the CFT, AWS requires that we first upload it to an S3 bucket prior to calling it and executing against it. The S3 bucket `n0work-{AWS_ACCOUNT_ID}` will be created by `launch.py` and will store the CFT file as well as deployment state. 

3. Two (2) Elastic IPs per student pod. These must be already *allocated* to your region, but not yet *assigned* to any ENIs. This requirement exists due to AWS not allowing a Public IP to be assigned to any EC2 instance with more than a single ENI. There are currently three instances that have multiple ENIs, including Guacamole, Tet Data Ingest, and ASAv. Guac requires one so that students can access the environment from the public internet, and Tet Data Ingest requires the ability to communicate out to the internet to reach the TaaS cluster. ASAv only communicates internally, even if you have ISE running on-prem, assuming you have a VGW back to your CGW. If you need ASAv to speak externally, there is some code that can be uncommented in the `cisco-hol-pod-cft-template.yml` file. 

> NOTE: By default, [AWS limits you to five (5) Elastic IPs per region](https://docs.aws.amazon.com/general/latest/gr/vpc-service.html#w571aab9d325b7b3b5){:target="_blank"}. If you plan to deploy more than two (2) student pods, you will need to [submit a request for service quota increase](https://console.aws.amazon.com/support/home?#/case/create?issueType=service-limit-increase&limitType=vpc){:target="_blank"}. 


#### Subnets

A quick discussion on subnets to be created at launch time is in order. This VPC must have at least two CIDR blocks, one for `subnet_range_primary` and one for `subnet_range_secondary`.

The `subnet_range_primary` and `subnet_range_secondary` field both require that you give them /16 address space. This is due to the fact that for every student pod to be created, the third octet will be used to indicate the student index #. 

Also due to AWS strict requirement that there be at least two subnets available in order to spin up an EKS cluster, there will be two subnets created in `subnet_range_primary` per student - one will begin at the base and the other will be calculated to begin much higher, so that each subnet's third octet should (for the most part) follow the student numbering index value. 

Say you chose `10.0.0.0/16` as your primary range, and `198.18.0.0/16` as your secondary. You could expect to see three subnets generated, only the first two of which would ever be populated with any workloads. 

##### Examples:

**_Student 1_**
* 10.0.1.0/24    < "Internal / Corporate" workload subnet (Inside ASAv)
* 198.18.1.0/24  < "External / Internet" workload subnet (Outside ASAv)
* 10.0.128.0/24  < not used, simply required by AWS

**_Student 2_**
* 10.0.2.0/24    < "Internal / Corporate" workload subnet (Inside ASAv)
* 198.18.2.0/24  < "External / Internet" workload subnet (Outside ASAv)
* 10.0.129.0/24  < not used, simply required by AWS


> Note that the default subnet value for the secondary range is `198.18.0.0/16` and was chosen specifically becuase it both represented a "real internet, non-RFC1918 IP range", and also that it falls in the *'Reserved'* range, specifically that "This block has been allocated for use in benchmark tests of network interconnect devices" per [RFC5735](https://tools.ietf.org/html/rfc5735){:target="_blank"}. It could initially be argued that a range such as `198.51.100.0/24` or `203.0.113.0/24` would seem more appropos as they were created so that "This block is assigned as "TEST-NET-2/3" for use in documentation and example code", but they weren't large enough (/24), so the decision was made soundly to provide a real-world-like environment whilst simultaneously avoiding any blackholing any legitimate internet traffic from within the lab environment. 

Here is a diagram that will help to explain the subnets described above in a bit better visual detail: 
<a href="https://www.lucidchart.com/documents/view/425e1b97-194e-413a-b793-0df939a87501" target="_blank"><img src="https://lucid.app/publicSegments/view/c88b4faf-7135-48ba-8344-1a75d6dc8fbe/image.png" style="width:100%;height:100%;"></a>  
More can be found [in the Diagrams section](../bootcamp/diagrams/){:target="_blank"}.  
  

#### IAM Role API Credentials - Scope and Permissions

The AWS API Access key and Secret key used to deploy must be stored in the local OS environment variables. The environment variables should be labeled as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, respectively. The `launch.py` script requires the environment variables to function properly.  These can be set using the `export` command in your terminal:

```
export AWS_ACCESS_KEY_ID=<YOUR ACCCESS KEY ID>
export AWS_SECRET_ACCESS_KEY=<YOUR SECRET ACCESS KEY>
```

The AWS credentials used need to have permissions that allow them to create, update, and delete the following:

(AWS global)
* S3 bucket (for vpc flow logs)
* IAM role (for EKS)
* IAM User and API Keys with RO access to EC2 & ELB (for student external orchestrators) (this still needs tightening and S3 flow log access)

(Region specific)
* CloudFormation
* Lambda
* CloudWatch
* Eventbridge
* EKS Cluster / EKS Node Groups

(VPC specific)
* Route Tables
* Subnets
* Security Groups
* EC2 (including autoscaling)
* ELB

#### Deploying Lab Environment to AWS

Assuming you've filled out your desired values in `parameters.yml`, it's time to deploy. Change directory to the `lab-env-build` directory and run python to launch (the below assumes `python` aliases to `python3` or `python3.7`).

```bash
cd lab-env-build
python launch.py
```
>  Enter "Y" (case insensitive) to proceed. Anything other than y/Y will terminate the launch. 


```
A session name is required to uniquely identify your deployment
The session name can be between 5 and 25 characters, with no special characters allowed except for a dash (-).
Please enter the session name: deft-consult
How many pods are needed? 1
1: us-east-1 (N. Virginia)
2: us-east-2 (Ohio)
3: us-west-2 (Oregon)
4: af-south-1 (Africa - Cape Town))
5: ap-east-1 (Asia Pacific - Hong Kong)
6: ap-south-1 (Asia Pacific - Mumbai)
7: ap-northeast-3 (Asia Pacific - Osaka-Local)
8: ap-northeast-2 (Asia Pacific - Seoul)
9: ap-southeast-1 (Singapore)
10: ap-southeast-2 (Asia Pacific - Sydney)
11: ap-northeast-1 (Asia Pacific - Tokyo)
Please enter the AWS region you would like to deploy these pods in by entering the corresponding number: 2

These lab environment pods can be deployed into an existing VPC, or a new VPC can be created for you.
It is HIGHLY encouraged to allow this process to create the VPC and all components therein, for you.
One reason to choose the option to use an existing VPC is if you require more than two (2) pods (which require a total of 4 EIPs),
in which case you will need to make a request to AWS to increase the number of EIPs and have them allocated to a specific VPC-Id PRIOR to running this script.
To deploy into an existing VPC, the VPC ID and the ID of the Internet Gateway in the existing VPC will be needed,
as well as requiring the two (2) subnets chosen in the parameters.yml file to be associated to the VPC as attached CIDR Blocks.

Again, unless you require more than 2 pods to be deployed, you should allow this script to create everything for you.

Do you require only 1 or 2 pods and wish to have everything, including the VPC, created for you? (Y/N) y


Next, we require two (2) /16 CIDR blocks that will be used to create each pod's 'Inside' (or Corporate) and 'Outside' (or psuedo-Internet) subnet.
Both CIDR blocks MUST end in /16. This is essentially due to the fact that we let you pick the first two octets, then use the third octet for each new pod #,
and the fourth octet for the hosts in each pod.

Please enter a CIDR block to be used for the 'INSIDE' subnet for each Pod (MUST be in the format x.x.0.0/16): 10.1.0.0/16
Please enter a CIDR block to be used for the 'OUTSIDE' subnet for each Pod (MUST be in the format x.x.0.0/16): 198.18.0.0/16

INFO: Checking Available Elastic IPs...
INFO: Number of required Elastic IPs is 2, you currently have 0 available for use
INFO: Attempting to allocate 2 additional Elastic IPs...
INFO: Successfully allocated 2 Elastic IPs
INFO: Validating Subnet Range...
INFO: 256 Subnets Are Available...
INFO: Subnet Range Validation Completed...
INFO: Creating Pod Accounts Collection...
INFO: Pod Accounts Collection Created...

************************************************************************************************************************************************************
The lab can run continuously or you can define a schedule which allows cost savings in AWS by powering off EC2 instances when not using the lab environment.
When setting a schedule, the instances will be deployed now and will be running at first, then upon inspection of both the defined schedule and the state
of each EC2 instance, any running instances will be stopped (not terminated) and will spin up automatically when at the properly scheduled time.
Note that there will still be some AWS billing incurred starting today for the resources associated with the stopped instances and other lab components.
************************************************************************************************************************************************************

Would you like to define a schedule for the lab? (Y/N) n
You are about to deploy 1 pod(s) to a new VPC in the us-east-2 Region
Are you sure you wish to proceed with this deployment (y/Y to continue)? y
INFO: Creating S3 Bucket n0work-155098718727
INFO: Bucket n0work-155098718727 already exists, skipping
INFO: Checking bucket n0work-155098718727 for AMI file us-east-2-ami-ids.yml
INFO: Loading AMI IDs from us-east-2-ami-ids.yml in S3 bucket n0work-155098718727
INFO: Created VPC with ID vpc-00b5910c7463b8bd8 and CIDR block 10.1.0.0/16
INFO: Created Secondary CIDR block 198.18.0.0/16 on VPC vpc-00b5910c7463b8bd8
INFO: Created Internet Gateway with ID igw-0c65f187f9cc328f9
INFO: Associated Internet Gateway with ID igw-0c65f187f9cc328f9 to VPC vpc-00b5910c7463b8bd8
INFO: Uploading state file n0work-deft-consult-us-east-2-state.yml To S3 bucket n0work-155098718727...
INFO: Uploaded state file n0work-deft-consult-us-east-2-state.yml to bucket n0work-155098718727...
INFO: Uploading CFT Template n0work-deft-consult-pod-cft-template.yml To S3...
INFO: CFT Template n0work-deft-consult-pod-cft-template.yml Uploaded To S3...
INFO: Creating S3 Bucket n0work-deft-consult-lambda
INFO: Created S3 bucket n0work-deft-consult-lambda
INFO: Uploading lambda_function/tvb-dyndns.zip To S3 bucket n0work-deft-consult-lambda
INFO: lambda_function/tvb-dyndns.zip Uploaded To S3 bucket n0work-deft-consult-lambda
https://n0work-155098718727.s3.amazonaws.com/n0work-deft-consult-pod-cft-template.yml
INFO: StackName: n0work-deft-consult-pod0000, Status: CREATE_IN_PROGRESS
INFO: StackName: n0work-deft-consult-pod0000, Status: CREATE_IN_PROGRESS
INFO: StackName: n0work-deft-consult-pod0000, Status: CREATE_IN_PROGRESS
.
.
.
INFO: StackName: n0work-deft-consult-pod0000, Status: CREATE_IN_PROGRESS
INFO: StackName: n0work-deft-consult-pod0000, Status: CREATE_COMPLETE
INFO: CloudFormation Completed Successfully...
INFO: Deleting CFT file n0work-deft-consult-pod-cft-template.yml from S3 bucket n0work-155098718727
INFO: Preparing to initialize the EKS DNS Assembly...
INFO Initializing EKS DNS Assembly for pod pod0000...
INFO: List of ELBs in VPC vpc-00b5910c7463b8bd8: []
.
.
.
INFO: List of ELBs in VPC vpc-00b5910c7463b8bd8: ['afb719912a9064eb9978338f1f9b0a82']
INFO: Updating DNS for hostname: deft-consult-pod0000-sock-shop.lab.tetration.guru IP Address: 3.132.248.214
INFO: DNS update successful
INFO: elb afb719912a9064eb9978338f1f9b0a82 for pod pod0000 was found!
Waiting for EKS worker node i-05837dfa2b648e8d0 to pass health checks
EKS worker node i-05837dfa2b648e8d0 now has status of 'ok'!
INFO: Registering instance deft-consult-pod0000-eks-worker with elb afb719912a9064eb9978338f1f9b0a82
INFO: Checking to see if the instance attached to the ELB
INFO: Instance i-05837dfa2b648e8d0 is attached to elb afb719912a9064eb9978338f1f9b0a82
INFO: Instance status: OutOfService
INFO: Instance not in service yet. Retry in 15 seconds
INFO: Registering instance deft-consult-pod0000-eks-worker with elb afb719912a9064eb9978338f1f9b0a82
INFO: Checking to see if the instance attached to the ELB
INFO: Instance i-05837dfa2b648e8d0 is attached to elb afb719912a9064eb9978338f1f9b0a82
INFO: Instance status: InService
INFO: InService count: 1, check again in 5 sec...
INFO: Registering instance deft-consult-pod0000-eks-worker with elb afb719912a9064eb9978338f1f9b0a82
INFO: Checking to see if the instance attached to the ELB
INFO: Instance i-05837dfa2b648e8d0 is attached to elb afb719912a9064eb9978338f1f9b0a82
INFO: Instance status: InService
INFO: InService count: 2, check again in 5 sec...
INFO: Registering instance deft-consult-pod0000-eks-worker with elb afb719912a9064eb9978338f1f9b0a82
INFO: Checking to see if the instance attached to the ELB
INFO: Instance i-05837dfa2b648e8d0 is attached to elb afb719912a9064eb9978338f1f9b0a82
INFO: Instance status: InService
INFO: EKS DNS Assembly Completed...
INFO: Beginning deployment of DNS updater stack
INFO: Retrieving the instance IDs of the EC2 instances for Dynamic DNS
INFO: Updating DNS for hostname: deft-consult-pod0000-nopcommerce-mssql.lab.tetration.guru IP Address: 18.216.9.10
INFO: DNS update successful
INFO: Updating DNS for hostname: deft-consult-pod0000-user-employee.lab.tetration.guru IP Address: 13.58.208.84
INFO: DNS update successful
INFO: Updating DNS for hostname: deft-consult-pod0000-microsoft-ad-dc.lab.tetration.guru IP Address: 3.15.144.105
INFO: DNS update successful
INFO: Updating DNS for hostname: deft-consult-pod0000-user-sysadmin.lab.tetration.guru IP Address: 3.17.187.12
INFO: DNS update successful
INFO: Updating DNS for hostname: deft-consult-pod0000-bad-guy.lab.tetration.guru IP Address: 18.191.218.186
INFO: DNS update successful
INFO: Updating DNS for hostname: deft-consult-pod0000-opencart-apache.lab.tetration.guru IP Address: 3.137.181.245
INFO: DNS update successful
INFO: Updating DNS for hostname: deft-consult-pod0000-nopcommerce-iis.lab.tetration.guru IP Address: 3.139.237.156
INFO: DNS update successful
INFO: Updating DNS for hostname: deft-consult-pod0000-rh-ansible.lab.tetration.guru IP Address: 3.22.61.199
INFO: DNS update successful
INFO: Updating DNS for hostname: deft-consult-pod0000-opencart-mysql.lab.tetration.guru IP Address: 18.191.162.254
INFO: DNS update successful
INFO: Updating DNS for hostname: deft-consult-pod0000-guac-pod-ui.lab.tetration.guru IP Address: 3.130.235.41
INFO: DNS update successful
INFO: Creating stack n0work-deft-consult-dns-updater
INFO: Creating cloudformation stack n0work-deft-consult-dns-updater. Status=CREATE_IN_PROGRESS
.
.
.
INFO: Creating cloudformation stack n0work-deft-consult-dns-updater. Status=CREATE_IN_PROGRESS
INFO: Creating cloudformation stack n0work-deft-consult-dns-updater. Status=CREATE_COMPLETE
STACKS_LIST: ['n0work-deft-consult-pod0000']
INFO: StackName: n0work-deft-consult-pod0000, Status: Generating CSV Report...
INFO: Writing file: reports/n0work-deft-consult-pod0000-report.csv to reports/.
INFO: The report was written to: reports/n0work-deft-consult-pod0000-report.csv
Exiting! All The Tasks Are Completed Successfully...
```


Then you should find in your project root a `reports` directory, a CSV file for each pod containing the information required to access the pod. 

> If the script reports that the EKS Worker image could not be found,  it may be that the AMI ID has changed since this lab was developed.  The AMI ID changes from time to time as operating system patches are released and Amazon updates the images.  If this is the case,  this link has all possible region-specific AMIs for the EKS worker: - https://cloud-images.ubuntu.com/docs/aws/eks/

#### Tearing Down Lab Environment

Teardown is simple. 

```shell
python rollback.py
```

> Notice that on rollback we require a bit more stringent checking. This is for your protection. You will be asked to enter 'Y' initially and this is case sensitive, then a second verification is performed ensuring your intent, and this one requires you to type out 'YES' initially and this is case sensitive. Anything else will terminate the destruction of the environment. 

Assuming everything is correct you should have output similar to the following:


```bash
SELECTION  SESSION                   REGION          VPC                       SCHEDULE                  CREATED              CREATED BY
1          deft-consult           us-east-2       vpc-00b5910c7463b8bd8     Always-On                 Dec-05-2020 14:36    mark@deftconsult.io


Please select the number corresponding to the deployment you would like to roll back: 1
INFO: Validating Subnet Range...
INFO: 256 Subnets Are Available...
INFO: Subnet Range Validation Completed...
INFO: Creating Pod Accounts Collection...
INFO: [{'account_name': 'pod0000', 'public_subnet_01': '10.1.0.0', 'public_subnet_02': '10.1.128.0', 'private_subnet': '198.18.0.0'}]
INFO: Pod Accounts Collection Created...
You are about to DESTROY all pod pod(s) in vpc-00b5910c7463b8bd8 in the us-east-2 Region
Are you sure you wish to destroy all of these pods (type "Y" to continue)? Y
ARE YOU ABSOLUTELY SURE (type "YES" to continue)? YES
INFO: Looking up current IP address for deft-consult-pod0000-bad-guy.lab.tetration.guru
INFO: found IP address 18.191.218.186
INFO: Deleting DNS entry for hostname: deft-consult-pod0000-bad-guy.lab.tetration.guru IP Address: 18.191.218.186
INFO: DNS update successful
INFO: Looking up current IP address for deft-consult-pod0000-guac-pod-ui.lab.tetration.guru
INFO: found IP address 3.130.235.41
INFO: Deleting DNS entry for hostname: deft-consult-pod0000-guac-pod-ui.lab.tetration.guru IP Address: 3.130.235.41
INFO: DNS update successful
INFO: Looking up current IP address for deft-consult-pod0000-nopcommerce-mssql.lab.tetration.guru
INFO: found IP address 18.216.9.10
INFO: Deleting DNS entry for hostname: deft-consult-pod0000-nopcommerce-mssql.lab.tetration.guru IP Address: 18.216.9.10
INFO: DNS update successful
INFO: Looking up current IP address for deft-consult-pod0000-user-employee.lab.tetration.guru
INFO: found IP address 13.58.208.84
INFO: Deleting DNS entry for hostname: deft-consult-pod0000-user-employee.lab.tetration.guru IP Address: 13.58.208.84
INFO: DNS update successful
INFO: Looking up current IP address for deft-consult-pod0000-microsoft-ad-dc.lab.tetration.guru
INFO: found IP address 3.12.123.44
INFO: Deleting DNS entry for hostname: deft-consult-pod0000-microsoft-ad-dc.lab.tetration.guru IP Address: 3.12.123.44
INFO: DNS update successful
INFO: Looking up current IP address for deft-consult-pod0000-opencart-apache.lab.tetration.guru
INFO: found IP address 3.137.181.245
INFO: Deleting DNS entry for hostname: deft-consult-pod0000-opencart-apache.lab.tetration.guru IP Address: 3.137.181.245
INFO: DNS update successful
INFO: Looking up current IP address for deft-consult-pod0000-nopcommerce-iis.lab.tetration.guru
INFO: found IP address 3.14.143.212
INFO: Deleting DNS entry for hostname: deft-consult-pod0000-nopcommerce-iis.lab.tetration.guru IP Address: 3.14.143.212
INFO: DNS update successful
INFO: Looking up current IP address for deft-consult-pod0000-user-sysadmin.lab.tetration.guru
INFO: found IP address 3.17.187.12
INFO: Deleting DNS entry for hostname: deft-consult-pod0000-user-sysadmin.lab.tetration.guru IP Address: 3.17.187.12
INFO: DNS update successful
INFO: Looking up current IP address for deft-consult-pod0000-rh-ansible.lab.tetration.guru
INFO: found IP address 3.22.61.199
INFO: Deleting DNS entry for hostname: deft-consult-pod0000-rh-ansible.lab.tetration.guru IP Address: 3.22.61.199
INFO: DNS update successful
INFO: Looking up current IP address for deft-consult-pod0000-opencart-mysql.lab.tetration.guru
INFO: found IP address 18.191.162.254
INFO: Deleting DNS entry for hostname: deft-consult-pod0000-opencart-mysql.lab.tetration.guru IP Address: 18.191.162.254
INFO: DNS update successful
INFO: Disassociating EIP 3.130.235.41 from instance i-066495b086eb7b41d
INFO: Releasing EIP 3.130.235.41
INFO: Disassociating EIP 3.140.158.26 from instance i-0d77f0fcaadfa42b6
INFO: Releasing EIP 3.140.158.26
INFO: Initializing VPC Flow Logs S3 Bucket Deletion...
INFO: Emptying s3 bucket n0work-deft-consult-pod0000-vpc-flow-logs
INFO: Deleting s3 bucket n0work-deft-consult-pod0000-vpc-flow-logs
INFO: S3 Bucket Deleted: n0work-deft-consult-pod0000-vpc-flow-logs
INFO: S3 Bucket Deletion Complete...
INFO: Initializing EKS Load Balancers Deletion...
INFO: ELB Deleted: afb719912a9064eb9978338f1f9b0a82...
INFO: EKS Load Balancers Deletion Complete...
INFO: Deleting the class schedule
INFO: Deleted class schedule n0work-deft-consult-class-schedule
INFO: Deleting the DNS updater Lambda function n0work-deft-consult-dns-updater
INFO: Deleted DNS updater Lambda function n0work-deft-consult-dns-updater
INFO: Emptying s3 bucket n0work-deft-consult-lambda
INFO: Deleting s3 bucket n0work-deft-consult-lambda
INFO: S3 Bucket Deleted: n0work-deft-consult-lambda
INFO: Commencing CloudFormation Stack Deletion...
INFO: Stack deletion initiated for: n0work-deft-consult-pod0000...
INFO: CloudFormation deletion initiated for n0work-deft-consult-pod0000...
INFO: StackName: n0work-deft-consult-pod0000, Status: DELETE_IN_PROGRESS
.
.
.
INFO: StackName: n0work-deft-consult-pod0000, Status: DELETE_IN_PROGRESS
WARN: n0work-deft-consult-pod0000 does not exist or was deleted...
INFO: CloudFormation Rollback Completed Successfully...
INFO: Retrieve Internet Gateways
INFO: Detaching Internet Gateway igw-0c65f187f9cc328f9 from vpc-00b5910c7463b8bd8
INFO: Deleting Internet Gateway igw-0c65f187f9cc328f9
INFO: Retrieve VPCs
INFO: Deleting security group sg-0e8e274a2ed215a31
INFO: Deleting vpc vpc-00b5910c7463b8bd8
INFO: Deleting state file n0work-deft-consult-us-east-2-state.yml from S3 bucket n0work-155098718727
INFO: State file n0work-deft-consult-us-east-2-state.yml deleted from S3 bucket n0work-155098718727
INFO: Deleting deft-consult.lab.tetration.guru from Route53
INFO: Response from API - Your hostname record deft-consult.lab.tetration.guru with IP 127.0.0.1has been deleted
INFO: Retrieving IP address for deft-consult-pod0000-sock-shop.lab.tetration.guru
INFO Deleting DNS entry from Route 53 for deft-consult-pod0000-sock-shop.lab.tetration.guru
INFO: Your hostname record deft-consult-pod0000-sock-shop.lab.tetration.guru with IP 3.132.248.214has been deleted
INFO: Stack deletion initiated for: n0work-instance-scheduler...
INFO: Stack n0work-instance-scheduler was deleted...
INFO: Rollback completed successfully!
```

#### Limitations

You must have 2x EIPs per pod allocated to your region, as per the above section labeled "Requirements / Dependencies". 

Currently there is a limitation that prevents any ability to increment student pod count once deployed. Since it would take a bit of an effort to add, it is something we will be looking at however, don't aim to add anytime soon.  
  
---  
  
[Go to Top of Page](README.md)