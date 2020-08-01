import os
import shutil
import argparse
import tempfile
import csv
import urllib.request
import zipfile

from distutils.dir_util import copy_tree


SCRIPT_FNAME = os.path.realpath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_FNAME)
PACKAGE_DIR = os.path.join(SCRIPT_DIR, "package")
BUILD_DIR = os.path.join(SCRIPT_DIR, "build_dir")


def download_dependencies(dependencies_fname, output_folder):
    """Download the dependencies of a lambda function, listed in a csv file

    Args:
        dependencies_fname (str): file name of csv file listing dependencies
        output_folder (str): location where dependencies are downloaded to
    """
    dependencies_urls = []
    with open(dependencies_fname) as fd:
        reader = csv.reader(fd)
        for row in reader:
            dependencies_urls.append(row)

    for name, url in dependencies_urls:
        whl_path = os.path.join(output_folder, name + ".whl")
        urllib.request.urlretrieve(url, whl_path)
        with zipfile.ZipFile(whl_path, "r") as zip_ref:
            zip_ref.extractall(output_folder)
        os.remove(whl_path)


def process_folder(dir_path):
    """Check if dir_path contains a python lambda function and create a package

    Args:
        dir_path (str): directory where to check for a lambda implementation
    """
    candidate_folder = os.path.join(dir_path, "lambdas", "python")
    if os.path.exists(candidate_folder):
        print(f"Found lambdas candidates in {candidate_folder}")
        for source_folder in os.listdir(candidate_folder):
            source_folder = os.path.join(candidate_folder, source_folder)
            dependencies = os.path.join(source_folder, "dependencies.csv")
            if os.path.isdir(source_folder) and os.path.exists(dependencies):
                print(f"Processing lambda function from {source_folder}")
                package_name = source_folder.split(os.sep)[-1]
                tmp_folder = tempfile.mkdtemp()
                download_dependencies(dependencies, tmp_folder)
                copy_tree(source_folder, tmp_folder)
                if not os.path.exists(BUILD_DIR):
                    os.makedirs(BUILD_DIR)
                shutil.make_archive(os.path.join(BUILD_DIR, package_name),
                                    'zip', tmp_folder, "./")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build script for AWS lambda')
    args = parser.parse_args()

    for dir_path in os.listdir(SCRIPT_DIR):
        if os.path.isdir(dir_path):
            process_folder(dir_path)

    # print("Build output path", tmp_folder)
