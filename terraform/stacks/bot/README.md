CLOUDSNIPER SLACK BOT 
=============
![alt text](images/img.png "button_bot")

## SLACK BOT
This bot is the slack automation of CloudSniper. The bot works with AWS lambda functions to manage messages and send them to slack.
The bot also can handle `slack actions` using `API GATEWAY` and `SLACKBOT`.

#### EVENT TO SEND AN EVENT

The format of the events to be sent is as below:

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

## HOW TO USE IT

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


#### HOW TO SEND A MESSAGE

Add execution permissions to your lambda/service and then use the `client.invoke` function, for example:

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

![alt text](images/bot_message.png "message_bot")


#### HOW TO SEND A MESSAGES WITH A BUTTON?

As befor, you need to add execution permissions to your lambda/service and use the `client.invoke` function:

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

![alt text](images/bot_message_button.png "button_bot")