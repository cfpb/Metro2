#!/bin/sh
set -e

echo "Setting up the seed data..."

echo
echo "Adding a superuser with username 'admin'."
python ./manage.py generate_admin_user --username=admin --password=admin

echo
echo "Add Evaluator MetaData to the database"
python manage.py import_evaluator_metadata -f evaluate_m2/m2_evaluators/eval_metadata.csv

echo
echo "Parse the data file and run the evaluators"
python manage.py parse_evaluate_local -e Sample-Dataset-007

echo
echo "Add the user as a member of the event"
python manage.py add_user_to_event --event=Sample-Dataset-007 --user=admin
