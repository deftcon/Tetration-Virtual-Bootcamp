# Cisco Tetration - Hands-On Lab

## Module25: Container Policies and Enforcement


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/25a_container_policies_and_enforcement.mp4" style="font-weight:bold" title="Container Policy Definition"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> Click here to view a video of tasks performed to define policies for a multi-tier microservices appplication.</a>

<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/25b_container_policies_and_enforcement.mp4" style="font-weight:bold" title="Container Policy Enforcement"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> Click here to view a video of tasks performed to analyze and enforce the policy for a multi-tier microservices appplication.</a>


### Steps for this Module  
<a href="#step-001" style="font-weight:bold">Step 001 - Navigate to Agent Config</a>  
<a href="#step-002" style="font-weight:bold">Step 002 - Click to select the Linux Inventory Filter</a>  
<a href="#step-003" style="font-weight:bold">Step 003 - Edit the Inventory Filter</a>  
<a href="#step-004" style="font-weight:bold">Step 004 - Modify the Query to include Ubuntu</a>  
<a href="#step-005" style="font-weight:bold">Step 005 - Navigate to Inventory Filters</a>  
<a href="#step-006" style="font-weight:bold">Step 006 - Create a new Inventory Filter</a>  
<a href="#step-007" style="font-weight:bold">Step 007 - Create a filter for the Worker Nodes</a>  
<a href="#step-008" style="font-weight:bold">Step 008 - Create the filter for Worker Nodes</a>  
<a href="#step-009" style="font-weight:bold">Step 009 - Edit the EKS WorkerNodes filter</a>  
<a href="#step-010" style="font-weight:bold">Step 010 - Change the Scope to SockShop</a>  
<a href="#step-011" style="font-weight:bold">Step 011 - Create another Inventory Filter</a>  
<a href="#step-012" style="font-weight:bold">Step 012 - Enter the address of the EKS master</a>  
<a href="#step-013" style="font-weight:bold">Step 013 - Create the Inventory Filter</a>  
<a href="#step-014" style="font-weight:bold">Step 014 - Create a new application workspace</a>  
<a href="#step-015" style="font-weight:bold">Step 015 - Create the Sock Shop workspace</a>  
<a href="#step-016" style="font-weight:bold">Step 016 - Create Cluster</a>  
<a href="#step-017" style="font-weight:bold">Step 017 - Edit the Cluster details</a>  
<a href="#step-018" style="font-weight:bold">Step 018 - Create the first cluster</a>  
<a href="#step-019" style="font-weight:bold">Step 019 - Create the additional clusters</a>  
<a href="#step-020" style="font-weight:bold">Step 020 - Add a manual policy</a>  
<a href="#step-021" style="font-weight:bold">Step 021 - Add all policies</a>  
<a href="#step-022" style="font-weight:bold">Step 022 - Test access to the Sock Shop application</a>  
<a href="#step-023" style="font-weight:bold">Step 023 - Navigate to Inventory Search</a>  
<a href="#step-024" style="font-weight:bold">Step 024 - Filter for OS contains Ubuntu</a>  
<a href="#step-025" style="font-weight:bold">Step 025 - Examine Container Policies</a>  
<a href="#step-026" style="font-weight:bold">Step 026 - Navigate to the Sock Shop application</a>  
<a href="#step-027" style="font-weight:bold">Step 027 - Click on Policy Analysis </a>  
<a href="#step-028" style="font-weight:bold">Step 028 - Start Policy Analysis </a>  
<a href="#step-029" style="font-weight:bold">Step 029 - Analyze policies</a>  
<a href="#step-030" style="font-weight:bold">Step 030 - Move the application into enforcement</a>  
<a href="#step-031" style="font-weight:bold">Step 031 - Enforce the latest policy</a>  
<a href="#step-032" style="font-weight:bold">Step 032 - Navigate to Inventory Search</a>  
<a href="#step-033" style="font-weight:bold">Step 033 - Click the link to the EKS worker node</a>  
<a href="#step-034" style="font-weight:bold">Step 034 - Examine the message regarding policies</a>  
<a href="#step-035" style="font-weight:bold">Step 035 - Review Container Policies</a>  
<a href="#step-036" style="font-weight:bold">Step 036 - Filter Container Policies</a>  
<a href="#step-037" style="font-weight:bold">Step 037 - Filter Container Policies</a>  
<a href="#step-038" style="font-weight:bold">Step 038 - Test the application</a>  


<div class="step" id="step-001"><a href="#step-001" style="font-weight:bold">Step 001</a></div>  

Rules will be implemented on the EKS worker node that is running Ubuntu.  Previously when we set up the Linux Inventory Filter,  we set it up to match on the CentOS operating system.   We must now modify the filter to include the Ubuntu operating system.  

Navigate to Agent Config.  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_001.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_001.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-002"><a href="#step-002" style="font-weight:bold">Step 002</a></div>  

Click on the Linux Inventory Filter.

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_002.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_002.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-003"><a href="#step-003" style="font-weight:bold">Step 003</a></div>  

Edit the Inventory Filter.

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_003.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_003.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-004"><a href="#step-004" style="font-weight:bold">Step 004</a></div>  

Edit the query by adding the criteria `or OS contains Ubuntu`.

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_004.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_004.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-005"><a href="#step-005" style="font-weight:bold">Step 005</a></div>  

Navigate to Inventory Filters.

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_005.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_005.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-006"><a href="#step-006" style="font-weight:bold">Step 006</a></div>  

Create a new Inventory Filter.

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_006.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_006.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-007"><a href="#step-007" style="font-weight:bold">Step 007</a></div>  

Name the filter `EKS WorkerNodes` and enter the query:

`* orchestrator_aws:autoscaling:groupName contains cisco-hol-eks-worker-us-east-1-NodeGroup`

> Substitute the AWS region you are using above for us-east-1

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_007.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_007.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-008"><a href="#step-008" style="font-weight:bold">Step 008</a></div>  

Click Create.  


<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_008.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_008.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-009"><a href="#step-009" style="font-weight:bold">Step 009</a></div>  

Edit the Inventory Filter we just created.

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_009.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_009.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-010"><a href="#step-010" style="font-weight:bold">Step 010</a></div>  

Change the Scope to the SockShop scope.  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_010.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_010.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-011"><a href="#step-011" style="font-weight:bold">Step 011</a></div>  

Create another Inventory Filter.

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_011.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_011.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-012"><a href="#step-012" style="font-weight:bold">Step 012</a></div>  

Use the name EKS Master,  and in the query field enter `Address = {eks_master_ip}` where eks_master_ip is the IP address of the Kubernetes master node which is provided in your student workbook.  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_012.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_012.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-013"><a href="#step-013" style="font-weight:bold">Step 013</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_013.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_013.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-014"><a href="#step-014" style="font-weight:bold">Step 014</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_014.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_014.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-015"><a href="#step-015" style="font-weight:bold">Step 015</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_015.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_015.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-016"><a href="#step-016" style="font-weight:bold">Step 016</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_016.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_016.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-017"><a href="#step-017" style="font-weight:bold">Step 017</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_017.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_017.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-018"><a href="#step-018" style="font-weight:bold">Step 018</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_018.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_018.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-019"><a href="#step-019" style="font-weight:bold">Step 019</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_019.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_019.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-020"><a href="#step-020" style="font-weight:bold">Step 020</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_020.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_020.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-021"><a href="#step-021" style="font-weight:bold">Step 021</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_021.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_021.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-022"><a href="#step-022" style="font-weight:bold">Step 022</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_022.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_022.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-023"><a href="#step-023" style="font-weight:bold">Step 023</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_023.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_023.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-024"><a href="#step-024" style="font-weight:bold">Step 024</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_024.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_024.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-025"><a href="#step-025" style="font-weight:bold">Step 025</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_025.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_025.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-026"><a href="#step-026" style="font-weight:bold">Step 026</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_026.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_026.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-027"><a href="#step-027" style="font-weight:bold">Step 027</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_027.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_027.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-028"><a href="#step-028" style="font-weight:bold">Step 028</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_028.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_028.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-029"><a href="#step-029" style="font-weight:bold">Step 029</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_029.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_029.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-030"><a href="#step-030" style="font-weight:bold">Step 030</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_030.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_030.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-031"><a href="#step-031" style="font-weight:bold">Step 031</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_031.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_031.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-032"><a href="#step-032" style="font-weight:bold">Step 032</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_032.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_032.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-033"><a href="#step-033" style="font-weight:bold">Step 033</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_033.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_033.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-034"><a href="#step-034" style="font-weight:bold">Step 034</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_034.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_034.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-035"><a href="#step-035" style="font-weight:bold">Step 035</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_035.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_035.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-036"><a href="#step-036" style="font-weight:bold">Step 036</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_036.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_036.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-037"><a href="#step-037" style="font-weight:bold">Step 037</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_037.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_037.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-038"><a href="#step-038" style="font-weight:bold">Step 038</a></div>  

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_038.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/images/module25_038.png" style="width:100%;height:100%;"></a>  





| [Return to Table of Contents](https://onstakinc.github.io/cisco-tetration-hol/labguide/) | [Go to Top of the Page](https://onstakinc.github.io/cisco-tetration-hol/labguide/module25/) | [Continue to the Next Module](https://onstakinc.github.io/cisco-tetration-hol/labguide/module26/) |
