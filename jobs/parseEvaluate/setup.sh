#!/bin/bash

# Set script to exit on any errors.
set -e

## Source .env, if it exists
if [ -f .env ]; then
  source .env
fi

# check for arguments and set exam constants
if [ -z $EXAM_NUMBER ] || [ -z $INDUSTRY_TYPE_CODE ]; then
    echo "Please provide valid .env file before running: docker compose up"
    exit 1
fi

# strip all non-numeric characters from exam number
CLEANED_EXAM_NUMBER=${EXAM_NUMBER//[^0-9]/}
# strip all non-alphabetic characters from industry type code
CLEANED_INDUSTRY_TYPE_CODE=${INDUSTRY_TYPE_CODE//[^a-zA-z]/}
# replace env variables with cleaned versions
export EXAM_NUMBER=$CLEANED_EXAM_NUMBER
export INDUSTRY_TYPE_CODE=$CLEANED_INDUSTRY_TYPE_CODE
export EXAM_ROOT="exam-${EXAM_NUMBER}"

# create required directory structure
mkdir -p $EXAM_ROOT/{data,reference}
mkdir results

./ingest-data.sh
./unzip.sh
# run parsing and evaluators
python3 -c "import run"
