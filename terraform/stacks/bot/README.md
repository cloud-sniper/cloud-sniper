CLOUDSNIPER SLACK BOT 
=============
![alt text](images/img.png "button_bot")

## SLACK BOT
This is the slack automation bot for cloudsniper. This bot works with lambdas to manage messages and delivers to slack the same using the `cloud-sniper` bot of slack.
The bot also can handle `slack actions` using `APIGATEWAY` and `SLACKBOLT`

#### EVENT TO SEND: 
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

##HOW TO USE IT? 

1. Create a SLACK BOT with the following permissions:\
                    - `incoming-webhook`\
                    - `app_mentions:read`\
                    - `chat:write`\
                    - `chat:write.public`

2. Deploy the stack using terraform.
3. UPDATE the content of the secret with the following structure:
```json
{
  "SLACK_API_SECRET": "xoxb-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "WEBHOOK_URL_SECRET": "https://hooks.slack.com/services/XXXXXX/XXXXXXXXXXXXXX",
  "SIGNING_SECRET": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```


#### HOW TO SEND A MESSAGE?
Add the permissions for execution into your lambda/service and add then use the `client.invoke` example:

```python
data = {
          "sendTo": "#security-testing-alerts",
          "button": "False",
          "title": "This is a test message from the automation bot stack",
          "description": "This is a test using the new automation stack for bot",
          "field_details": [
                {
                  "name": "date",
                  "description": "03/30/2021"
                },
                {
                  "name": "Project",
                  "description": "bla bla"
                },
                {
                  "name": "What to do?",
                  "description": "do no"
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
Add the permissions for execution into your lambda/service and add then use the `client.invoke` example:

```python
data = {
          "sendTo": "#security-testing-alerts",
          "button": "True",
          "title": "This is a test message from the automation bot stack",
          "description": "This is a test using the new automation stack for bot",
          "field_details": [
                {
                  "name": "date",
                  "description": "03/30/2021"
                },
                {
                  "name": "Project",
                  "description": "bla bla"
                },
                {
                  "name": "What to do?",
                  "description": "do no"
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