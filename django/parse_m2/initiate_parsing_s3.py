import zipfile
import boto3
import io
import logging
from django.conf import settings

from parse_m2.m2_parser import M2FileParser
from parse_m2.models import Metro2Event
from parse_m2.initiate_parsing_utils import data_file, zip_file, get_extension, parse_file_from_zip, parsed_file_exists

############################################
# Methods for parsing files from the S3 bucket

# This code assumes that the AWS credentials are available in the environment.
# It automatically finds and uses the following values to connect to S3:
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# AWS_SESSION_TOKEN
# For more on how to set credentials:
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html

def parse_s3_file(file, event: Metro2Event, skip_existing: bool):
    logger = logging.getLogger('parse_m2.parse_s3_file')
    full_name = f"s3:{file.key}"

    if skip_existing:
        # If the skip_existing flag is set to True, and this file
        # already exists on this event, don't parse it again.
        if parsed_file_exists(event, full_name):
            logger = logging.getLogger('parse_m2.parse_s3_file')
            logger.debug(f"Skipping existing file {full_name}, because skip_existing = True")
            return

    # Instantiate a parser
    parser = M2FileParser(event, full_name)

    # Parse the file
    fstream = file.get()["Body"]
    logger.debug(f"Successfully opened file: {full_name}. Now parsing...")
    parser.parse_file_contents(fstream, file.size)
    logger.info(f'File {full_name} written to database.')

def s3_bucket_files(bucket_directory: str):
    bucket_name = settings.S3_BUCKET_NAME
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    return bucket.objects.filter(Prefix=bucket_directory)

def parse_zip_file_contents_S3(zip_obj, event: Metro2Event, zipfile_name: str, skip_existing: bool):
    # TODO: If the files are large (>2GB), this method of streaming
    # zipfiles might fail. If that happens, we'll have to try another approach
    with io.BytesIO(zip_obj.get()["Body"].read()) as fstream:
        with zipfile.ZipFile(fstream, mode='r') as zipf:
            for f in zipf.filelist:
                full_name = f"s3:{zipfile_name}:{f.filename}"

                if skip_existing:
                    # If the skip_existing flag is set to True, and this file
                    # already exists on this event, don't parse it again.
                    if parsed_file_exists(event, full_name):
                        logger = logging.getLogger('parse_m2.s3.parse_zip_file_contents')
                        logger.debug(f"Skipping existing file {full_name}, because skip_existing = True")
                        return

                parse_file_from_zip(f, zipf, full_name, event)

def parse_files_from_s3_bucket(event: Metro2Event, skip_existing: bool = True):
    """
    Parse all files in the folder of the S3 bucket location indicated by
    event.directory, and save them to event. For any files that look like zip
    files, iterate through each file in the zip and parse each one.

    If skip_existing is True, the parser will not parse a file if one with
    a matching name already exists.
    """
    logger = logging.getLogger('parse_m2.parse_files_from_s3_bucket')


    logger.info(f"Finding all files in S3 bucket with prefix: {event.directory}")
    for file in s3_bucket_files(event.directory):
        logger.info(f"Encountered file: {file.key}")
        # TODO: Handle errors connecting to bucket and opening files

        if zip_file(file.key):
            parse_zip_file_contents_S3(file, event, file.key, skip_existing)
        elif data_file(file.key):
            parse_s3_file(file, event, skip_existing)
        else:
            error_message = f"File skipped because of invalid file extension: .{get_extension(file.key)}"
            M2FileParser(event, file.key).update_file_record(status="Not parsed", msg=error_message)
            logger.info("Skipping. Does not match an allowed file type.")
