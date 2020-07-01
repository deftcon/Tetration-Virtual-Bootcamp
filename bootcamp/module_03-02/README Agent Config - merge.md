# Cisco Tetration - Hands-On Lab

## Module04 - Agent Config Intent
Agent Config Intent defines what features will be enabled for a group of sensors.  The Config Intent can be tied to an Inventory Filter, which provides the capability to apply different configurations to different types of hosts.  For example, you could define a profile enabling a specific set of features to all Windows machines,  and a separate profile enabling a different set of features to all Linux machines.  We will see an example of doing just that in the exercise below.  

---
<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/04_agent_config.mp4" style="font-weight:bold" title="Agent Config Intent"><img src="https://tetration.guru/bootcamp/diagrams/images/video_icon_mini.png"> Click here to view a video of the tasks necessary to configure Tetration Agents for Windows and Linux machines.</a>

---

### Steps for this Module  
<a href="#step-001" style="font-weight:bold">Step 001 - Navigate to Agent Config</a>  
<a href="#step-002" style="font-weight:bold">Step 002 - Create a Profile for Windows machines</a>  
<a href="#step-003" style="font-weight:bold">Step 003 - Configure Windows Profile Settings</a>  
<a href="#step-004" style="font-weight:bold">Step 004 - Configure Windows Profile Settings</a>  
<a href="#step-005" style="font-weight:bold">Step 005 - Create a Profile for Linux machines</a>  
<a href="#step-006" style="font-weight:bold">Step 006 - Configure Linux Profile Settings</a>  
<a href="#step-007" style="font-weight:bold">Step 007 - Configure Linux Profile Settings</a>  
<a href="#step-008" style="font-weight:bold">Step 008 - Create a Config Intent for Windows</a>  
<a href="#step-009" style="font-weight:bold">Step 009 - Create a new Inventory Filter</a>  
<a href="#step-010" style="font-weight:bold">Step 010 - Configure Inventory Filter for Windows OS</a>  
<a href="#step-011" style="font-weight:bold">Step 011 - Apply the Inventory Filter to the Config Intent</a>  
<a href="#step-012" style="font-weight:bold">Step 012 - Create a Config Intent for Linux</a>  
<a href="#step-013" style="font-weight:bold">Step 013 - Create a new Inventory Filter</a>  
<a href="#step-014" style="font-weight:bold">Step 014 - Configure Inventory Filter for Linux OS</a>  
<a href="#step-015" style="font-weight:bold">Step 015 - Apply the Inventory Filter to the Config Intent</a>  

---
<div class="step" id="step-001"><a href="#step-001" style="font-weight:bold">Step 001</a></div>

Select the Gear icon and select Agent Config.  

<a href="images/module04_001.png"><img src="images/module04_001.png" style="width:100%;height:100%;"></a>  


<div class="step" id="step-002"><a href="#step-002" style="font-weight:bold">Step 002</a></div>  

Click Create Profile to being creating an Agent Config Profile that we will apply to Windows machines.

<a href="images/module04_002.png"><img src="images/module04_002.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-003"><a href="#step-003" style="font-weight:bold">Step 003</a></div>  

Enter the name Windows for the profile name,  and select to enable Enforcement and Preserve rules.  

> Enforcement - This agent config intent setting provides the capability to enable/disable the enforcement feature.  This can be useful to prevent a situation where you have a set of machines that you would like to ensure cannot be put into enforcement inadvertently.

> Preserve Rules - When enabled,  this setting will preserve any manually configured firewall rules that might be present on the servers when going into enforcement.  It is common to set this to enabled, such as to preserve any rules that might have been previously configured.

<a href="images/module04_003.png"><img src="images/module04_003.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-004"><a href="#step-004" style="font-weight:bold">Step 004</a></div>  

Click to enable the following settings and then Save the configuration:
- PID Lookup
- Forensics
- Meltdown Exploit Detection
- Anamalous Cache Activity Detection

> NOTE: The Auto-Upgrade setting will cause the agents to be upgraded automatically when Tetration code is updated.  It is common to disable this feature in a production environment so that agents can be upgraded in a more controlled manner.

<a href="images/module04_004.png"><img src="images/module04_004.png" style="width:100%;height:100%;"></a>  


<div class="step" id="step-005"><a href="#step-005" style="font-weight:bold">Step 005</a></div>  

Select Create Profile to create a new Agent Config Profile for Linux machines.

<a href="images/module04_005.png"><img src="images/module04_005.png" style="width:100%;height:100%;"></a>  


<div class="step" id="step-006"><a href="#step-006" style="font-weight:bold">Step 006</a></div>  

Enter the profile name Linux,  and enable Enforcement and Preserve Rules features.

<a href="images/module04_006.png"><img src="images/module04_006.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-007"><a href="#step-007" style="font-weight:bold">Step 007</a></div>  

Scroll down and Save the configuration.  

<a href="images/module04_007.png"><img src="images/module04_007.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-008"><a href="#step-008" style="font-weight:bold">Step 008</a></div>  

Click Create Intent to begin creating the Windows Agent Config Intent.  

<a href="images/module04_008.png"><img src="images/module04_008.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-009"><a href="#step-009" style="font-weight:bold">Step 009</a></div>  

Select to apply the profile that we just created called Windows,  and select to create a new filter.  This will create a new Inventory Filter that we will configure to match on the Windows Operating System.

<a href="images/module04_009.png"><img src="images/module04_009.png" style="width:100%;height:100%;"></a>  


<div class="step" id="step-010"><a href="#step-010" style="font-weight:bold">Step 010</a></div>  

Enter Windows for the name,  and enter the query "OS contains MS".  Then save the new filter.  This will match any machines with sensors installed that have "MS" in their Operating System name.  Also notice that the filter already matches inventory items (your number of matched items may differ from the image).  

<a href="images/module04_010.png"><img src="images/module04_010.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-011"><a href="#step-011" style="font-weight:bold">Step 011</a></div>  

Make sure the "to filter" field is set to the Windows inventory filter we just created,  and select Save.  We have now applied the new Config Intent.  Any Windows machines matching the inventory filter we created will now have the configuration applied.  

<a href="images/module04_011.png"><img src="images/module04_011.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-012"><a href="#step-012" style="font-weight:bold">Step 012</a></div>  

Create a new Config Intent for Linux machines.

<a href="images/module04_012.png"><img src="images/module04_012.png" style="width:100%;height:100%;"></a>  


<div class="step" id="step-013"><a href="#step-013" style="font-weight:bold">Step 013</a></div>  

Select to apply the Linux profile that we previously created,  and select Create new filter.

<a href="images/module04_013.png"><img src="images/module04_013.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-014"><a href="#step-014" style="font-weight:bold">Step 014</a></div>  

Enter the name Linux and the query "OS contains CentOS".  This will match any machines with sensors installed that are running the CentOS Operating System.  Later we will see how we can add additional OS flavors to this Config Intent.

<a href="images/module04_014.png"><img src="images/module04_014.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-015"><a href="#step-015" style="font-weight:bold">Step 015</a></div>  

Ensure that the Inventory Filter we just created called Linux is selected as the "to filter" and Save to apply the Config Intent.  

<a href="images/module04_015.png"><img src="images/module04_015.png" style="width:100%;height:100%;"></a>  





| [Return to Table of Contents](https://tetration.guru/bootcamp/) | [Go to Top of the Page]() | [Continue to the Next Module]() |
