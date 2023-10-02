# ParseEvaluate

The ParseEvaluate job is where the M2 application processes Metro2 data.
The job ingests Metro2 data from text files, saving the data in the postgres database,
then runs evaluators on the saved data to find inconsistencies.

In this README:
- [[Data sources]] - using environment variables to set where the parser should find Metro2 data
- [[Metro2 data]] - description of the data format as it is provided by financial institutions and how it is stored in the M2 database

## Data sources

The M2 parser uses the `S3_ENABLED` environment variable to determine whether to source Metro2 data files from the local filesystem or an S3 bucket.
In deployed environments, we plan to use the S3 bucket as the data source.
We use the local filesystem as the data source for testing and development purposes, when it would be impractical or risky to pull files from a remote source.

For both strategies, the system accepts a directory location as an argument.
It will find every `.txt` file in the given directory and attempt to parse and save it as Metro2 data.
See the following sections for how to prepare the environment in each scenario.

### S3 files

If the `S3_ENABLED` environment variable is set (to any value), the job will attempt to fetch data from the given S3 bucket.
In this case, the code will require the following environment variables to be set:
- `S3_BUCKET_NAME` - the name of the S3 bucket to use as the data source.
- `S3_EXAM_ROOT` - the directory within the S3 bucket where the code will look for this exam's data.
- `AWS_DEFAULT_REGION`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN`

### Local files

If the `S3_ENABLED` environment varible is not set in the environment, the job will find files in the local filesystem.
The following environment variable must be set:
- `LOCAL_EXAM_ROOT` - the directory, relative to the ParseEvaluate job root directory, where the code will look for Metro2 files to parse. Within that folder, it will look for a /data subfolder, and process all files within it with a `.txt` file extension (not case sensitive).

For example, if `LOCAL_EXAM_ROOT` is set to `temp`, it expects to find the following:
- `[project-root]/jobs/parseEvaluate/temp/`
  - `data/`
    - `data-file.txt` (can be named anything as long as the file extension is .txt)
    - `data-file2.txt` (can be named anything as long as the file extension is .txt)
    - ...

For testing, we use a set of sample de-identified data (data with all PII removed) provided by SEFL.
If you need to download the sample files, ask a team member where they are saved.

## Metro2 data

The M2 database is populated in two separate phases: parsing and evaluators.
- **parser**: The application reads Metro2 data files from an S3 bucket or the local file system (when running locally), then saves the data in the database.
- **evaluators**: The application runs lots of evaluators to check for inconsistencies in the data, then saves the results to the database.

### Background: The Metro2 data standard

The CRRG (Credit Reporting Resource Guide) contains a complete description of the Metro2 data format.
Ask a teammate for a shared copy of the CRRG.
Section 3-6 (Record Layouts) of the CRRG contains a description of each segment of the M2 data,
including the purpose of each segment, the list of fields in each segment, and the description of each field.

Basic structure of M2 data:
- Each file contains a collection of records from the same reporting period.
- Each file has one `header` and one `trailer` segment, which contain high-level information about the records in the file.
- Besides the `header` and `trailer`, all other lines of the file are records of consumer account information.
- Every record contains a `base` segment. It can also contain optional additional segments. The possible additional segments are `j1`, `j2`, `k1`, `k2`, `k3`, `k4`, `l1`, and `n1`.
- An individual record may have multiple extra segments, such as two `j2` segments, or a `k2` and a `l1`, etc.
- For alphanumeric fields, the M2 standard says the field should be left-justified and blank filled. That is, if a field width is 10 characters and the value in it is "example", the file will contain `example   `.
- For numeric fields, the standard says the field should be right-justified and zero filled. That is, if a field width is 10 characters and the value in it is 12,345, the file will contain `0000012345`.

### Parser results

Notes on our implementation of M2 data:
- In this tool, the code refers to each field by the name that was used in the legacy version of this tool. This allows us to more easliy translate evaluator logic from the legacy system to this one.
- Each different type of segment is stored in a separate table.
- In each segment of the m2 data, `id` is a hash of the file name and the location of that line of data in memory. `id` is the foreign key that ties all extra segments back to their `base` segment, and is shared among all segments on a single record.
- In each segment of the data, `file` is the foreign key that ties each segment to the `header` of the file, and is shared among all record segments in a file.
- If a field in the M2 data file is blank (i.e. filled with blank spaces), the parser will save that field as an empty string.
- If a field is filled with zeros--which can be valid, for instance, when a numeric field is not applicable in a record--the parser currently saves that field without modifying it, so it would stay a string of zeros. We could choose to modify this behavior if we wish.

### Evaluator results

The results data are stored in two tables:
- `evaluator_metadata` contains one record per evaluator. The `fields` column contains an ordered list of the field names (in plain language) that are included in the evaluator output.
- `evaluator_results` contains one record for each line of M2 data that each evaluator found as a "hit". The `field_values` column contains the values of the M2 record that are relevant to the evaluator, matching the field names in the `fields` column.
