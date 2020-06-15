# Cisco Tetration - Hands-On Lab
  
## Module08: Ingest Appliance - AWS VPC Flow Logs and ASA NAT Stitching

---


This diagram depicts the flow of traffic used by various devices to utimately ingest information into the Tetration cluster. The Tetration Edge appliance is used to subscribe to the pxGrid from ISE for SGT and user-based policy. The Tetration Data Ingest appliance is used to collect NetFlow v9 info from the ASAv which is useful in stitching together flows of traffic from outside the firewall all the way through being NAT'd by that ASAv and then traversing to the internal corporate network and making their way to app frontends. This same Tetration Data Ingest appliance is used to collect Flow Logs from an AWS VPC via an S3 bucket. This is useful for collecting traffic from any workload that may not have (or be able to have) a Tetration agent installed on it. 

<a href="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/diagrams_013.png"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/diagrams_013.png" style="width:100%;height:100%;"></a>  
  


---

<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/08a_comissioning_tetration_edge_appliance.mp4" style="font-weight:bold" title="Data Ingest Appliance"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> Click here to view a video showing the necessary tasks to comission the Tetration Data Ingest appliance to prepare for integration with ASA and AWS.</a>


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/08b_tetration_edge_aws_flow_logs.mp4" style="font-weight:bold" title="AWS VPC Flow Logs"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> Click here to view a video showing the necessary tasks to configure AWS VPC Flow Logs to be sent to the Tetration Data Ingest appliance and allow Tetration to see traffic in an AWS VPC other than that which has or speaks to a workload with a Tetration Agent.</a>


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/08c_data_ingest_asav.mp4" style="font-weight:bold" title="ASAv NAT Flow Stiching"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> Click here to view a video showing the necessary tasks to configure the ASAv to send NetFlow to the Tetration Data Ingest appliance and allow Tetration stich NAT'd flows together (note the appliance IPs in the video may differ based on env taken from).</a>

---

### Steps for this Module  

---

| [Return to Table of Contents](https://tetration.guru/cisco-tetration-hol/labguide/) | [Go to Top of the Page](https://tetration.guru/cisco-tetration-hol/labguide/module08/) | [Continue to the Next Module](https://tetration.guru/cisco-tetration-hol/labguide/module09/) |