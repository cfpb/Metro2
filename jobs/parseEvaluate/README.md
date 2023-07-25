The parseEvaluate job uses two separate databases:
- **parsed database** - data ingested from M2 data files, on which we run the evaluators
- **results database** - the results of the evaluators

Both databases are described in tables.py.

## Metro2 data

The CRRG (Credit Reporting Resource Guide) contains a complete description of the Metro2 data format.
Ask a teammate for a shared copy of the CRRG.
In our current copy of the CRRG, section 3-6 (Record Layouts) contains a description of each segment of the M2 data,
including the purpose of each segment, the list of fields in each segment, and the description of each field.

Basic structure of M2 data:
- Each file contains a collection of records from the same reporting period.
- Each file has one `header` and one `trailer` segment, which contain high-level information about the records in the file.
- Besides the `header` and `base`, all other lines of the file are records of consumer account information.
- Every record contains a `base` segment. It can also contain optional additional segments. The possible additional segments are `j1`, `j2`, `k1`, `k2`, `k3`, `k4`, `l1`, and `n1`.
- An individual record may have multiple extra segments, such as two `j2` segments, or a `k2` and a `l1`, etc.

Notes on our implementation of M2 data:
- In this tool, the code refers to each field by the name that was used in the legacy version of this tool. This allows us to more easliy translate evaluator logic from the legacy system to this one.
- Each different type of segment is stored in a separate table.
- In each segment of the m2 data, `id` is a hash of the file name and the data point's location in memory. `id` is the foreign key that ties all extra segments back to their `base` segment.
- In each segment of the data, `file` is the foreign key that ties each segment to the `header` of the file.

## Results data

The results database has two tables:
- `evaluator_metadata` contains one record per evaluator. The `fields` column contains an ordered list of the field names (in plain language) that are included in the evaluator output.
- `evaluator_results` contains one record for each line of M2 data that the evaluator found as a "hit". The `field_values` column contains the values of the M2 record that are relevant to the evaluator, matching the field names in the `fields` column.



---

TODO: update below this line with the most up-to-date information

## Starting a New Exam
## Define Exam Parameters

The following need to be updated for a different exam:

  - `EXAM_NUMBER` all other paths will be generated based on that exam number and the directory structure created above.

  - `INDUSTRY_TYPE_CODE` will be a constant for the exam, used in evaluators. This is provided by the OSP or ENF POCs.

These can be modified in the .env file before starting docker containers.

## Create a Data Dictionary to M2 Mapping File

- Each entity must submit a Data Dictionary along with their raw data.

- The evaluator criteria depend on the the raw data being parsed in exactly the same format for each exam.

- Since the entity may submit data in a format that differs from the standardized M2 format, we must create a "mapping" file to ensure fields are read and named properly.

- This also serves as a double check on if the entity submitted properly.

- A template for the M2 mapping file is in the shared folder for our team. Let a teammate know if you need a copy, and we'll help you locate it.

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
