import os
import ipaddress
import numpy as np
import pandas as pd
import datetime
import boto3
import gzip
import json

from signal_processing import signalProcess

BUCKET_NAME = os.environ.get("BUCKET_NAME", None)
VPC_FLOW_LOGS_PATH = os.environ.get("VPC_FLOW_LOGS_PATH", None)
FINDINGS_PATH = os.environ.get("FINDINGS_PATH", None)

TMP_DOWNLOAD_DIR = "/tmp/s3_download"

FLOW_COLUMNS = [
    "date",
    "version",
    "account-id",
    "interface-id",
    "srcaddr",
    "dstaddr",
    "srcport",
    "dstport",
    "protocol",
    "packets",
    "bytes",
    "start",
    "end",
    "action",
    "log-status",
]

def cloud_sniper_beaconing_detection(event, context):
    bucket_name = BUCKET_NAME
    vpc_flow_logs_path = VPC_FLOW_LOGS_PATH
    findings_path = FINDINGS_PATH
    df = load_data(bucket_name, vpc_flow_logs_path)
    print(f"Number of raw records: {len(df.index)}")
    version = df.version.iloc[0]  # constant
    account_id = df["account-id"].iloc[0]  # constant
    df = filter_format_data(df)
    print(f"Number of records after filtering missing data: {len(df.index)}")
    df = sort_data(df)
    print(f"Number of records after filtering by time: {len(df.index)}")
    df = filter_useless_data(df)
    print(f"Number of records after filtering by port: {len(df.index)}")
    df = filter_unfrequent_data(df)
    print(f"Number of records after filtering unfrequent: {len(df.index)}")
    res = find_beacons(df)
    new_fields = {
        "hits": "",
        "cloud.provider": "aws",
        "event.type": "beaconing",
        "cloud.account.name": "",
        "interface.vpc.id": "",
        "protocol": "",
        "version": version,
        "cloud.account.id": account_id,
    }
    list(map(lambda x: x.update(new_fields), res))
    print(f"Result: {res}")

    save_results(bucket_name, findings_path, res)

    return res


def load_data(s3_bucket, s3_vpc_flow_logs_path):
    s3 = boto3.resource('s3')

    bucket = s3.Bucket(name=s3_bucket)
    prefix = s3_vpc_flow_logs_path
    if prefix.startswith("/"):
        prefix = prefix[1:]
    if not prefix.endswith("/"):
        prefix += "/"

    if not os.path.exists(TMP_DOWNLOAD_DIR):
        os.mkdir(TMP_DOWNLOAD_DIR)
    for i, s3_file_obj in enumerate(bucket.objects.filter(Prefix=prefix)):
        if s3_file_obj.key.endswith(".log.gz"):
            extension = "log.gz"
        elif s3_file_obj.key.endswith(".log"):
            extension = "log"
        else:
            continue
        bucket.download_file(s3_file_obj.key,
                             TMP_DOWNLOAD_DIR + "/%06d" % i + "." + extension)

    data = []
    for fname in sorted(os.listdir(TMP_DOWNLOAD_DIR)):
        if fname.endswith(".log.gz"):
            open_ = gzip.open
            decode = True
        elif fname.endswith(".log"):
            open_ = open
            decode = False
        else:
            continue
        with open_(os.path.join(TMP_DOWNLOAD_DIR, fname), 'r') as fd:
            first_line = True
            for line in fd:
                if first_line:
                    first_line = False
                    continue
                if decode:
                    line = line.decode("utf-8").strip().split(" ")
                else:
                    line = line.strip().split(" ")
                data.append(line)

    if data and (len(data[0]) == len(FLOW_COLUMNS)):
        df = pd.DataFrame(data, columns=FLOW_COLUMNS)
        df.drop(['date'], axis=1, inplace=True)
    else:
        df = pd.DataFrame(data, columns=FLOW_COLUMNS[1:])
    return df


def filter_format_data(df):
    df = df[df.srcaddr != "-"]
    df = df[df.dstaddr != "-"]
    df.drop(["version", "srcport"], axis=1, inplace=True)
    df = df.replace("-", np.nan)
    df = df.replace("-", np.nan)
    df[["dstport", "protocol", "packets", "bytes", "start", "end"]] = \
        df[["dstport", "protocol", "packets", "bytes", "start", "end"]] \
        .apply(pd.to_numeric)
    return df


def sort_data(df):
    df['datetime'] = pd.to_datetime(df.start, unit='s')
    # TODO: should we process just the last hours?
    df = df.set_index('datetime')
    df.sort_index(inplace=True)
    return df.reset_index(level=0)


def filter_useless_data(df):
    # Requirements
    # * srcIP should be private
    # * dstport < 1024 and != 123
    if df.empty:
        return df
    df = df[df.srcaddr.map(lambda x: ipaddress.ip_address(x).is_private)]
    df = df[df.dstport <= 1024]
    df = df[df.dstport != 123]
    return df


def filter_unfrequent_data(df):
    # remove communications if there were less than 6 snippets
    selection = df.groupby(["srcaddr", "dstaddr", "dstport"])
    df = selection.filter(lambda x: len(x) >= 6)
    df = df.reset_index(level=0)
    return df


def find_beacons(df):
    res = []
    time_fmt = "%Y-%m-%dT%H:%M:%S.%f"
    groups = df.groupby(["srcaddr", "dstaddr", "dstport"])
    data_in = {
        "data": {},
        "time": {}
    }
    for (srcaddr, dstaddr, port), traffic in groups:
        k = (srcaddr, dstaddr, port)
        data_in["data"][k] = traffic.bytes
        data_in["time"][k] = traffic.datetime
    lrner = signalProcess(data_in, options_in=None)
    output = lrner.getPrimaryPeriods()
    for (srcaddr, dstaddr, port) in output["powers"]:
        if output["powers"][(srcaddr, dstaddr, port)][0] is not None:
            print(data_in["time"][k])
            k = (srcaddr, dstaddr, port)
            start_time = data_in["time"][k].iloc[0].strftime(time_fmt)[:-3] + 'Z'
            end_time = data_in["time"][k].iloc[-1].strftime(time_fmt)[:-3] + 'Z'
            res.append({
                "source.ip": srcaddr,
                "destination.ip": dstaddr,
                "destination.port": int(port),
                "timestamp": start_time,
                "event.end": end_time,
                "event.start": start_time
            })
    return res


def save_results(bucket_name, findings_path, res):
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(name=bucket_name)
    if findings_path.startswith("/"):
        findings_path = findings_path[1:]
    if findings_path.endswith("/"):
        findings_path = findings_path[:-1]

    (bucket.Object(key=f"{findings_path}/beaconing_detection_{now}.json")
           .put(Body=bytes(json.dumps(res).encode('UTF-8'))))


if __name__ == "__main__":
    print(json.dumps(cloud_sniper_beaconing_detection(None, None), indent=4))
