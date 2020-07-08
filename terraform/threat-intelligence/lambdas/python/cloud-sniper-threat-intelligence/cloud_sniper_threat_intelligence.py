import boto3
import json
import datetime
import logging
import os
import ipaddress
import requests

log = logging.getLogger()
log.setLevel(logging.INFO)

QUEUE_URL = os.environ['SQS_QUEUE_CLOUD_SNIPER']
DYNAMO_TABLE = os.environ['DYNAMO_TABLE_CLOUD_SNIPER']
WEBHOOK_URL = os.environ['WEBHOOK_URL_IR']
HUB_ACCOUNT_ID = os.environ['HUB_ACCOUNT_ID_CLOUD_SNIPER']
ROLE_SPOKE = os.environ['ROLE_SPOKE_CLOUD_SNIPER']
BUCKET_NAME = os.environ['BUCKET_NAME']
IOCS_PATH = os.environ['IOCS_PATH']
NOW = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

message = []
json_a = []

# hub account
s = boto3.session.Session(region_name=os.environ['AWS_REGION'])
ec2 = s.client('ec2')
sqs = s.client('sqs')
iam = s.client('iam')
r_ec2 = s.resource('ec2')
dynamodb = s.resource('dynamodb')

# spoke account
sts_connection = boto3.client('sts')

networkConnectionAction = [
    "UnauthorizedAccess:EC2/SSHBruteForce",
]

portProbeAction = [
    "Recon:EC2/PortProbeUnprotectedPort",
]

instanceDetails = [
    "UnauthorizedAccess:EC2/TorIPCaller",
]


def read_sqs():
    log.info("Processing queue")

    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=10,
        MessageAttributeNames=[
            'All'
        ],
    )

    if 'Messages' in response:
        return response['Messages']
    else:
        log.info("There is no new message in the queue")
        return


def search_ioc():
    log.info("Searching for IOC ...")

    global json_a

    for b in message:
        body = b['Body']

        data = json.loads(body)

        try:
            flag = 0

            try:
                for dt in networkConnectionAction:
                    if data["detail"]["type"] == dt:
                        flag = 1
                        break
                for dt in portProbeAction:
                    if data["detail"]["type"] == dt:
                        flag = 2
                        break

            except Exception as e:

                for e in instanceDetails:
                    if data["type"] == e:
                        flag = 3
                        break

            if flag == 1:
                ioc = []

                src_ip = (json.dumps(
                    data["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"][
                        "ipAddressV4"])).strip('"')
                direction = data["detail"]["service"]["action"]["networkConnectionAction"]["connectionDirection"]

                if ipaddress.ip_address(src_ip).is_private is False and direction == "INBOUND":

                    account_id = data["detail"]["accountId"]
                    region = data["region"]
                    subnet_id = data["detail"]["resource"]["instanceDetails"]["networkInterfaces"][0]["subnetId"]
                    instance_id = data["detail"]["resource"]["instanceDetails"]["instanceId"]
                    ttp = data["detail"]["type"]
                    asn = \
                        data["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"][
                            "organization"][
                            "asn"]
                    asn_org = (
                        data["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"][
                            "organization"][
                            "asnOrg"]).replace(",", " ")
                    isp = (
                        data["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"][
                            "organization"][
                            "isp"]).replace(",", " ")
                    org = (
                        data["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"][
                            "organization"][
                            "org"]).replace(",", " ")
                    country = \
                        data["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"]["country"][
                            "countryName"]
                    city = (data["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"]["city"][
                        "cityName"]).replace(",", " ")
                    nacl_id = get_netacl_id(subnet_id, account_id)
                    hits = str(data["detail"]["service"]["count"])
                    vpc_id = data["detail"]["resource"]["instanceDetails"]["networkInterfaces"][0]["vpcId"]
                    sg_name = data["detail"]["resource"]["instanceDetails"]["networkInterfaces"][0]["securityGroups"][0]["groupName"]
                    sg_id = data["detail"]["resource"]["instanceDetails"]["networkInterfaces"][0]["securityGroups"][0]["groupId"]
                    tags = (str(data["detail"]["resource"]["instanceDetails"]["tags"])).replace(",", "")
                    account_alias = str(get_account_alias(account_id))

                    ioc = ttp + "," + hits + "," + account_id + "," + account_alias + "," + region + "," + subnet_id + "," + src_ip + "," + instance_id + "," + nacl_id + "," + country + "," + city + "," + asn_org + "," + org + "," + isp + "," + asn + "," + vpc_id + "," + sg_name + "," + sg_id + "," + tags
                    log.info("IOCs: " + str(ioc))

                    if len(json_a) == 0:
                        json_a.append(ioc)
                    else:
                        for e in json_a:
                            if e != ioc:
                                json_a.append(ioc)

            elif flag == 2:
                ioc = []

                src_ip = (json.dumps(
                    data["detail"]["service"]["action"]["portProbeAction"]["portProbeDetails"][0]["remoteIpDetails"][
                        "ipAddressV4"])).strip('"')

                if ipaddress.ip_address(src_ip).is_private is False:

                    account_id = data["detail"]["accountId"]
                    region = data["region"]
                    subnet_id = data["detail"]["resource"]["instanceDetails"]["networkInterfaces"][0]["subnetId"]
                    instance_id = data["detail"]["resource"]["instanceDetails"]["instanceId"]
                    ttp = data["detail"]["type"]
                    country = \
                        data["detail"]["service"]["action"]["portProbeAction"]["portProbeDetails"][0][
                            "remoteIpDetails"][
                            "country"][
                            "countryName"]
                    city = (
                        data["detail"]["service"]["action"]["portProbeAction"]["portProbeDetails"][0][
                            "remoteIpDetails"][
                            "city"][
                            "cityName"]).replace(",", " ")
                    asn_org = (
                        data["detail"]["service"]["action"]["portProbeAction"]["portProbeDetails"][0][
                            "remoteIpDetails"][
                            "organization"][
                            "asnOrg"]).replace(",", " ")
                    org = (
                        data["detail"]["service"]["action"]["portProbeAction"]["portProbeDetails"][0][
                            "remoteIpDetails"][
                            "organization"][
                            "org"]).replace(",", " ")
                    isp = (
                        data["detail"]["service"]["action"]["portProbeAction"]["portProbeDetails"][0][
                            "remoteIpDetails"][
                            "organization"][
                            "isp"]).replace(",", " ")
                    asn = \
                        data["detail"]["service"]["action"]["portProbeAction"]["portProbeDetails"][0][
                            "remoteIpDetails"][
                            "organization"][
                            "asn"]

                    nacl_id = get_netacl_id(subnet_id, account_id)
                    hits = str(data["detail"]["service"]["count"])
                    vpc_id = data["detail"]["resource"]["instanceDetails"]["networkInterfaces"][0]["vpcId"]
                    sg_name = data["detail"]["resource"]["instanceDetails"]["networkInterfaces"][0]["securityGroups"][0]["groupName"]
                    sg_id = data["detail"]["resource"]["instanceDetails"]["networkInterfaces"][0]["securityGroups"][0]["groupId"]
                    tags = (str(data["detail"]["resource"]["instanceDetails"]["tags"])).replace(",", "")
                    account_alias = str(get_account_alias(account_id))

                    ioc = ttp + "," + hits + "," + account_id + "," + account_alias + "," + region + "," + subnet_id + "," + src_ip + "," + instance_id + "," + nacl_id + "," + country + "," + city + "," + asn_org + "," + org + "," + isp + "," + asn + "," + vpc_id + "," + sg_name + "," + sg_id + "," + tags
                    log.info("IOCs: " + str(ioc))

                    if len(json_a) == 0:
                        json_a.append(ioc)
                    else:
                        for e in json_a:
                            if e != ioc:
                                json_a.append(ioc)

            elif flag == 3:
                ioc = []

                src_ip = (json.dumps(
                    data["service"]["action"]["networkConnectionAction"]["remoteIpDetails"][
                        "ipAddressV4"])).strip('"')
                direction = data["service"]["action"]["networkConnectionAction"]["connectionDirection"]

                if ipaddress.ip_address(src_ip).is_private is False and direction == "INBOUND":

                    account_id = data["accountId"]
                    region = data["region"]
                    subnet_id = data["resource"]["instanceDetails"]["networkInterfaces"][0]["subnetId"]
                    instance_id = data["resource"]["instanceDetails"]["instanceId"]
                    ttp = data["type"]

                    asn = \
                        data["service"]["action"]["networkConnectionAction"]["remoteIpDetails"][
                            "organization"][
                            "asn"]
                    asn_org = (
                        data["service"]["action"]["networkConnectionAction"]["remoteIpDetails"][
                            "organization"][
                            "asnOrg"]).replace(",", " ")
                    isp = (
                        data["service"]["action"]["networkConnectionAction"]["remoteIpDetails"][
                            "organization"][
                            "isp"]).replace(",", " ")
                    org = (
                        data["service"]["action"]["networkConnectionAction"]["remoteIpDetails"][
                            "organization"][
                            "org"]).replace(",", " ")
                    country = \
                        data["service"]["action"]["networkConnectionAction"]["remoteIpDetails"]["country"][
                            "countryName"]
                    try:
                        city = str((data["service"]["action"]["networkConnectionAction"]["remoteIpDetails"]["city"][
                            "cityName"]).replace(",", " "))
                    except Exception as e:
                        city = "NIA"

                    nacl_id = get_netacl_id(subnet_id, account_id)
                    hits = str(data["service"]["count"])
                    vpc_id = data["resource"]["instanceDetails"]["networkInterfaces"][0]["vpcId"]
                    sg_name = data["resource"]["instanceDetails"]["networkInterfaces"][0]["securityGroups"][0]["groupName"]
                    sg_id = data["resource"]["instanceDetails"]["networkInterfaces"][0]["securityGroups"][0]["groupId"]
                    tags = (str(data["resource"]["instanceDetails"]["tags"])).replace(",", "")
                    account_alias = str(get_account_alias(account_id))

                    ioc = ttp + "," + hits + "," + account_id + "," + account_alias + "," + region + "," + subnet_id + "," + src_ip + "," + instance_id + "," + nacl_id + "," + country + "," + city + "," + asn_org + "," + org + "," + isp + "," + asn + "," + vpc_id + "," + sg_name + "," + sg_id + "," + tags
                    log.info("IOCs: " + str(ioc))

                    if len(json_a) == 0:
                        json_a.append(ioc)
                    else:
                        for e in json_a:
                            if e != ioc:
                                json_a.append(ioc)

        except Exception as e:
            log.info("JSON could not be parsed:" + str(e))


def get_netacl_id(subnet_id, account_id):
    log.info("Getting NACL id for subnet: " + str(subnet_id) + " account: " + str(account_id))

    global HUB_ACCOUNT_ID

    try:
        nacl_id = ""

        if account_id != HUB_ACCOUNT_ID:
            client = assume_role(account_id, "client")

            response = client.describe_network_acls(
                Filters=[
                    {
                        'Name': 'association.subnet-id',
                        'Values': [
                            subnet_id,
                        ]
                    }
                ]
            )
        else:
            response = ec2.describe_network_acls(
                Filters=[
                    {
                        'Name': 'association.subnet-id',
                        'Values': [
                            subnet_id,
                        ]
                    }
                ]
            )

        nacls = response['NetworkAcls'][0]['Associations']

        for n in nacls:
            if n['SubnetId'] == subnet_id:
                nacl_id = n['NetworkAclId']
                log.info("NACL found:" + str(nacl_id))

        return nacl_id

    except Exception as e:
        log.info("Failed to get NACL id:" + str(e))


def incident_and_response():
    log.info("Incident and Response Automation ...")

    ts = str(datetime.datetime.now())

    ujsa = set(json_a)

    for jsa in ujsa:

        lst = jsa.split(",")
        ioc = len(lst)

        rule_no = "-1"
        if ioc == 19:
            ttp, hits, account_id, account_alias, region, subnet_id, src_ip, instance_id, nacl_id, country, city, asn_org, org, isp, asn, vpc_id, sg_name, sg_id, tags = jsa.split(",")

            lst_nacl = get_nacl_rule(nacl_id, account_id)
            rule_no = int(lst_nacl.pop())
            result = create_nacl_rule(nacl_id, src_ip, rule_no, account_id, set(lst_nacl))

            if result:
                update_ioc(src_ip, ts, ttp, hits, region, account_id, account_alias, nacl_id, subnet_id, instance_id, country, city, asn_org, org, isp, asn, rule_no, vpc_id, sg_name, sg_id, tags)
                # message_to_slack(src_ip, ttp, hits, account_id, account_alias, nacl_id, subnet_id, instance_id, country, city, asn_org, org, isp, vpc_id, tags)
        else:
            country = city = asn_org = org = isp = asn = "NIA"
            ttp, account_id, account_alias, region, subnet_id, src_ip, instance_id, nacl_id, vpc_id, sg_name, sg_id, tags = jsa.split(",")

            lst_nacl = get_nacl_rule(nacl_id, account_id)
            rule_no = int(lst_nacl.pop())
            result = create_nacl_rule(nacl_id, src_ip, rule_no, account_id, set(lst_nacl))

            if result:
                update_ioc(src_ip, ts, ttp, hits, region, account_id, account_alias, nacl_id, subnet_id, instance_id, country, city, asn_org, org, isp, asn, rule_no, vpc_id, sg_name, sg_id, tags)
                # message_to_slack(src_ip, ttp, hits, account_id, account_alias, nacl_id, subnet_id, instance_id, country, city, asn_org, org, isp, vpc_id, tags)


def get_nacl_rule(nacl_id, account_id):
    rule = get_rules(nacl_id, account_id)

    log.info("Getting rule number (entry) for NACL: " + str(nacl_id) + " account: " + str(account_id))

    lst_no = []
    lst_cidr = []

    for r in rule:
        no, cidr = r.split(",")
        lst_no.append(int(no))
        lst_cidr.append(cidr)

    i = int(min(lst_no)) + 1

    if int(min(lst_no)) == 100:
        rule_no = 1
    else:
        count = 1
        while count < 98:
            count += 1

            if i < 100 and i not in lst_no:
                rule_no = i
                break
            else:
                i += 1

    log.info("Rule number (entry): " + str(rule_no))
    log.info("CIDR already added: " + str(set(lst_cidr)))

    lst_cidr.append(str(rule_no))
    return lst_cidr


def get_rules(nacl_id, account_id):
    log.info("Getting rules for NACL: " + str(nacl_id) + " account: " + str(account_id))

    global HUB_ACCOUNT_ID

    rules = []

    if account_id != HUB_ACCOUNT_ID:

        client = assume_role(account_id, "client")

        response = client.describe_network_acls(
            NetworkAclIds=[
                nacl_id,
            ],
        )
    else:
        response = ec2.describe_network_acls(
            NetworkAclIds=[
                nacl_id,
            ],
        )

    data = response['NetworkAcls'][0]['Entries']

    for d in data:
        entry = str(d['RuleNumber']) + "," + str(d['CidrBlock'])
        rules.append(entry)

    return rules


def create_nacl_rule(nacl_id, attacker_ip, rule_no, account_id, lst_nacl):
    global HUB_ACCOUNT_ID

    log.info("Creating NACL rule for attacker:" + str(attacker_ip))

    if attacker_ip + '/32' not in lst_nacl and len(lst_nacl) <= 18:
        if account_id != HUB_ACCOUNT_ID:

            client = assume_role(account_id, "resource")

            nacl = client.NetworkAcl(nacl_id)

        else:
            nacl = r_ec2.NetworkAcl(nacl_id)

        response = nacl.create_entry(
            CidrBlock=attacker_ip + '/32',
            Egress=False,
            PortRange={
                'From': 0,
                'To': 65535
            },
            Protocol='-1',
            RuleAction='deny',
            RuleNumber=rule_no
        )

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            return False

    elif len(lst_nacl) == 19:
        log.info("NACL is full, no more than 18 entries can be added")

    else:
        log.info("Attacker is already blocked")


def get_account_alias(account_id):
    log.info("Getting alias for account: " + str(account_id))

    global HUB_ACCOUNT_ID

    rules = []

    if account_id != HUB_ACCOUNT_ID:

        client = assume_role(account_id, "iam")
        response = client.list_account_aliases()

    else:
        response = iam.list_account_aliases()

    alias = str(response['AccountAliases'])
    result = alias[2:-2]

    return result


def update_ioc(attacker_ip, timestamp, ttp, hits, region, account_id, account_alias, nacl_id, subnet_id, instance_id, country, city, asn_org, org, isp, asn, rule_no, vpc_id, sg_name, sg_id, tags):

    log.info("Sending IOCs to DynamoDB ...")

    try:
        table = dynamodb.Table(DYNAMO_TABLE)
        scan = table.scan()

        if scan['Items']:

            updated = 0
            for s in scan['Items']:

                if s['attacker_ip'] == attacker_ip:

                    update_entry_attackers(attacker_ip, hits, rule_no, False)
                    updated = 1

            if updated == 0:
                create_entry_attackers(attacker_ip, timestamp, ttp, hits, region, account_id, account_alias, nacl_id, subnet_id,
                                       instance_id, country, city, asn_org, org, isp, asn, rule_no, vpc_id, sg_name, sg_id, tags)

        else:
            create_entry_attackers(attacker_ip, timestamp, ttp, hits, region, account_id, account_alias, nacl_id, subnet_id,
                                   instance_id, country, city, asn_org, org, isp, asn, rule_no, vpc_id, sg_name, sg_id, tags)

    except Exception as e:
        log.info("DynamoDB entry could not be updated" + str(e))


def update_entry_attackers(attacker_ip, hits, rule_no, deleted):

    table = dynamodb.Table(DYNAMO_TABLE)

    try:
        if not deleted:
            log.info("Updating new DynamoDB entry for attacker: " + str(attacker_ip))

            response = table.update_item(
                Key={
                    'attacker_ip': attacker_ip
                },
                UpdateExpression="set hits = :h, rule_no = :r_no",
                ExpressionAttributeValues={
                    ':h': hits,
                    ':r_no': rule_no
                },
                ReturnValues="UPDATED_NEW"
            )
            return

        else:
            log.info("Updating cleaned (NACL) DynamoDB entry for attacker: " + str(attacker_ip))

            response = table.update_item(
                Key={
                    'attacker_ip': attacker_ip
                },
                UpdateExpression="set hits = :h, rule_no = :r_no",
                ExpressionAttributeValues={
                    ':h': hits,
                    ':r_no': rule_no
                },
                ReturnValues="UPDATED_NEW"
            )
            return

    except Exception as e:
        log.info("DynamoDB could not be updated:" + str(e))


def create_entry_attackers(attacker_ip, timestamp, ttp, hits, region, account_id, account_alias, nacl_id, subnet_id, instance_id, country, city, asn_org, org, isp, asn, rule_no, vpc_id, sg_name, sg_id, tags):
    if not city:
        city = "NIA"

    log.info("Creating DynamoDB entry for attacker:" + str(attacker_ip))

    try:
        table = dynamodb.Table(DYNAMO_TABLE)

        response = table.put_item(
            Item={
                'attacker_ip': str(attacker_ip),
                'timestamp': str(timestamp),
                'ttp': str(ttp),
                'hits': str(hits),
                'region': str(region),
                'account_id': str(account_id),
                'account_alias': str(account_alias),
                'vpc_id': str(vpc_id),
                'nacl_id': str(nacl_id),
                'subnet_id': str(subnet_id),
                'instance_id': str(instance_id),
                'tags': str(tags),
                'sg_name': str(sg_name),
                'sg_id': str(sg_id),
                'country': str(country),
                'city': str(city),
                'asn_org': str(asn_org),
                'org': str(org),
                'isp': str(isp),
                'asn': str(asn),
                'rule_no': str(rule_no)
            }
        )

    except Exception as e:
        log.info("DynamoDB entry could not be created" + str(e))


def assume_role(account_id, boto_type):
    global ROLE_SPOKE

    log.info("Assuming role: " + str(ROLE_SPOKE) + " account: " + str(account_id))
    try:

        sts = sts_connection.assume_role(
            RoleArn="arn:aws:iam::" + account_id + ":role/" + ROLE_SPOKE,
            RoleSessionName="cross_acct_lambda"
        )

        ACCESS_KEY = sts['Credentials']['AccessKeyId']
        SECRET_KEY = sts['Credentials']['SecretAccessKey']
        SESSION_TOKEN = sts['Credentials']['SessionToken']

        if boto_type == "resource":
            client = boto3.resource(
                'ec2',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
                aws_session_token=SESSION_TOKEN,
            )
        elif boto_type == "client":
            client = boto3.client(
                'ec2',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
                aws_session_token=SESSION_TOKEN,
            )
        elif boto_type == "iam":
            client = boto3.client(
                'iam',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
                aws_session_token=SESSION_TOKEN,
            )

        return client
    except Exception as e:
        log.info("Role could not be assumed" + str(e))


def clean_nacls():
    global HUB_ACCOUNT_ID

    log.info("Cleaning old NACLs entries ... ")

    try:
        now = datetime.datetime.now()

        table = dynamodb.Table(DYNAMO_TABLE)
        response = table.scan()

        for r in response['Items']:

            if str(r['rule_no']) != "0":

                t = r['timestamp']
                account = r['account_id']
                log.info("Searching for oldest entries in the account: " + str(account) + " attacker: " + str(r['attacker_ip']))

                old = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f')
                difh = ((now - old).days * 24) + int((now - old).seconds / 3600)

                log.info("Hours that remained blocked: " + str(difh))

                if difh >= 6:
                    log.info("Cleaning NACL entry: " + str(r['rule_no']) + " account: " + str(account))

                    try:
                        if account != HUB_ACCOUNT_ID:

                            client = assume_role(account, "resource")
                            network_acl = client.NetworkAcl(r['nacl_id'])

                        else:
                            network_acl = r_ec2.NetworkAcl(r['nacl_id'])

                        response2 = network_acl.delete_entry(
                            Egress=False,
                            RuleNumber=int(r['rule_no'])
                        )

                        if response2['ResponseMetadata']['HTTPStatusCode'] == 200:
                            log.info("NACL rule deleted for attacker: " + str(r['attacker_ip']))
                            update_entry_attackers(str(r['attacker_ip']), str(r['hits']), "0", True)
                            return
                        else:
                            log.info("Failed to delete the entry")
                    except Exception as e:
                        log.info("Failed to instantiate resource NetworkAcl " + str(e))
                        log.info("Updating IOCs db to keep consistency ... " + str(e))

                        try:
                            update_entry_attackers(str(r['attacker_ip']), str(r['hits']), "0", True)
                        except Exception as e:
                            log.info("Updating IOCs db to keep consistency failed: " + str(e))

    except Exception as e:
        log.info("NACLs could not be deleted: " + str(e))


def message_to_slack(src_ip, ttp, hits, account_id, account_alias, nacl_id, subnet_id, instance_id, country, city, asn_org, org, isp, vpc_id, tags):

    excluded = False
    nacl_url = "https://console.aws.amazon.com/vpc/home?region=us-east-1#acls:networkAclId=" + nacl_id + ";sort=networkAclId"

    for e in exclusion_list:
        if e == tags:
            excluded = True

    try:
        if not excluded:
            log.info("Sending message to Slack")

            data = {
                'text': '***************************************************************\n\n'
                        + '*ATTACKER IP:* ' + src_ip + '   *HITS:* ' + hits + '\n'
                        + '*TTP:* ' + ttp + '\n'
                        + '*ACCOUNT ID:* ' + '`' + account_id + '`' + '   *ACCOUNT ALIAS:* ' + account_alias + '   *INSTANCE ID:* ' + '`' + instance_id + '`' + '\n'
                        + '*TAGS:* ' + tags + '\n'
                        + '*NACL:* ' + nacl_url + '\n'
                        + '*VPC ID:* ' + '`' + vpc_id + '`' + '   *SUBNET ID:* ' + '`' + subnet_id + '`' + '\n'
                        + '*COUNTRY:* ' + country + '   *CITY:* ' + city + '\n'
                        + '*ASN ORG:* ' + asn_org + '   *ORG:* ' + org + '   *ISP:* ' + isp + '\n'
                        + '***************************************************************',
                'username': 'IR BUDDY',
                'icon_emoji': ':robot_face:'
            }

            response = requests.post(WEBHOOK_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'})

            log.info('Sending message to Slack. Response: ' + str(response.text) + ' Response Code: ' + str(response.status_code))

    except Exception as e:
        log.info("Message could not be send to Slack: " + str(e))


def delete_sqs():
    log.info("Deleting queue ...")
    try:
        for rh in message:
            receipt_handle = rh['ReceiptHandle']

            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=receipt_handle
            )
            log.info('Processed and deleted message: %s' % receipt_handle)
    except Exception as e:
        log.info("SQS queue could not be deleted" + str(e))


def put_s3(res):
    s3_resource = boto3.resource('s3')
    bucket_name = BUCKET_NAME
    iocs_path = IOCS_PATH

    bucket = s3_resource.Bucket(name=bucket_name)

    if iocs_path.startswith("/"):
        iocs_path = iocs_path[1:]
    if iocs_path.endswith("/"):
        iocs_path = iocs_path[:-1]

    (bucket.Object(key=f"{iocs_path}/beaconing_detection_{NOW}.json")
           .put(Body=bytes(json.dumps(res).encode('UTF-8'))))


def security_ir(event, context):
    global message

    log.info("Processing GuardDuty findings: %s" % json.dumps(event))

    try:
        clean_nacls()
        message = read_sqs()
        if message:
            search_ioc()
            incident_and_response()
            delete_sqs()

            log.info("Findings properly processed")

    except Exception as e:
        log.error('Failure to process finding ' + str(e))
