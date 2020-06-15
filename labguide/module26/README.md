# Cisco Tetration - Hands-On Lab

## Module26: Security Visibility & Monitoring
In this module we will review key security visibility and monitoring features of Tetration such as the Security dashboard, Vulnerability dashboard, and others. We'll also investigate configuration of Alert triggers and the multiple alert destinations that can be configured.   


---
<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/26_security_visibility_monitoring.mp4" style="font-weight:bold"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> Click here to view a video reviewing the Security and Vulnerability Dashboards.</a>

---
### Steps for this Module  
<a href="#step-001" style="font-weight:bold">Step 001 - Examine Vulerability Score</a>  
<a href="#step-002" style="font-weight:bold">Step 002 - Review Vulnerability Score Help</a>  
<a href="#step-003" style="font-weight:bold">Step 003 - Examine Process Hash Score</a>  
<a href="#step-004" style="font-weight:bold">Step 004 - Review Process Hash Score Help</a>  
<a href="#step-005" style="font-weight:bold">Step 005 - Change Scope to the nopCommerce application</a>  
<a href="#step-006" style="font-weight:bold">Step 006 - Navigate to the Vulnerabilities Dashboard</a>  
<a href="#step-007" style="font-weight:bold">Step 007 - View vulnerable Packages</a>  
<a href="#step-008" style="font-weight:bold">Step 008 - View vulnerable Workloads</a>  
<a href="#step-009" style="font-weight:bold">Step 009 - View CVE details</a>  
<a href="#step-010" style="font-weight:bold">Step 010 - Review the CVE database</a>  
<a href="#step-011" style="font-weight:bold">Step 011 - Change the Scope to the nopCommerce application</a>  
<a href="#step-012" style="font-weight:bold">Step 012 - Examine the Remotely Exploitable vulnerabilities</a>  
<a href="#step-013" style="font-weight:bold">Step 013 - Review vulnerable nopCommerce Workloads</a>  
<a href="#step-014" style="font-weight:bold">Step 014 - Review IIS web server CVEs</a>  
<a href="#step-015" style="font-weight:bold">Step 015 - Examine the NIST database</a>  
<a href="#step-016" style="font-weight:bold">Step 016 - Navigate to vulnerabilities in the Workload Profile</a>  
<a href="#step-017" style="font-weight:bold">Step 017 - Filter for high CVE score vulnerabilities</a>  
<a href="#step-018" style="font-weight:bold">Step 018 - Review vulnerable packages</a>  
<a href="#step-019" style="font-weight:bold">Step 019 - Review the Process Snapshot</a>  
<a href="#step-020" style="font-weight:bold">Step 020 - Examine Process details</a>  
<a href="#step-021" style="font-weight:bold">Step 021 - Navigate to the Vulnerability Dashboard</a>  
<a href="#step-022" style="font-weight:bold">Step 022 - Change Scope to the OpenCart application</a>  
<a href="#step-023" style="font-weight:bold">Step 023 - Select the Apache web server workload</a>  
<a href="#step-024" style="font-weight:bold">Step 024 - Review the vulnerable packages</a>  
<a href="#step-025" style="font-weight:bold">Step 025 - Examine the Process Snapshot</a>  
<a href="#step-026" style="font-weight:bold">Step 026 - Review process details</a>  
<a href="#step-027" style="font-weight:bold">Step 027 - Navigate to Applications</a>  
<a href="#step-028" style="font-weight:bold">Step 028 - Manage Alerts for an Appication Workspace</a>  
<a href="#step-029" style="font-weight:bold">Step 029 - Configure Compliance Alerts</a>  
<a href="#step-030" style="font-weight:bold">Step 030 - Review current alerts</a>  
<a href="#step-031" style="font-weight:bold">Step 031 - Filter alerts by severity</a>  
<a href="#step-032" style="font-weight:bold">Step 032 - Navigate to alert configuration</a>  
<a href="#step-033" style="font-weight:bold">Step 033 - View alert destinations</a>    

---
<div class="step" id="step-001"><a href="#step-001" style="font-weight:bold">Step 001</a></div>  

Click on the Vulnerability Score on the main dashboard to view Vulnerability Score Help.

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_001.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_001.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-002"><a href="#step-002" style="font-weight:bold">Step 002</a></div>  

The help screen provides explanation of the vulnerability score, how it is calculated, and details on how to improve the score.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_002.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_002.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-003"><a href="#step-003" style="font-weight:bold">Step 003</a></div>  

Scroll down and click on the Process Hash score to reveal Process Hash help.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_003.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_003.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-004"><a href="#step-004" style="font-weight:bold">Step 004</a></div>  

The help screen provides information on what agents are supported as well as how the score is calculated and how to improve the score.  Each of the vulnerability score sections has a similar help screen.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_004.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_004.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-005"><a href="#step-005" style="font-weight:bold">Step 005</a></div>  

By default you are viewing the overall score for all applications and workloads that are installed with Tetration sensors.  It is also possible to drill down to a specific application by changing the Scope.  Change the scope to the nopCommerce application and review how the dashboard has changed to now more specific scores for the nopCommerce application and workloads.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_005.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_005.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-006"><a href="#step-006" style="font-weight:bold">Step 006</a></div>  

Navigate to the Vulnerability dashboard.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_006.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_006.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-007"><a href="#step-007" style="font-weight:bold">Step 007</a></div>  

There are three main tabs; CVEs, Packages, and Workloads.  Click on the Packages tab and review the vulnerable packages.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_007.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_007.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-008"><a href="#step-008" style="font-weight:bold">Step 008</a></div>  

Click on the Workloads tab.  This shows all of the workloads in the environment that are installed with Tetration sensors and their CVE score.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_008.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_008.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-009"><a href="#step-009" style="font-weight:bold">Step 009</a></div>  
Go back to the CVEs tab and click on one of the CVEs.  This will launch a web browser to the NIST National Vulnerability Database which includes all of the details about the vulnerability.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_009.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_009.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-010"><a href="#step-010" style="font-weight:bold">Step 010</a></div>  

Clicking a CVE will launch a web page similar to the one below.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_010.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_010.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-011"><a href="#step-011" style="font-weight:bold">Step 011</a></div>  

It is also possible to filter to a specific application in the vulnerability dashboard by changing the Scope.  Change the scope to the nopCommerce application.

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_011.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_011.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-012"><a href="#step-012" style="font-weight:bold">Step 012</a></div>  

Click on the Remotely Exploitable Low Complexity indicator on the dashboard.  A list of CVEs will be shown below.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_012.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_012.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-013"><a href="#step-013" style="font-weight:bold">Step 013</a></div>  

Click on the Workloads tab,  and then click on the IIS web server.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_013.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_013.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-014"><a href="#step-014" style="font-weight:bold">Step 014</a></div>  

Click on one of the CVEs on the Workload Vulnerability Details screen.  This will once again open a browser to the National Vulnerability Database for the specific details on the vulnerability.

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_014.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_014.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-015"><a href="#step-015" style="font-weight:bold">Step 015</a></div>  

A page such as the one shown below will be displayed.

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_015.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_015.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-016"><a href="#step-016" style="font-weight:bold">Step 016</a></div>  

Click on the link to the IIS web server at the top of the Workload Vulnerability Details screen.  This launches into the Workload Profile Vulnerabilities tab.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_016.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_016.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-017"><a href="#step-017" style="font-weight:bold">Step 017</a></div>  

Here you can view all of the vulnerabilities associated with the server,  and can filter the output based on many factors including severity.  Enter the filter `Score (V2) >= 9` to view vulnerabilities with CVE score of 9 or above.

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_017.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_017.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-018"><a href="#step-018" style="font-weight:bold">Step 018</a></div>  

Click on the Packages tab.  A list of all of the packages running on the machine is displayed.  If a package has vulnerabilities,  it will have a warning sign next to it and you can click on the warning sign to view the vulnerabilities for that package.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_018.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_018.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-019"><a href="#step-019" style="font-weight:bold">Step 019</a></div>  

Click on the Process Snapshot tab.  The process snapshot shows all of the processes that have been seen and that are currently running on the machine.  It displays processes launched as regular users as well as those launched by privileged users.  Hover your mouse over the dots to view the processes.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_019.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_019.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-020"><a href="#step-020" style="font-weight:bold">Step 020</a></div>  

You can also get more details about a process by clicking on it.  Click on a process to view the details.

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_020.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_020.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-021"><a href="#step-021" style="font-weight:bold">Step 021</a></div>  

Navigate to the Vulnerability Dashboard.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_021.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_021.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-022"><a href="#step-022" style="font-weight:bold">Step 022</a></div>  

Change the Scope to OpenCart.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_022.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_022.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-023"><a href="#step-023" style="font-weight:bold">Step 023</a></div>  

Click on the Workloads tab,  and then click on the Apache web server.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_023.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_023.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-024"><a href="#step-024" style="font-weight:bold">Step 024</a></div>  

Click on the link to the Apache web server.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_024.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_024.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-025"><a href="#step-025" style="font-weight:bold">Step 025</a></div>  

Click on the Process Snapshot tab.  Several of the processes on the Apache web server have vulnerabilities, which are shown on the process tree with an orange triangle.  Click on one of the vulnerabilities.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_025.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_025.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-026"><a href="#step-026" style="font-weight:bold">Step 026</a></div>  

Clicking on a vulnerable process shows the process details,  along with the links to the vulnerabilities in the CVE database.


<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_026.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_026.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-027"><a href="#step-027" style="font-weight:bold">Step 027</a></div>  

Next we will explore the ability of Tetration to send notifications upon detected events.  Navigate to Application Workspaces and select any application workspace.  Then click on the Enforcement tab.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_027.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_027.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-028"><a href="#step-028" style="font-weight:bold">Step 028</a></div>  

Click on Manage Alerts.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_028.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_028.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-029"><a href="#step-029" style="font-weight:bold">Step 029</a></div>  

Here we can configure alerts to be generated when Rejected flows exceed a specified threshold,  or when Escaped or Misdropped flows are reported.  Enter the criteria `Enforcement Rejected Flows > 0` and set the Severity to High.  Optionally,  you can choose to receive flow details with the alerts and/or an hourly or daily summary of all alerts.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_029.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_029.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-030"><a href="#step-030" style="font-weight:bold">Step 030</a></div>  

To view alerts within Tetration,   click on Alerts and Current Alerts.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_030.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_030.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-031"><a href="#step-031" style="font-weight:bold">Step 031</a></div>  

Here you can see all of the alerts that have been generated, and can filter the alerts by severity, alert type, alert text, or status.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_031.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_031.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-032"><a href="#step-032" style="font-weight:bold">Step 032</a></div>  

Click on Alerts and then Configuration.  

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_032.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_032.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-033"><a href="#step-033" style="font-weight:bold">Step 033</a></div>  

Here you can configure alert destinations for each type of alert.  The internal Kafka data tap is where the alerts we just viewed are stored.  Alerts can also be sent to an External Kafka data tap,  Syslog, E-Mail,  Slack, Pager Duty or Kinesis.

<a href="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_033.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/module26/images/module26_033.png" style="width:100%;height:100%;"></a>  


YOU HAVE FINISHED THIS MODULE


| [Return to Table of Contents](https://tetration.guru/cisco-tetration-hol/labguide/) | [Go to Top of the Page](https://tetration.guru/cisco-tetration-hol/labguide/module26/) | [Continue to the Next Module](https://tetration.guru/cisco-tetration-hol/labguide/z-appendix-legacy-policy/) |
