import boto3
import os
import logging
import sys
import json
from parser_arn_user import parse_arn


# SETUP LOGGING & LAMBDA OPTIONS
logging.basicConfig(stream=sys.stdout)
log = logging.getLogger("tdir-automation")
log.setLevel(logging.INFO)
lambda_client = boto3.client('lambda')
LambdaFunctionName = os.environ['LAMBDA_BOT_NAME']


# send to slack
def message_to_slack(event, context, checkQuadCero):
    ACCOUNT = str((event['account']))
    ID = str((event['detail']['requestParameters']
              ['groupId']))
    CREATOR_ARN = str((event['detail']['userIdentity']
                   ['arn']))
    ARN_DATA = parse_arn(CREATOR_ARN)
    CREATOR_USER = str((event['detail']['userIdentity']
    ['userName']))
    DATE = str((event['time']))
    REGION = str((event['region']))
    

    try:
        log.info("Sending message to Slack ...")
        to_group = {
            "sendTo": "#black-hat-demo",
            "title": "A new open security group has just been created: `" + ID + "`",
            "button": "True",
            "button_id": "open_sg_automation",
            "description": "A new open security group has just been created: `" + ID + "`",
            "field_details": [
                {
                    "name": "Date",
                    "description": DATE
                },
                {
                    "name": "Account ID",
                    "description": "`" + ACCOUNT + "`" + '/' + "`" + REGION + "`"
                },
                {
                    "name": "Who created it?",
                    "description": "*User*: `" + CREATOR_USER + "`, *ARN*: `" + CREATOR_ARN + "`"
                },
                {
                    "name": "What does it mean?",
                    "description": "The user: `" + CREATOR_USER + "` creates a security group open to the outside "
                                                                  "world (quad zero rule). "
                },
                {
                    "name": "More info +",
                    "description": "We automatically remove the insecure rules and replace them with a private class "
                                   "CIDR.  You can run the automation to exclude this SG. "
                }
            ]
        }
        lambda_client.invoke(FunctionName=LambdaFunctionName,
                             InvocationType='Event',
                             Payload=json.dumps(to_group))
    except Exception as e:
        log.error("Message could not be send to Slack: " + str(e))
