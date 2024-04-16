![Cloud Sniper](../../../images/logo.png "Cloud Sniper")

## *Cloud Sniper Threat Intelligence Stack*

**Cloud Sniper** is a robust threat intelligence system designed to bolster your cloud security posture. It actively receives threat intelligence feeds and swiftly takes action by blocking attackers within the VPCs of affected instances. Particularly adept at identifying Command and Control (C2) activity, **Cloud Sniper** generates actionable insights, triggering an analytics function for beaconing detection.

When an attack is detected, **Cloud Sniper** generates detailed Slack alerts, providing comprehensive information about the attacker and contextual details of the cloud resources involved. It ensures transparency and facilitates swift response by storing Indicators of Compromise (IOCs) in S3, seamlessly integrated with the ELK stack for further analysis.

This adaptable stack is architected for deployment across multiple accounts and regions, following a hub-spoke format for scalable and efficient security operations.
