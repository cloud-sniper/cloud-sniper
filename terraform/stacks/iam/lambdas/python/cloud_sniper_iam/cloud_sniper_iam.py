import boto3
import datetime
import os
import logging
import json
import requests

ROLE_SPOKE = os.environ['ROLE_SPOKE_CLOUD_SNIPER']
WEBHOOK_URL = os.environ['WEBHOOK_URL_CLOUD_SNIPER']
HUB_ACCOUNT_ID = os.environ['HUB_ACCOUNT_CLOUD_SNIPER']
HUB_ACCOUNT_NAME = os.environ['HUB_ACCOUNT_NAME_CLOUD_SNIPER']
BUCKET_NAME = os.environ['BUCKET_NAME']
IAM_PATH = os.environ['IAM_PATH']

log = logging.getLogger()
log.setLevel(logging.INFO)

# your accounts mapping
account_ids = {
    "name": "id",
}


def assume_role(account_id, boto_type):

    log.info("Assuming role: " + str(ROLE_SPOKE) + " account: " + str(account_id))

    try:
        sts = sts_connection.assume_role(
            RoleArn="arn:aws:iam::" + account_id + ":role/" + ROLE_SPOKE,
            RoleSessionName="cross_acct_lambda"
        )

        ACCESS_KEY = sts['Credentials']['AccessKeyId']
        SECRET_KEY = sts['Credentials']['SecretAccessKey']
        SESSION_TOKEN = sts['Credentials']['SessionToken']

        if boto_type == "iam":
            client = boto3.client(
                'iam',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
                aws_session_token=SESSION_TOKEN,
            )
        elif boto_type == "iam-resource":
            client = boto3.resource(
                'iam',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
                aws_session_token=SESSION_TOKEN,
            )
        return client
    except Exception as e:
        log.info("Role could not be assumed " + str(e))


def iam_user_password_last_used():

    log.info("[IAM] Console password last use ...")

    if account_name != HUB_ACCOUNT_NAME:
        iam_resource_users_all = assume_iam_resource.users.all()
    else:
        iam_resource_users_all = iam_resource.users.all()

    try:
        for iam_user in iam_resource_users_all:
            user_name = str(iam_user.LoginProfile()).split('\'')

            if iam_user.password_last_used:
                log.info("User has console access: " + str(iam_user))

                date_last_used = iam_user.password_last_used
                days_unused = (datetime.datetime.now() - date_last_used.replace(tzinfo=None)).days

                if days_unused >= 1:
                    last_login_console_delete.append(str(user_name[1]))
                break

            else:
                log.info('User has only programmatic access')
                last_login_console_delete.append(str(user_name[1]))

    except Exception as e:
        log.info("No user resources in the collection" + str(e))


def iam_list_access_keys():

    log.info("[IAM] Static key last use ...")

    last_date = 'LastUsedDate'

    try:
        if account_name != HUB_ACCOUNT_NAME:
            iam_resource_users_all = assume_iam_resource.users.all()
        else:
            iam_resource_users_all = iam_resource.users.all()

        for user in iam_resource_users_all:

            if account_name != HUB_ACCOUNT_NAME:
                metadata = assume_iam.list_access_keys(UserName=user.user_name)
            else:
                metadata = iam.list_access_keys(UserName=user.user_name)

            if metadata['AccessKeyMetadata']:
                for key in user.access_keys.all():

                    AccessId = key.access_key_id
                    Status = key.status

                    if account_name != HUB_ACCOUNT_NAME:
                        last_used = assume_iam.get_access_key_last_used(AccessKeyId=AccessId)
                    else:
                        last_used = iam.get_access_key_last_used(AccessKeyId=AccessId)

                    if Status == "Active":
                        if last_date in last_used['AccessKeyLastUsed']:
                            date_last_used = last_used['AccessKeyLastUsed'][last_date]
                            days_unused = (datetime.datetime.now() - date_last_used.replace(tzinfo=None)).days
                            if days_unused >= 90:
                                access_keys_last_delete.append(user.user_name)
                            else:
                                access_keys_last_keep.append(user.user_name)
                        else:
                            # Key is Active but never used
                            access_keys_last_delete.append(user.user_name)
                    else:
                        # Keys is inactive
                        access_keys_last_delete.append(user.user_name)
            else:
                # No keys for this user
                access_keys_last_delete.append(user.user_name)

    except Exception as e:
        log.info("No user resources in the collection", str(e))


def iam_users_to_nuke():

    log.info("IAM users to nuke ...")

    global account_name

    remove_access_keys = [item for item in access_keys_last_delete if item not in access_keys_last_keep]

    for console in last_login_console_delete:
        for static in remove_access_keys:
            if console == static:
                iam_users_to_clean.append(console)


def message_to_slack():

    users = ""
    for u in set(iam_users_to_clean):
        users += u + " "

    try:
        log.info("Sending message to Slack ...")

        if users != "":

            data = {
                'text': '***************************************************************\n'
                        + '* [' + account_name + '] IAM users have passwords and active access keys that have not been used within 90 days:* \n\n'
                        + '*IAM USERS:* ' + '`' + users + '`' + '\n'
                        + '***************************************************************',
                'username': 'CLOUD SNIPER BUDDY',
                'icon_emoji': ':robot_face:'
            }
            response = requests.post(WEBHOOK_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            log.info('Sending message to Slack. Response: ' + str(response.text) + ' Response Code: ' + str(response.status_code))
        else:
            log.info(str(account_name) + ": No IAM user has passwords and active access keys that have not been used within 90 days")

    except Exception as e:
        log.info("Message could not be send to Slack: " + str(e))


def put_to_s3():

    log.info("Sending findings to S3 ...")

    dataset = {
        'cloud.account.name': str(account_name),
        'cloud.account.users': str(iam_users_to_clean),
        'cloud.provider': 'aws'
    }

    NOW = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    s3_resource = boto3.resource('s3')
    bucket_name = BUCKET_NAME
    iam_path = IAM_PATH

    bucket = s3_resource.Bucket(name=bucket_name)

    if iam_path.startswith("/"):
        iam_path = iam_path[1:]
    if iam_path.endswith("/"):
        iam_path = iam_path[:-1]

    try:
        (bucket.Object(key=f"{iam_path}/iam_{NOW}.json")
               .put(Body=bytes(json.dumps(dataset).encode('UTF-8'))))
    except Exception as e:
        log.info("Could not put the object to S3" + str(e))


def cloud_sniper_iam(event, context):

    global assume_iam_resource
    global assume_iam
    global account_id
    global account_name
    global iam_users_to_clean
    global iam
    global iam_resource
    global access_keys_last_delete
    global access_keys_last_keep
    global last_login_console_delete
    global sts_connection

    s = boto3.session.Session(region_name=os.environ['AWS_REGION'])
    iam_resource = s.resource('iam')
    iam = s.client('iam')
    sts_connection = boto3.client('sts')

    assume_iam_resource = ""
    assume_iam = ""
    account_id = ""
    account_name = ""

    last_login_console_delete = []
    access_keys_last_delete = []
    access_keys_last_keep = []
    iam_users_to_clean = []

    for k, v in account_ids.items():
        account_name = k
        account_id = v
        del iam_users_to_clean[:]
        del last_login_console_delete[:]
        del access_keys_last_delete[:]
        del access_keys_last_keep[:]

        if account_name != HUB_ACCOUNT_NAME:
            assume_iam_resource = assume_role(account_id, 'iam-resource')
            assume_iam = assume_role(account_id, 'iam')

        try:
            iam_user_password_last_used()
            iam_list_access_keys()
            iam_users_to_nuke()
            message_to_slack()
            put_to_s3()

        except Exception as e:
            log.error('IAM report failed ' + str(e))
