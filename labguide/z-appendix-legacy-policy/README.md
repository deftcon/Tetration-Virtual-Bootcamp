# Cisco Tetration - Hands-On Lab
  
## Appendix: Legacy Alternative Policy
  
Recent advancements in algorithmic efficencies have allowed the type of policy that has been shown throughout this lab. That which was computationally prohibitive prior to recently now allows such policy to make policy creation and ongoing operationalization much simpler. 

A simple example of this algorithmic efficency can be denoted in the deceptively simple ability to use the boolean NOT operator. Take for instance the following example where someone wishes to categorize the big bad internet - in all of it's hugeness. The current routing table (as of this writing) is [nearing half a million prefixes](https://www.cidr-report.org/as2.0/) and can be viewed by going to the [Looking Glass Project](http://www.us.ntt.net/support/looking-glass/).

Previously, if you wished to represent or categorize this in Tetration, you could use the Root Scope which essentially equated to your Tenant VRF ID, and represented the whole of all Internet prefixes, however also represented your own internal corporate prefixes, as well, that (generally speaking) fell into the [RFC1918 category](https://tools.ietf.org/html/rfc1918). While this worked fine from the perspective of the policy it generated for the end host workload built-in firewalls, it certainly didn't make policy to terribly easy to read. 

While it would seem that the type of policy we use today should have been perfectly fine to use then -that such as perhaps a Filter we might call "Internet" that consisted of a query such of `'Scope=Root' AND NOT 'RFC1918'` (where of course RFC1918 was either another Filter or the enumerated RFC1918 space (10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16). The problem was, doing this would cause an unnecessary burden on both the computational calculation as well as the overwhelming amount of IP prefixes that would need to be programed into endpoint workload firewalls. 

We could compensate for this with creative filter named apropriately, however it did mean we usually also had to use some creative policy that provided a workaround. Today due to the aforementioned efficiencies, we no longer have those impositions, and filters such as the previous example of `'Scope=Root' AND NOT 'RFC1918'` are perfectly acceptable, and indeed caused us to go back and re-record all of our policy videos to show this preferred method of policy creation. 

That being said, we thought there would innevitably be some older legacy versions of Tetration deployed in various on-prem locations, and felt that for that reason, it warranted this section that would show video highlighting those older, and sometimes merely alternative ways of creating policy and going into enforcement. While we don't have any plans to enumerate any of these videos into detailed step-by-step screenshots and corresponding instructions, we nevertheless provide them here for your benefit, or perhaps simple amusement. 

At any rate, enjoy. 


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/legacy/08_global_services.mp4" style="font-weight:bold"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> Global Services</a>


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/legacy/09_common_pol_ADM_begin.mp4" style="font-weight:bold"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> Common Policy ADM</a>


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/legacy/10_common_pol_ADM_clusters.mp4" style="font-weight:bold"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> Common Policy Clusters</a>


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/legacy/11_common_policy_tuning.mp4" style="font-weight:bold"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> Common Policy Tuning</a>


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/legacy/12_nopcommerce_adm_clusters.mp4" style="font-weight:bold"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> nopCommerce ADM & Clusters</a>


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/legacy/13_nopcommerce_policy_tuning.mp4" style="font-weight:bold"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> nopCommerce Policy Tuning</a>


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/legacy/14_opencart_adm_clusters.mp4" style="font-weight:bold"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> OpenCart ADM & Clusters</a>


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/legacy/15_opencart_policy_tuning.mp4" style="font-weight:bold"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> OpenCart Policy Tuning</a>


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/legacy/16_nopcommerce_policy_analysis.mp4" style="font-weight:bold"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> nopCommerce Policy Analysis</a>


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/legacy/17_opencart_policy_analysis.mp4" style="font-weight:bold"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> OpenCart Policy Analysis</a>


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/legacy/18_common_policy_analysis.mp4" style="font-weight:bold"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> Common Policy Analysis</a>


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/legacy/19_global_policy_analysis.mp4" style="font-weight:bold"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> Global Policy Analysis</a>


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/legacy/20_pre_enforcement_checks.mp4" style="font-weight:bold"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> Pre-Enforcement Checks</a>


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/legacy/21_enforcement_nopcommerce.mp4" style="font-weight:bold"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> nopCommerce Enforcement (includes Global and Common enforcement)</a>


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/legacy/22_enforcement_opencart.mp4" style="font-weight:bold"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> OpenCart Enforcement</a>


<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/legacy/23_enforcement_tuning.mp4" style="font-weight:bold"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> Enforcement Policy Tuning</a>

<a href="https://cisco-tetration-hol-content.s3.amazonaws.com/videos/legacy/24_aws_lambda.mp4" style="font-weight:bold" title="AWS Lambda"><img src="https://tetration.guru/cisco-tetration-hol/labguide/diagrams/images/video_icon_mini.png"> AWS Lambda when run from within a VPC</a>


| [Return to Table of Contents](https://tetration.guru/cisco-tetration-hol/labguide/) | [Go to Top of the Page](https://tetration.guru/cisco-tetration-hol/labguide/module27/) | 