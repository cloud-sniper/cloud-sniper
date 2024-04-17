Cloud Sniper Slack Bot (to be refactored)
=============
![alt text](../../images/logo.png "button_bot")

## Slack bot integration
This bot is CloudSniper's Slack automation. The bot works with AWS Lambda functions to manage messages and send them to slack.
The bot can also handle `slack actions` using `API GATEWAY` and `SLACK BOT`.

#### Event management

The format of the events to be sent is as follows:

```json
    {
        "sendTo": "#channel/@user",
        "button": "True/False",
        "title": "Short title for the message",
        "description": "Description for the message"
        "field_details": [
                    {
                        "name": "date/user/abc",
                        "description": "description for value",
                    }
        ]
    }
```

## How to use it

1. Create a SLACK BOT with the following permissions:\
                    - `incoming-webhook`\
                    - `app_mentions:read`\
                    - `chat:write`\
                    - `chat:write.public`
2. Deploy the stack using terraform.
3. UPDATE the content of the secret with the structure below:
```json
{
  "SLACK_API_SECRET": "xoxb-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "WEBHOOK_URL_SECRET": "https://hooks.slack.com/services/XXXXXX/XXXXXXXXXXXXXX",
  "SIGNING_SECRET": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```


#### How to send a message

Add execution permissions to your Lambda/service and then use the `client.invoke` function, for example:

```python
data = {
          "sendTo": "#security-testing-alerts",
          "button": "False",
          "title": "This is a test message from the automation stack of the bot",
          "description": "This is a test using the new automation stack of the bot",
          "field_details": [
                {
                  "name": "date",
                  "description": "03/30/2021"
                },
                {
                  "name": "Project",
                  "description": "blah blah"
                },
                {
                  "name": "What to do?",
                  "description": "do not know"
                },
                {
                  "name": "Who calls?",
                  "description": "reach to #security"
                }
              ]
        }
response = client.invoke(
        FunctionName = 'arn:aws:lambda:XXXXXXXXXXXXXXXX',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(data)
    )
```

#### How to send a message through a button?

As mentioned above, you need to add execution permissions to your Lambda/service and use the `client.invoke` function:

```python
data = {
          "sendTo": "#security-testing-alerts",
          "button": "True",
          "title": "This is a test message from the automation stack of the bot",
          "description": "This is a test using the new automation stack of the bot",
          "field_details": [
                {
                  "name": "date",
                  "description": "03/30/2021"
                },
                {
                  "name": "Project",
                  "description": "blah blah"
                },
                {
                  "name": "What to do?",
                  "description": "do not know"
                },
                {
                  "name": "Who calls?",
                  "description": "reach to #security"
                }
              ]
        }
response = client.invoke(
        FunctionName = 'arn:aws:lambda:XXXXXXXXXXXXXXXX',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(data)
    )
```
