# Overview

The purpose of the Metro 2 evaluator tool is to automate as much as possible in regard to parsing, evaluating, and analyzing. The tool is currently configured to be run locally, but will soon be modified to run in any environment.

## Sections

- [Copy .env_SAMPLE to .env and change values](#copy-.env_sample-to-.env-and-change-values)
- [Define Exam Parameters](#define-exam-parameters)
- [Docker container running postgres for local development](#docker-container-running-postgres-for-local-development)
- [Create a Data Dictionary to M2 Mapping File](#create-a-data-dictionary-to-m2-mapping-file)
- [Populate the Mapping File](#populate-the-mapping-file)
- [Create local folder for running locally](#create-local-folder-for-running-locally)
- [Parse Data and Write to Database](#parse-data-and-write-to-database)
- [Run Evaluators](#run-evaluators)
- [Running Tests](#running-tests)

## Copy .env_SAMPLE to .env and change values

.env_SAMPLE contains environment variables that will be fed into the application. In order for the file to be recognized by docker compose, run `cp .env_SAMPLE .env`.

## Define Exam Parameters

The following need to be updated for a different exam:

  - `EXAM_NUMBER` all other paths will be generated based on that exam number and the directory structure created above.
  
  - `INDUSTRY_TYPE_CODE` will be a constant for the exam, used in evaluators. This is provided by the OSP or ENF POCs.

These can be modified in the .env file before starting docker containers.

## Docker container running postgres for local development

If docker desktop is not already installed, please [download and install it](https://www.docker.com/products/docker-desktop/)

For local development, postgresql will run inside a docker container with sample data. To start the container in the background, run `docker-compose up -d`. This will create a postgresql container, a container to run the app, a volume to persist data for both postgres and the application, and a default network that allows communication with the containers from the host machine.

Once your containers are up and running, you can connect to the postgres container using `docker-compose exec -it metro2_postgres_1 sh` and the application container using `docker-compose exec -it metro2_evaluator_1 sh`

To run the application once you are connected to the evaluator container, run the command `./setup.sh'`.

To bring down the created containers when you are done with them, run `docker-compose down`. To also remove volumes at the same time, run `docker-compose down -v`. To remove images in addition to volumes, run `docker-compose down --rmi "all" -v`.

## Starting a New Exam

## Create a Data Dictionary to M2 Mapping File

- Each entity must submit a Data Dictionary along with their raw data.

- The evaluator criteria depend on the the raw data being parsed in exactly the same format for each exam.

- Since the entity may submit data in a format that differs from the standardized M2 format, we must create a "mapping" file to ensure fields are read and named properly.

- This also serves as a double check on if the entity submitted properly.

- A template for the M2 mapping file can be found in the Reference folder from the root directory on GitHub (the root directory is where this README exists)

## Populate the Mapping File

This is a manual process, but it can be helped with some code and Excel formulas, pre-populated in the template.

- Open the mapping file that was written to the exam folder above.

- "Evaluator" and "M2" sheets are static. We must populate the DataDictionary sheet first, and then choose fields from "M2" that match the submitted fields.

- "Evaluator" contains all of the fields used in the evaluator functions.

- "M2" is a tabular form of the 2022 CRRG file. It outlines the standard M2 format.

- "DataDictionary" sheet:
  
  + Use the submitted data dictionary to create a flat file of that information. 
  
  + Copy/paste (as values!) the fields, descriptions, and lengths from each segment sheet in the entity's data dictionary.
  
  + The DictSegment column should be whatever sheet you copied the data from. Follow the format on the "M2" sheet for segments (e.g., "base" instead of "Base", etc).
  
- "Mapping" sheet:

  + Copy/paste (as values!) the data from DataDictionary sheet to the Mapping sheet.
  
  + The orange column, M2FieldLower, needs to be filled in manually. You can deduce the intended M2 field from the entity's field most of the time. Some are exact matches. If there are any discrepancies, check the CRRG first, then work with the OSP or ENF POCs to clear them up if necessary.
  
_Note: the field type for phone numbers must be `col_double()` because R cannot handle integers above about 2 billion. All other numeric fields are okay as integers, because they are only 9 characters long, and the M2 format calls for truncating decimals._

## Create Local Folder for Running Locally

When the tool runs locally, it expects to find the following files to copy from a local directory named `local`

- local
  - data
    - data-file.txt (can be named anything as long as the file extension is .txt)
    - data-file2.txt (can be named anything as long as the file extension is .txt)
    - ...
  - reference
    - sample-map.xlsx (keep this name consistent)

## Parse Data and Write to Database

With your docker containers up and running and unzipped .txt data files, connect to the evaluator container using `docker-compose exec evaluator sh` and run the following command:

`./setup.sh`

## Run Evaluators

After parsing, the same script that was used to parse will run all evaluators and output the results to a json file. This file is intended to be passed to a frontend in order to visualize data.

The data returned by the JSON is formatted as follows:
- Criteria name (i.e. 6-4C)
  - Description
  - Data
    - Record number
      - Date
      - Checked field values
  - Number of hits

The results.json file can be retrieved from the docker container by exiting the container with the command `exit` and then running the following command (replacing local/path/to/results.json with whatever local path you want to store it in):

`docker-compose cp evaluator:"src/metro2/exam-<replace with exam number>/results/results.json" "local/path/to/results.json"`

## Cross Reference Hits with Consumer Disputes

## Running Tests

Connect to the application container with `docker-compose exec evaluator sh` then run `python3 -m unittest metro2.tests.test-to-run`

Currently available test files:
- `test-evaluate`
- `test-parse`

TODO: Add tests, improve running tests, and run on PRs


### Test Coverage

To measure test coverage of metro2, connect to the application with `docker-compose exec -it metro2_evaluator_1 sh` and run `coverage run -m --source=./metro2 unittest discover metro2/tests`.  
