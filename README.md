# Overview

The purpose of the Metro2 evaluator tool is to automate as much as possible in regard to parsing, evaluating, and analyzing Metro2 data. The tool will be used by SEFL to assist with cases and exams.

The application consists of three main components:
- The **evaluator** job ingests and saves Metro2 data, then runs a set of evaluators on the data and saves the results
- The two components of the user-facing portion of the application:
    - The **Django** container handles internal permissions and retrieves data from the results database to populate the front end
    - The **front-end** container provides a visual interface for authenticated and authorized users and allows them to interact with the data

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
## Alto Dev

Not currently available

|Server|IP Address|Name|
|------|----------|----|

## Alto Staging

Not currently available

|Server|IP Address|Name|
|------|----------|----|

## Alto Prod

Not currently available

|Server|IP Address|Name|
|------|----------|----|


# Deploying

TODO: add documentation about how to deploy, how to upload data in a deployed environment, how to configure a deployment, etc.

# Running the project

Choose the way to run the project that best suits your needs:
1. **Helm** is the way the project will run in deployed environments. Use this when you need a production-like setup and you don't need the code to reload when there are local changes.
2. **Docker-compose** is best for local development. It allows dynamically reloading code while still providing all parts of the project setup.
3. It is also possible to run some of the sub-projects locally, but this is usually only practical for active development on a specific aspect of the codebase.

For both the Helm and Docker-compose setup, first you'll need to prepare data for the evaluator:

## Prepare your environment

In order to run the parseEvaluate job locally, sample data needs to be present in your local environment.
We use a set of sample de-identified data (data with all PII removed) provided by SEFL.
If you need to download the sample files, ask a team member where they are saved.

When the job runs locally, it expects to find the following files to copy from a local directory located at `[project-root]/jobs/parseEvaluate/temp`. The files in the `data` directory should be Metro2 data files. The `sample-map.xlsx` should be a Metro2 data mapping file, as described in [parseEvaluate/README.md](/jobs/parseEvaluate/README.md)

- `jobs/parseEvaluate/temp/`
  - `data/`
    - `data-file.txt` (can be named anything as long as the file extension is .txt)
    - `data-file2.txt` (can be named anything as long as the file extension is .txt)
    - ...
  - `jobs/parseEvaluate/reference/`
    - `sample-map.xlsx` (keep this name consistent)

TODO: In future releases, replace the reference file with in-code data dictionary.

## Running in Helm

Install helm (`brew install helm`) and optionally install [OpenLens](https://github.com/MuhammedKalkan/OpenLens) for better visualization.

Enable Kubernetes in Docker Desktop under `Settings` > `Kubernetes`.

Before building the metro2 helm charts, run `build-images.sh`.

After building images, run `helm-install.sh`.

### Running the evaluator in Helm

After `helm-install.sh` brings up the containers, it automatically runs the `parseEvaluate`job.
Currently, this job runs on the data in the local `temp` folder.
In (future) deployed environments, the job will run on data in an S3 bucket.

## Running in docker-compose

If docker desktop is not already installed, please [download and install it](https://www.docker.com/products/docker-desktop/).

### Copy .env_SAMPLE to .env and change values

`.env_SAMPLE` contains environment variables that will be fed into the application. In order for the file to be recognized by docker compose, run `cp .env_SAMPLE .env`.

TODO: There may be a cleaner, more secure way to send variables to the container.

### Run the project

`docker-compose build` to build the images.

`docker-compose up` or `docker-compose up -d` to run the application.

To connect to a running container, (e.g. to run scripts or tests), `docker-compose exec [container-name] sh`, where `[container-name]` is any of the services named in [docker-compose.yml](/docker-compose.yml), such as `evaluator`, `django`, or `frontend`.

To bring down the created containers when you are done with them, run `docker-compose down`. To also remove volumes at the same time, run `docker-compose down -v`. To remove images in addition to volumes, run `docker-compose down --rmi "all" -v`.

### Running the evaluator in docker-compose

In docker-compose, the evaluator job does not run automatically.
When the docker-compose setup is running, you can use `docker-compose exec evaluator sh` to connect to the container, then run `./setup.sh`. This ingests the files in the `temp` folder and runs the evaluators on them.

## Individual jobs

Both the **django** and **front-end** code bases can be run locally. See the README for each subdirectory for instructions.

# Testing

## Running tests and checking coverage

**For the `parseEvaluate` job:**

1. Connect to the evaluator container: while the docker-compose setup is running, `docker-compose exec evaluator sh`
2. Run the tests: once connected to the container, run `python3 -m unittest`, or `python3 -m unittest tests.test-file-to-run` to run a specific test.
2. Check test coverage: `coverage run -m --source=. unittest discover tests`

**For the `django` code:**

1. Connect to the django container: while the docker-compose setup is running, `docker-compose exec django sh`
2. Run the tests: once connected to the container, run `coverage run ./manage.py test`
2. Check test coverage: `coverage report` or `coverage html`

**For the `front-end` code:**

1. Install any front-end dependencies listed in [front-end/README.md](/front-end/README.md)
2. Run linting and tests: From the `/front-end` directory, run `yarn validate`