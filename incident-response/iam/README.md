![Cloud Sniper Logo](../../images/logo.png "Cloud Sniper")

---

## **Cloud Sniper IAM Stack**

The Cloud Sniper IAM Stack is a powerful tool designed to monitor and manage IAM users within your AWS environment. Here's how it works:

- **Monitoring Inactive Users**: This stack evaluates IAM users' activity over the last 90 days. It identifies users who have been inactive in the AWS Console, made no API calls, or have accounts that have never been used.

- **Integrating with ELK Stack**: The identified Indicators of Compromise (IOCs) are stored in an S3 bucket and automatically consumed by the ELK stack for further analysis.

- **Alerting Mechanism**: When Cloud Sniper detects inactive users, it generates a Slack alert providing detailed information about the inactive users per account.

- **Future Enhancements**: In the upcoming release, the stack will include an automated user deletion feature to streamline IAM management further.

This stack is designed to be versatile, supporting multi-account and multi-region deployments in a hub-spoke format, ensuring comprehensive coverage across your AWS infrastructure.
