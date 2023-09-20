#!/bin/bash

# Set script to exit on any errors.
set -e

## Source .env, if it exists
if [ -f .env ]; then
  source .env
fi

export EXAM_ROOT="temp"

# unzip zipped files if necessary
# ./unzip.sh
# run parsing and evaluators
python3 -c "import run"
