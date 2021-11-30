import json
import os
import logging
import boto3
import base64
import sys
from urllib.parse import parse_qs
from dynamodb_functions import putToDynamo

from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler


# SETUP LOGGING OPTIONS
logging.basicConfig(stream=sys.stdout)
log = logging.getLogger("slack-automation-bot")
log.setLevel(logging.INFO)

# SETUP SECRETS
secrets_client = boto3.client(
    'secretsmanager', region_name=os.environ['AWS_REGION'])
secret_data = json.loads(secrets_client.get_secret_value(
    SecretId=os.environ['SLACK_AUTOMATION_BOT'])['SecretString'])

SLACK_TOKEN = secret_data['SLACK_API_SECRET']
SIGNING_TOKEN = secret_data['SIGNING_SECRET']
os.environ['SLACK_BOT_TOKEN'] = SLACK_TOKEN
os.environ['SLACK_SIGNING_SECRET'] = SIGNING_TOKEN


app = App(
    token=SLACK_TOKEN,
    signing_secret=SIGNING_TOKEN
)


# from here all custom def for actions


# process_before_response must be True when running on FaaS
# from here all slack_bolt actions
app = App(process_before_response=True)

@app.block_action("open_sg_automation")
def open_sg_automation(body, respond):
    log.info("Running automation")
    log.info(body)
    confirming_username = str(body['user']['username'])
    blocks = body['message']['blocks']
    block_send = []
    for section in blocks:
        if "section" == section["type"]:
            block_send.append(section)
    response_confirm = {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": ":warning: *LOG* The user: @{0} creates an a exception for this event.".format(
                                    confirming_username)
                            },
                        }
    message = str(body['message']['text']).split(':', 2)
    sg_id = message[1].replace("`", "")
    putToDynamo(sg_id, confirming_username)
    block_send.append(response_confirm)
    respond(replace_original=True, blocks=block_send)

@app.block_action("confirmed_event")
def confirmed_event(body, respond):
    log.info("Running automation")
    log.info(body)
    confirming_username = str(body['user']['username'])
    blocks = body['message']['blocks']
    block_send = []
    for section in blocks:
        if "section" == section["type"]:
            block_send.append(section)
    response_confirm = {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": ":white_check_mark: *LOG* The user: @{0} confirms this notification and doesn't request the automated exception.".format(
                                    confirming_username)
                            },
                        }
    block_send.append(response_confirm)
    respond(replace_original=True, blocks=block_send)


SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def lambda_handler(event, context):
    try:
        payload = base64.b64decode(str(event["body"]))
        payload_2 = parse_qs(payload.decode("utf-8"))
        log.info(payload_2)
        log.info('sending payload to the interactive response')
        slack_handler = SlackRequestHandler(app=app)
        log.info('response sent')
        return slack_handler.handle(event, context)
    except Exception as e:
        log.info(" something goes wrong: "+str(e))
        return {
            'statusCode': 401
        }