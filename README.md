# Overview

CFPB’s Metro2 Evaluator Tool (M2) evaluates Metro2 data for inaccuracies which may prove harmful to consumers’ credit. CFPB’s Supervision and Enforcement teams will use this tool while conducting cases and exams to find inaccuracies in entity-provided data and assess their potential harm to consumers. 

The application has a Django back-end which connects to a Postgres database. The back end fetches Metro2 data files from an S3 bucket, parses the relevant data into the database, and runs evaluators on the data. The back end also handles authorization for users and provides API endpoints to expose the evaluated data to the front end.

The front-end provides a React-based interface for authenticated and authorized users and allows them to interact with the data.

## Sections
- [Deployments](#deployments)
    - [Alto Dev](#alto-dev)
    - [Alto Staging](#alto-staging)
    - [Alto Prod](#alto-prod)
- [Deploying the project](#deploying)
- [Running the project](#running-the-project)
    - [Running in Helm](#running-in-helm)
    - [Running in docker-compose](#running-in-docker-compose)
    - [Running jobs individually](#individual-jobs)
- [Testing](#testing)
  - [Running tests and checking coverage](#running-tests-and-checking-coverage)


# Deployments

TODO: add documentation about how to deploy, how to upload data in a deployed environment, how to configure a deployment, etc.

## Alto Dev

- [Metro2 ALTO Dev Internal Jenkins](https://INTERNAL)

## Alto Staging

- [Metro2 ALTO Staging Internal Jenkins](https://INTERNAL)

## Alto Prod

Not currently available

# Running the project locally

Choose the way to run the project that best suits your needs:
1. **Helm** is the way the project will run in deployed environments. Use this when you need a production-like setup and you don't need the code to reload when there are local changes.
2. **Docker-compose** is best for local development. It allows dynamically reloading code while still providing all parts of the project setup.
3. It is also possible to run some of the sub-projects locally, but this is usually only practical for active development on a specific aspect of the codebase.

## Running in Helm

When running locally a helm deployment locally, we use the docker-desktop cluster that comes with Docker.
To prepare your environment, make sure that you have [kubernetes enabled in Docker](https://docs.docker.com/desktop/kubernetes/).
Install helm (`brew install helm`) and optionally install [OpenLens](https://github.com/MuhammedKalkan/OpenLens) for better visualization.

With that in place, you must do the following:
    1. Ensure that your Docker daemon is running.
        - Without Docker running, your docker-desktop cluster will not be running.
    2. Run `build-images.sh -e local`
    3. Run `helm-install.sh`

This will deploy the Metro2 Application to the Docker Desktop Cluster and create three images:
    1. metro2-frontend:local
    2. metro2-evaluator:local
    3. metro2-django:local

## Running in docker-compose

If docker desktop is not already installed, please [download and install it](https://www.docker.com/products/docker-desktop/).

`docker-compose build` to build the images.

`docker-compose up` or `docker-compose up -d` to run the application.

To connect to a running container, (e.g. to run scripts or tests), `docker-compose exec [container-name] sh`, where `[container-name]` is one of the services named in [docker-compose.yml](/docker-compose.yml), i.e. `django` or `frontend`.

To bring down the created containers when you are done with them, run `docker-compose down`. To also remove volumes at the same time, run `docker-compose down -v`. To remove images in addition to volumes, run `docker-compose down --rmi "all" -v`.


## Individual jobs

Both the **django** and **front-end** code bases can be run locally. See the README for each subdirectory for instructions.

# Testing

## Running tests and checking coverage

**For the `django` code:**

1. Connect to the django container: while the docker-compose setup is running, `docker-compose exec django sh`
2. Run the tests: once connected to the container, run `coverage run ./manage.py test`
2. Check test coverage: `coverage report` or `coverage html`

**For the `front-end` code:**

1. Install any front-end dependencies listed in [front-end/README.md](/front-end/README.md)
2. Run linting and tests: From the `/front-end` directory, run `yarn validate`
