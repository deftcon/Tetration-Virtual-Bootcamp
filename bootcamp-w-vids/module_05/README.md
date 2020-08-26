# Cisco Tetration Virtual Bootcamp

## Module 05.00  Connectors

---

## --- Lecture Video ---  
---  
<a href="https://deftcon-tetration-virtual-bootcamp.s3.us-east-2.amazonaws.com/lectures/Module_05.00__Lecture__Connectors.mp4" style="font-weight:bold"><img src="https://tetration.guru/bootcamp-w-vids/diagrams/images/video_icon_small.png">Connectors :: Lecture Video :: Runtime: 29 mins</a>  
  
---  
  

## --- Demo Video ---  
---  
<a href="https://deftcon-tetration-virtual-bootcamp.s3.us-east-2.amazonaws.com/demos/Module_05.00__Demo__Connectors.mp4" style="font-weight:bold"><img src="https://tetration.guru/bootcamp-w-vids/diagrams/images/video_icon_small.png">Connectors :: Demo Video :: Runtime: 28 mins</a>  
  
---  

## --- Lab :: AWS VPC Flow Logs ---
### Steps for this Lab  
<a href="#step-001" style="font-weight:bold">Step 001 - Naviaget to Connectors</a>  
<a href="#step-002" style="font-weight:bold">Step 002 - Select AWS under Flow Ingest</a>  
<a href="#step-003" style="font-weight:bold">Step 003 - Enable the AWS Flow Ingest Connector</a>  
<a href="#step-004" style="font-weight:bold">Step 004 - Deploy Appliance</a>  
<a href="#step-005" style="font-weight:bold">Step 005 - Proceed to the next step</a>  
<a href="#step-006" style="font-weight:bold">Step 006 - Enter the appliance details</a>  
<a href="#step-007" style="font-weight:bold">Step 007 - Complete entering details</a>  
<a href="#step-008" style="font-weight:bold">Step 008 - Download the .iso file</a>  
<a href="#step-009" style="font-weight:bold">Step 009 - Save the file to disk</a>  
<a href="#step-010" style="font-weight:bold">Step 010 - Open a session to the Tetration Data Ingest Appliance</a>  
<a href="#step-011" style="font-weight:bold">Step 011 - Copy the files from the .iso to the appliance</a>  
<a href="#step-012" style="font-weight:bold">Step 012 - Wait for all files to copy</a>  
<a href="#step-013" style="font-weight:bold">Step 013 - Test connectivity and verify files</a>  
<a href="#step-014" style="font-weight:bold">Step 014 - Reboot the appliance</a>  
<a href="#step-015" style="font-weight:bold">Step 015 - Reconnect when the appliance finished rebooting</a>  
<a href="#step-016" style="font-weight:bold">Step 016 - Copy the resolv.conf file to /etc/resolv.conf </a>  
<a href="#step-017" style="font-weight:bold">Step 017 - Reboot the appliance again</a>  
<a href="#step-018" style="font-weight:bold">Step 018 - Examine the logs</a>  
<a href="#step-019" style="font-weight:bold">Step 019 - Proceed to the next step</a>  
<a href="#step-020" style="font-weight:bold">Step 020 - Finish the Deploy Virtual Appliance wizard</a>  
<a href="#step-021" style="font-weight:bold">Step 021 - Check status of the Ingest Appliance</a>  
<a href="#step-022" style="font-weight:bold">Step 022 - Verify the VM details</a>  
<a href="#step-023" style="font-weight:bold">Step 023 - Configure NTP</a>  
<a href="#step-024" style="font-weight:bold">Step 024 - Verify and save NTP configuration</a>  
<a href="#step-025" style="font-weight:bold">Step 025 - Configure Logs</a>  
<a href="#step-026" style="font-weight:bold">Step 026 - Verify and save Log configuration</a>  
<a href="#step-027" style="font-weight:bold">Step 027 - Enable a connector</a>  
<a href="#step-028" style="font-weight:bold">Step 028 - Select the AWS connector</a>  
<a href="#step-029" style="font-weight:bold">Step 029 - Check status of AWS connector</a>  
<a href="#step-030" style="font-weight:bold">Step 030 - Check logs on the appliance</a>  
<a href="#step-031" style="font-weight:bold">Step 031 - Verify AWS connector status</a>  
<a href="#step-032" style="font-weight:bold">Step 032 - Begin AWS Configuration</a>  
<a href="#step-033" style="font-weight:bold">Step 033 - Configure AWS details</a>  
<a href="#step-034" style="font-weight:bold">Step 034 - Complete AWS configuration</a>  
<a href="#step-035" style="font-weight:bold">Step 035 - Begin AWS log configuration</a>  
<a href="#step-036" style="font-weight:bold">Step 036 - Verify and Save Configs</a>  


---  

The diagram below depicts the flow of traffic used by various devices to utimately ingest information into the Tetration cluster. The Tetration Edge appliance is used to subscribe to the pxGrid from ISE for SGT and user-based policy. The Tetration Data Ingest appliance is used to collect NetFlow v9 info from the ASAv which is useful in stitching together flows of traffic from outside the firewall all the way through being NAT'd by that ASAv and then traversing to the internal corporate network and making their way to app frontends. This same Tetration Data Ingest appliance is used to collect Flow Logs from an AWS VPC via an S3 bucket. This is useful for collecting traffic from any workload that may not have (or be able to have) a Tetration agent installed on it.

<a href="https://www.lucidchart.com/documents/view/425e1b97-194e-413a-b793-0df939a87501" target="_blank"><img src="../diagrams/images/diagrams_013.png" style="width:100%;height:100%;"></a>  


### AWS VPC Flow Logs Lab Portion
<div class="step" id="step-001"><a href="#step-001" style="font-weight:bold">Step 001</a></div>  

Navigate to Connectors.

<a href="images/module_05_001.png"><img src="images/module_05_001.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-002"><a href="#step-002" style="font-weight:bold">Step 002</a></div>  

Under Flow Ingest,  select the AWS connector.

<a href="images/module_05_002.png"><img src="images/module_05_002.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-003"><a href="#step-003" style="font-weight:bold">Step 003</a></div>  

Click Enable to begin deploying the appliance.

<a href="images/module_05_003.png"><img src="images/module_05_003.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-004"><a href="#step-004" style="font-weight:bold">Step 004</a></div>  

Select Yes to begin deploying the appliance.

<a href="images/module_05_004.png"><img src="images/module_05_004.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-005"><a href="#step-005" style="font-weight:bold">Step 005</a></div>

Although the instructions on screen indicate downloading an OVA file, this is not necessary because we have deployed the appliance already in AWS.  Click Next to continue.    

<a href="images/module_05_005.png"><img src="images/module_05_005.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-006"><a href="#step-006" style="font-weight:bold">Step 006</a></div>  

The below information will be used to create a .iso file that we will download,  extract, and then copy the files to the appliance.  

> If we were deploying an on-prem appliance, then we would mount the .iso to the virtual CD-ROM on the VM.  

Fill in the appropriate details as can be found on your student worksheet.  There are three IP addresses for the appliance because it runs three Docker containers that must each have a routable IP address on the network.  The IP address of the Active Directory server should be entered as the Name Server.   

<a href="images/module_05_006.png"><img src="images/module_05_006.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-007"><a href="#step-007" style="font-weight:bold">Step 007</a></div>  

Scroll down and click Next to continue.



<a href="images/module_05_007.png"><img src="images/module_05_007.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-008"><a href="#step-008" style="font-weight:bold">Step 008</a></div>  

Click Download Configuration Bundle to download the .iso file to your desktop.  

<a href="images/module_05_008.png"><img src="images/module_05_008.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-009"><a href="#step-009" style="font-weight:bold">Step 009</a></div>  

Save the .iso file to your desktop.  

<a href="images/module_05_009.png"><img src="images/module_05_009.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-010"><a href="#step-010" style="font-weight:bold">Step 010</a></div>  

Open a session to the Tetration Data Ingest Appliance.  This opens a session to the already deployed instance of the ingest appliance in AWS.  

<a href="images/module_05_010.png"><img src="images/module_05_010.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-011"><a href="#step-011" style="font-weight:bold">Step 011</a></div>  

Extract the contents of the .iso file and drag the contents to the ingest appliance window that we opened in step 10.  

<a href="images/module_05_011.png"><img src="images/module_05_011.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-012"><a href="#step-012" style="font-weight:bold">Step 012</a></div>  

Wait for all of the files to fully copy. A status window should be displayed in the lower right hand corner of the screen.

<a href="images/module_05_012.png"><img src="images/module_05_012.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-013"><a href="#step-013" style="font-weight:bold">Step 013</a></div>  

Make sure the appliance has outbound Internet connectivity by pinging well-known web sites such as google.com.  Do an `ls -l` to make sure that the files we copied are present on the appliance.

<a href="images/module_05_013.png"><img src="images/module_05_013.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-014"><a href="#step-014" style="font-weight:bold">Step 014</a></div>  

Type `reboot` to reboot the appliance.  

<a href="images/module_05_014.png"><img src="images/module_05_014.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-015"><a href="#step-015" style="font-weight:bold">Step 015</a></div>  

Once the appliance is done rebooting, reconnect to the session.

<a href="images/module_05_015.png"><img src="images/module_05_015.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-016"><a href="#step-016" style="font-weight:bold">Step 016</a></div>  

Copy the resolv.conf file to /etc/resolv.conf.  Use the command `sudo cp resolf.conf /etc/resolv.conf`.    

<a href="images/module_05_016.png"><img src="images/module_05_016.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-017"><a href="#step-017" style="font-weight:bold">Step 017</a></div>  

Type `reboot` to reboot the appliance again.  

<a href="images/module_05_017.png"><img src="images/module_05_017.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-018"><a href="#step-018" style="font-weight:bold">Step 018</a></div>  

Reconnect to the appliance once it is done rebooting.  Review the log files using the command `cat /local/tetration/logs/tet-controller.log`.  You will at first see error messages as shown in the below image.  Once the messages "registration succeeded" and "controller initialized" appear in the output, we are read to proceed with the next task.

<a href="images/module_05_018.png"><img src="images/module_05_018.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-019"><a href="#step-019" style="font-weight:bold">Step 019</a></div>  

Click Next in the Deploy Virtual Appliance wizard.  

<a href="images/module_05_019.png"><img src="images/module_05_019.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-020"><a href="#step-020" style="font-weight:bold">Step 020</a></div>  

The instructions here once again refer to deployment of an on-prem appliance in VMware.  Click Done to complete the wizard.  

<a href="images/module_05_020.png"><img src="images/module_05_020.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-021"><a href="#step-021" style="font-weight:bold">Step 021</a></div>  

Check the status of the Data Ingest Appliance.  It should be Active.

<a href="images/module_05_021.png"><img src="images/module_05_021.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-022"><a href="#step-022" style="font-weight:bold">Step 022</a></div>  

Click on the VM tab to review the configuration.  The information that we entered and downloaded into the .iso file should be displayed.  

<a href="images/module_05_022.png"><img src="images/module_05_022.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-023"><a href="#step-023" style="font-weight:bold">Step 023</a></div>

Click on the NTP tab and click Start NTP Configuration.   

<a href="images/module_05_023.png"><img src="images/module_05_023.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-024"><a href="#step-024" style="font-weight:bold">Step 024</a></div>  

Enter the NTP server `time.google.com` and click Verify & Save Configs.  

<a href="images/module_05_024.png"><img src="images/module_05_024.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-025"><a href="#step-025" style="font-weight:bold">Step 025</a></div>  

Click on the Log tab and select Start Log Configuration.  

<a href="images/module_05_025.png"><img src="images/module_05_025.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-026"><a href="#step-026" style="font-weight:bold">Step 026</a></div>

Change the Logging Level to info, and then click Verify & Save Configs.  

<a href="images/module_05_026.png"><img src="images/module_05_026.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-027"><a href="#step-027" style="font-weight:bold">Step 027</a></div>  

Click the button to Enable a Connector.  

<a href="images/module_05_027.png"><img src="images/module_05_027.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-028"><a href="#step-028" style="font-weight:bold">Step 028</a></div>  

Choose AWS and enable the connector.  

<a href="images/module_05_028.png"><img src="images/module_05_028.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-029"><a href="#step-029" style="font-weight:bold">Step 029</a></div>  

Click on the AWS tab.  It takes a few minutes for the connector to become active,  so you will likely see the "Connector must be active for any config changes"

<a href="images/module_05_029.png"><img src="images/module_05_029.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-030"><a href="#step-030" style="font-weight:bold">Step 030</a></div>  

Open a session to the Tetration data ingest appliance and use the command `cat /local/tetration/logs/tet-controller.log` to view the log files.  Once messages are seen that indicate "registration succeeded" and "aws_sensor-3.3.2.16-aws image is created",  the connector should be ready.

<a href="images/module_05_030.png"><img src="images/module_05_030.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-031"><a href="#step-031" style="font-weight:bold">Step 031</a></div>  

You should now have a green checkmark next to the AWS connector.  Click on the AWS connector.  

<a href="images/module_05_031.png"><img src="images/module_05_031.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-032"><a href="#step-032" style="font-weight:bold">Step 032</a></div>  

On the AWS tab,  select Start AWS Configuration.

<a href="images/module_05_032.png"><img src="images/module_05_032.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-033"><a href="#step-033" style="font-weight:bold">Step 033</a></div>  

Enter in the AWS details as provided in your student spreadsheet.  

<a href="images/module_05_033.png"><img src="images/module_05_033.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-034"><a href="#step-034" style="font-weight:bold">Step 034</a></div>  

A message should be received "AWS configurations successfully applied"

<a href="images/module_05_034.png"><img src="images/module_05_034.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-035"><a href="#step-035" style="font-weight:bold">Step 035</a></div>  

Click on the Log tab and select Start Log Configuration.

<a href="images/module_05_035.png"><img src="images/module_05_035.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-036"><a href="#step-036" style="font-weight:bold">Step 036</a></div>  

Change the Logging Level to debug and click Verify & Save Configs.  

<a href="images/module_05_036.png"><img src="images/module_05_036.png" style="width:100%;height:100%;"></a>  


## --- Lab :: ASA Connector and NAT Stitching ---
<a href="#step-037" style="font-weight:bold">Step 037 - Open a session to the Windows 10 employee desktop </a>  
<a href="#step-038" style="font-weight:bold">Step 038 - Open a web browser and point to the NAT IP of the IIS web server</a>  
<a href="#step-039" style="font-weight:bold">Step 039 - Navigate to Flow Search and filter the flows</a>  
<a href="#step-040" style="font-weight:bold">Step 040 - Click on the graph</a>  
<a href="#step-041" style="font-weight:bold">Step 041 - Review the flow without NAT information</a>  
<a href="#step-042" style="font-weight:bold">Step 042 - Navigate to Virtual Appliances</a>  
<a href="#step-043" style="font-weight:bold">Step 043 - Select Tetration Data Ingest</a>  
<a href="#step-044" style="font-weight:bold">Step 044 - Enable another connector</a>  
<a href="#step-045" style="font-weight:bold">Step 045 - Enable the ASA connector</a>  
<a href="#step-046" style="font-weight:bold">Step 046 - Click on the ASA connector</a>  
<a href="#step-047" style="font-weight:bold">Step 047 - Review the IP bindings</a>  
<a href="#step-048" style="font-weight:bold">Step 048 - Open a session to the ASA</a>  
<a href="#step-049" style="font-weight:bold">Step 049 - Review ASA configuration</a>  
<a href="#step-050" style="font-weight:bold">Step 050 - Review ASA verification commands</a>  
<a href="#step-051" style="font-weight:bold">Step 051 - Navigate to Flow Search</a>  
<a href="#step-052" style="font-weight:bold">Step 052 - Click on time range and select 1hr</a>  
<a href="#step-053" style="font-weight:bold">Step 053 - Filter the flows</a>  
<a href="#step-054" style="font-weight:bold">Step 054 - View flow details</a>  
<a href="#step-055" style="font-weight:bold">Step 055 - Review Related Flow information</a>  

---  
#### ASA Connector and NAT Stitching Lab Portion

<div class="step" id="step-037"><a href="#step-037" style="font-weight:bold">Step 037</a></div>  

Open a session to the employee desktop machine,  open a terminal session and enter the command `ifconfig` to view the IP address.   

> REPLACE IMAGE WITH UBUNTU!  

<a href="images/module_05_037.png"><img src="images/module_05_037.png" style="width:100%;height:100%;"></a>  


<div class="step" id="step-038"><a href="#step-038" style="font-weight:bold">Step 038</a></div>  

Open a web browser and connect to the OpenCart web server outside NAT address as provided in your student workbook.  The outside NAT IP is a static NAT on an ASA firewall that sits between the employee desktop on the outside and the servers on the inside.

> REPLACE IMAGE WITH UBUNTU!

<a href="images/module_05_038.png"><img src="images/module_05_038.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-039"><a href="#step-039" style="font-weight:bold">Step 039</a></div>  

Navigate to Flow Search,  and enter the a filter where the Provider is the inside IP address of the Apache web server and the Consumer is the IP address of the employee desktop.

<a href="images/module_05_039.png"><img src="images/module_05_039.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-040"><a href="#step-040" style="font-weight:bold">Step 040</a></div>  

Click on a point in the graph where there is data.  You may need to change the time range to display the last hour, and also may need to wait a few minutes for the traffic we just generated to the web server from the employee desktop to show up.  

<a href="images/module_05_040.png"><img src="images/module_05_040.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-041"><a href="#step-041" style="font-weight:bold">Step 041</a></div>  

Click on one of the flows to bring up Flow Details.  Notice that there is no mention of the outside NAT IP of the Apache web server that we used to connect from the employee desktop.  

<a href="images/module_05_041.png"><img src="images/module_05_041.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-042"><a href="#step-042" style="font-weight:bold">Step 042</a></div>  

Navigate to Connectors and select Virtual Appliances.

<a href="images/module_05_042.png"><img src="images/module_05_042.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-043"><a href="#step-043" style="font-weight:bold">Step 043</a></div>  

Click on the Tetration Data Ingest heading.  

<a href="images/module_05_043.png"><img src="images/module_05_043.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-044"><a href="#step-044" style="font-weight:bold">Step 044</a></div>  

Click Enable Another Connector.  

<a href="images/module_05_044.png"><img src="images/module_05_044.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-045"><a href="#step-045" style="font-weight:bold">Step 045</a></div>  

Select ASA from the dropdown and then select Enable Selected Connector.


<a href="images/module_05_045.png"><img src="images/module_05_045.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-046"><a href="#step-046" style="font-weight:bold">Step 046</a></div>  

Click on the ASA connector.  

<a href="images/module_05_046.png"><img src="images/module_05_046.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-047"><a href="#step-047" style="font-weight:bold">Step 047</a></div>  

It will take a few minutes for the ASA connector to come online.  Once it does,  an IP bindings tab should become available.  Click on the tab to deplay the target IP address and UDP port for Netflow.  This is the information that is needed to configure the ASA for Netflow.  

<a href="images/module_05_047.png"><img src="images/module_05_047.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-048"><a href="#step-048" style="font-weight:bold">Step 048</a></div>  

The ASA firewall was configured as part of the lab build process. Open a session to the ASA firewall to view the configuration.   Enter the command `show run | in flow` to view the commands associated with the Netflow configuration.  

<a href="images/module_05_048.png"><img src="images/module_05_048.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-049"><a href="#step-049" style="font-weight:bold">Step 049</a></div>  

Enter the command `show run | g policy-map flow-export` to view additional configuration that is needed for Netflow.

<a href="images/module_05_049.png"><img src="images/module_05_049.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-050"><a href="#step-050" style="font-weight:bold">Step 050</a></div>  

Enter the `show flow-export counters` command to display the Netflow statistics.  

<a href="images/module_05_050.png"><img src="images/module_05_050.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-051"><a href="#step-051" style="font-weight:bold">Step 051</a></div>  

Navigate to Flow Search.

<a href="images/module_05_051.png"><img src="images/module_05_051.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-052"><a href="#step-052" style="font-weight:bold">Step 052</a></div>  

Change the time range to 1 hr.  

<a href="images/module_05_052.png"><img src="images/module_05_052.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-053"><a href="#step-053" style="font-weight:bold">Step 053</a></div>  

Create a filter where the Provider Hostname = the hostname of the Apache web server and Consumer Address = the IP of the employee desktop.  

<a href="images/module_05_053.png"><img src="images/module_05_053.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-054"><a href="#step-054" style="font-weight:bold">Step 054</a></div>

Click on one of the flows returned under Flow Observations. Notice that there is now a field called NAT Direction.  Also there is a new link that says "Related Flow".  Click on the Related Flow link.   

<a href="images/module_05_054.png"><img src="images/module_05_054.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-055"><a href="#step-055" style="font-weight:bold">Step 055</a></div>  

The original flow details are displayed including the outside NAT IP of the Apache web server.  

<a href="images/module_05_055.png"><img src="images/module_05_055.png" style="width:100%;height:100%;"></a>  

---   

## --- OPTIONAL Lab :: ISE
> NOTE: ISE does not deploy via API at this time. You must have ISE deployed and establish a tunnel to your AWS VPC to complete this portion. 
### Steps for this Lab  
<a href="#step-001" style="font-weight:bold">Step 001 - Navigate to Connectors</a>  
<a href="#step-002" style="font-weight:bold">Step 002 - Click on ISE</a>  
<a href="#step-003" style="font-weight:bold">Step 003 - Enable the ISE connector</a>  
<a href="#step-004" style="font-weight:bold">Step 004 - Begin deploying the virtual appliance</a>  
<a href="#step-005" style="font-weight:bold">Step 005 - Begin deploying Tetration Edge</a>  
<a href="#step-006" style="font-weight:bold">Step 006 - Enter .iso file details</a>  
<a href="#step-007" style="font-weight:bold">Step 007 - Complete .iso file details</a>  
<a href="#step-008" style="font-weight:bold">Step 008 - Download Configuration Bundle</a>  
<a href="#step-009" style="font-weight:bold">Step 009 - Finish deploying the virtual appliance</a>  
<a href="#step-010" style="font-weight:bold">Step 010 - Extract the .iso file</a>  
<a href="#step-011" style="font-weight:bold">Step 011 - Open a session to the Tetration Edge appliance</a>  
<a href="#step-012" style="font-weight:bold">Step 012 - Copy the extracted files to the appliance </a>  
<a href="#step-013" style="font-weight:bold">Step 013 - List the copied files</a>  
<a href="#step-014" style="font-weight:bold">Step 014 - Reboot the appliance</a>  
<a href="#step-015" style="font-weight:bold">Step 015 - Extract the provided certificate data</a>  
<a href="#step-016" style="font-weight:bold">Step 016 - Create an RSA key file</a>  
<a href="#step-017" style="font-weight:bold">Step 017 - Open the certificates and key</a>  
<a href="#step-018" style="font-weight:bold">Step 018 - Navigate to the ISE connector</a>  
<a href="#step-019" style="font-weight:bold">Step 019 - Add Instance Config</a>  
<a href="#step-020" style="font-weight:bold">Step 020 - Copy/paste the ISE Client Certificate</a>  
<a href="#step-021" style="font-weight:bold">Step 021 - Copy/paste the ISE Client Key</a>  
<a href="#step-022" style="font-weight:bold">Step 022 - Copy/paste the ISE CA Certificate</a>  
<a href="#step-023" style="font-weight:bold">Step 023 - Enter the ISE hostname and node name</a>  
<a href="#step-024" style="font-weight:bold">Step 024 - Configuration successfully applied</a>  
<a href="#step-025" style="font-weight:bold">Step 025 - View the pxGrid certificates in ISE</a>  
<a href="#step-026" style="font-weight:bold">Step 026 - Refresh to see the new tet-edge certificate</a>  
<a href="#step-027" style="font-weight:bold">Step 027 - Begin LDAP configuration</a>  
<a href="#step-028" style="font-weight:bold">Step 028 - Enter LDAP parameters</a>  
<a href="#step-029" style="font-weight:bold">Step 029 - Enter LDAP parameters</a>  
<a href="#step-030" style="font-weight:bold">Step 030 - Enter LDAP attributes</a>  
<a href="#step-031" style="font-weight:bold">Step 031 - Apply LDAP configuration</a>  
<a href="#step-032" style="font-weight:bold">Step 032 - View endpoint timeout</a>  
<a href="#step-033" style="font-weight:bold">Step 033 - Start Log configuration</a>  
<a href="#step-034" style="font-weight:bold">Step 034 - Verify and Save Configs</a>  

---

<div class="step" id="step-001"><a href="#step-001" style="font-weight:bold">Step 001</a></div>  

Navigate to Connectors.

<a href="images/module_05-ISE_001.png"><img src="images/module_05-ISE_001.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-002"><a href="#step-002" style="font-weight:bold">Step 002</a></div>  

Click on ISE.

<a href="images/module_05-ISE_002.png"><img src="images/module_05-ISE_002.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-003"><a href="#step-003" style="font-weight:bold">Step 003</a></div>  

Click to Enable the ISE Connector.

<a href="images/module_05-ISE_003.png"><img src="images/module_05-ISE_003.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-004"><a href="#step-004" style="font-weight:bold">Step 004</a></div>  

Select Yes to begin deploying the virtual appliance.

<a href="images/module_05-ISE_004.png"><img src="images/module_05-ISE_004.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-005"><a href="#step-005" style="font-weight:bold">Step 005</a></div>  

The on-screen instructions refer to downloading an .ova file,  this would be done if we were using an on-prem VMware installation.  We have already deployed the Tetration Edge virtual appliance in AWS,  so we can skip this step.  Select Next.  

<a href="images/module_05-ISE_005.png"><img src="images/module_05-ISE_005.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-006"><a href="#step-006" style="font-weight:bold">Step 006</a></div>  

Enter the information that will be populated into the Edge appliance.  The IP addressing information is provided in your student workbook.  Please make sure to enter the IP address of the Windows Active Directory server for the Name Server field.  Do not enter 1.1.1.1 and 8.8.8.8 as shown in the diagram,  or name resolution will not work from the Edge appliance to the ISE appliance and result in not being able to bring up the ISE integration.

<a href="images/module_05-ISE_006.png"><img src="images/module_05-ISE_006.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-007"><a href="#step-007" style="font-weight:bold">Step 007</a></div>  

Enter the Search Domain `hol.local` and then select Next.    

<a href="images/module_05-ISE_007.png"><img src="images/module_05-ISE_007.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-008"><a href="#step-008" style="font-weight:bold">Step 008</a></div>  

 Click Download Configuration Bundle and save the .iso file to your desktop.  

<a href="images/module_05-ISE_008.png"><img src="images/module_05-ISE_008.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-009"><a href="#step-009" style="font-weight:bold">Step 009</a></div>  

Click Done to complete the Deploy Virtual Appliance wizard.

<a href="images/module_05-ISE_009.png"><img src="images/module_05-ISE_009.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-010"><a href="#step-010" style="font-weight:bold">Step 010</a></div>  

Extract the contents of the .iso file.  

<a href="images/module_05-ISE_010.png"><img src="images/module_05-ISE_010.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-011"><a href="#step-011" style="font-weight:bold">Step 011</a></div>  

Open a session to the Tetration Edge appliance.  

<a href="images/module_05-ISE_011.png"><img src="images/module_05-ISE_011.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-012"><a href="#step-012" style="font-weight:bold">Step 012</a></div>  

Copy the extracted files from the .iso to the Tetration Edge appliance. You can drag and drop the files on the browser window to accomplish this.  

<a href="images/module_05-ISE_012.png"><img src="images/module_05-ISE_012.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-013"><a href="#step-013" style="font-weight:bold">Step 013</a></div>  

Enter the command `ls -l` and ensure all of the files from the .iso were copied over.

<a href="images/module_05-ISE_013.png"><img src="images/module_05-ISE_013.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-014"><a href="#step-014" style="font-weight:bold">Step 014</a></div>  

Reboot the appliance by issuing the `reboot` command.

<a href="images/module_05-ISE_014.png"><img src="images/module_05-ISE_014.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-015"><a href="#step-015" style="font-weight:bold">Step 015</a></div>  

Extract the provided certificate data to your desktop.  

<a href="images/module_05-ISE_015.png"><img src="images/module_05-ISE_015.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-016"><a href="#step-016" style="font-weight:bold">Step 016</a></div>  

Open a command prompt and change directory into the folder where the certificate data was extracted.  Enter the following command, substituting the correct IP address for the Tetration Edge appliance for 10.0.1.164.  

`openssl rsa -in tet-edge.hol.local_10.0.1.164.key -out openISE.key`

Enter a passphrase that you will remember.  

<a href="images/module_05-ISE_016.png"><img src="images/module_05-ISE_016.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-017"><a href="#step-017" style="font-weight:bold">Step 017</a></div>  

Open the certificates and key file in a text editor.  

<a href="images/module_05-ISE_017.png"><img src="images/module_05-ISE_017.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-018"><a href="#step-018" style="font-weight:bold">Step 018</a></div>  

Navigate to Connectors and select ISE.  

<a href="images/module_05-ISE_018.png"><img src="images/module_05-ISE_018.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-019"><a href="#step-019" style="font-weight:bold">Step 019</a></div>  

Click on Add Instance Config.  

<a href="images/module_05-ISE_019.png"><img src="images/module_05-ISE_019.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-020"><a href="#step-020" style="font-weight:bold">Step 020</a></div>  

Paste the contents of file `tet-edge.hol.local_10.0.1.164.cer` to the ISE Client Certificate.

<a href="images/module_05-ISE_020.png"><img src="images/module_05-ISE_020.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-021"><a href="#step-021" style="font-weight:bold">Step 021</a></div>  

Paste the contents of the openISE.key file to the ISE Client Key.

<a href="images/module_05-ISE_021.png"><img src="images/module_05-ISE_021.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-022"><a href="#step-022" style="font-weight:bold">Step 022</a></div>  

Paste the contents of the file `isev-small-2-4.hol.local_cer` to the ISE Server CA Certificate.  

<a href="images/module_05-ISE_022.png"><img src="images/module_05-ISE_022.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-023"><a href="#step-023" style="font-weight:bold">Step 023</a></div>  

Set the ISE Hostname to `isev-small-2-4.hol.local` and the ISE Node Name to `isev-small-2-4`. Then click Verify & Save configs.

<a href="images/module_05-ISE_023.png"><img src="images/module_05-ISE_023.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-024"><a href="#step-024" style="font-weight:bold">Step 024</a></div>  

You should receive the message "ISE configurations successfully applied"


<a href="images/module_05-ISE_024.png"><img src="images/module_05-ISE_024.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-025"><a href="#step-025" style="font-weight:bold">Step 025</a></div>  

Open a session to ISE and navigate to Administration > PxGrid Services > Web Clients.

<a href="images/module_05-ISE_025.png"><img src="images/module_05-ISE_025.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-026"><a href="#step-026" style="font-weight:bold">Step 026</a></div>  

Click on Refresh to view the new certificate that was assigned to the Tetration Edge appliance.

<a href="images/module_05-ISE_026.png"><img src="images/module_05-ISE_026.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-027"><a href="#step-027" style="font-weight:bold">Step 027</a></div>

Navigate back to Connectors and select the ISE connector.  Click on the LDAP tab.  In addition to ISE attributes,  we can also bring in LDAP attributes from Active Directory which will be populated into Tetration as annotations.  

<a href="images/module_05-ISE_027.png"><img src="images/module_05-ISE_027.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-028"><a href="#step-028" style="font-weight:bold">Step 028</a></div>  

Enter the LDAP configuration parameters as shown in the image. However, you must substitute the LDAP Server IP address with your Active Directory server IP address.

<a href="images/module_05-ISE_028.png"><img src="images/module_05-ISE_028.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-029"><a href="#step-029" style="font-weight:bold">Step 029</a></div>  

Enter the LDAP Base DN and Filter String as shown.  Then select Next.  


<a href="images/module_05-ISE_029.png"><img src="images/module_05-ISE_029.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-030"><a href="#step-030" style="font-weight:bold">Step 030</a></div>  

Enter the LDAP Username Attribute and the LDAP Attributes to Fetch as shown in the image.

<a href="images/module_05-ISE_030.png"><img src="images/module_05-ISE_030.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-031"><a href="#step-031" style="font-weight:bold">Step 031</a></div>

Click Save & Apply Configs.  

<a href="images/module_05-ISE_031.png"><img src="images/module_05-ISE_031.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-032"><a href="#step-032" style="font-weight:bold">Step 032</a></div>  

Click on the Endpoint tab.  This displays the inactivity timeout for ISE endpoints.

<a href="images/module_05-ISE_032.png"><img src="images/module_05-ISE_032.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-033"><a href="#step-033" style="font-weight:bold">Step 033</a></div>  

Click the Log tab and select Start Log Configuration.

<a href="images/module_05-ISE_033.png"><img src="images/module_05-ISE_033.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-034"><a href="#step-034" style="font-weight:bold">Step 034</a></div>  

Enter the Logging Level of info,  then Verify & Save Configs.  

<a href="images/module_05-ISE_034.png"><img src="images/module_05-ISE_034.png" style="width:100%;height:100%;"></a>  

---   



| [Return to Table of Contents](https://tetration.guru/bootcamp-w-vids/) | [Go to Top of the Page](README.md) | [Continue to the Next Module](../module_06/) |