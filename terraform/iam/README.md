![alt text](../../images/logo.png "Cloud Sniper")
<br> </br>
## *Cloud Sniper IAM stack*

This stack evaluates whether there is an IAM user with no activity for the last 90 days. The function checks if active users have no activity both in AWS Console, API calls and accounts created that have never been used. The IOCs will be stored in S3 and then automatically consumed by the ELK stack.

If ***Cloud Sniper*** finds inactive users, it produces a slack alert with the detail of inactive users by account. In the next release the automatic deletion of users will be automated.

The stack is designed to be applied multi-account and multi-region in hub-spoke format.
