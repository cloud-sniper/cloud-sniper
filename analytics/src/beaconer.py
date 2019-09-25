#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import scipy.stats
import ipaddress
import numpy as np
import pandas as pd
import gzip
import datetime
import boto3

import results_generator


TMP_DOWNLOAD_DIR = "/tmp/s3_download"
TMP_REPORT_DIR = "/tmp/report"
PROCESS_LAST_HOURS = 10
now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
RESULTS_FNAME = "%s.json" % now
RESULTS_FNAME_PDF = "%s.pdf" % now

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

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("s3_bucket", help="AWS S3 bucket name where to read the vpc flows from and write the results")
    parser.add_argument("s3_input_path", help="path in the s3_backet to look for the data")
    parser.add_argument("s3_output_path", help="path in the s3_backet to write the results")

    return parser.parse_args()


def load_data(s3_bucket, s3_input_path):
    s3 = boto3.resource('s3')

    bucket = s3.Bucket(name=s3_bucket)
    prefix = s3_input_path
    if not prefix.endswith("/"): prefix += "/"

    if not os.path.exists(TMP_DOWNLOAD_DIR):
        os.mkdir(TMP_DOWNLOAD_DIR)
    for i, s3_file_obj in enumerate(bucket.objects.filter(Prefix=prefix)):
        bucket.download_file(s3_file_obj.key, TMP_DOWNLOAD_DIR + "/%06d" % i + ".log.gz")
        if i == 110: break

    data = []
    for fname in sorted(os.listdir(TMP_DOWNLOAD_DIR)):
        if not fname.endswith(".log.gz"):
            continue
        with gzip.open(os.path.join(TMP_DOWNLOAD_DIR, fname), 'r') as fd:
            first_line = True
            for line in fd:
                if first_line:
                    first_line = False
                    continue
                data.append(line.decode("utf-8").strip().split(" "))

    if len(data[0]) == len(FLOW_COLUMNS):
        df = pd.DataFrame(data, columns=FLOW_COLUMNS)
        df.drop(['date'], axis=1, inplace=True)
    else:
        df = pd.DataFrame(data, columns=FLOW_COLUMNS[1:])
    return df


def filter_format_data(df):
    df = df[df.srcaddr != "-"]
    df = df[df.dstaddr != "-"]
    df.drop(["version", "account-id", "interface-id", "srcport"], axis=1, inplace=True)
    df = df.replace("-", np.nan)
    df = df.replace("-", np.nan)
    df[["dstport", "protocol", "packets", "bytes", "start", "end"]] = \
        df[["dstport", "protocol", "packets", "bytes", "start", "end"]].apply(pd.to_numeric)
    return df


def sort_data(df):
    df['datetime'] = pd.to_datetime(df.start, unit='s')
    # TODO: should we process just the last hours?
    if PROCESS_LAST_HOURS:
        last_N_hs = max(df.datetime) - datetime.timedelta(hours=PROCESS_LAST_HOURS)
        df = df[df.datetime >= last_N_hs]
    df = df.set_index('datetime')
    df.sort_index(inplace=True)
    return df.reset_index(level=0)


def filter_useless_data(df):
    # Requirements
    # * srcIP should be private
    # * dstport < 1024 and != 123
    df = df[df.srcaddr.map(lambda x: ipaddress.ip_address(x).is_private)]
    df = df[df.dstport <= 1024]
    df = df[df.dstport != 123]
    return df


def filter_unfrequent_data(df):
    # remove communications if there were less than 24 snippets
    selection = df.groupby(["srcaddr", "dstaddr", "dstport"])
    df = selection.filter(lambda x: len(x) >= 24)
    df = df.reset_index(level=0)#, inplace=True)
    return df


def get_features(groups):
    features = {}
    histograms = {}

    def compute_features(series):
        res = []
        res.append(scipy.stats.skew(series, bias=False))
        res.append(np.std(series))
        res.append(series.kurt())
        return res

    for (srcaddr, dstaddr, port), traffic in groups:
        deltas = traffic.datetime - traffic.datetime.shift(1)
        deltas = deltas.dt.seconds/60
        deltas = deltas.fillna(0).astype(int)
        packets = traffic.packets.astype(int)
        bytes_ = traffic.bytes.astype(int)
        cond = deltas > 0
        deltas = deltas[cond]
        packets = packets[cond]
        bytes_ = bytes_[cond]
        if deltas.size == 0 or packets.size == 0 or bytes_.size == 0:
            continue
        ftrs = [compute_features(x) for x in [deltas, packets, bytes_]]
        ftrs = [x for sublist in ftrs for x in sublist] # flatten
        if (srcaddr, dstaddr, port) not in features:
            features[(srcaddr, dstaddr, port)] = []
        features[(srcaddr, dstaddr, port)].append(ftrs)
        histograms[(srcaddr, dstaddr, port)] = (deltas, packets, bytes_)
    return features, histograms


# Heuristics based classification
def classify(features):
    res = []
    for k in features:
        counter = 0
        feature = features[k][0]
        counter += feature[1] < 100 # deltas std
        counter += abs(feature[3]) < 10 # packages skew
        counter += feature[4] < 50 # packages std
        counter += abs(feature[5]) < 100 or np.isnan(feature[5]) # packages kurt
        counter += feature[7] < 5000 # bytes std
        counter += feature[8] < 50 or np.isnan(feature[8])# bytes kurt
        if counter >= 5:
            res.append(k)
    return res


def get_report(groups, histograms, keys):
    r = results_generator.ResultsGenerator()

    for (srcaddr, dstaddr, port) in keys:
        first = groups.get_group((srcaddr, dstaddr, port)).iloc[0]
        last = groups.get_group((srcaddr, dstaddr, port)).iloc[-1]

        deltas, packets, bytes_ = histograms[(srcaddr, dstaddr, port)]
        comm_hist = results_generator.Histogram()
        comm_hist.set_points(deltas.index.tolist(), deltas.values.tolist(), [True] * len(deltas))
        pack_hist = results_generator.Histogram()
        pack_hist.set_points(packets.index.tolist(), packets.values.tolist(), [True] * len(packets))
        bytes_hist = results_generator.Histogram()
        bytes_hist.set_points(bytes_.index.tolist(), bytes_.values.tolist(), [True] * len(bytes_))

        r.add_communication("", "", "", srcaddr, dstaddr, np.asscalar(port),
                            "", first.datetime.ctime(), last.datetime.ctime(),
                            comm_hist, pack_hist, bytes_hist)
    return r


def write_results(report, s3_bucket, s3_output_fname):
    s3 = boto3.resource('s3')
    s3.Object(s3_bucket, s3_output_fname).put(Body=report)


def write_pdf_report(grouped_df, bad_stuff, s3_bucket, s3_output_fname):
    if not os.path.exists(TMP_REPORT_DIR):
        os.mkdir(TMP_REPORT_DIR)
    tmp_fname = os.path.join(TMP_REPORT_DIR, RESULTS_FNAME_PDF)
    create_pdf_report(tmp_fname, grouped_df, bad_stuff)
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(tmp_fname, s3_bucket, s3_output_fname)


def create_pdf_report(tmp_fname, grouped_df, bad_stuff):
    REPORT_TITLE = "CLOUD SNIPER®"
    REPORT_SUBTITLE = "BEACONING DETECTION REPORT"
    REPORT_DATE = datetime.datetime.now().strftime("%B %d, %Y (at %H:%M)")

    import io
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates


    def add_text_to_doc(text, style="Normal", fontsize=12):
        Story.append(Spacer(1, 12))
        ptext = "<font size={}>{}</font>".format(fontsize, text)
        Story.append(Paragraph(ptext, styles[style]))
        Story.append(Spacer(1, 12))

    def plot_hist(x, xlabel, ylabel, title, color='b'):
        fig, ax = plt.subplots(figsize=(7, 1.8))
        plt.hist(x, bins=300, facecolor=color, rwidth=2)
        date_fmt = mdates.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(date_fmt)
        ax.set(title=title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300)
        buf.seek(0)
        plt.close()
        return buf

    styles=getSampleStyleSheet()
    doc = SimpleDocTemplate(tmp_fname,pagesize=letter,
                            rightMargin=inch/2,leftMargin=inch/2,
                            topMargin=72,bottomMargin=18)
    # Title section
    Story=[]
    Story.append(Image("./cloud_sniper_800.png", width=5*inch, height=1*inch))
    Story.append(Spacer(1, 200))
#     add_text_to_doc(REPORT_TITLE, style="Title", fontsize=24)
    add_text_to_doc(REPORT_SUBTITLE, style="Title", fontsize=24)
    add_text_to_doc("Report generated on " + REPORT_DATE, style="Title", fontsize=14)

    # Nothing to report
    if not bad_stuff:
        add_text_to_doc("No suspicious beaconing communications found :)")

    # Reporting for every suspicious communication
    image_buffers = []
    hist_size = (7*inch, 1.5*inch)
    for (srcaddr, dstaddr, dstport) in bad_stuff:
        Story.append(PageBreak())
        # subtitle describing the communication IP -> IP (port number)
        comm_description = "%s -> %s (port %s)" %(srcaddr, dstaddr, dstport)
        add_text_to_doc(comm_description, style="Title", fontsize=14)
        df = grouped_df.get_group((srcaddr, dstaddr, dstport))
        # plotting delta time
        plot = plot_hist(list(df.datetime), "Time (s)", "Frequency", 
                         "Communications in the last %i hours" %PROCESS_LAST_HOURS)
        image_buffers.append(plot)
        im = Image(image_buffers[-1], hist_size[0], hist_size[1])
        Story.append(im)
#         # plotting packets
#         hist = get_list_from_histogram(histograms["packets"])
#         plot = plot_hist(hist, "Number of packets sent", "Frequency", 
#                          "Packets sent distribution", color=(1,.5,0))
#         image_buffers.append(plot)
#         im = Image(image_buffers[-1], hist_size[0], hist_size[1])
#         Story.append(im)
#         # plotting bytes
#         hist = get_list_from_histogram(histograms["bytes"])
#         plot = plot_hist(hist, "Number of bytes sent", "Frequency", 
#                          "Bytes sent distribution", color='m')
#         image_buffers.append(plot)
#         im = Image(image_buffers[-1], hist_size[0], hist_size[1])
#         Story.append(im)

    doc.build(Story)
    for image_buffer in image_buffers:
        image_buffer.close()


if __name__ == "__main__":
    args = get_args()
    df = load_data(args.s3_bucket, args.s3_input_path)
    df = filter_format_data(df)
    df = sort_data(df)
    df = filter_useless_data(df)
    df = filter_unfrequent_data(df)
    groups = df.groupby(["srcaddr", "dstaddr", "dstport"])
    features, histograms = get_features(groups)
    bad_stuff_keys = classify(features)
    report = get_report(groups, histograms, bad_stuff_keys)
    s3_output_path = args.s3_output_path
    if not s3_output_path.endswith("/"): s3_output_path += "/"
    write_results(report.to_json(), args.s3_bucket, args.s3_output_path +  RESULTS_FNAME)
    write_pdf_report(groups, bad_stuff_keys, args.s3_bucket, args.s3_output_path + RESULTS_FNAME_PDF)

