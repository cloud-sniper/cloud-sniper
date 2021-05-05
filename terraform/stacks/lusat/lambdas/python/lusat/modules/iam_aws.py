
import os
import botocore
import boto3
import datetime
import logging
import sys
from dateutil.tz import tzlocal

# SETUP LOGGING OPTIONS
logging.basicConfig(format="%(asctime)s %(message)s", stream=sys.stdout)
log = logging.getLogger("cloud-lusat-inventory-iam-connector")
log.setLevel(logging.INFO)


def AssumedRoleSession(account_id: str, role_spoke: str, base_session: botocore.session.Session = None):
    log.info("starting to assume role")
    # base_session = base_session or boto3.session.Session()._session
    # log.info("using role: "+role_spoke)
    # fetcher = botocore.credentials.AssumeRoleCredentialFetcher(
    #     client_creator=base_session.create_client,
    #     source_credentials=base_session.get_credentials(),
    #     role_arn="arn:aws:iam::"+account_id+":role/"+role_spoke,
    #     extra_args={
    #         #    'RoleSessionName': None # set this if you want something non-default
    #     }
    # )
    # creds = botocore.credentials.DeferredRefreshableCredentials(
    #     method='assume-role',
    #     refresh_using=fetcher.fetch_credentials,
    #     time_fetcher=lambda: datetime.datetime.now(tzlocal())
    # )
    botocore_session = botocore.session.Session()
    log.info("credential ready for account: "+account_id)
    return boto3.Session(botocore_session=botocore_session)