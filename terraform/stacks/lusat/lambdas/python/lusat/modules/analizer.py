import logging
from datetime import datetime, timezone
from botocore.exceptions import ClientError
import sys

# SETUP LOGGING OPTIONS
logging.basicConfig(format="%(asctime)s %(message)s", stream=sys.stdout)
log = logging.getLogger("cloud-lusat-inventory-analyzer")
log.setLevel(logging.INFO)

def analizer_expose_sg(data):
    log.info("starting the expose sg analyzer")
    sg_status = 'closed'
    full_access = "0.0.0.0/0"
    for permission in data:
        for ip in permission['IpRanges']:
            for _ in ip['CidrIp']:
                if ip['CidrIp'] == full_access:
                    sg_status = 'open'
    log.info("done sg analyzer")
    return sg_status


def analizer_launch_days(data):
    log.info("starting the launch days count analyzer")
    if data != '':
        diff_time = datetime.now(timezone.utc) - data
    else:
        diff_time = 'n/a'
    log.info("done count analyzer")
    return diff_time.days


def security_groupUSE(data, aws_region_name, session):
    try:
        eni_client = session.client('ec2', region_name=aws_region_name)
        eni_dict = eni_client.describe_network_interfaces()
        eni = 0
        for i in eni_dict['NetworkInterfaces']:
            try:
                for j in i['Groups']:
                    if data == j['GroupId']:
                        eni = 1
            except Exception as e:
                log.info("no sgs found into the EC2: " + str(e))

        # Security groups used by classic ELBs
        elb_client = session.client('elb', region_name=aws_region_name)
        elb_dict = elb_client.describe_load_balancers()
        elb = 0
        for i in elb_dict['LoadBalancerDescriptions']:
            try:
                for j in i['SecurityGroups']:
                    if data == j:
                        elb = 1
            except Exception as e:
                log.info("no sgs found into the ELB: " + str(e))

        # Security groups used by ALBs
        elb2_client = session.client('elbv2', region_name=aws_region_name)
        elb2_dict = elb2_client.describe_load_balancers()
        alb = 0
        for i in elb2_dict['LoadBalancers']:
            try:
                for j in i['SecurityGroups']:
                    if data == j:
                        alb = 1
            except Exception as e:
                log.info("no sgs found into the ALB: " + str(e))

        # Security groups used by RDS
        rds_client = session.client('rds', region_name=aws_region_name)
        rds_dict = rds_client.describe_db_instances()
        rds = 0
        for i in rds_dict['DBInstances']:
            try:
                for j in i['VpcSecurityGroups']:
                    if data == j['VpcSecurityGroupId']:
                        rds = 1
            except Exception as e:
                log.info("no sgs found into the RDS: " + str(e))

        security_group_status = (eni + elb + rds + alb)
        return security_group_status
    except ClientError:
        return 'error'


def ami_informationOWNER(data, aws_region_name, session):
    try:
        client = session.client('ec2', region_name=aws_region_name)
        response = client.describe_images(
            ImageIds=[data],
        )
        return response['Images'][0]['OwnerId']
    except Exception as e:
        log.info("something goes wrong: " + str(e))


def ami_informationNAME(data, aws_region_name, session):
    try:
        client = session.client('ec2', region_name=aws_region_name)
        response = client.describe_images(
            ImageIds=[data],
        )
        return response['Images'][0]['Name']
    except Exception as e:
        log.info("something goes wrong: " + str(e))


def ami_informationcreationDays(data, aws_region_name, session):
    try:
        client = session.client('ec2', region_name=aws_region_name)
        response = client.describe_images(
            ImageIds=[data],
        )
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        days_create = str(response['Images'][0]['CreationDate'])
        if days_create != '':
            convert_date = datetime.strptime(days_create, date_format)
            diff_time = datetime.now() - convert_date
        else:
            diff_time = 'n/a'
        return diff_time.days
    except Exception as e:
        log.info("something goes wrong: " + str(e))


def vpc_informationLog(data, aws_region_name, session):
    try:
        log.info("starting the flowlog analizer")
        client = session.client('ec2', region_name=aws_region_name)
        response = client.describe_flow_logs(
            Filters=[
                {
                    'Name': 'resource-id',
                    'Values': [data]
                }
            ]
        )
        for data in response['FlowLogs']:
            data = [{
                "traffic_type": data.get('TrafficType'),
                "log.destination": data.get('LogDestination'),
                "log.status": data.get('DeliverLogsStatus'),
                "id": data.get('FlowLogId')
            }]
            return data
        else:
            return 'noData'
    except ClientError as e:
        log.info("something goes wrong: " + str(e))
        return 'error'


def lb_informationLog(data, aws_region_name, session):
    try:
        log.info("starting the LB_LOG analizer")
        client = session.client('elb', region_name=aws_region_name)
        response = client.describe_load_balancer_attributes(
            LoadBalancerName=data)
        for data in response['LoadBalancerAttributes']:
            data = [{
                "log": data.get('AccessLog')
            }]
            return data
        else:
            return 'noData'
    except ClientError as e:
        log.info("something goes wrong: " + str(e))
        return 'error'


def lb_informationLogV2(data, aws_region_name, session):
    try:
        log.info("starting the LB_LOG analizer")
        client = session.client('elbv2', region_name=aws_region_name)
        response = client.describe_load_balancer_attributes(
            LoadBalancerArn=data)
        try:
            data = response['Attributes']
            return data
        except:
            return 'noData'
    except ClientError as e:
        log.info("something goes wrong: " + str(e))
        return 'error'
