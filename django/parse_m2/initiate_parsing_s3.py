import io
import logging
import zipfile

from django_application.s3_utils import s3_bucket_files
from parse_m2.initiate_parsing_utils import (
    is_data_file,
    is_zip_file,
    log_invalid_file_extension,
    parse_file_from_zip,
    parsed_file_exists,
)
from parse_m2.m2_parser import M2FileParser
from parse_m2.models import Metro2Event


############################################
# Methods for parsing files from the S3 bucket

# This code assumes that the AWS credentials are available in the environment.
# It automatically finds and uses the following values to connect to S3:
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# AWS_SESSION_TOKEN
# For more on how to set credentials:
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html

def parse_s3_file(
    file, event: Metro2Event, collection: str = None,
):
    logger = logging.getLogger('parse_m2.parse_s3_file')

    # Instantiate a parser
    parser = M2FileParser(event, full_name, collection)

    # Parse the file
    fstream = file.get()["Body"]
    logger.debug(f"Successfully opened file: {full_name}. Now parsing...")
    parser.parse_file_contents(fstream, file.size)
    logger.info(f'File {full_name} written to database.')

def parse_zip_file_contents_S3(
    zip_obj,
    event: Metro2Event,
    zipfile_name: str,
    collection: str = None
):
    # TODO: If the files are large (>2GB), this method of streaming
    # zipfiles might fail. If that happens, we'll have to try another approach
    with (
        io.BytesIO(zip_obj.get()["Body"].read()) as fstream,
        zipfile.ZipFile(fstream, mode='r') as zipf
    ):
        for f in zipf.filelist:
            full_name = f"s3:{zipfile_name}:{f.filename}"

            # If this file already exists on this event, don't parse it again.
            if parsed_file_exists(event, full_name):
                logger = logging.getLogger('parse_m2.s3.parse_zip_file_contents')
                logger.debug(f"Skipping existing file {full_name}")
                return

            parse_file_from_zip(f, zipf, full_name, event, collection)

def parse_files_from_s3_bucket(
    event: Metro2Event, directory: str = None, collection: str = None
):
    """
    Parse all files in the folder of the S3 bucket location indicated by
    event.directory, and save them to event. For any files that look like zip
    files, iterate through each file in the zip and parse each one.

    The parser will not parse a file if one with a matching name already exists.
    """
    logger = logging.getLogger('parse_m2.parse_files_from_s3_bucket')


    logger.info(f"Finding all files in S3 bucket with prefix: {event.directory}")
    for file in s3_bucket_files(event.directory):
        logger.info(f"Encountered file: {file.key}")
        # TODO: Handle errors connecting to bucket and opening files

        if is_zip_file(file.key):
            parse_zip_file_contents_S3(file, event, file.key, collection)

        elif parsed_file_exists(event, file_name_s3(file)):
            # If this file already exists on this event, don't parse it again.
            logger.debug(f"Skipping existing file {file_name_s3(file)}")
        elif is_data_file(file.key):
            parse_s3_file(file, event, collection)
        else:
            log_invalid_file_extension(event, file.key, skip_existing, logger)
