![alt text](../../images/logo.png "Cloud Sniper")
<br> </br>
## *Cloud Sniper Dashboard stack*


***Cloud Sniper*** introduces the ability to monitor security in cloud environments by adding telemetry, providing metrics and alerts based on the information collected.

The dashboard is a Kibana object that can be exported very easily. If you already have an ELK stack, just import the *dashboard.ndjson* object located in the *dashboard/logstash* folder to start viewing your findings.

This stack includes everything you need to run the ELK on an EC2 instance. *Open Distro* distribution is used.

To deploy the Cloud Sniper dashboard stack, you should run:

1. ~$ git clone https://github.com/cloud-sniper/cloud-sniper.git
2. ~$ cd cloud-sniper/dashboard
3. Set the environment variables corresponding to the account in the variables.tf file
4. Create main.tf file with your credentials or use your role as appropriate
5. ~/cloud-sniper/dashboard$ terraform init
6. ~/cloud-sniper/dashboard$ terraform plan
7. ~/cloud-sniper/dashboard$ terraform apply [yes]

*Notes:*
1. Access to EC2 is restricted to your current public IP
2. When initializing the EC2 instance, the file /dashboard/logstash/logstash.conf' must be copied manually into '/etc/logstash/conf.d/logstash.conf'

<br> </br>
![alt text](../../images/gif/dashboard.gif)
