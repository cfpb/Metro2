This Django app is the future home of the user-facing Metro2 results app.

There are two ways to run Django for local development: in the docker-compose setup and in a local virtualenv.

## How to run in docker-compose (recommended)
If you have docker-compose installed, this will be the simplest strategy.
From the Metro2 project root, run `docker-compose build` and `docker-compose up` to get the app running.
When docker-compose starts the project, it automatically runs the database migrations, so you don't need to do so manually.
Once it is running, you can see the app running by visiting http://localhost:8000/.

### Running the tests
First, enter the django container by running `docker-compose exec django sh`.
Next, you can run `coverage run manage.py test` to run the test suite and calculate coverage.
View the coverage report with `coverage report` (full documentation for the coverage libarary is [here](https://coverage.readthedocs.io/en/7.3.2/)).
(TODO: figure out how to view the HTML version of the coverage report when running in docker-compose)

### Using the django shell
Another way to interact with the codebase is via the django shell.
[Here's a useful resource](https://studygyaan.com/django/django-shell-tutorial-explore-your-django-project) on how the django shell can be useful for development.
To use it, run `docker-compose exec django sh` to enter the running container, then use `python manage.py shell` to start the interactive python console for this project.

### Using the django administrator interface
First you'll need to create an admin account. (TODO: maybe we could automate this).
Note that if you've already done this, the account will still exist, unless you've deleted your local database.

To so so, first enter the django container by running `docker-compose exec django sh`.
Next, `python ./manage.py createsuperuser --username=admin --email=""` (or you can substitute whatever admin username you want).
The `createsuperuser` script will ask you to enter a password twice.

Once you have done that, you can log in to the admin interface at http://localhost:8000/admin using the username and password you entered in the previous step.

## How to run locally
You can use this strategy if docker-compose isn't working for you, for whatever reason.

Instructions for running locally (for now):
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
