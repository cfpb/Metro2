# Metro2 Django

The Metro2 Django app parses Metro2 data, runs evaluators, manages user access, and provides an API to support the React front-end.

# Sections
- Two ways to run the project:
    - How to run in docker-compose
    - How to run locally in a virtualenv


## How to run in docker-compose (recommended)
If you have docker-compose installed, this will be the simplest strategy.
If not, you can use the instructions under [[How to run locally]] below.
Running in docker-compose uses the Django settings specified in `django_application/settings/docker-compose.py` and connects to a PostgreSQL database that is managed by docker-compose.

Running the project:
1. From the Metro2 project root, run `docker compose build` and `docker compose up` to get the app running.
When docker-compose starts the project, it automatically runs the database migrations, so you don't need to do so manually.
It will also run a script that:
  - Adds Evaluator Metadata to the database if it does not already exist.
  - Creates a Metro2Event called Sample-Dataset-007 if it doesn't already exist, parses all data files in the `local_data` directory, and evaluates them.
  - Adds an administrator user that has access to the Sample-Dataset-007 event.
Once it is running, you can see the app running by visiting http://localhost:3000/.

**Other useful actions in the system while running in docker-compose:**

To run the tests and view coverage:
1. Enter the Django container: `docker compose exec django sh`.
2. Run `coverage run manage.py test` to run the test suite and calculate coverage.
3. View the coverage report in the container with `coverage report`.
4. View the coverage report in the browser:
    - Run `coverage html` in the container. This will generate a directory `htmlcov` with all the HTML coverage files.
    - Locate and double-click on the `index.html` file in Finder `{Metro2 Directory}/django/htmlcov/` to open the coverage report in the browser.

Full documentation for the coverage libarary is [here](https://coverage.readthedocs.io/en/7.3.2/).

Use the Django shell to interact with the codebase:
1. Run `docker compose exec django sh` to enter the running container
2. Use `python manage.py shell` to start the interactive python console for this project.

[Here's a useful resource](https://studygyaan.com/django/django-shell-tutorial-explore-your-django-project) on how the Django shell can be useful for development.

Use the Django administrator interface:
1. If you already have a superuser login, skip to step 4. If one is needed, do steps 2 and 3:
2. Enter the Django container: `docker compose exec django sh`.
3. Run `python manage.py generate_admin_user --username=admin --password=admin` (or you can substitute whatever admin username you want).
4. Log in to the admin interface at http://localhost:8000/admin/ using the username and password you entered in the previous step.

Run the parser:
1. Use the administrator view to create an event record.
    - In the `directory` field, enter a file location with Metro2 files, such as `parse_m2/local_data/`.
2. After saving the event record, take note of the event ID (can be found in the URL).
3. Enter the Django container: `docker compose exec django sh`.
4. Run `python manage.py parse -e [event_id]` to parse the files from the provided directory.

Run the evaluators for an event:
1. Enter the Django container: `docker compose exec django sh`.
2. Run `python manage.py evaluate -e [event_ID]` to run the evaluators on a dataset associated to the provided event.
    - If there are existing evaluator results for this event, the previous results will be deleted before running the evaluator.
    - You can also use `python manage.py evaluate -h` for the help text.


To run the lint checks:
1. Enter the Django container: `docker compose exec django sh`.
1. Run `ruff check .`


## How to run locally
You can use this strategy if docker-compose isn't working for you, for whatever reason.
This uses the Django settings specified in `django_application/settings/local.py`, including using a SQLite database instead of PostgreSQL.

Instructions for running locally (for now):
1. Prepare a python environment. I used pyenv-virtualenv.
2. From the metro2 project root, `pip install -r django/requirements.txt`
3. `./django/manage.py migrate`
4. If you want to run the server: `./django/run-local.sh`, then visit localhost:8000/admin to log in to the admin site
5. If you want to access the python console for the project: `./manage.py shell`

All of the useful actions listed above for use in docker-compose can also be used in the local virtualenv.
