#!/bin/bash

# Set script to exit on any errors.
set -e

# check for arguments and set exam constants
if [ -z $EXAM_NUMBER ] || [ -z $INDUSTRY_TYPE_CODE ]; then
    echo "Please provide valid .env file before running: docker compose up"
    exit 1
fi

export EXAM_ROOT="exam-${EXAM_NUMBER}"

# create required directory structure
mkdir -p $EXAM_ROOT/{data,reference,results}

./ingest-data.sh
./unzip.sh
# run parsing and evaluators
python3 -c "import metro2.run"
