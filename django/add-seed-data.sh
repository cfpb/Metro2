#!/bin/sh
set -e

echo "Setting up the seed data..."

echo
echo "Add Evaluator MetaData to the database"
python manage.py import_evaluator_metadata -f evaluate_m2/m2_evaluators/eval_metadata.csv

echo
echo "Parse the seed data files"
python manage.py parse_local -e Sample-Dataset-007
echo
echo "Run Evaluate on the seed data"
python manage.py run_evaluators --e 1
