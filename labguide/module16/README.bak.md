# Cisco Tetration - Hands-On Lab
  
## Module16: Policy Creation - User-Based Policy

---


This diagram depicts the flow of traffic that will be used during the lab that has you use the general "Employee" machine outside of the ASAv firewall in your lab-simulated "Internet" to VPN into the organization and gain access via user-identification based policy which relies on ISE authenticating to Windows Active Directory and mapping the AD Security Group (AD-SG) to the ISE TrustSec Security Group (TrustSec-SG). Upon successful authentication and mapping of an AD-SG to an ISE TrustSec-SG, a SGT or Security Group Tag will be assigned, which is a numerical value. This SGT is what will be used by Tetration in creating policy to allow certain users access to certain defined resources. Whenever a user gets both authenticated (ID verification) and authorized (permissions granted via group mapping) by ISE to a SGT, ISE will update its ["pxGrid" or "Platform Group Exchange Grid"](https://www.cisco.com/c/en/us/products/security/pxgrid.html){:target="_blank"} and those subscribed to that grid -which in this case is Tetration- will get an updated list of Users, their SGTs, and their IP Addresses, among a slew of other information. Tetration will then use the IP addresses of these hosts to update various workload firewall rules where enforcement is in place. 

In this lab diagram, Employees get standard access to the app front-ends and no more - essentially what everyone else gets. 

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/diagrams/images/diagrams_011.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/diagrams/images/diagrams_011.png" style="width:100%;height:100%;"></a>  
  

In this lab diagram, SysAdmins not only get standard access to the app front-ends, but they also gain RDP and/or SSH access to each app's frontend workload as well as the backend databases, so that they can properly perform necessary administration. 

<a href="https://onstakinc.github.io/cisco-tetration-hol/labguide/diagrams/images/diagrams_012.png"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/diagrams/images/diagrams_012.png" style="width:100%;height:100%;"></a>  



---

<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/16_policy_creation_user_based_policy.mp4" style="font-weight:bold" title="Policy Analysis - nopCommerce Policies"><img src="https://onstakinc.github.io/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> Click here to view a video of the tasks necessary to configure dynamic user-based policy.</a>

---

### Steps for this Module  
  

--- 


| [Return to Table of Contents](https://onstakinc.github.io/cisco-tetration-hol/labguide/) | [Go to Top of the Page](https://onstakinc.github.io/cisco-tetration-hol/labguide/module16/) | [Continue to the Next Module](https://onstakinc.github.io/cisco-tetration-hol/labguide/module17/) |