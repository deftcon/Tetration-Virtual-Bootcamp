# Cisco Tetration Virtual Bootcamp

## Module 07.00  Segmentation - Inventory Filters

Inventory Filters provide a way to describe a group of endpoints as an object for easy  identification when used within policy and other areas of the system. For example, earlier in the lab when creating Agent Config Intents we created Inventory Filters that matched all Windows and Linux machines by matching on the Operating System.  This was done by creating a query that matched on the Operating System reported by the agent.  Inventory Filter queries can match on annotations, tags being received from the various External Orchestrators, inventory characteristics such as Operating System,  or security characteristics such as CVE score. This allows the administrator great flexibility when building policy.  

In this module we will create Inventory Filters that will be used in later modules to build our policies.   


## --- Lecture Video ---  
---  
<a href="https://deftcon-tetration-virtual-bootcamp.s3.us-east-2.amazonaws.com/lectures/Module_07.00__Lecture__Segmentation__Inventory_Filters.mp4" style="font-weight:bold"><img src="https://tetration.guru/bootcamp/diagrams/images/video_icon_small.png">Segmentation - Inventory Filters :: Lecture Video :: Runtime: 9 mins</a>  
  
---  
  

## --- Demo Video ---  
---  
<a href="https://deftcon-tetration-virtual-bootcamp.s3.us-east-2.amazonaws.com/demos/Module_07.00__Demo__Segmentation__Inventory_Filters.mp4" style="font-weight:bold"><img src="https://tetration.guru/bootcamp/diagrams/images/video_icon_small.png">Segmentation - Inventory Filters :: Demo Video :: Runtime: 2 mins</a>  
  
---  

## --- Lab ---
### Steps for this Lab  
<a href="#step-001" style="font-weight:bold">Step 001 - Navigate to Inventory Filters</a>  
<a href="#step-002" style="font-weight:bold">Step 002 - Create a new Inventory Filter</a>  
<a href="#step-003" style="font-weight:bold">Step 003 - Create Inventory Filter for Any</a>  
<a href="#step-004" style="font-weight:bold">Step 004 - View query results</a>  
<a href="#step-005" style="font-weight:bold">Step 005 - Create a new Inventory Filter</a>  
<a href="#step-006" style="font-weight:bold">Step 006 - Create Inventory Filter for Any-Internal</a>  
<a href="#step-007" style="font-weight:bold">Step 007 - View query results</a>  
<a href="#step-008" style="font-weight:bold">Step 008 - Create a new Inventory Filter</a>  
<a href="#step-009" style="font-weight:bold">Step 009 - Create Inventory Filter for Guacamole server</a>  
<a href="#step-010" style="font-weight:bold">Step 010 - View query results</a>  

---

<div class="step" id="step-001"><a href="#step-001" style="font-weight:bold">Step 001</a></div>  

Navigate to Inventory Filters.

<a href="images/module_07_001.png"><img src="images/module_07_001.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-002"><a href="#step-002" style="font-weight:bold">Step 002</a></div>  

Click on Create Filter.

<a href="images/module_07_002.png"><img src="images/module_07_002.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-003"><a href="#step-003" style="font-weight:bold">Step 003</a></div>  

Create the filter named Any with the query Address = 0.0.0.0/0.  This will match any IPv4 address.

<a href="images/module_07_003.png"><img src="images/module_07_003.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-004"><a href="#step-004" style="font-weight:bold">Step 004</a></div>  

Examine the query results.  The query will return all of the IP addresses that have been learned by Tetration and stored in inventory.

> The number of inventory items shown in the image may differ.  This is because endpoints in inventory are learned based on traffic that is reported into the cluster by the agents.

<a href="images/module_07_004.png"><img src="images/module_07_004.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-005"><a href="#step-005" style="font-weight:bold">Step 005</a></div>  

Click Create Filter to create the next Inventory Filter.  

<a href="images/module_07_005.png"><img src="images/module_07_005.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-006"><a href="#step-006" style="font-weight:bold">Step 006</a></div>  

Create a filter named Any-Internal with the query *PodSubnet = internal.  This will match the static annotation entries that we uploaded previously which describe the internal IP address space of the lab.  In this case it is all RFC1918 private IP address space - 10.0.0.0/8,  172.16.0.0/12, and 192.168.0.0/16.

<a href="images/module_07_006.png"><img src="images/module_07_006.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-007"><a href="#step-007" style="font-weight:bold">Step 007</a></div>  

Observe the query results and then create the filter.

<a href="images/module_07_007.png"><img src="images/module_07_007.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-008"><a href="#step-008" style="font-weight:bold">Step 008</a></div>  

Click Create Filter to create another Inventory Filter.

<a href="images/module_07_008.png"><img src="images/module_07_008.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-009"><a href="#step-009" style="font-weight:bold">Step 009</a></div>  

Create the filter named Guacamole with query * orchestrator_Name contains guac.  This will match an AWS tag placed on the Apache Guacamole instance.   

> Apache Guacamole is the dashboard that you will be connecting to in order to gain access to the consoles of the servers. We will later use the Inventory Filter created here in our policy definition to ensure that the Guacamole server can access the rest of the workloads using SSH and RDP. It provides an easy way to refer to the server without having to remember its IP address or hostname.  We could also add additional Guacamole servers with the AWS tag,  and they would automatically be grouped into this filter and automatically inherit any rules that are using the Inventory Filter.

<a href="images/module_07_009.png"><img src="images/module_07_009.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-010"><a href="#step-010" style="font-weight:bold">Step 010</a></div>  

The query matches only the internal IP of the Guacamole server.  Click Create.  

> The Guacamole server has both an external public IP which is indicated in your lab information under "Web Console URL", and an internal IP which is the one shown here.  

<a href="images/module_07_010.png"><img src="images/module_07_010.png" style="width:100%;height:100%;"></a>  


---  

## SubModules for Module 07
[Module 07.01: Segmentation - ADM, Policy Analysis, and Enforcement](../module_07-01/)  
[Module 07.02: Segmentation - ADM - Common Services](../module_07-02/)  
[Module 07.03: Segmentation - ADM - Windows App](../module_07-03/)  
[Module 07.04: Segmentation - ADM - Linux App](../module_07-04/)  
[Module 07.05: Segmentation - User-Based Policy](../module_07-05/)  
[Module 07.06: Segmentation - Policy Analysis - Global Services](../module_07-06/)  
[Module 07.07: Segmentation - Policy Analysis - Common Services](../module_07-07/)  
[Module 07.08: Segmentation - Policy Analysis - Windows App](../module_07-08/)  
[Module 07.09: Segmentation - Policy Analysis - Linux App](../module_07-09/)  
[Module 07.10: Segmentation - Enforcement - Pre Enforcement Checks](../module_07-10/)  
[Module 07.11: Segmentation - Enforcement - Global and Common](../module_07-11/)  
[Module 07.12: Segmentation - Enforcement - Windows App](../module_07-12/)  
[Module 07.13: Segmentation - Enforcement - Linux App](../module_07-13/)  
[Module 07.14: Segmentation - Enforcement - Containers](../module_07-14/)  
  
---  
  


| [Return to Table of Contents](https://tetration.guru/bootcamp/) | [Go to Top of the Page](README.md) | [Continue to the Next Module](../module_07-01/) |