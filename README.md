# Overview

CFPB’s Metro2 Evaluator Tool (M2) evaluates Metro2 data for inaccuracies which may prove harmful to consumers’ credit.

The application has a Django back-end which connects to a Postgres database. The back end fetches Metro2 data files from an S3 bucket, parses the relevant data into the database, and runs evaluators on the data. The back end also handles authorization for users and provides API endpoints to expose the evaluated data to the front end. The front-end provides a React-based interface for authenticated and authorized users and allows them to interact with the data.

## Sections
- [Running the project locally](#running-the-project-locally)
    - [Running in docker-compose](#running-in-docker-compose)
- [Management commands](#running-management-commands)
- [Handling evaluator metadata](#handling-evaluator-metadata)
- [Testing](#testing)
  - [Running tests and checking coverage](#running-tests-and-checking-coverage)


# Running the project locally
**Docker-compose** is best way to run Metro2 for local development. It allows dynamically reloading code while still providing all parts of the project setup.

It is also possible to run some of the sub-projects **locally**, but this is usually only practical for active development on a specific aspect of the codebase.

## Running in docker-compose
If docker desktop is not already installed, please [download and install it](https://www.docker.com/products/docker-desktop/).

`docker-compose build` to build the images.

`docker-compose up` or `docker-compose up -d` to run the application.

The front end is served by Vite in development mode at http://localhost:3000. The Django app runs on port 8000 and the admin can be accessed at http://localhost:8000/admin/.

To connect to a running container, (e.g. to run scripts or tests), `docker-compose exec [container-name] sh`, where `[container-name]` is one of the services named in [docker-compose.yml](/docker-compose.yml), i.e. `django` or `frontend`.

To bring down the created containers when you are done with them, run `docker-compose down`. To also remove volumes at the same time, run `docker-compose down -v`. To remove images in addition to volumes, run `docker-compose down --rmi "all" -v`.

## Individual jobs
Both the **Django** and **Front-end** code bases can be run locally. See the README for each subdirectory for instructions.

# Running management commands
Django management commands are used for several essential actions in the Metro2 application, including parsing new data, running evaluators, and importing evaluator metadata from CSV.
To see the full list of available management commands, run `python manage.py help` from the django directory.
In local environments, use the command line to run these commands.

# Handling evaluator metadata

Each evaluator has several metadata fields associated with it, such as name, short description, long description, fields used, rationale, and more.
We seed the database with initial metadata about each evaluator, then allow users to modify some of the fields.

## Evaluator CSV format
When importing and exporting evaluator metadata, we use a CSV with the following columns:
`id`,`category`,`description`,`long_description`,`fields_used`,`fields_display`,`rationale`,`potential_harm`,`alternate_explanation`,`crrg_reference`

The `id` column is what we use to connect the evaluator metadata to the evaluator function, which is defined in code.
This means that the `id` column needs to exactly match the name of the function in the code.
If the names don't match, any evaluator results won't be correctly associated with the evaluator in the system.

## Importing metadata
Do this when deploying the project to a new environment to create evaluator metadata records in the database.

How to import the evaluator metadata into the system:
1. Create a CSV of all known evaluator metadata using the format described above.
2. Save the CSV to this repo using the following filename: `evaluate_m2/m2_evaluators/eval_metadata.csv`.
3. Import the metadata by running the following Django management command in the environment where the metadata should be imported: `python manage.py import_evaluator_metadata`.
    - This command will update any existing records with the new metadata and create any that don't already exist. It won't delete existing records that are missing from the csv.

## Exporting metadata
Do this when users have made manual updates to the evaluator metadata and you want to propagate those updates to another environment.

How to export the evaluator metadata:
1. Visit the `/all-evaluator-metadata` endpoint for the environment in the browser.
    - This will download a CSV of all evaluator metadata in the system, which you can import into any Metro2 environment.


# Testing

## Running tests and checking coverage

**For the Django code:**

1. Connect to the Django container: while the docker-compose setup is running, `docker-compose exec django sh`
2. Run the tests: once connected to the container, run `coverage run ./manage.py test`
2. Check test coverage: `coverage report` or `coverage html`

**For the Front-end code:**

1. Install any front-end dependencies listed in [front-end/README.md](/front-end/README.md)
2. Run linting and tests: From the `/front-end` directory, run `yarn validate`
