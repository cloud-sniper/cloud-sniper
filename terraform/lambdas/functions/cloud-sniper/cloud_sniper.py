import boto3
import json
import datetime
import logging
import os
from boto3.dynamodb.conditions import Attr

log = logging.getLogger()
log.setLevel(logging.INFO)

IPSET_ID = os.environ['CLOUDSNIPER-WAFREGIONAL-IPSET-BLOCK-THESE-IP']
DYNAMO_TABLE = os.environ['DYNAMO_TABLE_CLOUD_SNIPER']
SQS_QUEUE = os.environ['SQS_QUEUE_CLOUD_SNIPER']

s = boto3.session.Session(region_name=os.environ['AWS_REGION'])

json_a = []
json_b = []

message = []

sqs = s.client('sqs')
queue_url = SQS_QUEUE
waf = s.client('waf-regional')
ec2 = s.client('ec2')
dynamodb = s.resource('dynamodb')
r_ec2 = s.resource('ec2')


networkConnectionAction = [
	"UnauthorizedAccess:EC2/SSHBruteForce",
	"Recon:EC2/Portscan",
]

portProbeAction = [
	"Recon:EC2/PortProbeUnprotectedPort",
]

awsApiCallAction = [
	"Recon:IAMUser/MaliciousIPCaller.Custom",
	"Recon:IAMUser/MaliciousIPCaller",
	"Recon:IAMUser/TorIPCaller",
	"PenTest:IAMUser/KaliLinux",
	"PenTest:IAMUser/PentooLinux",
	"PenTest:IAMUser/ParrotLinux",
]

instanceDetails = [
	"Trojan:EC2/BlackholeTraffic!DNS",
	"Trojan:EC2/DGADomainRequest.B",
	"Trojan:EC2/DGADomainRequest.C!DNS",
	"Trojan:EC2/DNSDataExfiltration",
	"Trojan:EC2/DriveBySourceTraffic!DNS",
	"Trojan:EC2/DropPoint!DNS",
	"Trojan:EC2/PhishingDomainRequest!DNS",
	"Trojan:EC2/BlackholeTraffic",
	"Trojan:EC2/DropPoint",
	"CryptoCurrency:EC2/BitcoinTool.B!DNS",
	"CryptoCurrency:EC2/BitcoinTool.B",
	"Backdoor:EC2/C&CActivity.B!DNS",
	"Backdoor:EC2/Spambot",
	"Backdoor:EC2/XORDDOS",
	"UnauthorizedAccess:EC2/MaliciousIPCaller.Custom",
	"UnauthorizedAccess:EC2/RDPBruteForce",
	"UnauthorizedAccess:EC2/TorClient",
	"UnauthorizedAccess:EC2/TorIPCaller",
	"UnauthorizedAccess:EC2/TorRelay",
]


def read_sqs():

	response = sqs.receive_message(
		QueueUrl=queue_url,
		MaxNumberOfMessages=10,
		MessageAttributeNames=[
			'All'
		],		
	)

	if 'Messages' in response:
		return response['Messages']
	else:
		return


def search_ioc():	
	
	log.info("searching for IOC ...")

	global json_a
	global json_b

	for b in message:		
		body = b['Body']
		
		data = json.loads(body)

		try:	
			flag = 0
			for e in networkConnectionAction:
				if data["detail"]["type"] == e:
					flag = 1
					break

			for e in portProbeAction:
					if data["detail"]["type"] == e:
						flag = 2
						break

			for e in awsApiCallAction:
				if data["detail"]["type"] == e:
					flag = 3
					break

			for e in instanceDetails:
				if data["detail"]["type"] == e:
					flag = 4
					break
			
			if flag == 1:
				ioc = []
				
				account_id = data["detail"]["accountId"]				
				region = data["region"]
				subnet_id = data["detail"]["resource"]["instanceDetails"]["networkInterfaces"][0]["subnetId"]
				nacl_id = get_netacl_id(subnet_id)
				src_ip = (json.dumps(data["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"]["ipAddressV4"])).strip('"')		
				instance_id = data["detail"]["resource"]["instanceDetails"]["instanceId"]
				ttp = data["detail"]["type"]

				asn = data["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"]["organization"]["asn"]
				asn_org = (data["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"]["organization"]["asnOrg"]).replace(","," ")
				isp = (data["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"]["organization"]["isp"]).replace(","," ")
				org = (data["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"]["organization"]["org"]).replace(","," ")
				country = data["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"]["country"]["countryName"]
				city = (data["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"]["city"]["cityName"]).replace(","," ")
							
				if nacl_id != '':									
					ioc = ttp + "," + account_id + "," + region + "," + subnet_id + "," + src_ip + "," + instance_id + "," + nacl_id + "," + country + "," + city + "," + asn_org + "," + org + "," + isp + "," + asn
				else:
					ioc = ttp + "," + account_id + "," + region + "," + subnet_id + "," + src_ip + "," + instance_id + "," + "external_nacl " + "," + country + "," + city + "," + asn_org + "," + org + "," + isp + "," + asn

				if len(json_a) == 0:
					json_a.append(ioc)					
				else:
					for e in json_a:
						if e != ioc:											
							json_a.append(ioc)				
				
			elif flag == 2:
				ioc = []				
				
				account_id = data["detail"]["accountId"]				
				region = data["region"]
				subnet_id = data["detail"]["resource"]["instanceDetails"]["networkInterfaces"][0]["subnetId"]				
				nacl_id = get_netacl_id(subnet_id)
				src_ip = (json.dumps(data["detail"]["service"]["action"]["portProbeAction"]["portProbeDetails"][0]["remoteIpDetails"]["ipAddressV4"])).strip('"')				
				instance_id = data["detail"]["resource"]["instanceDetails"]["instanceId"]
				ttp = data["detail"]["type"]
				
				country = data["detail"]["service"]["action"]["portProbeAction"]["portProbeDetails"][0]["remoteIpDetails"]["country"]["countryName"]
				city = (data["detail"]["service"]["action"]["portProbeAction"]["portProbeDetails"][0]["remoteIpDetails"]["city"]["cityName"]).replace(",", " ")
				asn_org = (data["detail"]["service"]["action"]["portProbeAction"]["portProbeDetails"][0]["remoteIpDetails"]["organization"]["asnOrg"]).replace(",", " ")
				org = (data["detail"]["service"]["action"]["portProbeAction"]["portProbeDetails"][0]["remoteIpDetails"]["organization"]["org"]).replace(",", " ")
				isp = (data["detail"]["service"]["action"]["portProbeAction"]["portProbeDetails"][0]["remoteIpDetails"]["organization"]["isp"]).replace(",", " ")
				asn = data["detail"]["service"]["action"]["portProbeAction"]["portProbeDetails"][0]["remoteIpDetails"]["organization"]["asn"]
				
				if nacl_id != '':									
					ioc = ttp + "," + account_id + "," + region + "," + subnet_id + "," + src_ip + "," + instance_id + "," + nacl_id + "," + country + "," + city + "," + asn_org + "," + org + "," + isp + "," + asn
				else:
					ioc = ttp + "," + account_id + "," + region + "," + subnet_id + "," + src_ip + "," + instance_id + "," + "external_nacl" + "," + country + "," + city + "," + asn_org + "," + org + "," + isp + "," + asn

				if len(json_a) == 0:
					json_a.append(ioc)					
				else:
					for e in json_a:
						if e != ioc:											
							json_a.append(ioc)				
				
			elif flag == 3:
				ioc = []				
			
				account_id = data["detail"]["accountId"]			
				region = data["region"]				
				src_ip = (json.dumps(data["detail"]["service"]["action"]["awsApiCallAction"]["remoteIpDetails"]["ipAddressV4"])).strip('"')
				ttp = data["detail"]["type"]
				
				asn = data["detail"]["service"]["action"]["awsApiCallAction"]["remoteIpDetails"]["organization"]["asn"]
				asn_org = (data["detail"]["service"]["action"]["awsApiCallAction"]["remoteIpDetails"]["organization"]["asnOrg"]).replace(",", " ")
				isp = (data["detail"]["service"]["action"]["awsApiCallAction"]["remoteIpDetails"]["organization"]["isp"]).replace(",", " ")
				org = (data["detail"]["service"]["action"]["awsApiCallAction"]["remoteIpDetails"]["organization"]["org"]).replace(",", " ")
				country = data["detail"]["service"]["action"]["awsApiCallAction"]["remoteIpDetails"]["country"]["countryName"]
				city = (data["detail"]["service"]["action"]["awsApiCallAction"]["remoteIpDetails"]["city"]["cityName"]).replace(",", " ")
				
				ioc = ttp + "," + account_id + "," + region + "," + src_ip + "," + country + "," + city + "," + asn_org + "," + org + "," + isp + "," + asn

				if len(json_b) == 0:
					json_b.append(ioc)					
				else:
					for e in json_b:
						if e != ioc:											
							json_b.append(ioc)	
							
			elif flag == 4:				
				account_id = data["detail"]["accountId"]				
				region = data["region"]		
				subnet_id = data["detail"]["resource"]["instanceDetails"]["networkInterfaces"][0]["subnetId"]
				nacl_id = get_netacl_id(subnet_id)
				src_ip = (json.dumps(data["detail"]["resource"]["instanceDetails"]["networkInterfaces"][0]["publicIp"])).strip('"')
				instance_id = data["detail"]["resource"]["instanceDetails"]["instanceId"]
				ttp = data["detail"]["type"]				

				if nacl_id != '':									
					ioc = ttp + "," + account_id + "," + region + "," + subnet_id + "," + src_ip + "," + instance_id + "," + nacl_id
				else:
					ioc = ttp + "," + account_id + "," + region + "," + subnet_id + "," + src_ip + "," + instance_id + "," + "external_nacl"

				if len(json_a) == 0:
					json_a.append(ioc)					
				else:
					for e in json_a:
						if e != ioc:											
							json_a.append(ioc)

				# dump_flows(subnet_id)

		except Exception as e:
			log.info("json could not be parsed:", e)


def get_netacl_id(subnet_id):	
	try:        
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
		
		return nacl_id

	except:
		return ''


def incident_and_response():	

	log.info("Incident and Response...")

	ts = str(datetime.datetime.now())

	ujsa = set(json_a)
	ujsb = set(json_b)

	for jsa in ujsa:

		lst = jsa.split(",")
		ioc = len(lst)
		
		rule_no = "-1"		
		if ioc == 13:
			ttp, account_id, region, subnet_id, src_ip, instance_id, nacl_id, country, city, asn_org, org, isp, asn = jsa.split(",")

			update_ip_set(src_ip)

			if nacl_id != "external_nacl":
				rule_no = get_nacl_rule_no(nacl_id)				
				create_nacl_rule(nacl_id, src_ip, rule_no)

			update_table_attackers(src_ip, ts, subnet_id, region, account_id, instance_id, nacl_id, ttp, country, city, asn_org, org, isp, asn, rule_no)
		else:
			country=city=asn_org=org=isp=asn="NIA"
			ttp, account_id, region, subnet_id, src_ip, instance_id, nacl_id = jsa.split(",")
			

			update_ip_set(src_ip)
			
			if nacl_id != "external_nacl":
				rule_no = get_nacl_rule_no(nacl_id)
				create_nacl_rule(nacl_id, src_ip, rule_no)

			update_table_attackers(src_ip, ts, subnet_id, region, account_id, instance_id, nacl_id, ttp, country, city, asn_org, org, isp, asn, rule_no)

	for jsb in ujsb:
		
		ttp, account_id, region, src_ip, country, city, asn_org, org, isp, asn= jsb.split(",")

		update_ip_set(src_ip)
		
		rule_no = "-1"
		if nacl_id != "external_nacl":
			rule_no = get_nacl_rule_no(nacl_id)
			create_nacl_rule(nacl_id, src_ip, rule_no)

		update_table_attackers(src_ip, ts, subnet_id, region, account_id, instance_id, nacl_id, ttp, country, city, asn_org, org, isp, asn, rule_no)


def update_ip_set(src_ip):

	log.info("updating ip set...")
	try:
		response = waf.update_ip_set(
			IPSetId=IPSET_ID,
			ChangeToken=waf.get_change_token()['ChangeToken'],
			Updates=[{
				'Action': 'INSERT',
				'IPSetDescriptor': {
					'Type': 'IPV4',
					'Value': "%s/32"%src_ip
				}
			}]
		)       
	except Exception as e:
		log.info("WAF IPSet could not be updated",e)


def update_table_attackers(attacker_ip, timestamp, subnet_id, region, account_id, instance_id, nacl_id, ttp, country, city, asn_org, org, isp, asn, rule_no):

	if not city:
		city = "NIA"

	log.info("updating table attackers ...")

	table = dynamodb.Table(DYNAMO_TABLE)

	try:
		response = table.put_item(
			Item={
				'ip_attacker': str(attacker_ip),
				'timestamp': str(timestamp),
				'subnet_id': str(subnet_id),
				'region': str(region),
				'account_id': str(account_id),
				'instance_id': str(instance_id),
				'nacl_id': str(nacl_id),
				'ttp': str(ttp),
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
		log.info("table could not be updated", e)


def get_nacl_rule_no(nacl_id):

	log.info("get NACL id")
	rule = get_rules(nacl_id)
	i = min(rule) + 1

	if min(rule) == 100:
		rule_no = 1
	else:
		count = 1
		while count < 98:
			count += 1
			
			if i < 100 and i not in rule:
				rule_no = i
				break
			else:
				i += 1
	
	return rule_no


def create_nacl_rule(nacl_id, attacker_ip, rule_no):
	
	nacl = r_ec2.NetworkAcl(nacl_id)

	response = nacl.create_entry(
	CidrBlock = attacker_ip + '/32',
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


def get_rules(nacl_id):
	
	log.info("get rules for", nacl_id)

	rules = []

	response = ec2.describe_network_acls(
		NetworkAclIds=[ 
			nacl_id,
		],
	)

	data = response['NetworkAcls'][0]['Entries']
	
	for d in data:		
		rules.append(d['RuleNumber'])
	
	log.info("rules",rules)
	return set(rules)
	
		
def delete_sqs():

	log.info("deleting sqs queue ...")
	try:
		for rh in message:
			receipt_handle= rh['ReceiptHandle']

			sqs.delete_message(
				QueueUrl=queue_url,
				ReceiptHandle=receipt_handle
				)
	except Exception as e:
		log.info("SQS queue could not be deleted", e)


def dump_flows(subnet_id):

	log.info("creating flows logs on the subnet:", subnet_id)

	try:
		response = ec2.create_flow_logs(
			ResourceIds=[
				subnet_id,
			],
			ResourceType='Subnet',
			TrafficType='ALL',
			LogDestinationType='s3',
			LogDestination='arn:aws:s3:::s3-bucket-cloud-sniper/analytics/'
		)
	except Exception as e:
		log.info("Flow logs could not be created", e)


def clean_nacls():

	log.info("Cleaning NACls")

	try:
		now = datetime.datetime.now()

		table = dynamodb.Table(DYNAMO_TABLE)
		response = table.scan()
	
		for r in response['Items']:

			t = r['timestamp']
			old = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f')
			difh = (now - old).seconds//(60*60)					
			
			if difh >= 6:
				try:
					network_acl = r_ec2.NetworkAcl(r['nacl_id'])
					response2 = network_acl.delete_entry(
						Egress=False,
						RuleNumber=int(r['rule_no'])
					)

					if response2['ResponseMetadata']['HTTPStatusCode'] == 200:
						log.info('NACL rule deleted')

					else:
						log.info('Failed to delete the rule')

				except Exception as e:
					log.info("Failed to instantiate resource NetworkAcl", e)
			
	except Exception as e:        
		log.info("NACls could not be deleted:", e)


def cloud_sniper (event, context):

	global message

	log.info("GuardDuty findings: %s" % json.dumps(event))

	try:
		message = read_sqs()
		if message:
			search_ioc()
			incident_and_response()
			clean_nacls()	
			delete_sqs()

			log.info("Properly processed findings")
		else:
			log.info("There is no new message in the queue")
		
	except Exception as e:
		log.error('Failure to process GD finding')
