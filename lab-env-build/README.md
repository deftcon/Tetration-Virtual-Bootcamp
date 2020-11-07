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
NOTE: You cannot move on and run `ami_create.py` as instructed below until _**after**_ you receive an email reply indicating the permissions have been added to allow you access to the necessary AMIs. Failure to follow this will result in both the `ami_create.py` and the `launch.py` failing miserably.

---  

For a few of the images, you must Subscribe to use them in AWS Marketplace before they can be launched.  Please follow the links below and proceed to "Continue to Subscribe".   

<a href="https://aws.amazon.com/marketplace/pp?sku=89bab4k3h9x4rkojcm2tj8j4l" target="_blank">Kali Linux</a>  
<a href="https://aws.amazon.com/marketplace/pp?sku=aw0evgkw8e5c1q413zgy5pjce" target="_blank">CentOS 7</a>      
<a href="https://aws.amazon.com/marketplace/pp/B00WRGASUC" target="_blank">ASAv</a>  

Accept the terms for each product and after a few moments a date should appear under "Effective Date".  It is not necessary to proceed to "Continue to Configuration" as this would be used to manually deploy an instance,  and this will be accomplished by automation using the lab setup script. 

Once you are subscribed to the above products,  a script called `ami_create.py` can be run to create new image files in your account and optionally copy them to another region. The script automates the process of creating the AMIs and populates the AMI IDs into the `parameters.yml` file which will later be used to launch all of the instances.  

`ami_create.py` requires Python 3.7 or later as well as the boto3 and pyyaml packages which can be installed by executing the following commands:

```
pip install boto3
pip install pyyaml
```
  
You will also need to retrieve your AWS API Keys and export them as environment variables in your terminal session as shown below:  
```
export AWS_ACCESS_KEY_ID=<YOUR AWS ACCESS KEY>
export AWS_SECRET_ACCESS_KEY=<YOUR AWS SECRET KEY>
```  
> Generating API keys can be accomplished by navigating to the Identity and Access Management (IAM) service in the AWS console.  Under Users, select your user account and click on the `Security credentials` tab. 

In addition, when the AMIs were shared with your account you should have also been emailed the API Gateway URL and API Gateway Key.  These are used to dynamically update the DNS records of the public-facing web servers when they are booted. They will also need to be entered as environment variables on your system as shown below. 

```
export API_GATEWAY_URL=<API GATEWAY URL>
export API_GATEWAY_KEY=<API GATEWAY KEY>
```
> If you did not receive this information,  please open an issue  https://github.com/deftcon/Tetration-Virtual-Bootcamp/issues


The script can then be run with the below command.  The region command-line argument is optional, and if omitted the AMIs will be created in the us-east-2 region.  If you plan to run the lab from an AWS region other than us-east-2, specify `--region` followed by the region name to have the AMIs copied to the destination region. 

```
python ami_create.py --region us-east-1
```

> It may be a good time to take a break as this script will take around 10-15 minutes to complete. 
  
#### Files Required to Deploy to AWS

Deployment of the environment for lab pod(s) requires the use of three files - namely: `parameters.yml`, `cisco-hol-pod-cft-template.yml`, and `launch.py`. 


`launch.py` reads in the parameters unique to each deployment set from `parameters.yml`, then executes one entire deployment of `cisco-hol-pod-cft-template.yml` per number of `student_count` found in `parameters.yml`. Student count begins with `00` and thus we recommend designating the first pod for the lab admin/instructor as a pristine deployment for use in demoing or troubleshooting any issues an actual student might for some reason encounter, and allowing the first student to be the second pod, which would begin with the numbering `01`. 

#### Parameters File Example

Below is an example of a `parameters.yml` file. You will need to modify the file to meet your needs and save it in the `lab-env-build` directory.  Note that you can deploy into an existing VPC or a new VPC can be created.  To deploy a new VPC,  comment out the lines beginning with `vpc_id` and `internet_gateway_id` by placing a `#` symbol in front of them.  If using an existing VPC, you must retrieve the VPC ID and Internet Gateway ID from the AWS dashboard and populate those values as shown in the example below.  


```yaml
---
---
aws_region: us-east-2

student_count: 1
student_prefix: cisco-student

# Enter the VPC ID below if using existing VPC. Comment if creating new VPC, it will be populated here upon creation.
# vpc_id: vpc-0b60cc1d07160596b

# Enter the IG_ID if using existing VPC. Comment if auto-creating new VPC by commenting out the VPC above.
# internet_gateway_id: igw-036df93d2c7cc253b 
subnet_range_primary: 10.1.0.0/16
subnet_range_secondary: 198.18.0.0/16

# S3 Bucket is global DNS unique name, use any arbitrary desired non-overlapping name. Will be created if doesn't exist.
s3_bucket: 'deft2-tetration-hol-cft-template' 

# This is your own private on-prem ISE instance - needs VPN with AWS VGW. If not using ISE simply give it any value, however do not comment. 
ise_server_ip: '172.16.171.49' 

asav_ami: ami-0cc6d931eeb481121
eks_worker_ami: ami-0c12dc9171d7252ad
ldap_ami: ami-063ca8b269537841f
mssql_ami: ami-090a4930496cbe28a
iis_ami: ami-02066420ce75afcb0
mysql_ami: ami-0caaa7c0eadaec7b5
apache_ami: ami-01d583af8e8932759
ansible_ami: ami-02e353df2bfb03bc1
tet_data_ami: ami-014df3ebd0af05bbe
tet_edge_ami: ami-028c27c2b07a3aee7
employee_ubuntu_ami: ami-08f5365f20685309f
sysadmin_ubuntu_ami: ami-08f5365f20685309f
attack_server_ami: ami-0011d2ead8e1e276f
guacamole_ami: ami-0a4a0a2c7dd763d53


```

#### Requirements / Dependencies

Important items to note prior to running `launch.py`:
1. You may use an existing VPC and Internet Gateway, and if so their IDs must be specified in the `parameters.yml` file. Alternatively, you can comment out the `vpc_id` line in the `parameters.yml` file which will cause the script to create a new VPC and Internet Gateway. This VPC must have at least two CIDR blocks, one for `subnet_range_primary` and one for `subnet_range_secondary`. It is important that **no** subnets be created in this VPC whatsoever, else the script will error out. `launch.py` will create the subnets and we have a brief discussion about them below.  

2. S3 Bucket: Due to the size of the CFT, AWS requires that we first upload it to an S3 bucket prior to calling it and executing against it. The S3 bucket will be created by `launch.py` using the bucket name defined in the `parameters.yml` file `s3_bucket` value.  
The name must be unique globally, and must conform to standard DNS naming nomenclature.  

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

The AWS API Access key and Secret key used to deploy must be stored in the local OS environment variables. The environment variables should be labeled as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, respectively. Both the `ami_create.py` and `launch.py` scripts require the environment variables to function properly.  These can be set using the `export` command in your terminal:

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
> Note that you will be asked to verify most of the data in parameters before proceeding. Enter "Y" (case insensitive) to proceed. Anything other than y/Y will terminate the launch. 

Assuming everything is correct you should have output similar to the following:

```bash
INFO: Fetching Public IP Of The Orchestrator...
INFO: Management Cidr: <--REDACTED - YOUR CURRENT IP-->/32
INFO: Checking VPC ID: vpc-082d43bff04cd342e...
INFO: VPC ID Verified: vpc-082d43bff04cd342e...
INFO: Checking Existing Subnets...
INFO: Subnet Check Completed...
INFO: Checking Available Elastic IPs...
INFO: Created Available Elastic IPs Collection...
INFO: Validating Subnet Range...
INFO: 256 Subnets Are Available...
INFO: Subnet Range Validation Completed...
INFO: Creating Student Accounts Collection...
INFO: [{'account_name': 'cisco-student-00', 'account_password': '8AetfFvCbUiKue', 'public_subnet_01': '10.1.0.0', 'public_subnet_02': '10.1.128.0', 'private_subnet': '198.18.0.0', 'eks_dns': '', 'guacamole_elastic_ip': '3.134.26.220', 'guacamole_elastic_ip_allocation_id': 'eipalloc-00ff1ef8b0c8562ad', 'tet_data_elastic_ip': '3.20.190.112', 'tet_data_elastic_ip_allocation_id': 'eipalloc-025e2db995a9b3751'}]
INFO: Student Accounts Collection Created...
You are about to deploy 1 student pod(s) to vpc-082d43bff04cd342e in the us-east-2 Region
Are you sure you wish to proceed with this deployment (y/Y to continue)? y
INFO: Uploading Template To S3...
INFO: CFT Template Uploaded To S3...
INFO: [{'ParameterKey': 'AccessKey', 'ParameterValue': '<--REDACTED-->'}, {'ParameterKey': 'SecretKey', 'ParameterValue': '<--REDACTED-->'}, {'ParameterKey': 'StudentIndex', 'ParameterValue': '0'}, {'ParameterKey': 'StudentName', 'ParameterValue': 'cisco-student-00'}, {'ParameterKey': 'StudentPassword', 'ParameterValue': '8AetfFvCbUiKue'}, {'ParameterKey': 'ManagementCidrBlock', 'ParameterValue': '172.116.159.56/32'}, {'ParameterKey': 'VpcID', 'ParameterValue': 'vpc-082d43bff04cd342e'}, {'ParameterKey': 'InternetGatewayId', 'ParameterValue': 'igw-0fec2ea47e798ea86'}, {'ParameterKey': 'Subnet01CidrBlock', 'ParameterValue': '10.1.0.0/24'}, {'ParameterKey': 'Subnet02CidrBlock', 'ParameterValue': '10.1.128.0/24'}, {'ParameterKey': 'Subnet03CidrBlock', 'ParameterValue': '198.18.0.0/24'}, {'ParameterKey': 'ASAvInsideSubnet', 'ParameterValue': '10.1.0.0'}, {'ParameterKey': 'ASAvOutsideSubnet', 'ParameterValue': '198.18.0.0'}, {'ParameterKey': 'GuacamoleElasticIp', 'ParameterValue': '3.134.26.220'}, {'ParameterKey': 'GuacamoleElasticIpAllocationId', 'ParameterValue': 'eipalloc-00ff1ef8b0c8562ad'}, {'ParameterKey': 'TetDataElasticIp', 'ParameterValue': '3.20.190.112'}, {'ParameterKey': 'TetDataElasticIpAllocationId', 'ParameterValue': 'eipalloc-025e2db995a9b3751'}, {'ParameterKey': 'Region', 'ParameterValue': 'us-east-2'}, {'ParameterKey': 'Subnet01AvailabilityZone', 'ParameterValue': 'a'}, {'ParameterKey': 'Subnet02AvailabilityZone', 'ParameterValue': 'b'}, {'ParameterKey': 'Subnet03AvailabilityZone', 'ParameterValue': 'a'}, {'ParameterKey': 'ISEIPAddress', 'ParameterValue': '172.16.171.49'}, {'ParameterKey': 'Win10EmployeePrivateIp', 'ParameterValue': '198.18.0.12'}, {'ParameterKey': 'Win10SysAdminPrivateIp', 'ParameterValue': '198.18.0.13'}, {'ParameterKey': 'AttackerPrivateIp', 'ParameterValue': '198.18.0.14'}, {'ParameterKey': 'IISOutsidePrivateIp', 'ParameterValue': '198.18.0.15'}, {'ParameterKey': 'ApacheOutsidePrivateIp', 'ParameterValue': '198.18.0.16'}, {'ParameterKey': 'ASAvOutsidePrivateIp01', 'ParameterValue': '198.18.0.17'}, {'ParameterKey': 'ASAvOutsidePrivateIp02', 'ParameterValue': '198.18.0.18'}, {'ParameterKey': 'Ubuntu1804EmployeePrivateIp', 'ParameterValue': '198.18.0.19'}, {'ParameterKey': 'Ubuntu1804SysAdminPrivateIp', 'ParameterValue': '198.18.0.20'}, {'ParameterKey': 'GuacamoleOutsidePrivateIp', 'ParameterValue': '198.18.0.21'}, {'ParameterKey': 'ASAvImageID', 'ParameterValue': 'ami-018637632d5e62976'}, {'ParameterKey': 'LDAPImageID', 'ParameterValue': 'ami-0273c11f1bc3fff82'}, {'ParameterKey': 'MSSQLImageID', 'ParameterValue': 'ami-090ab21d87411b44e'}, {'ParameterKey': 'IISImageID', 'ParameterValue': 'ami-0c4e857f7ec9de0dc'}, {'ParameterKey': 'MySQLImageID', 'ParameterValue': 'ami-0c170ef4a4f9b1789'}, {'ParameterKey': 'ApacheImageID', 'ParameterValue': 'ami-0bb3d60453bbc693a'}, {'ParameterKey': 'AnsibleImageID', 'ParameterValue': 'ami-08faf88a030245bd6'}, {'ParameterKey': 'TetrationDataIngestImageID', 'ParameterValue': 'ami-0c2276fc51ad25018'}, {'ParameterKey': 'TetrationEdgeImageID', 'ParameterValue': 'ami-0cb78ddba97ce6591'}, {'ParameterKey': 'Win10EmployeeImageID', 'ParameterValue': 'ami-03a948df14a70d159'}, {'ParameterKey': 'Win10SysAdminImageID', 'ParameterValue': 'ami-03a948df14a70d159'}, {'ParameterKey': 'Ubuntu1804EmployeeImageID', 'ParameterValue': 'ami-0483fe5b0c9444daa'}, {'ParameterKey': 'Ubuntu1804SysAdminImageID', 'ParameterValue': 'ami-0483fe5b0c9444daa'}, {'ParameterKey': 'AttackerImageID', 'ParameterValue': 'ami-09b253f6574754048'}, {'ParameterKey': 'GuacamoleImageID', 'ParameterValue': 'ami-04e70edcc169673d7'}, {'ParameterKey': 'EKSWorkerImageID', 'ParameterValue': 'ami-0c4c60006aa81c29b'}]
INFO: StackName: cisco-student-00, Status: CREATE_IN_PROGRESS
INFO: StackName: cisco-student-00, Status: CREATE_IN_PROGRESS
INFO: StackName: cisco-student-00, Status: CREATE_IN_PROGRESS
INFO: StackName: cisco-student-00, Status: CREATE_IN_PROGRESS
INFO: StackName: cisco-student-00, Status: CREATE_IN_PROGRESS
INFO: StackName: cisco-student-00, Status: CREATE_IN_PROGRESS
.
.
.
INFO: StackName: cisco-student-00, Status: CREATE_IN_PROGRESS
INFO: StackName: cisco-student-00, Status: CREATE_IN_PROGRESS
INFO: StackName: cisco-student-00, Status: CREATE_COMPLETE
INFO: CloudFormation Completed Successfully...
INFO: Initializing EKS DNS Assembly...
INFO: EKS DNS Assembly Completed...
INFO: StackName: cisco-student-00, Status: Generating CSV Report...
Exiting! All The Tasks Are Completed Successfully...
```

Then you should find in your project root a `reports` directory, a CSV file with every students' information. An enhancement to export a single XLS file with nicely formatted info *per student* is something we aim to do, in addition to the currently exported single CSV which is still very useful for the Lab Admin. 

> If the script reports that the EKS Worker image could not be found,  it may be that the AMI ID has changed since this lab was developed.  The AMI ID changes from time to time as operating system patches are released and Amazon updates the images.  If this is the case,  this link has all possible region-specific AMIs for the EKS worker: - https://cloud-images.ubuntu.com/docs/aws/eks/

#### Tearing Down Lab Environment

Teardown is simple. **_Ensure your `parameters.yml` file is the environment you want to teardown, and ...:_**

```shell
python rollback.py
```

> Note that you will be asked to verify most of the data in parameters before proceeding. Notice that on rollback we require a bit more stringent checking. This is for your protection. You will be asked to enter 'Y' initially and this is case sensitive, then a second verification is performed ensuring your intent, and this one requires you to type out 'YES' initially and this is case sensitive. Anything else will terminate the destruction of the environment. 

Assuming everything is correct you should have output similar to the following:


```bash
INFO: Checking VPC ID: vpc-082d43bff04cd342e...
INFO: VPC ID Verified: vpc-082d43bff04cd342e...
INFO: Validating Subnet Range...
INFO: 256 Subnets Are Available...
INFO: Subnet Range Validation Completed...
INFO: Creating Student Accounts Collection...
INFO: [{'account_name': 'cisco-student-00', 'public_subnet_01': '10.1.0.0', 'public_subnet_02': '10.1.128.0', 'private_subnet': '198.18.0.0'}]
INFO: Student Accounts Collection Created...
You are about to DESTROY all student pod(s) in vpc-082d43bff04cd342e in the us-east-2 Region
Are you sure you wish to destory all of these pods (type "Y" to continue)? Y
ARE YOU ABSOLUTELY SURE (type "YES" to continue)? YES
INFO: Initializing VPC Flow Logs S3 Bucket Deletion...
INFO: S3 Bucket Deleted: cisco-hol-cisco-student-00-vpc-flow-logs-us-east-2a
INFO: S3 Bucket Deletion Complete...
INFO: Initializing EKS Load Balancers Deletion...
INFO: ELB Deleted: a360fa1f4581311eab1f0066d929a5c5...
INFO: EKS Load Balancers Deletion Complete...
INFO: Commencing CloudFormation Stack Deletion...
INFO: Stack Deleted: cisco-student-00...
INFO: CloudFormation Stacks Deletion Complete...
INFO: StackName: cisco-student-00, Status: DELETE_IN_PROGRESS
INFO: StackName: cisco-student-00, Status: DELETE_IN_PROGRESS
INFO: StackName: cisco-student-00, Status: DELETE_IN_PROGRESS
INFO: StackName: cisco-student-00, Status: DELETE_IN_PROGRESS
INFO: StackName: cisco-student-00, Status: DELETE_IN_PROGRESS
INFO: StackName: cisco-student-00, Status: DELETE_IN_PROGRESS
INFO: StackName: cisco-student-00, Status: DELETE_IN_PROGRESS
.
.
.
INFO: StackName: cisco-student-00, Status: DELETE_IN_PROGRESS
INFO: StackName: cisco-student-00, Status: DELETE_IN_PROGRESS
INFO: StackName: cisco-student-00, Status: DELETE_IN_PROGRESS
WARN: cisco-student-00 Does Not Exist...
INFO: CloudFormation Rollback Completed Successfully...
```
> Note that the VPC will not be deleted because the rollback script has no way of knowing whether an existing VPC was used or a new one created.  Also note that when the `launch.py` script was run, if you had commented the `vpc_id` line it created a new VPC and populated the new vpc_id into the `parameters.yml` un-commented.  This was done because `rollback.py` needs to know the vpc_id in order to delete other resources.


#### Limitations

Currently deploying this lab environment only supports a single 'deployment set' per region, where 'deployment set' is defined as any numerical value defined in `parameters.yml` under the `student_count` field. It essentially is the number of student pods you are deploying at any one time. You must have 2x EIPs per student allocated to your region, as per the above section labeled "Requirements / Dependencies". Removing the single deployment option per region is an enhancement that we aim to add shortly. 

Currently there is a limitation that prevents any ability to increment student pod count once deployed. Since it would take a bit of an effort to add, it is something we will be looking at however, don't aim to add anytime soon.  
  
---  
  
[Go to Top of Page](README.md)