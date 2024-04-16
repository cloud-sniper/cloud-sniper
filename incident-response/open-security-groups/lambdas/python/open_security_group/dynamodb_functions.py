import boto3
import os
import logging
import sys

# SETUP LOGGING OPTIONS
logging.basicConfig(stream=sys.stdout)
log = logging.getLogger("open-security-groups-automation")
log.setLevel(logging.INFO)

# DynamoDB configuration
DynamoDBTableName = os.environ['DYNAMODB_NAME']
Primary_Column_Name = 'ID'
Primary_Key = 1
columns = ["ID", "region", "account", "creator_arn", "date_reported", "last_update", "violation_rule", "notes", "status_ir"]
client = boto3.client('dynamodb')
DB = boto3.resource('dynamodb')
table = DB.Table(DynamoDBTableName)


# check into dynamodb.
def query_to_dynamo(id):
    log.info("Checking SG: " + id + " into dynamoDB.")
    try:
        response = table.get_item(
            Key={
                Primary_Column_Name: id
            }
        )
        if 'Item' in response:
            return "Reported"
        else:
            return "NoReported"
    except Exception as e:
        log.error("Error trying to get ID from dynamodb" + str(e))

# put into dynamodb.
def put_to_dynamo(id, region, account, creator_arn, date, update_date, violation_rule):
    try:
        response = table.put_item(
            Item={
                Primary_Column_Name:id,
                columns[0]: id,
                columns[1]: region,
                columns[2]: account,
                columns[3]: creator_arn,
                columns[4]: date,
                columns[5]: update_date,
                columns[6]: violation_rule,
                columns[8]: "reported",
                    }
                )
    except Exception as e:
        exit("Error putting into DynamoDB" + str(e))

# update item dynamodb.
def update_to_dynamo(id, colum, value):
    try:
        expression = "set "+colum+" = :value"
        response = table.update_item(
            Key={
                "ID": id
            },
            UpdateExpression=expression,
            ExpressionAttributeValues={
                ":value": value
            },
            ReturnValues="UPDATED_NEW"
        )
    except Exception as e:
        exit("Error updating into DynamoDB" + str(e))
