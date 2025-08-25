# Parsing Metro2 data

Parsing is the process by which the Metro 2 Evaluator Tool ingests Metro 2-formatted files and saves the data in the database. This page contains instructions for managing that process.

Contents:
- [How to parse a dataset](#how-to-parse-a-dataset)
- [Normalizing mal-formatted data](#normalizing-mal-formatted-data)
- [Appendix: How the parser works](#appendix-how-the-parser-works)

## How to parse a dataset

### Step 1: Prepare the files to be parsed
The tool can parse Metro2 files from either an AWS S3 bucket or a local directory.

To parse from an S3 bucket:
1. Set `S3_ENABLED=True` in your Django settings file.
2. Set `S3_BUCKET_NAME` to your AWS S3 bucket name.
3. Set up your AWS credentials according to the [Boto3 library](https://boto3.amazonaws.com/v1/documentation/api/1.35.6/guide/credentials.html)'s instructions
2. Create a folder in your S3 bucket for this dataset's files.
3. Place all of the dataset files into the folder. Ideally this would contain all of the files for the dataset an no extras.
    - All files should have a `.txt` file extension, or be `.zip` files that contain `.txt` files.
    - Note: the file format normalization process (below) currently only works if the folder names don't contain any spaces.

Optional step: If you want to check what files the parser will find and attempt to parse, you can use the `s3_connection_test` management command. To do so, use `python manage.py s3_connection_test -d <your-directory>`. If your S3 connection is configured correctly, the command will output a list of files and the total number of files.


To parse from a local directory:
1. Set `S3_ENABLED=False` in your Django settings file.
2. Create a folder in your local environment 
3. Place all of the dataset files into the folder. Ideally this would contain all of the files for the dataset an no extras.
    - All files should have a `.txt` file extension, or be `.zip` files that contain `.txt` files.
    - Note: the file format normalization process (below) currently only works if the folder names don't contain any spaces.

### Step 2: Create a new event record in the Metro2 admin
In the M2 admin interface, use the "Add Metro2 Event" function. In the New M2 Event form, the key field to fill out is 'directory' -- most of the other fields can be filled and/or updated later.

The value in the `directory` field must match the directory where the files are saved. When parsing from S3, this will be the full path of the directory. For example, if the full S3 url is `S3://my-m2-bucket/raw-data/my-dataset/`, you would use `/raw-data/my-dataset/`. When parsing from a local directory, specify the path relative to the `/django` directory of this repo.

 Once you press "Save", the Event record will be saved with an event ID. Take note of the event ID (in the URL), since it's used in the next step.

### Step 3: Parse the files
Use the `parse` management command to begin parsing files: `python manage.py parse -e [id]`, where `id` is the ID of the Metro2 event record you created in the previous step.

You can monitor the parsing progress in two ways:
- The console output of the management command shows the logs from the parsing process
- In the Metro2 admin interface, navigate to "Metro2 Events", find your event in the event list, then click "Data import info". This shows a summary of all of the file parsing progress that has happened so far.

### Step 5: troubleshoot
The parser is designed to be hands-off, but sometimes it doesn't work out that way. Some things to note when things go wrong:
- If you re-start the parser (or start a second process running the parser concurrently), it won't re-parse any files it's already started parsing. It checks the 'file name' value for each file on an event before parsing, and skips over any that already exist.
- If the parser stops or fails in the middle of a file, we generally delete that file's data and parse it again. There's a management command for deleting a file: `delete_single_datafile`.
- If a file's first line parses successfully, it will parse all of the rest of the lines, even if they are all being marked as unparseable data. We could consider an improvement where we stop parsing if the first 100 lines are all unparseable. But for now, we have to stop it manually if we want it stopped.
- (there's probably more to put here. TBA.)


## Normalizing mal-formatted data

Sometimes entities provide data that doesn't conform to the Metro2 standard. Sometimes, for a variety of reasons, we may decide it's not worth waiting for the entity to produce better data. Instead, we make do with the data we have. In these cases, we use a process to "normalize" the data files, i.e. produce a corrected file that can be parsed by our parser.

To make the explanation easier to understand, we'll use a specific dataset flaw as an example in the steps below.

### Step 1: understand the format issue
The Metro 2 parser tries to return meaningful errors when formatting issues are encountered. You can try parsing a file, and if all of the records are being counted as Unparseable Data, you can assume that file file is malformed. The error messages may help understand what the formatting error is.

In our example, with some analysis, we found that some of the files omitted the RDW/BDW, which is a 4-character data field in position 1 of the base segment.

### Step 2: create a method to correct the format issue
For our exmaple, we created a method that iterates through each line of a file (and each file in a S3 bucket directory), creates a "normalized" (corrected) version of the files, and saves them back to the S3 bucket in a new folder. For that case, the normalization method we used was specific to the missing RDW field issue.

The code from the example above is designed to be modified to correct any format issue (assuming it's consistent on every line of a file). To do that, update [`normalize_format.py`](/django/parse_m2/normalize_format.py). Test your code using sample data that has the format issue you're correcting.

### Step 3: determine which files have the format issue
Our example dataset combined data from two different sources; some of them had the format issue and others didn't, but we didn't know which. The files were collected into folders, and we assumed that each folder would be consistent in format (luckily, that assumption was correct). With that assumption, we used the parser to parse a few files from each folder and checked whether they parsed successfully. 

More detailed instructions for that:
1. Take note of the file structure of files for this event, either locally or in S3
2. To test-parse a subset of an event's files, visit the event record in the Metro2 Django Admin site, and update the `directory` value to the specific S3 directory you want to test
2. Use the `parse` management command to begin the parsing process on that specific directory
3. Visit the Django admin page to see whether the tradelines are parsing successfully or being marked as unparseable. If a file has 0 parsed and lots of unparseable lines, assume the whole folder has the parsing issue. For files with lots of parsed and very few unparseable lines, assume they don't have the parsing issue
4. Repeat with each folder of files in the event's S3 bucket directory; create a list of which folders need to have files normalized and which don't.

### Step 4: normalize file formats
1. Pick a folder that needs to be normalized based on Step 3 and take note of its directory path. Let's say it's something like `raw-data/my-dataset/09-2025`. You'll use this as the input path for the file correction script.
2. Decide what path you want to save the normalized files at. In this example, you could decide to use `raw-data/my-dataset-normalized/09-2025`. You'll use this as the output path. It should not end with a slash.
3. Use the `normalize_format` management command on the files. In the given example, the command would be `python manage.py normalize_format -i raw-data/my-dataset/09-2025 -o raw-data/my-dataset-normalized/09-2025`.
4. The job will iterate through all of the files in the input directory and make a format-normalized copy in the output directory. You can check on the progress by browsing to the S3 bucket in the AWS console and seeing the files uploaded to the output folder.
6. Repeat for any other folders of files that need to be normalized.

Note: this currently only works if the input and output paths don't contain spaces.

### Step 5: Create a clean directory of files ready to parse
In the previous step, we created a directory that contains normalized data files, but is missing ones that didn't need correction. In order to make use of the parser's hands-off operation, we make a copy of the files that didn't need normalization and add them to the directory of corrected data. We keep the original files intact in case we need to audit or troubleshoot the normalizing process.

### Step 6: Clean up test-parsed files
You can delete the set of test-parsed records that were created during the normalizing process. The management command `delete_event_data -e [event_id]` deletes all Metro2 records that are associated with this event, including every file and segment record produced by the parser (and all eval results, if any).

### Step 7: Parse
Follow the steps in the [How to parse](#how-to-parse-a-dataset) above, starting with step 2. The `directory` value of the Metro2Event will be the clean directory of parseable files. In the example above, it would be `raw-data/my-dataset-normalized`.


## Appendix: How the parser works

### Iterating through files
The parser filters the S3 bucket for files that match the `directory` for the event. For each matching file, it does the following:
- It checks whether there's already a file whose full file path matches the one we're about to parse. If the file already exists on this event, it skips it and moves on to the next one. (This is so we can start and stop the parser as needed without having to re-parse all of the data for an event)
- If the file isn't a .txt file, (or a .txt file inside of a .zip file), it skips the file and puts a message in the 'error message' field for that file
- It attempts to save the `activity_date` from the top line (the "header record") of the file.
    - If the first line appears to be a header but the activity date value is malformed, it skips the file and puts a message in the 'error message' field for that file.
    - If the first line is not a header (is just a regular row), that signals the parser to use the 'date of account activity' in place of 'activity date' for the entire file. It puts a message in the 'error message' field, but continues on to parse the file.
- for files it hasn't skipped, it parses the remaining rows of the file. 
    - For a given row, if all of the required fields are present (certain numeric and date values are required to be parseable as ints and dates), the row gets saved. 
    - If the required fields aren't present (or certain other error situations), the row is marked as 'unparseable', and saved in the `UnparseableData` table, with a message describing the error.

### Saving individual values
Here's some information about exactly how the information gets interpreted and what counts as 'unparseable' data.

Our system has 3 column types -- numeric, date, and other.
- Date fields are saved either as a date or blank. The parser regards all non-date values as invalid, regardless of whether they are reported correctly ("not applicable" is _supposed_ to be reported as `00000000`), or not (e.g. `        `, or `20130229`, or `0191231a`).
    - If the date field is required but the value isn't a valid date, the whole row is marked as unparseable. Required date fields: activity date, date open, DOAI
    - If the date field is non-required and not valid, it will be saved as `None`. Optional date fields: DOFD, date closed, DOLP, K4 deferred pmt date, K4 balloon pmt due date
- Numeric fields are saved as either an integer or blank. Any non-integer values are regarded as invalid, including blanks, letters, as well as strings that have non-integer characters, like `$123` or `4.85`.
    - If the numeric field is required but the value isn't a valid integer, the whole row is marked as unparseable. Required numeric fields: credit limit, HCOLA, SMPA, actual payment amount, current balance, amount past due, original charge-off amount
    -  If the numeric field is non-required and not valid, it will be saved as `None`. Optional numeric field: K4 balloon payment amt
- All of the other fields can have anything in them, and they will be saved exactly as they were in the original metro2 file. For instance, if the port_type we received in the original metro2 file was "!", the parser will save "!", even though it's nonsense.