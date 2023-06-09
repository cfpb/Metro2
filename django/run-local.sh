#!/bin/bash
set -e

echo "Setting up the django project..."

echo
echo "Running migrations"
python ./manage.py migrate

echo
echo "Adding a superuser with username 'admin'."
echo "Please set a password for your superuser (e.g. 'admin'):"
python ./manage.py createsuperuser --username=admin --email=""
echo "Log in with your superuser account at http://localhost:8000/admin"

echo
echo "Starting the server..."
python ./manage.py runserver