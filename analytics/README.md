![alt text](../images/logo.png "Cloud Sniper")
<br> </br>
## *Cloud Security Operations*

### *Cloud Sniper Analytics module*

***Cloud Sniper*** introduces an analytics module to analyze data, metrics and telemetry generated on the cloud. This first version analyzes VPC flows to detect beaconing (call home) patterns.

Ideally, the module will be deployed with terra, but currently it is to be done manually.

VPC-Flowlogs should be stored on S3 and the beaconing module looks for beaconing patterns in those flows. To configure it, update:
* aws_credentials.txt: include your aws credentials to be used by boto3 library
* environment.env: set the s3 paths where to read the VPC flows from and where to write the generated report

Create the docker image on an EC2 instance (`sh docker_build.sh`) and run the container (`docker run cloudsniper/beaconer`). A pdf report is stored in the configured S3 path.
