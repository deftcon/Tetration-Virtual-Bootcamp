# Cisco Tetration - Hands-On Lab

## Module09: Edge Appliance - ISE

---

This diagram depicts the flow of traffic used by various devices to utimately ingest information into the Tetration cluster. The Tetration Edge appliance is used to subscribe to the pxGrid from ISE for SGT and user-based policy. The Tetration Data Ingest appliance is used to collect NetFlow v9 info from the ASAv which is useful in stitching together flows of traffic from outside the firewall all the way through being NAT'd by that ASAv and then traversing to the internal corporate network and making their way to app frontends. This same Tetration Data Ingest appliance is used to collect Flow Logs from an AWS VPC via an S3 bucket. This is useful for collecting traffic from any workload that may not have (or be able to have) a Tetration agent installed on it.

<a href="images/diagrams_013.png"><img src="images/diagrams_013.png" style="width:100%;height:100%;"></a>  

---

<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/09a_comissioning_tetration_edge_appliance.mp4" style="font-weight:bold" title="Data Ingest Appliance and ASAv NAT Flow Stiching"><img src="https://tetration.guru/bootcamp/diagrams/images/video_icon_mini.png">Click here to view a video showing the necessary tasks to comission the Tetration Edge appliance to prepare for integration with Cisco ISE (note this is similar to data ingest with nuanced differences).</a>

<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/09b_ise_integration.mp4" style="font-weight:bold" title="Data Ingest Appliance and ASAv NAT Flow Stiching"><img src="https://tetration.guru/bootcamp/diagrams/images/video_icon_mini.png"> Click here to view a video showing the necessary tasks to integrate Cisco ISE with Tetration to prepare to support user-based policy in Module 16.</a>

---

### Steps for this Module  
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

<a href="images/module09_001.png"><img src="images/module09_001.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-002"><a href="#step-002" style="font-weight:bold">Step 002</a></div>  

Click on ISE.

<a href="images/module09_002.png"><img src="images/module09_002.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-003"><a href="#step-003" style="font-weight:bold">Step 003</a></div>  

Click to Enable the ISE Connector.

<a href="images/module09_003.png"><img src="images/module09_003.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-004"><a href="#step-004" style="font-weight:bold">Step 004</a></div>  

Select Yes to begin deploying the virtual appliance.

<a href="images/module09_004.png"><img src="images/module09_004.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-005"><a href="#step-005" style="font-weight:bold">Step 005</a></div>  

The on-screen instructions refer to downloading an .ova file,  this would be done if we were using an on-prem VMware installation.  We have already deployed the Tetration Edge virtual appliance in AWS,  so we can skip this step.  Select Next.  

<a href="images/module09_005.png"><img src="images/module09_005.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-006"><a href="#step-006" style="font-weight:bold">Step 006</a></div>  

Enter the information that will be populated into the Edge appliance.  The IP addressing information is provided in your student workbook.  Please make sure to enter the IP address of the Windows Active Directory server for the Name Server field.  Do not enter 1.1.1.1 and 8.8.8.8 as shown in the diagram,  or name resolution will not work from the Edge appliance to the ISE appliance and result in not being able to bring up the ISE integration.

<a href="images/module09_006.png"><img src="images/module09_006.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-007"><a href="#step-007" style="font-weight:bold">Step 007</a></div>  

Enter the Search Domain `hol.local` and then select Next.    

<a href="images/module09_007.png"><img src="images/module09_007.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-008"><a href="#step-008" style="font-weight:bold">Step 008</a></div>  

 Click Download Configuration Bundle and save the .iso file to your desktop.  

<a href="images/module09_008.png"><img src="images/module09_008.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-009"><a href="#step-009" style="font-weight:bold">Step 009</a></div>  

Click Done to complete the Deploy Virtual Appliance wizard.

<a href="images/module09_009.png"><img src="images/module09_009.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-010"><a href="#step-010" style="font-weight:bold">Step 010</a></div>  

Extract the contents of the .iso file.  

<a href="images/module09_010.png"><img src="images/module09_010.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-011"><a href="#step-011" style="font-weight:bold">Step 011</a></div>  

Open a session to the Tetration Edge appliance.  

<a href="images/module09_011.png"><img src="images/module09_011.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-012"><a href="#step-012" style="font-weight:bold">Step 012</a></div>  

Copy the extracted files from the .iso to the Tetration Edge appliance. You can drag and drop the files on the browser window to accomplish this.  

<a href="images/module09_012.png"><img src="images/module09_012.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-013"><a href="#step-013" style="font-weight:bold">Step 013</a></div>  

Enter the command `ls -l` and ensure all of the files from the .iso were copied over.

<a href="images/module09_013.png"><img src="images/module09_013.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-014"><a href="#step-014" style="font-weight:bold">Step 014</a></div>  

Reboot the appliance by issuing the `reboot` command.

<a href="images/module09_014.png"><img src="images/module09_014.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-015"><a href="#step-015" style="font-weight:bold">Step 015</a></div>  

Extract the provided certificate data to your desktop.  

<a href="images/module09_015.png"><img src="images/module09_015.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-016"><a href="#step-016" style="font-weight:bold">Step 016</a></div>  

Open a command prompt and change directory into the folder where the certificate data was extracted.  Enter the following command, substituting the correct IP address for the Tetration Edge appliance for 10.0.1.164.  

`openssl rsa -in tet-edge.hol.local_10.0.1.164.key -out openISE.key`

Enter a passphrase that you will remember.  

<a href="images/module09_016.png"><img src="images/module09_016.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-017"><a href="#step-017" style="font-weight:bold">Step 017</a></div>  

Open the certificates and key file in a text editor.  

<a href="images/module09_017.png"><img src="images/module09_017.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-018"><a href="#step-018" style="font-weight:bold">Step 018</a></div>  

Navigate to Connectors and select ISE.  

<a href="images/module09_018.png"><img src="images/module09_018.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-019"><a href="#step-019" style="font-weight:bold">Step 019</a></div>  

Click on Add Instance Config.  

<a href="images/module09_019.png"><img src="images/module09_019.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-020"><a href="#step-020" style="font-weight:bold">Step 020</a></div>  

Paste the contents of file `tet-edge.hol.local_10.0.1.164.cer` to the ISE Client Certificate.

<a href="images/module09_020.png"><img src="images/module09_020.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-021"><a href="#step-021" style="font-weight:bold">Step 021</a></div>  

Paste the contents of the openISE.key file to the ISE Client Key.

<a href="images/module09_021.png"><img src="images/module09_021.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-022"><a href="#step-022" style="font-weight:bold">Step 022</a></div>  

Paste the contents of the file `isev-small-2-4.hol.local_cer` to the ISE Server CA Certificate.  

<a href="images/module09_022.png"><img src="images/module09_022.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-023"><a href="#step-023" style="font-weight:bold">Step 023</a></div>  

Set the ISE Hostname to `isev-small-2-4.hol.local` and the ISE Node Name to `isev-small-2-4`. Then click Verify & Save configs.

<a href="images/module09_023.png"><img src="images/module09_023.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-024"><a href="#step-024" style="font-weight:bold">Step 024</a></div>  

You should receive the message "ISE configurations successfully applied"


<a href="images/module09_024.png"><img src="images/module09_024.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-025"><a href="#step-025" style="font-weight:bold">Step 025</a></div>  

Open a session to ISE and navigate to Administration > PxGrid Services > Web Clients.

<a href="images/module09_025.png"><img src="images/module09_025.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-026"><a href="#step-026" style="font-weight:bold">Step 026</a></div>  

Click on Refresh to view the new certificate that was assigned to the Tetration Edge appliance.

<a href="images/module09_026.png"><img src="images/module09_026.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-027"><a href="#step-027" style="font-weight:bold">Step 027</a></div>

Navigate back to Connectors and select the ISE connector.  Click on the LDAP tab.  In addition to ISE attributes,  we can also bring in LDAP attributes from Active Directory which will be populated into Tetration as annotations.  

<a href="images/module09_027.png"><img src="images/module09_027.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-028"><a href="#step-028" style="font-weight:bold">Step 028</a></div>  

Enter the LDAP configuration parameters as shown in the image. However, you must substitute the LDAP Server IP address with your Active Directory server IP address.

<a href="images/module09_028.png"><img src="images/module09_028.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-029"><a href="#step-029" style="font-weight:bold">Step 029</a></div>  

Enter the LDAP Base DN and Filter String as shown.  Then select Next.  


<a href="images/module09_029.png"><img src="images/module09_029.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-030"><a href="#step-030" style="font-weight:bold">Step 030</a></div>  

Enter the LDAP Username Attribute and the LDAP Attributes to Fetch as shown in the image.

<a href="images/module09_030.png"><img src="images/module09_030.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-031"><a href="#step-031" style="font-weight:bold">Step 031</a></div>

Click Save & Apply Configs.  

<a href="images/module09_031.png"><img src="images/module09_031.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-032"><a href="#step-032" style="font-weight:bold">Step 032</a></div>  

Click on the Endpoint tab.  This displays the inactivity timeout for ISE endpoints.

<a href="images/module09_032.png"><img src="images/module09_032.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-033"><a href="#step-033" style="font-weight:bold">Step 033</a></div>  

Click the Log tab and select Start Log Configuration.

<a href="images/module09_033.png"><img src="images/module09_033.png" style="width:100%;height:100%;"></a>  



<div class="step" id="step-034"><a href="#step-034" style="font-weight:bold">Step 034</a></div>  

Enter the Logging Level of info,  then Verify & Save Configs.  

<a href="images/module09_034.png"><img src="images/module09_034.png" style="width:100%;height:100%;"></a>  

YOU HAVE COMPLETED THIS MODULE



| [Return to Table of Contents](https://tetration.guru/bootcamp/) | [Go to Top of the Page]() | [Continue to the Next Module]() |
