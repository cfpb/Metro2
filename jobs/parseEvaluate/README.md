The M2 database is populated in two separate phases: parsing and evaluators.
- **parser**: The application reads Metro2 data files from an S3 bucket or the local file system (when running locally), then saves the data in the database.
- **evaluators**: The application runs lots of evaluators to check for inconsistencies in the data, then saves the results to the database.

## Background: Metro2 data

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

## Parser results

Notes on our implementation of M2 data:
- In this tool, the code refers to each field by the name that was used in the legacy version of this tool. This allows us to more easliy translate evaluator logic from the legacy system to this one.
- Each different type of segment is stored in a separate table.
- In each segment of the m2 data, `id` is a hash of the file name and the location of that line of data in memory. `id` is the foreign key that ties all extra segments back to their `base` segment, and is shared among all segments on a single record.
- In each segment of the data, `file` is the foreign key that ties each segment to the `header` of the file, and is shared among all record segments in a file.
- If a field in the M2 data file is blank (i.e. filled with blank spaces), the parser will save that field as an empty string.
- If a field is filled with zeros--which can be valid, for instance, when a numeric field is not applicable in a record--the parser currently saves that field without modifying it, so it would stay a string of zeros. We could choose to modify this behavior if we wish.

## Evaluator results

The results data are stored in two tables:
- `evaluator_metadata` contains one record per evaluator. The `fields` column contains an ordered list of the field names (in plain language) that are included in the evaluator output.
- `evaluator_results` contains one record for each line of M2 data that each evaluator found as a "hit". The `field_values` column contains the values of the M2 record that are relevant to the evaluator, matching the field names in the `fields` column.


---

TODO: update below this line with the most up-to-date information

## Starting a New Exam
## Define Exam Parameters

The following need to be updated for a different exam:

  - `EXAM_NUMBER` all other paths will be generated based on that exam number and the directory structure created above.

  - `INDUSTRY_TYPE_CODE` will be a constant for the exam, used in evaluators. This is provided by the OSP or ENF POCs.

These can be modified in the .env file before starting docker containers.