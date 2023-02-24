#!/bin/bash

# Set script to exit on any errors.
set -e

if [ -z $METRO2ENV ] || [ -z $APP_HOME ]; then
    echo "Runtime environment not set. Please set a runtime environment."
    exit 1
fi

if [ $METRO2ENV == "local" ]; then
    cp -a $APP_HOME/local/data/. $EXAM_ROOT/data/
    cp -a $APP_HOME/local/reference/. $EXAM_ROOT/reference/
fi
