import sys
import logging
from datetime import datetime
import boto3
import os
import json

##### define standard configurations ####

# SETUP LOGGING OPTIONS
logging.basicConfig(format="%(asctime)s %(message)s", stream=sys.stdout)
log = logging.getLogger("cloud-lusat-inventory-s3-sender")
log.setLevel(logging.INFO)

# Setup for S3 general
BucketName = os.environ['BUCKET_NAME']
BucketPath = os.environ['LUSAT_PATH']

def put_to_s3(data):
    log.info("starting to put_to_s3")
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(name=BucketName)
    (bucket.Object(key=BucketPath+"/lusat_finding_"+now+".json")
           .put(Body=bytes(json.dumps(data).encode('UTF-8'))))
    log.info("done put_to_s3")
