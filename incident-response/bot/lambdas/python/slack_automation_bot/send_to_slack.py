import boto3
import os
import logging
import json
import sys
from slack_sdk import WebClient

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


# Lambda handler for incoming messages.
def lambda_handler(event, Context=None):
    log.info('Received event: {0}'.format(event))
    message_to_slack(event)
    log.info('Done!')
    return


# send to slack
def message_to_slack(event):
    send_to = str((event['sendTo']))
    title = str((event['title']))
    description = (event['description'])

    try:
        fields_data = []
        if 'field_details' in event:
            field_details = event['field_details']
            for detail in field_details:
                field = {
                    "type": "mrkdwn",
                    "text": "*"+detail['name']+":*\n" + detail['description']
                }
                fields_data.append(field)
        else:
            log.warning("No additional details for this even")
        if 'button' in event:
            button = (event['button'])
            button_id = (event['button_id'])
            if "True" == button:
                blocks = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": description
                        }
                    },
                    {
                        "type": "section",
                        "fields": fields_data,
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "emoji": True,
                                    "text": "Acknowledge this event."
                                },
                                "style": "primary",
                                "value": description,
                                "action_id": "confirmed_event"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "emoji": True,
                                    "text": "Create an exception for this."
                                },
                                "style": "danger",
                                "value": description,
                                "action_id": button_id
                            }
                        ]
                    }
                ]
            else:
                log.warning("No button for this even")
        else:
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": description
                    }
                },
                {
                    "type": "section",
                    "fields": fields_data,
                }
            ]
        log.info("Sending message to Slack ...")
        client = WebClient(token=SLACK_TOKEN)
        channel = send_to
        response = client.chat_postMessage(channel=channel,
                                           text=title,
                                           blocks=blocks,
                                           link_names=True
                                           )
        log.info("Message send: " + str(response))
    except Exception as e:
        log.error("Message could not be send to Slack: " + str(e))
