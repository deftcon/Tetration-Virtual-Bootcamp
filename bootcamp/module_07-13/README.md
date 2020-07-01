# Cisco Tetration - Hands-On Lab

## Module 07.13  Segmentation - Enforcement - Linux App

In this module we will enable enforcement for the OpenCart application.  We will review the deployed policies both before and after enabling enforcement to compare the results,  and then once in enforcement test access to the application.  We will also test the user-based policy as defined in <a href="">Module 16</a> 

---
<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/24_policy_enforcement_opencart.mp4" style="font-weight:bold" title="Enforcement - OpenCart"><img src="https://tetration.guru/bootcamp/diagrams/images/video_icon_mini.png"> Click here to view a video showing the necessary tasks to be performed to take the Linux-based OpenCart into full enforcement mode with micro-segmentation.</a>

---

### Steps for this Module  
<a href="#step-001" style="font-weight:bold">Step 001 - Navigate to Inventory Search</a>  
<a href="#step-002" style="font-weight:bold">Step 002 - Search for the Apache Linux machine</a>  
<a href="#step-003" style="font-weight:bold">Step 003 - View the policies on the Apache Linux machine</a>  
<a href="#step-004" style="font-weight:bold">Step 004 - View current number of policies present</a>  
<a href="#step-005" style="font-weight:bold">Step 005 - Switch to OpenCart application workspace</a>  
<a href="#step-006" style="font-weight:bold">Step 006 - Begin Enforcement</a>  
<a href="#step-007" style="font-weight:bold">Step 007 - Enforce the latest published policies</a>  
<a href="#step-008" style="font-weight:bold">Step 008 - Navigate to Inventory Search</a>  
<a href="#step-009" style="font-weight:bold">Step 009 - Click on the Apache Linux server</a>  
<a href="#step-010" style="font-weight:bold">Step 010 - View current Policies</a>  
<a href="#step-011" style="font-weight:bold">Step 011 - Observe the increased policy rules</a>  
<a href="#step-012" style="font-weight:bold">Step 012 - Open a session to the Employee Ubuntu desktop</a>  
<a href="#step-013" style="font-weight:bold">Step 013 - Open a session to the SysAdmin Ubuntu desktop</a>  
<a href="#step-014" style="font-weight:bold">Step 014 - Open a browser session to the external IP </a>  
<a href="#step-015" style="font-weight:bold">Step 015 - Connect to the Apache Linux machine from the Employee desktop</a>  
<a href="#step-016" style="font-weight:bold">Step 016 - Attempt to SSH to the Apache Linux machine from the Employee desktop</a>  
<a href="#step-017" style="font-weight:bold">Step 017 - Connect to the Apache Linux machine from the SysAdmin desktop</a>  
<a href="#step-018" style="font-weight:bold">Step 018 - Attempt to SSH to the Apache Linux machine from the SysAdmin desktop</a>  
<a href="#step-019" style="font-weight:bold">Step 019 - Attempt to SSH to the MySQL machine from the Employee desktop</a>  
<a href="#step-020" style="font-weight:bold">Step 020 - Open a session to the Kali Linux machine</a>  
<a href="#step-021" style="font-weight:bold">Step 021 - Attempt to connect to the Apache Linux machine on TCP 8080</a>  
<a href="#step-022" style="font-weight:bold">Step 022 - Connect to TCP 8080 on the Apache Linux machine from the Employee desktop</a>  
<a href="#step-023" style="font-weight:bold">Step 023 - View the curl output from the previous task</a>  
<a href="#step-024" style="font-weight:bold">Step 024 - Open a session to the nopCommerce IIS server</a>  
<a href="#step-025" style="font-weight:bold">Step 025 - Attempt a web session to the Apache Linux server</a>  
<a href="#step-026" style="font-weight:bold">Step 026 - Open a session to the Apache Linux server</a>  
<a href="#step-027" style="font-weight:bold">Step 027 - Attempt a web session to the IIS web server</a>  

---

<div class="step" id="step-001"><a href="#step-001" style="font-weight:bold">Step 001</a></div>  

Navigate to Inventory Search.

<a href="images/module24_001.png"><img src="images/module24_001.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-002"><a href="#step-002" style="font-weight:bold">Step 002</a></div>  

Filter for the IP address of the Apache web server.  Then click on the IP address under the Address column.

<a href="images/module24_002.png"><img src="images/module24_002.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-003"><a href="#step-003" style="font-weight:bold">Step 003 </a></div>  

On the Workload Profile,  click on Policies.

<a href="images/module24_003.png"><img src="images/module24_003.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-004"><a href="#step-004" style="font-weight:bold">Step 004</a></div>  

Notice that there are currently 22 policies present.  We will see this increase when we enable enforcement on the OpenCart application workspace.

<a href="images/module24_004.png"><img src="images/module24_004.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-005"><a href="#step-005" style="font-weight:bold">Step 005</a></div>  

Navigate to Applications and select the OpenCart application workspace.

<a href="images/module24_005.png"><img src="images/module24_005.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-006"><a href="#step-006" style="font-weight:bold">Step 006</a></div>  

Click on the Enforcement tab,  and select Enforce Policies.

<a href="images/module24_006.png"><img src="images/module24_006.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-007"><a href="#step-007" style="font-weight:bold">Step 007</a></div>  

Select the latest version of policy, and then click Accept and Enforce.  Optionally,  a reason can be entered which will show up in the application event log.

<a href="images/module24_007.png"><img src="images/module24_007.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-008"><a href="#step-008" style="font-weight:bold">Step 008</a></div>  

Navigate to Inventory Search.  

<a href="images/module24_008.png"><img src="images/module24_008.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-009"><a href="#step-009" style="font-weight:bold">Step 009</a></div>  

Search for the IP address of the Apache web server and then click on the IP address.

<a href="images/module24_009.png"><img src="images/module24_009.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-010"><a href="#step-010" style="font-weight:bold">Step 010</a></div>  

Click on Policies.

<a href="images/module24_010.png"><img src="images/module24_010.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-011"><a href="#step-011" style="font-weight:bold">Step 011</a></div>  

Check the number of policies. This number should increase from what we observed previously. It may take a minute for the increased number of policies to be displayed.  

<a href="images/module24_011.png"><img src="images/module24_011.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-012"><a href="#step-012" style="font-weight:bold">Step 012</a></div>  

Open a session to the Employee desktop.

<a href="images/module24_012.png"><img src="images/module24_012.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-013"><a href="#step-013" style="font-weight:bold">Step 013</a></div>  

In a new tab, also open a session to the SysAdmin desktop.  

<a href="images/module24_013.png"><img src="images/module24_013.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-014"><a href="#step-014" style="font-weight:bold">Step 014</a></div>  

In another tab, test connectivity to the Apace web server public IP address.  

<a href="images/module24_014.png"><img src="images/module24_014.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-015"><a href="#step-015" style="font-weight:bold">Step 015</a></div>  

From the Employee desktop,  open the Terminal application and use the curl command to attempt an HTTP connection to the IIS web server.  The Terminal application can be opened by clicking the black icon on the menu at the bottom middle of the screen.  The command should return output indicating "The document has moved", which indicates that the traffic is getting there on TCP port 80.  This is attempting a redirect to SSL.  To make the connection with ssl,  type `curl -k https://<APACHE_WEB_SERVER_IP>`.  This should return a text representation of the web site.  

<a href="images/module24_015.png"><img src="images/module24_015.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-016"><a href="#step-016" style="font-weight:bold">Step 016</a></div>  

Attempt an SSH connection to the Apache web server from the Employee desktop.  This connection should time out,  as SSH is not permitted from Employees to the Apache web server.  

<a href="images/module24_016.png"><img src="images/module24_016.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-017"><a href="#step-017" style="font-weight:bold">Step 017</a></div>  

From the SysAdmin desktop,  open the Terminal application and attempt an HTTP connection to the Apache web server using the curl command as shown in the image.  Output should be returned indicating "The document has moved".  Attempt a connection using SSL with the command `curl -k https://<APACHE_WEB_SERVER_IP`.  The text-based web site should be returned.  

<a href="images/module24_017.png"><img src="images/module24_017.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-018"><a href="#step-018" style="font-weight:bold">Step 018</a></div>  

From the SysAdmin desktop,  attempt to SSH to the Apache web server and the MySQL server.  The connections should both be successful.  

<a href="images/module24_018.png"><img src="images/module24_018.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-019"><a href="#step-019" style="font-weight:bold">Step 019</a></div>  

Return to the Employee desktop and attempt SSH connections to both the Apache web server and the MySQL servers. Both of these connections should time out because we have not configured rules to allow Employees to SSH to the servers.

<a href="images/module24_019.png"><img src="images/module24_019.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-020"><a href="#step-020" style="font-weight:bold">Step 020</a></div>  

Open a session to the Kali Linux server.  

<a href="images/module24_020.png"><img src="images/module24_020.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-021"><a href="#step-021" style="font-weight:bold">Step 021</a></div>  

Attempt a HTTP session to the Apache web server using the curl command as shown in the image.  Output should be returned for the connection on TCP port 80.   Now attempt a connection on TCP port 8080 using the curl command shown in the image.  This connection should time out, as we have blocked external access to the application on TCP port 8080.    

<a href="images/module24_021.png"><img src="images/module24_021.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-022"><a href="#step-022" style="font-weight:bold">Step 022</a></div>  
Return to the Employee desktop,  and attempt a curl command to the Apache web server on port 8080 as shown in the image.  This connection should be successful because we have created a rule to explicitly allow employees to connect to the server on port 8080.


<a href="images/module24_022.png"><img src="images/module24_022.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-023"><a href="#step-023" style="font-weight:bold">Step 023</a></div>  

The below image shows the output from the previous curl command.

<a href="images/module24_023.png"><img src="images/module24_023.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-024"><a href="#step-024" style="font-weight:bold">Step 024</a></div>  

Open a connection to the IIS web server.  

<a href="images/module24_024.png"><img src="images/module24_024.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-025"><a href="#step-025" style="font-weight:bold">Step 025</a></div>  

Attempt to connect to the Apache web server in a web browser.  The connection should be blocked as we have not created any rules to allow the IIS web server to talk to the Apache web server, nor would we want to allow the communication.

<a href="images/module24_025.png"><img src="images/module24_025.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-026"><a href="#step-026" style="font-weight:bold">Step 026</a></div>  

Open a session to the Apache web server.  

<a href="images/module24_026.png"><img src="images/module24_026.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-027"><a href="#step-027" style="font-weight:bold">Step 027</a></div>  

Attempt a connection from the Apache web server to the IIS web server using the curl command.  The connection should time out.

<a href="images/module24_027.png"><img src="images/module24_027.png" style="width:100%;height:100%;"></a>  


YOU HAVE FINISHED THIS MODULE


| [Return to Table of Contents](https://tetration.guru/bootcamp/) | [Go to Top of the Page]() | [Continue to the Next Module]() |
