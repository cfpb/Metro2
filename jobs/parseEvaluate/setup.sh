#!/bin/bash

# Set script to exit on any errors.
set -e

## Source .env, if it exists
if [ -f .env ]; then
  source .env
fi

# check for arguments and set exam constants
if [ -z $EXAM_NUMBER ] ; then
    echo "Please provide valid .env file before running: docker compose up"
    exit 1
fi

# strip all non-numeric characters from exam number
CLEANED_EXAM_NUMBER=${EXAM_NUMBER//[^0-9]/}
# replace env variables with cleaned versions
export EXAM_NUMBER=$CLEANED_EXAM_NUMBER
# the file system location(local) where M2 data files are located, will be updated for s3 bucket
export EXAM_ROOT="temp"

# unzip zipped files if necessary
# ./unzip.sh
# run parsing and evaluators
python3 -c "import run"
