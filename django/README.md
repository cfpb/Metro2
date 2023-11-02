This Django app is the future home of the user-facing Metro2 results app.

How to run this app locally, for now:
1. Prepare a python environment. I used pyenv-virtualenv.
2. From the metro2 project root, `pip install -r django/requirements.txt`
3. `./django/manage.py migrate`
4. If you want to run the server: `./django/run-local.sh`, then visit localhost:8000/admin to log in to the admin site
5. If you want to access the python console for the project: `./manage.py shell`

To run the lint checks:
1. `ruff check django/`

To run the tests and check test coverage:
1. Run the tests: `coverage run ./django/manage.py test`
2. Check test coverage: `coverage report` or `coverage html`
