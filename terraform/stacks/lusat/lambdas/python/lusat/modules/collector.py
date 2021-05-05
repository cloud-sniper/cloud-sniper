import sys
import logging
from datetime import datetime
from .setup import put_to_s3
from .iam_aws import AssumedRoleSession
from .analizer import analizer_expose_sg, analizer_launch_days, security_groupUSE, ami_informationcreationDays, ami_informationOWNER, ami_informationNAME, vpc_informationLog, lb_informationLog, lb_informationLogV2

# SETUP LOGGING OPTIONS
logging.basicConfig(format="%(asctime)s %(message)s", stream=sys.stdout)
log = logging.getLogger("cloud-lusat-inventory-collector")
log.setLevel(logging.INFO)

def ENICollector(args):
    print("starting")
    try:
        account_id = args.get('account_id')
        role_spoke = args.get('role_assume')
        session = AssumedRoleSession(account_id, role_spoke)
        account_alias = session.client('iam').list_account_aliases()[
            'AccountAliases'][0]

        aws_regions = session.client('ec2').describe_regions()
        for region in aws_regions['Regions']:
            aws_region_name = region['RegionName']

            client = session.client('ec2', region_name=aws_region_name)
            log.info("getting ENI interfaces")
            for data in client.describe_network_interfaces()['NetworkInterfaces']:
                try:
                    data = {
                        "@timestamp": str(datetime.now()),
                        "cloud.account.id": account_id,
                        "cloud.region": aws_region_name,
                        "labels": "inventory",
                        "eni.ip.private": data.get('PrivateIpAddress'),
                        "eni.dns.private": data.get('PrivateDnsName'),
                        "eni.id": data.get('NetworkInterfaceId'),
                        "eni.owner.id": data.get('OwnerId'),
                        "eni.description": data.get('Description'),
                        "eni.vpc.id": data.get('VpcId'),
                        "eni.mac_address": data.get('MacAddress'),
                        "eni.type": data.get('InterfaceType'),
                        "eni.attachments": data.get('Attachment'),
                        "eni.status": data.get('Status'),
                        "eni.subnet.id": data.get('SubnetId'),
                        "eni.ip.addresses": data.get('PrivateIpAddresses'),
                        "tags": data.get('TagSet'),
                        "inventory.type": 'ENI',
                        "cloud.account.name": account_alias
                    }
                    log.info("sending to s3")
                    put_to_s3(data)
                except Exception as e:
                    log.info("something goes wrong: "+str(e))
            log.info("done ENI")
    except Exception as e:
        print(e)
        log.info("something goes wrong: "+str(e))


def VPCCollector(args):
    try:
        account_id = args.get('account_id')
        role_spoke = args.get('role_assume')
        session = AssumedRoleSession(account_id, role_spoke)
        account_alias = session.client('iam').list_account_aliases()[
            'AccountAliases'][0]

        aws_regions = session.client('ec2').describe_regions()
        for region in aws_regions['Regions']:
            aws_region_name = region['RegionName']

            client = session.client('ec2', region_name=aws_region_name)
            log.info("getting VPC interfaces")
            for data in client.describe_vpcs()['Vpcs']:
                try:
                    vpcid = data.get('VpcId')
                    data = {
                        "@timestamp": str(datetime.now()),
                        "vpc.dhcp.id": data.get('DhcpOptionsId'),
                        "vpc.id": data.get('VpcId'),
                        "vpc.owner.id": data.get('OwnerId'),
                        "vpc.state": data.get('State'),
                        "vpn.associations": data.get('CidrBlockAssociationSet'),
                        "tags": data.get('Tags'),
                        "inventory.type": 'VPC',
                        "labels": "inventory",
                        "cloud.account.id": account_id,
                        "cloud.region": aws_region_name,
                        "cloud.account.name": account_alias,
                        "vpc.flowlogs": str(vpc_informationLog(vpcid, aws_region_name, session)),
                    }
                    log.info("sending to ELK")
                    put_to_s3(data)
                except Exception as e:
                    log.info("something goes wrong: "+str(e))
            log.info("done VPC")
    except Exception as e:
        log.info("something goes wrong: "+str(e))


def SGCollector(args):
    try:
        account_id = args.get('account_id')
        role_spoke = args.get('role_assume')
        session = AssumedRoleSession(account_id, role_spoke)
        account_alias = session.client('iam').list_account_aliases()[
            'AccountAliases'][0]

        aws_regions = session.client('ec2').describe_regions()
        for region in aws_regions['Regions']:
            aws_region_name = region['RegionName']

            client = session.client('ec2', region_name=aws_region_name)
            log.info("getting security groups")
            for data in client.describe_security_groups()['SecurityGroups']:
                try:
                    data = {
                        "@timestamp": str(datetime.now()),
                        "security_group.ip_permission": data['IpPermissions'],
                        "security_group.name": data['GroupName'],
                        "security_group.description": data['Description'],
                        "security_group.id": data['GroupId'],
                        "security_group.owner.id": data['OwnerId'],
                        "security_group.vpc.id": data.get('VpcId'),
                        "tags": data.get('Tags'),
                        "inventory.type": 'SG',
                        "labels": "inventory",
                        "cloud.account.id": account_id,
                        "cloud.region": aws_region_name,
                        "cloud.account.name": account_alias,
                        "security_group.analyzer.expose": analizer_expose_sg(data['IpPermissions']),
                        "security_group.status.use": security_groupUSE(data['GroupId'], aws_region_name, session)
                    }
                    if data['security_group.status.use'] == 0:
                        log.info("here you can send to sqs")
                    log.info("sending to ELK")
                    put_to_s3(data)
                except Exception as e:
                    log.info("something goes wrong: "+str(e))
            log.info("done SG")
    except Exception as e:
        log.info("something goes wrong: "+str(e))


def EC2Collector(args):
    try:
        account_id = args.get('account_id')
        role_spoke = args.get('role_assume')
        session = AssumedRoleSession(account_id, role_spoke)
        account_alias = session.client('iam').list_account_aliases()[
            'AccountAliases'][0]

        aws_regions = session.client('ec2').describe_regions()
        for region in aws_regions['Regions']:
            aws_region_name = region['RegionName']

            client = session.client('ec2', region_name=aws_region_name)
            log.info("getting EC2 instances")
            for data in client.describe_instances()['Reservations']:
                try:
                    for instances in data['Instances']:
                        instances = {
                            "labels": "inventory",
                            "@timestamp": str(datetime.now()),
                            "instance.id": instances['InstanceId'],
                            "cloud.account.id": account_id,
                            "cloud.region": aws_region_name,
                            "instance.state": instances.get('State'),
                            "instance.running.days": str(analizer_launch_days(instances['LaunchTime'])),
                            "instance.launch_time": str(instances['LaunchTime'].replace(tzinfo=None)),
                            "instance.architecture": instances['Architecture'],
                            "instance.subnet": instances.get('SubnetId'),
                            "instance.dns.public": instances.get('PublicDnsName'),
                            "instance.dns.private": instances.get('PrivateDnsName'),
                            "instance.type": instances.get('InstanceType'),
                            "instance.image.id": instances.get('ImageId'),
                            "instance.image.owner.id": ami_informationOWNER(instances.get('ImageId'), aws_region_name, session),
                            "instance.image.name": ami_informationNAME(instances.get('ImageId'), aws_region_name, session),
                            "instance.image.create.days": str(ami_informationcreationDays(instances.get('ImageId'), aws_region_name, session)),
                            "inventory.type": 'EC2',
                            "tags": instances.get('Tags'),
                            "instance.security_group": instances.get('SecurityGroups'),
                            "instance.role": instances.get('IamInstanceProfile'),
                            "instance.ip.private": instances.get('PrivateIpAddress'),
                            "instance.ip.public": instances.get('PublicIpAddress'),
                            "instance.vpc": instances.get('VpcId'),
                            "account_id": account_id,
                            "cloud.account.name": account_alias,
                            "instance.key": instances.get('KeyName'),
                        }
                        log.info("sending to s3")
                        put_to_s3(instances)
                except Exception as e:
                    log.error("something goes wrong: "+str(e))
                log.info("done EC2")
    except Exception as e:
        log.error("something goes wrong: "+str(e))


def LBCollector(args):
    try:
        account_id = args.get('account_id')
        role_spoke = args.get('role_assume')
        session = AssumedRoleSession(account_id, role_spoke)
        account_alias = session.client('iam').list_account_aliases()[
            'AccountAliases'][0]

        aws_regions = session.client('ec2').describe_regions()
        for region in aws_regions['Regions']:
            aws_region_name = region['RegionName']
            client = session.client('elb', region_name=aws_region_name)
            log.info("getting elastic load balancers")
            for data in client.describe_load_balancers()['LoadBalancerDescriptions']:
                print(data)
                try:
                    lbname = data.get('LoadBalancerName')
                    data = {
                        "@timestamp": str(datetime.now()),
                        "loadbalancer.name": data.get('LoadBalancerName'),
                        "loadbalancer.dns": data.get('DNSName'),
                        "loadbalancer.vpc": data.get('VPCId'),
                        "loadbalancer.security_group": data.get('SecurityGroups'),
                        "inventory.type": 'LB',
                        "labels": "inventory",
                        "cloud.account.id": account_id,
                        "cloud.region": aws_region_name,
                        "cloud.account.name": account_alias,
                        "loadbalancer.access_log": str(lb_informationLog(lbname, aws_region_name, session)),
                    }
                    log.info("sending to ELK")
                    put_to_s3(data)
                except Exception as e:
                    log.info("something goes wrong: "+str(e))
            client = session.client('elbv2', region_name=aws_region_name)
            log.info("getting application load balancers")
            for data in client.describe_load_balancers()['LoadBalancers']:
                try:
                    lbarn = data.get('LoadBalancerArn')
                    data = {
                        "@timestamp": str(datetime.now()),
                        "loadbalancer.name": data.get('LoadBalancerName'),
                        "loadbalancer.arn": data.get('LoadBalancerArn'),
                        "loadbalancer.dns": data.get('DNSName'),
                        "loadbalancer.vpc": data.get('VPCId'),
                        "loadbalancer.security_group": data.get('SecurityGroups'),
                        "loadbalancer.scheme": data.get('Scheme'),
                        "inventory.type": 'LB',
                        "labels": "inventory",
                        "cloud.account.id": account_id,
                        "cloud.region": aws_region_name,
                        "cloud.account.name": account_alias,
                        "loadbalancer.access_log": str(lb_informationLogV2(lbarn, aws_region_name, session)),
                    }
                    log.info("sending to ELK")
                    put_to_s3(data)
                except Exception as e:
                    log.info("something goes wrong: "+str(e))
            log.info("done LoadBalancers")
        log.info("done "+aws_region_name)
    except Exception as e:
        log.info("something goes wrong: "+str(e))
