![alt text](../../images/logo.png "Cloud Sniper")
<br> </br>
## *Cloud Sniper Threat Intelligence stack*

***Cloud Sniper*** receives threat intelligence feeds and will start blocking attackers in the VPCs of the affected instances. When processing findings related to C2 activity, ***Cloud Sniper*** will generate a topic that will call the analytics function for beaconing detection.

The corresponding Slack alert will be triggered with attacker's information and context of the cloud resources involved in that attack. The IOCs will be stored in S3 and then automatically consumed by the ELK stack.

The stack is designed to be applied multi-account and multi-region in hub-spoke format.
