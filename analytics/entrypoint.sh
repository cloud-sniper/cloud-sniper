#!/bin/bash

source environment.env

python beaconer.py ${S3_BUCKET} ${S3_INPUT_PATH} ${S3_OUTPUT_PATH}
