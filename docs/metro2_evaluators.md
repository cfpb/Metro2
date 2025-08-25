# Metro2 evaluators

- [Existing Metro2 evaluators]()
- [Creating evalutors]()
- [Handling evaluator metadata](#handling-evaluator-metadata)
- [How to run the evaluators]()

## Handling evaluator metadata

Each evaluator has several metadata fields associated with it, such as name, short description, long description, fields used, rationale, and more.
We seed the database with initial metadata about each evaluator, then allow users to modify some of the fields.

### Evaluator CSV format
When importing and exporting evaluator metadata, we use a CSV with the following columns:
`id`,`category`,`description`,`long_description`,`fields_used`,`fields_display`,`rationale`,`potential_harm`,`alternate_explanation`,`crrg_reference`

The `id` column is what we use to connect the evaluator metadata to the evaluator function, which is defined in code.
This means that the `id` column needs to exactly match the name of the function in the code.
If the names don't match, any evaluator results won't be correctly associated with the evaluator in the system.

### Importing metadata
Do this when deploying the project to a new environment to create evaluator metadata records in the database.

How to import the evaluator metadata into the system:
1. Create a CSV of all known evaluator metadata using the format described above.
2. Save the CSV to this repo using the following filename: `cfpb_evaluators/eval_metadata.csv`.
3. Import the metadata by running the following Django management command in the environment where the metadata should be imported: `python manage.py import_evaluator_metadata`.
    - This command will update any existing records with the new metadata and create any that don't already exist. It won't delete existing records that are missing from the csv.

### Exporting metadata
Do this when users have made manual updates to the evaluator metadata and you want to propagate those updates to another environment.

How to export the evaluator metadata:
1. Visit the `/all-evaluator-metadata` endpoint for the environment in the browser.
    - This will download a CSV of all evaluator metadata in the system, which you can import into any Metro2 environment.

## How to run evaluators

After a dataset has been parsed and is saved in the Metro 2 database, the evaluators can be used to analyze and find inconsistencies in the data. To do so, use the `evaluate` management command: `python manage.py evaluate -e [event_id]`. This will run all of the evaluators that have been configured in the `METRO2_EVALUATORS` django setting.

When the evaluators are run, the results are saved in the Metro 2 database. When the process is finished, the results are available to be viewed in the Metro 2 application.