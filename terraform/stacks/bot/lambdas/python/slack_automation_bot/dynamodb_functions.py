import boto3
import os
import logging
import sys
from datetime import datetime

# SETUP LOGGING OPTIONS
logging.basicConfig(stream=sys.stdout)
log = logging.getLogger("lambda-functions")
log.setLevel(logging.INFO)

# DynamoDB configuration
DynamoDBTableName = os.environ['DYNAMODB_NAME']
Primary_Column_Name = 'ID'
Primary_Key = 1
columns = ["ID", "date", "user", "notes"]
client = boto3.client('dynamodb')
DB = boto3.resource('dynamodb')
table = DB.Table(DynamoDBTableName)


# check into dynamodb.
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

# put into dynamodb.
def putToDynamo(ID, USER):
    try:
        response = table.put_item(
            Item={
                Primary_Column_Name:ID,
                columns[0]: ID,
                columns[1]: str(datetime.now()),
                columns[2]: USER,
                columns[3]: "the user create an exeption"
                    }
                )
    except Exception as e:
        exit("Errot putting into DynamoDB" + str(e))