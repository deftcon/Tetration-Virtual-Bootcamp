# Cisco Tetration Virtual Bootcamp

## Module 03.02  Data Sources - Agents
Tetration agent (also called sensor) installation can be performed manually using a shell script for Linux and a Powershell script (.ps1) for Windows. These scripts can also be leveraged by 3rd party software configuration management systems such as Ansible, Puppet, Microsoft SCCM, etc. to automate deployment across multiple machines. The installation does not require any modification to run unattended, the scripts run without any interaction required from the administrator. It is important that the scripts be downloaded from the Tetration cluster, as they have specific information embedded to connect to the cluster.  When the script is executed, it will pull down the required software from the Tetration cluster based on the Operating System in use. This means that outbound connectivity from each server to the Tetration cluster is a requirement.

In this module, we'll download the installation scripts for Windows and Linux from the Tetration cluster and use Ansible to perform automated rollout of the sensors.

---

This diagram depicts how you will deploy Tetration Agents out to each of your workloads in your lab environment. Deployment will occur by performing the following tasks:
   1. Connect to the Guac server via HTTPS
   2. Click on and connecting to the Ansible machine
   3. Verify and, if necessary, edit the inventory for deployment by first changing directories with `cd /opt/ansible-tetration-sensor/` running `sudo nano inventory/hosts` and when prompted with `[sudo] password for ciscolab:`, entering the standard lab password of `tet123$$!`. 

<a href="images/diagrams_007.png"><img src="images/diagrams_007.png" style="width:100%;height:100%;"></a>  

The Ansible machine is already configured to deploy agents out to the following workloads by OS:

   * Windows 2019
      * nopCommerce IIS server
      * nopCommerce MSSQL server
      * Active Directory server
   * CentOS 7
      * OpenCart Apache server
      * OpenCart MySQL server
      * Ansible Automation server (itself)
   * Ubuntu 16.04
      * EKS Worker Node

---


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/03a_agent_installation_manual.mp4" style="font-weight:bold" title="Collection Rules Title"><img src="https://tetration.guru/bootcamp/diagrams/images/video_icon_mini.png"> Click here to view a video of demonstrating how to install Tetration sensors manually (this is for demo only - these tasks will not be performed in this module).</a>  


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/03b_firewalld_ipsets_iptables.mp4" style="font-weight:bold" title="Collection Rules Title"><img src="https://tetration.guru/bootcamp/diagrams/images/video_icon_mini.png"> Click here to view a video of demonstrating how to disable firewalld and install ipsets and iptables in linux prior to sensor install (this is for demo only - these tasks will not be performed in this module).</a>  


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/03c_agent_installation_w_ansible.mp4" style="font-weight:bold" title="Collection Rules Title"><img src="https://tetration.guru/bootcamp/diagrams/images/video_icon_mini.png"> Click here to view a video of the tasks being performed to install Tetration sensors using Ansible (tasks covered in this module).</a>  


---

### Steps for this Module  
<a href="#step-001" style="font-weight:bold">Step 001 - Navigate to Agent Config</a>  
<a href="#step-002" style="font-weight:bold">Step 002 - Click on Software Agent Download</a>  
<a href="#step-003" style="font-weight:bold">Step 003 - Select the Linux Enforcement Agent</a>  
<a href="#step-004" style="font-weight:bold">Step 004 - Save the Linux shell script</a>  
<a href="#step-005" style="font-weight:bold">Step 005 - Select the Windows Enforcement Agent</a>  
<a href="#step-006" style="font-weight:bold">Step 006 - Save the Windows Powershell script</a>  
<a href="#step-007" style="font-weight:bold">Step 007 - Open a session to the Ansible machine</a>  
<a href="#step-008" style="font-weight:bold">Step 008 - Copy the scripts to the Ansible machine</a>  
<a href="#step-009" style="font-weight:bold">Step 009 - Examine the Ansible inventory</a>  
<a href="#step-010" style="font-weight:bold">Step 010 - Run the Ansible playbook</a>  
<a href="#step-011" style="font-weight:bold">Step 011 - Verify Ansible playbook results</a>  
<a href="#step-012" style="font-weight:bold">Step 012 - Open a session to the IIS web server</a>  
<a href="#step-013" style="font-weight:bold">Step 013 - Locate the Services console</a>  
<a href="#step-014" style="font-weight:bold">Step 014 - Verify the Tetration services are active</a>  
<a href="#step-015" style="font-weight:bold">Step 015 - Open a session to the Apache web server</a>  
<a href="#step-016" style="font-weight:bold">Step 016 - Verify the Tetration services are active</a>  
<a href="#step-017" style="font-weight:bold">Step 017 - Navigate to Software Agents</a>  
<a href="#step-018" style="font-weight:bold">Step 018 - Verify the agents are registered</a>  


<div class="step" id="step-001"><a href="#step-001" style="font-weight:bold">Step 001</a></div>  

Navigate to Agent Config.

<a href="images/module03_001.png"><img src="images/module03_001.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-002"><a href="#step-002" style="font-weight:bold">Step 002</a></div>  

Select the Software Agent Download tab.

<a href="images/module03_002.png"><img src="images/module03_002.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-003"><a href="#step-003" style="font-weight:bold">Step 003</a></div>  

Select the Linux platform,  Enforcement Agent,  and then click Download Installer.

<a href="images/module03_003.png"><img src="images/module03_003.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-004"><a href="#step-004" style="font-weight:bold">Step 004</a></div>  

Save the file to the desktop and rename it to `tet-linux.sh`.  

<a href="images/module03_004.png"><img src="images/module03_004.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-005"><a href="#step-005" style="font-weight:bold">Step 005</a></div>  

Select the Windows platform, Enforcement Agent,  and then Download Installer.

<a href="images/module03_005.png"><img src="images/module03_005.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-006"><a href="#step-006" style="font-weight:bold">Step 006</a></div>  

Name the file `tet-win.ps1` and save the file to the desktop.

<a href="images/module03_006.png"><img src="images/module03_006.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-007"><a href="#step-007" style="font-weight:bold">Step 007</a></div>  

Log into the Apache Guacamole server and open a session to the Ansible machine.

<a href="images/module03_007.png"><img src="images/module03_007.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-008"><a href="#step-008" style="font-weight:bold">Step 008</a></div>  

Copy the scripts from the desktop to the Ansible machine by clicking and dragging them from the desktop to the Ansible console window.  A file copy dialogue should be displayed in the lower right-hand corner.   Once complete,  do an `ls` to list the directory on the Ansible machine and make sure the files are present.

<a href="images/module03_008.png"><img src="images/module03_008.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-009"><a href="#step-009" style="font-weight:bold">Step 009</a></div>  

Switch to the directory containing the Ansible playbooks with the command `cd /opt/ansible-tetration-sensor/` and then `cd inventory` to switch to the Inventory directory.  Type the command `cat hosts` and examine the contents in the inventory file. The Linux and Windows machine IP addresses as listed in your student spreadsheet should already be populated in the [centos] section for Linux and the [win] section for Windows.

<a href="images/module03_009.png"><img src="images/module03_009.png" style="width:100%;height:100%;"></a>  


<div class="step" id="step-010"><a href="#step-010" style="font-weight:bold">Step 010</a></div>  

Type `cd ..` to exit the Inventory directory and run the following command to execute the Ansible playbook:

`ansible-playbook playbooks/clean-install-with-script.yml`


<a href="images/module03_010.png"><img src="images/module03_010.png" style="width:100%;height:100%;"></a>  

<div class="step" id="step-011"><a href="#step-011" style="font-weight:bold">Step 011</a></div>  

The Ansible playbook will take a few minutes to complete.  When finished, you should see a PLAY RECAP section indicating the success or failure of installation on each machine.  

> Ignore the failure of host 10.1.0.162 in the image below, the machine was undergoing maintenance when the installation was performed.

<a href="images/module03_011.png"><img src="images/module03_011.png" style="width:100%;height:100%;"></a>  

> The playbook may display an error such as the one below for the Windows machines. Ignore the error,  the installation actually completed successfully but the connection from the Ansible machine was disrupted briefly by the sensor installation.  We are currently investigating workarounds to avoid the error in the future.    

<a href="images/module03_010.png"><img src="images/module03_011b.jpg" style="width:100%;height:100%;"></a>

<div class="step" id="step-012"><a href="#step-012" style="font-weight:bold">Step 012</a></div>  

Open a session to the IIS Web Server.

<a href="images/module03_012.png"><img src="images/module03_012.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-013"><a href="#step-013" style="font-weight:bold">Step 013</a></div>  

Click on the Search button and enter "services",  and then open up Services Control Panel.

<a href="images/module03_013.png"><img src="images/module03_013.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-014"><a href="#step-014" style="font-weight:bold">Step 014</a></div>  

Scroll down and locate the WindowsAgentEngine and WindowsTetEngine services and ensure they are in Running state.

<a href="images/module03_014.png"><img src="images/module03_014.png" style="width:100%;height:100%;"></a>  


### REPEAT STEPS 012-14 FOR THE MS-SQL DB SERVER AND MICROSOFT ACTIVE DIRECTORY SERVER

<div class="step" id="step-015"><a href="#step-015" style="font-weight:bold">Step 015</a></div>  

Open a session to the Apache Web Server.

<a href="images/module03_015.png"><img src="images/module03_015.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-016"><a href="#step-016" style="font-weight:bold">Step 016</a></div>  

Run the command `ps -ef | grep tet` and ensure that the tet-engine, and ensure that the tet-engine, tet-enforcer, and tet-sensor services are displayed.

<a href="images/module03_016.png"><img src="images/module03_016.png" style="width:100%;height:100%;"></a>  

### REPEAT STEPS 15-16 FOR THE MYSQL DB SERVER

<div class="step" id="step-017"><a href="#step-017" style="font-weight:bold">Step 017</a></div>  

Navigate to Agent Config. 

<a href="images/module03_017.png"><img src="images/module03_017.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-018"><a href="#step-018" style="font-weight:bold">Step 018</a></div>  

Click on the Software Agents tab,  and ensure that all of the sensors that were installed are displayed.  

<a href="images/module03_018.png"><img src="images/module03_018.png" style="width:100%;height:100%;"></a>  

YOU HAVE FINISHED THIS MODULE



| [Return to Table of Contents](https://tetration.guru/bootcamp/) | [Go to Top of the Page](readme.md) | [Continue to the Next Module]() |
