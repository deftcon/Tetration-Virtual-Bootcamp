# Cisco Tetration Virtual Bootcamp

## Module 07.10  Segmentation - Enforcement - Pre Enforcement Checks

In this module we will test access to the applications and workloads prior to enabling enforcement to ensure that everything worked as expected prior to enforcement.  Later when we enable enforcement we will re-run these same tests to ensure that the desired intent was achieved. 

<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/21_policy_enforcement_pre-enforcement.mp4" style="font-weight:bold" title="Enforcement Policy Tuning"><img src="https://tetration.guru/bootcamp/diagrams/images/video_icon_mini.png"> Click here to view a video of tasks performed to go through a series of pre-enforcement checks prior to taking all workloads into enforcement mode.</a>


### Steps for this Module  
<a href="#step-001" style="font-weight:bold">Step 001 - Test public access to the IIS web server</a>  
<a href="#step-002" style="font-weight:bold">Step 002 - Test public access to the Apache web server</a>  
<a href="#step-003" style="font-weight:bold">Step 003 - Open a session to the IIS web server</a>  
<a href="#step-004" style="font-weight:bold">Step 004 - Test outbound access to the Internet</a>  
<a href="#step-005" style="font-weight:bold">Step 005 - Open a browser to the Apache web server</a>  
<a href="#step-006" style="font-weight:bold">Step 006 - Continue opening a browser to the Apache web server </a>  
<a href="#step-007" style="font-weight:bold">Step 007 - Browser loaded to the Apache web server</a>  
<a href="#step-008" style="font-weight:bold">Step 008 - Open a session to the Apache web server</a>  
<a href="#step-009" style="font-weight:bold">Step 009 - Test outbound access to the Internet via ping</a>  
<a href="#step-010" style="font-weight:bold">Step 010 - Test outbound access to the Internet using HTTP</a>  
<a href="#step-011" style="font-weight:bold">Step 011 - Test HTTP connection to the IIS web server</a>  
<a href="#step-012" style="font-weight:bold">Step 012 - Open a session to the Employee desktop</a>  
<a href="#step-013" style="font-weight:bold">Step 013 - Open the Cisco Anyconnect client</a>  
<a href="#step-014" style="font-weight:bold">Step 014 - Connect to VPN</a>  
<a href="#step-015" style="font-weight:bold">Step 015 - Ignore the security warning and connect</a>  
<a href="#step-016" style="font-weight:bold">Step 016 - Enter employee credentials</a>  
<a href="#step-017" style="font-weight:bold">Step 017 - Test access to the IIS web server via HTTP</a>  
<a href="#step-018" style="font-weight:bold">Step 018 - Test access to the IIS web server via HTTPS</a>  
<a href="#step-019" style="font-weight:bold">Step 019 - View HTTPS output</a>  
<a href="#step-020" style="font-weight:bold">Step 020 - Test connectivity to the Apache web server via HTTP</a>  
<a href="#step-021" style="font-weight:bold">Step 021 - Test connectivity to the Apache web server via HTTPS</a>  
<a href="#step-022" style="font-weight:bold">Step 022 - Review the HTTPS output</a>  
<a href="#step-023" style="font-weight:bold">Step 023 - Test SSH access to the Apache web server</a>  
<a href="#step-024" style="font-weight:bold">Step 024 - Open the Remmina RDP application</a>  
<a href="#step-025" style="font-weight:bold">Step 025 - Test RDP to the IIS web server</a>  

---

<div class="step" id="step-001"><a href="#step-001" style="font-weight:bold">Step 001</a></div>  

Test public access to the IIS web server.

<a href="images/module21_001.png"><img src="images/module21_001.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-002"><a href="#step-002" style="font-weight:bold">Step 002</a></div>  

Test public access to the Apache web server.

<a href="images/module21_002.png"><img src="images/module21_002.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-003"><a href="#step-003" style="font-weight:bold">Step 003</a></div>  

Open a session to the IIS web server.

<a href="images/module21_003.png"><img src="images/module21_003.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-004"><a href="#step-004" style="font-weight:bold">Step 004</a></div>  

Test outbound access to the Internet from the IIS web server.

<a href="images/module21_004.png"><img src="images/module21_004.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-005"><a href="#step-005" style="font-weight:bold">Step 005</a></div>  

Next we will test access from the IIS web server to the Apache web server.  This is traffic that should be blocked once we implement our policy. Browse to the IP address of the Apache web server.  Click Advanced on the security warning.

<a href="images/module21_005.png"><img src="images/module21_005.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-006"><a href="#step-006" style="font-weight:bold">Step 006</a></div>  

Click on Proceed to continue.  

<a href="images/module21_006.png"><img src="images/module21_006.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-007"><a href="#step-007" style="font-weight:bold">Step 007</a></div>  

The ACME Digital Store web site should be displayed.  

<a href="images/module21_007.png"><img src="images/module21_007.png" style="width:100%;height:100%;"></a>  




<div class="step" id="step-008"><a href="#step-008" style="font-weight:bold">Step 008</a></div>  

Open a session to the Apache web server.  

<a href="images/module21_008.png"><img src="images/module21_008.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-009"><a href="#step-009" style="font-weight:bold">Step 009</a></div>  

Test outbound Internet access by issuing ping commands to well-known web sites.  

<a href="images/module21_009.png"><img src="images/module21_009.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-010"><a href="#step-010" style="font-weight:bold">Step 010</a></div>  

Use the curl command to initiate an outbound HTTP connection to well-known web sites.

<a href="images/module21_010.png"><img src="images/module21_010.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-011"><a href="#step-011" style="font-weight:bold">Step 011</a></div>  

Use the curl command to create an HTTP session from the Apache web server to the IIS web server.

<a href="images/module21_011.png"><img src="images/module21_011.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-012"><a href="#step-012" style="font-weight:bold">Step 012</a></div>  

Open a session to the Employee desktop.  

<a href="images/module21_012.png"><img src="images/module21_012.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-013"><a href="#step-013" style="font-weight:bold">Step 013</a></div>  

Click on the Cisco AnyConnect VPN Client icon on the desktop.  

<a href="images/module21_013.png"><img src="images/module21_013.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-014"><a href="#step-014" style="font-weight:bold">Step 014</a></div>  

Click Connect.  

<a href="images/module21_014.png"><img src="images/module21_014.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-015"><a href="#step-015" style="font-weight:bold">Step 015</a></div>  

Select Connect Anyway on the security warning.  

<a href="images/module21_015.png"><img src="images/module21_015.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-016"><a href="#step-016" style="font-weight:bold">Step 016</a></div>  

Log in using your employee credentials.

<a href="images/module21_016.png"><img src="images/module21_016.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-017"><a href="#step-017" style="font-weight:bold">Step 017</a></div>  

Open the terminal application and use the curl command to open an HTTP connection to the IIS web server.  The terminal application can be launched by clicking the black icon in the bottom middle of the screen.  

<a href="images/module21_017.png"><img src="images/module21_017.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-018"><a href="#step-018" style="font-weight:bold">Step 018</a></div>  

Use curl to open an HTTPS session to the IIS web server. This can be accomplished by using the -k flag and https for the URL as shown in the below image.   

<a href="images/module21_018.png"><img src="images/module21_018.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-019"><a href="#step-019" style="font-weight:bold">Step 019</a></div>  

The below image shows the output of the curl command which is a text-based representation of the web site.

<a href="images/module21_019.png"><img src="images/module21_019.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-020"><a href="#step-020" style="font-weight:bold">Step 020</a></div>  

Test an HTTP connection to the Apache web server using the curl command.    

<a href="images/module21_020.png"><img src="images/module21_020.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-021"><a href="#step-021" style="font-weight:bold">Step 021</a></div>  

Test an HTTPS connection to the Apache web server using the curl command.

<a href="images/module21_021.png"><img src="images/module21_021.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-022"><a href="#step-022" style="font-weight:bold">Step 022</a></div>  

The below image shows the text-based representation of the web site that is returned from the previous curl command.

<a href="images/module21_022.png"><img src="images/module21_022.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-023"><a href="#step-023" style="font-weight:bold">Step 023</a></div>  

Connect to the Apache web server using SSH.  The connection should be successful.  

<a href="images/module21_023.png"><img src="images/module21_023.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-024"><a href="#step-024" style="font-weight:bold">Step 024</a></div>  
Click on the Search icon at the bottom of the screen and search for the Remmina application.  This is an Remote Desktop application for Ubuntu.  Click on Remmina,  and select Launch.  


<a href="images/module21_024.png"><img src="images/module21_024.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-025"><a href="#step-025" style="font-weight:bold">Step 025</a></div>  

Enter the IP address of the IIS web server and click Connect.  A userid/password dialogue should be display.  This indicates that the connection was successful to the IIS server.  There is no need to log into the RDP session.  Close the login dialogue.

<a href="images/module21_025.png"><img src="images/module21_025.png" style="width:100%;height:100%;"></a>  

REPEAT STEPS 12-25 ON THE SYSADMIN MACHINE.  

YOU HAVE FINISHED THIS MODULE

| [Return to Table of Contents](https://tetration.guru/bootcamp/) | [Go to Top of the Page](readme.md) | [Continue to the Next Module]() |
