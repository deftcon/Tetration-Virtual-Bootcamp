# Cisco Tetration - Hands-On Lab
  
## Module09: Edge Appliance - ISE

---



This diagram depicts the flow of traffic used by various devices to utimately ingest information into the Tetration cluster. The Tetration Edge appliance is used to subscribe to the pxGrid from ISE for SGT and user-based policy. The Tetration Data Ingest appliance is used to collect NetFlow v9 info from the ASAv which is useful in stitching together flows of traffic from outside the firewall all the way through being NAT'd by that ASAv and then traversing to the internal corporate network and making their way to app frontends. This same Tetration Data Ingest appliance is used to collect Flow Logs from an AWS VPC via an S3 bucket. This is useful for collecting traffic from any workload that may not have (or be able to have) a Tetration agent installed on it. 

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/diagrams/images/diagrams_013.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/diagrams/images/diagrams_013.png" style="width:100%;height:100%;"></a>  
  

---

<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/09a_comissioning_tetration_edge_appliance.mp4" style="font-weight:bold" title="Data Ingest Appliance and ASAv NAT Flow Stiching"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png">Click here to view a video showing the necessary tasks to comission the Tetration Edge appliance to prepare for integration with Cisco ISE (note this is similar to data ingest with nuanced differences).</a>

<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/09b_ise_integration.mp4" style="font-weight:bold" title="Data Ingest Appliance and ASAv NAT Flow Stiching"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> Click here to view a video showing the necessary tasks to integrate Cisco ISE with Tetration to prepare to support user-based policy in Module 16.</a>


### Steps for this Module  


---

| [Return to Table of Contents](https://onstakinc.github.io/cisco-tetration-hol/labguide/) | [Go to Top of the Page](https://onstakinc.github.io/cisco-tetration-hol/labguide/module09/) | [Continue to the Next Module](https://onstakinc.github.io/cisco-tetration-hol/labguide/module10/) |