from datetime import datetime
import io

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

import numpy as np
import matplotlib.pyplot as plt



REPORT_TITLE = "CLOUD SNIPER®"
REPORT_SUBTITLE = "BEACONING DETECTION REPORT"
REPORT_DATE = datetime.now().strftime("%B %d, %Y (at %H:%M)")


def get_list_from_histogram(histogram):
    x = []
    for entry in histogram:
        x += entry["frequency"] * [entry["value"]]
    return x


def plot_hist(x, xlabel, ylabel, title, color='b'):
    n, bins, patches = plt.hist(x, facecolor=color, alpha=0.75)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    buf.seek(0)
    plt.close()

    return buf


def create_report(fname, report):
    def add_text_to_doc(text, style="Normal", fontsize=12):
        Story.append(Spacer(1, 12))
        ptext = "<font size={}>{}</font>".format(fontsize, text)
        Story.append(Paragraph(ptext, styles[style]))
        Story.append(Spacer(1, 12))

    styles=getSampleStyleSheet()
    doc = SimpleDocTemplate(fname,pagesize=letter,
                            rightMargin=inch/2,leftMargin=inch/2,
                            topMargin=72,bottomMargin=18)
    # Title section
    Story=[]
    Story.append(Spacer(1, 200))
    add_text_to_doc(REPORT_TITLE, style="Title", fontsize=24)
    add_text_to_doc(REPORT_SUBTITLE, style="Title", fontsize=24)
    add_text_to_doc("Report generated on " + REPORT_DATE, style="Title", fontsize=14)

    # Nothing to report
    if not report.get("suspiciousCommunications"):
        add_text_to_doc("No suspicious beaconing communications found :)")

    # Reporting for every suspicious communication
    image_buffers = []
    hist_size = (4.5*inch, 2.7*inch)
    for comm in report.get("suspiciousCommunications"):
        Story.append(PageBreak())
        # subtitle describing the communication IP -> IP (port number)
        comm_description = "%s -> %s (port %s)" %(comm["srcIp"], comm["dstIp"], comm["dstPort"])
        add_text_to_doc(comm_description, style="Title", fontsize=14)
        histograms = comm["histograms"]
        # plotting delta time
        hist = get_list_from_histogram(histograms["communicationDeltaTime"])
        plot = plot_hist(hist, "Delta time (s)", "Frequency", 
                         "Delta time between consecutive communications")
        image_buffers.append(plot)
        im = Image(image_buffers[-1], hist_size[0], hist_size[1])
        Story.append(im)
        # plotting packets
        hist = get_list_from_histogram(histograms["packets"])
        plot = plot_hist(hist, "Number of packets sent", "Frequency", 
                         "Packets sent distribution", (1,.5,0))
        image_buffers.append(plot)
        im = Image(image_buffers[-1], hist_size[0], hist_size[1])
        Story.append(im)
        # plotting bytes
        hist = get_list_from_histogram(histograms["bytes"])
        plot = plot_hist(hist, "Number of bytes sent", "Frequency", 
                         "Bytes sent distribution", 'm')
        image_buffers.append(plot)
        im = Image(image_buffers[-1], hist_size[0], hist_size[1])
        Story.append(im)

    doc.build(Story)
    for image_buffer in image_buffers:
        image_buffer.close()

