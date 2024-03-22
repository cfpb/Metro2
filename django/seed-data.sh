#!/bin/sh
set -e

echo "Setting up the seed data..."

echo
echo "Add Evaluator MetaData to the database"
python manage.py import_evaluator_metadata -f evaluate_m2/m2_evaluators/eval_metadata.csv

echo
echo "Parse the data file and running the evaluators"
python manage.py parse_local_and_evaluate -e Sample-Dataset-007
echo
