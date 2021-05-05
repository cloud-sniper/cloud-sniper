import boto3
import logging
import json
import sys
from dynamodb_functions import query_to_dynamo
from send_to_slack import message_to_slack

# SETUP LOGGING OPTIONS
logging.basicConfig(stream=sys.stdout)
log = logging.getLogger("open-security-groups-automation")
log.setLevel(logging.INFO)


def lambda_handler(event, context):
    # handler for lambda
    SKIP_USER = 'role/open'
    CREATOR = str((event['detail']['userIdentity']['arn']))
    if SKIP_USER not in CREATOR:
        log.info('New SG created by a human, running automation....')
        log.info("Event Recived: " + json.dumps(event, indent=2))

        checkQuadCero = checkCIDR(event)
        if checkQuadCero:
            ID = str((event['detail']['requestParameters']['groupId']))
            if query_to_dynamo(ID) == 'NoReported':
                try:
                    log.info('rebooking the sg rule....')
                    ec2 = boto3.client('ec2', region_name=event['region'])
                    sg = ec2.revoke_security_group_ingress(GroupId=checkQuadCero[0]['groupIdentifier'],IpProtocol=checkQuadCero[0]['ipProtocol'],CidrIp=checkQuadCero[0]['cidrIp'],FromPort=checkQuadCero[0]['fromPort'],ToPort=checkQuadCero[0]['toPort'])
                    log.info('allowing internal sg rule....')
                    sg_auth_1 = ec2.authorize_security_group_ingress(GroupId=checkQuadCero[0]['groupIdentifier'],IpProtocol=checkQuadCero[0]['ipProtocol'],CidrIp='10.0.0.8/8',FromPort=checkQuadCero[0]['fromPort'],ToPort=checkQuadCero[0]['toPort'])
                    sg_auth_2 = ec2.authorize_security_group_ingress(GroupId=checkQuadCero[0]['groupIdentifier'],IpProtocol=checkQuadCero[0]['ipProtocol'],CidrIp='172.16.0.0/12',FromPort=checkQuadCero[0]['fromPort'],ToPort=checkQuadCero[0]['toPort'])
                    log.info("Sending Violation for:"
                             + str(json.dumps(checkQuadCero, indent=2)))
                    message_to_slack(event, context, checkQuadCero)
                except KeyError:
                    log.error('something fails')
    else:
        log.info('this action is not performed by a human')
        log.info(json.dumps(event, indent=2))



def checkCIDR(event):
    checkQuadCero = []
    try:
        security_group_rules = (event['detail']['requestParameters']
                                ['ipPermissions']['items'])

    except KeyError:
        log.info('Security group rules not found in the event.')
        evaluation_status = True
        return evaluation_status, checkQuadCero

    if "groupId" in event['detail']["requestParameters"]:
        security_group_identifier = (event['detail']["requestParameters"]
                                     ["groupId"])
    elif "groupName" in event['detail']["requestParameters"]:
        security_group_identifier = (event['detail']["requestParameters"]
                                     ["groupName"])
    else:
        log.info('No VPC Security Group ID or Classic Security Group Name \
Found.')
    for rule in security_group_rules:
        checkQuadCero = ipv4_checks(security_group_identifier, rule,
                                    checkQuadCero)
        checkQuadCero = ipv6_checks(security_group_identifier, rule,
                                    checkQuadCero)
    return checkQuadCero

# check if quad0 exist
def ipv4_checks(security_group_identifier, rule, checkQuadCero):
    try:
        for ipRange in rule['ipRanges']['items']:
            if ipRange['cidrIp'] == '0.0.0.0/0':
                log.info('Violation - Contains IP/CIDR of 0.0.0.0/0')
                cidr_ip = ipRange["cidrIp"]
                create_violation_list(security_group_identifier, rule,
                                      cidr_ip, checkQuadCero)

    except KeyError:
        log.info('There is not any Items under ipRanges')

    return checkQuadCero


def ipv6_checks(security_group_identifier, rule, checkQuadCero):
    try:
        for ipv6Range in rule['ipv6Ranges']['items']:
            if ipv6Range['cidrIpv6'] == '::/0':
                log.info('Violation - Contains CIDR IPv6 equal to ::/0')
                cidr_ip = ipv6Range["cidrIpv6"]
                create_violation_list(security_group_identifier, rule,
                                      cidr_ip, checkQuadCero)

    except KeyError:
        log.warning('There is not any Items under ipv6Ranges')

    return checkQuadCero

# create list
def create_violation_list(security_group_identifier,
                          rule, cidr_ip, checkQuadCero):
    checkQuadCero.append({
        "groupIdentifier": security_group_identifier,
        "ipProtocol": rule["ipProtocol"],
        "toPort": rule["toPort"],
        "fromPort": rule["fromPort"],
        "cidrIp": cidr_ip
    })
    return checkQuadCero

