# *Cloud Sniper*
## *How it works*

### Cloud Sniper - AWS native version

***Cloud Sniper*** receives cloud-based or third-party feeds to take remediation actions in the cloud. Currently, the AWS native version, gets feeds from GuardDuty, a continuous security monitoring service that detects threats based on *CloudTrial Logs/VPC Flow Logs/DNS Logs artifacts*.

The *GuardDuty* security analysis is based on the *Shared Responsibility Model* of cloud environments, in which the provider has access to hidden information for the security analyst (such as DNS logs). *GuardDuty* provides findings, categorized in a pseudo *MITRE's TTP's* tagging.

When *GuardDuty* detects an incident, ***Cloud Sniper*** automatically analyzes what actions are available to mitigate and remediate that threat. If layer 7/4/3 attacks are taking place, it blocks the corresponding sources, both in the WAF and in the Network Access Control Lists of the affected instances.

A knowledge database will be created to store the *IOCs* that affect the cloud environments and will build its own *Threat Intelligence* feeds to use in the future.

The ***Cloud Sniper Analytics*** module allows to analyze the flow logs of the entire network where an affected instance is deployed and obtain analytics on traffic behavior, looking for *Command and Control (C2)* activity.

### Installation (for AWS)

    Cloud Sniper uses Terraform to automatically deploy the entire infrastructure in the cloud. The core is programmed in python, so it can be extended according to the needs of each vSOC.
    
    You must have:

    1.  AWS cli  installed
    2.  A programmatic access key
    3.  AWS local profile configured
    4.  Terraform client installed

    To deploy Cloud Sniper you must run:

    1.  ~$ git clone https://github.com/cloud-sniper/cloud-sniper.git
    2.  ~$ cd cloud-sniper
    3.  Set the environment variables corresponding to the account in the variables.tf file
    4.  Create main.tf file

        provider "aws" {
            region                    = "region"
            shared_credentials_file   = "/your-home/.aws/credentials"
            profile                   = "your-profile"
        }

    5.  ~/cloud-sniper$ terraform init
    6.  ~/cloud-sniper$ terraform plan
    7.  ~/cloud-sniper$ terraform apply [yes]


### AWS artifacts integration:

    The platform is integrated with the following cloud technologies:

    1.  GuardDuty findings
    2.  SQS
    3.  CloudWatch
    4.  WAF
    5.  EC2 
    6.  VPC Flow Logs
    7.  DynamoDB
    8.  IAM
    9.  S3
    10. Lambda
    11. Kinesis Firehose
