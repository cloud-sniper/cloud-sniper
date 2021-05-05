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
columns = ["ID", "date", "user", "notes"]
client = boto3.client('dynamodb')
DB = boto3.resource('dynamodb')
table = DB.Table(DynamoDBTableName)


# check SG into dynamodb.
def query_to_dynamo(ID):
    log.info("Checking SG: " + ID + " into dynamoDB.")
    try:
        response = table.get_item(
            Key={
                Primary_Column_Name: ID
            }
        )
        if 'Item' in response:
            return "Reported"
        else:
            return "NoReported"
    except Exception as e:
        log.error("error trying to get ID from dynamodb" + str(e))
