#!/bin/bash

# Set script to exit on any errors.
set -e

if [ -z $METRO2ENV ]; then
    echo "Runtime environment not set. Please set a runtime environment."
    exit 1
fi

if [ $METRO2ENV == "local" ]; then
    cp -a ./local/data/. $EXAM_ROOT/data/
    cp -a ./local/reference/. $EXAM_ROOT/reference/
fi
