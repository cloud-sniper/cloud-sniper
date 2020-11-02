![alt text](../../images/logo.png "Cloud Sniper")
<br> </br>
## *Cloud Sniper Dashboard stack*

***Cloud Sniper*** introduces the ability to monitor security in cloud environments by adding telemetry, metrics and alerts based on the information collected.

The dashboard is a Kibana object that can be exported very easily. If you already have an ELK stack, just import the *dashboard.ndjson* object located in the *dashboard/logstash* folder to start viewing your findings.

# Getting Started

![alt text](../../images/gif/dashboard.gif)

## How works?

This stack includes everything you need to run the ELK on an EC2 instance. *Open Distro* distribution is used.

## Requeriments

1. Repo cloned locally
2. AWS credentials/access key
3. terraform (https://www.terraform.io/)

## Deployment

To deploy the Cloud Sniper dashboard stack, you should run:


### 1
clone & update your repo with the current master ```git clone https://github.com/cloud-sniper/cloud-sniper.git // git pull```
### 2
go to the dashboard stack ```cd cloud-sniper/dashboard```
### 3 
set the environment variables corresponding to the account into ```variables.tf``` like:  
```
variable ssh_key_name {
  description = "key pair name to be used in the EC2 instance"
  default = "mysecretkey.pem'
}
```
### 4
Create/update the main.tf file with your credentials or use your role as appropriate:
```
   provider "aws" {
    region                    = "region"
    shared_credentials_file   = "/your-home/.aws/credentials"
    profile                   = "your-profile"
   }
```
### 5
Initialized your terraform ```
terraform init```
### 6
make a terraform plan and export to a file to store the state: ```terrafom plan --out dashboard.tfplan```
### 7
apply your changes into your aws account ```terraform apply dashboard.tfplan```
### 8
Read the notes and browser your kinana URL.

**Notes:**
1. Access to EC2 is restricted to your current public IP
2. When initializing the EC2 instance, the file /dashboard/logstash/logstash.conf' must be copied manually into '/etc/logstash/conf.d/logstash.conf'