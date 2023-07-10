TODO: update this README with the most up-to-date information


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
