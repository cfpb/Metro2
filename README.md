# Overview

CFPB’s Metro2 Evaluator Tool (M2) evaluates Metro2 data for inaccuracies which may prove harmful to consumers’ credit. CFPB’s Supervision and Enforcement teams will use this tool while conducting cases and exams to find inaccuracies in entity-provided data and assess their potential harm to consumers.

The application has a Django back-end which connects to a Postgres database. The back end fetches Metro2 data files from an S3 bucket, parses the relevant data into the database, and runs evaluators on the data. The back end also handles authorization for users and provides API endpoints to expose the evaluated data to the front end.

The front-end provides a React-based interface for authenticated and authorized users and allows them to interact with the data.

## Sections
- [Deployments](#deployments)
    - [Alto Dev](#alto-dev-internal)
    - [Alto Staging](#alto-staging-internal)
    - [Alto Prod](#alto-prod-internal)
- [Deployment automations](#deployment-automations)
- [Running the project locally](#running-the-project-locally)
    - [Running in Helm](#running-in-helm)
    - [Running in docker-compose](#running-in-docker-compose)
    - [Running jobs individually](#individual-jobs)
- [Handling evaluator metadata](#handling-evaluator-metadata)
- [Testing](#testing)
  - [Running tests and checking coverage](#running-tests-and-checking-coverage)


# Deployments

Metro2 is deployed to the internal accounts of ALTO's 3 Environments: Dev, Staging, and Prod.

## ALTO Dev-Internal

**Quick Links**
- [Metro2 in Dev-Internal](https://INTERNAL/)

**How to deploy**
1. Prepare a branch that has the changes you wish to make.
2. In that branch, make any updates to the `buildspec.yaml` file to customize your deployment. (See [Dev branch automation](#dev-branch-automation) below for details)
3. Push your branch to the `dev` branch of this repo.
4. AWS CodeBuild will automatically run the buildspec code, which builds and deploys Metro2 to the Dev-Internal cluster.
5. The app will be available at `https://INTERNAL/` (if using the `metro` release), or `https://[release-name]-eksINTERNAL/` (if you specified a release name)

## ALTO Staging-Internal

**Quick Links**
- [Metro2 in Staging-Internal](https://INTERNAL/)
- [Jenkins for Metro2 Staging-Internal](https://INTERNAL)

**How to deploy**
1. Log in to Jenkins via the link above.
2. To build the images, use Images > Push build images to ECR. Parameters:
    - GitHub Repo: `https://GHE/Metro2/metro2`
    - Build Images Flags: `-e eks -t <tag>`, where `tag` is a unique identifier, such as `2024-04-17-hotfix`
3. To deploy, use Metro2 > Helm Deploy Metro2. Parameters:
    - METRO2 Django Tag: the same tag you used to build the images

## ALTO Prod-Internal

Not currently available

## Deployment automations
### Dev branch automation

Inside the ALTO Dev-Internal account, a Codebuild Job, `cfpb-team-metro2-metro2-dev-deploy` has been set up from the [Service Catalog](https://GHE/aws/service-catalog-cdk/blob/master/products/shared/codebuild-project-eks/v1/product.yml).  `cfpb-team-metro2-metro2-dev-deploy` is pointed to Metro2's [dev branch](https://GHE/Metro2/metro2/tree/dev).  Whenever a change is pushed to [dev branch](https://GHE/Metro2/metro2/tree/dev), `cfpb-team-metro2-metro2-dev-deploy` is automatically triggered and begins running branch's [buildspec](./buildspec.yaml).

What the buildspec does:
First, the `env` section of the [buildspec](./buildspec.yaml) configures the environment with the necessary env vars. Three important env vars that will affect your deployment are:
- `DOCKER_TAG`: the tag you want for the `metro2-django` image. (default: `YYYY-MM-DD-H-m`)
- `ENABLE_SSO`: if you want SSO enabled, set to `enabled` or blank. (default: blank)
- `RELEASE_NAME`: the name of the metro2 release, which determines the URL of the deployed application. (default: `metro2`)

Next, The `build` section of the [buildspec](./buildspec.yaml) is broken into three phases: [install](https://GHE/Metro2/metro2/blob/4bf5b4ce4f65f743746aa49f315e1514586815bf/buildspec.yaml#L26), [pre-build](https://GHE/Metro2/metro2/blob/4bf5b4ce4f65f743746aa49f315e1514586815bf/buildspec.yaml#L60), and [build](https://GHE/Metro2/metro2/blob/4bf5b4ce4f65f743746aa49f315e1514586815bf/buildspec.yaml#L84). Each phase's purpose and steps are explained in the buildspec file.

# Running the project locally

Choose the way to run the project that best suits your needs:
1. **Helm** is the way the project will run in deployed environments. Use this when you need a production-like setup and you don't need the code to reload when there are local changes.
2. **Docker-compose** is best for local development. It allows dynamically reloading code while still providing all parts of the project setup.
3. It is also possible to run some of the sub-projects locally, but this is usually only practical for active development on a specific aspect of the codebase.

## Running in Helm

When running a helm deployment locally, we use the docker-desktop cluster that comes with Docker.
To prepare your environment, make sure that you have [kubernetes enabled in Docker](https://docs.docker.com/desktop/kubernetes/).
Install helm (`brew install helm`) and optionally install [OpenLens](https://github.com/MuhammedKalkan/OpenLens) for better visualization.

With that in place, you must do the following:
    1. Ensure that your Docker daemon is running.
        - Without Docker running, your docker-desktop cluster will not be running.
    2. Run `build-images.sh -e local`
    3. Run `helm-install-local.sh`

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

Both the **Django** and **Front-end** code bases can be run locally. See the README for each subdirectory for instructions.

# Handling evaluator metadata

Each evaluator has several metadata fields associated with it, such as name, short description, long description, fields used, rationale, and more.
We seed the database with initial metadata about each evaluator, then allow users to modify some of the fields.

## Evaluator CSV format
When importing and exporting evaluator metadata, we use a CSV with the following columns:
`id`, `description`, `long_description`, `fields_used`, `fields_display`, `crrg_reference`, `potential_harm`, `rationale`, and `alternate_explanation`.
Column headers in the file should match the column names in this list.
For columns contain a list of fields (`fields_used` and `fields_display`, currently), the items in each list should be separated by colons (`;`).

The `id` column is what we use to connect the evaluator metadata to the evaluator function, which is defined in code.
This means that the `id` column needs to exactly match the name of the function in the code.
If the names don't match, any evaluator results won't be correctly associated with the evaluator in the system.

## Importing metadata
Do this when deploying the project to a new environment to create evaluator metadata records in the database.

How to import the evaluator metadata into the system:
1. Create a CSV of all known evaluator metadata using the format described above.
2. Save the CSV to this repo using the following filename: `evaluate_m2/m2_evaluators/eval_metadata.csv`.
3. Import the metadata by running the following Django management command in the environment where the metadata should be imported: `python manage.py import_evaluator_metadata`.
    - This command will update any existing records with the new metadata, and create any that don't already exist.

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
