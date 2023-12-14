import boto3
import os
import logging
from django.conf import settings

from parse_m2.m2_parser import M2FileParser
from parse_m2.models import Metro2Event


############################################
# Methods for parsing files from the local filesystem
def parse_local_file(event: Metro2Event, filepath):
    logger = logging.getLogger('parse_m2.parse_local_file')

    # Instantiate a parser
    parser = M2FileParser(event, f"local:{filepath}")

    logger.debug(f"Parsing local file: {filepath}")
    try:
        fstream = open(filepath, 'r')
        file_size = os.path.getsize(filepath)
        # Parse the file
        parser.parse_file_contents(fstream, file_size)
        logger.info(f'File {os.path.basename(fstream.name)} written to database.')
    except FileNotFoundError as e:
        logger.error(f"There was an error opening the file: {e}")
    finally:
        if fstream:
            fstream.close()


def parse_files_from_local_filesystem(event_identifier: str, data_directory: str) -> Metro2Event:
    logger = logging.getLogger('parse_m2.parse_files_from_local_filesystem')

    # Create a new Metro2Event. All records parsed will be associated with this Event.
    event = Metro2Event(name=event_identifier)
    event.save()

    # iterate over files in LOCAL_EVENT_DATA directory
    for filename in os.listdir(data_directory):
        logger.info(f"Encountered file in local data path: {filename}")
        filepath = os.path.join(data_directory, filename)

        # Only use files ending in .txt
        if os.path.isfile(filepath) and filename.lower().endswith('.txt'):
            parse_local_file(event, filepath)

    return event


############################################
# Methods for parsing files from the S3 bucket

# This code assumes that the AWS credentials are available in the environment.
# It automatically finds and uses the following values to connect to S3:
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# AWS_SESSION_TOKEN
# For more on how to set credentials:
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html

def parse_s3_file(file, event: Metro2Event):
    logger = logging.getLogger('parse_m2.parse_s3_file')
    key = file.key
    # Instantiate a parser
    parser = M2FileParser(event, f"s3:{key}")

    # Parse the file
    fstream = file.get()["Body"]
    logger.debug(f"Successfully opened file: {key}. Now parsing...")
    parser.parse_file_contents(fstream, file.size)
    logger.info(f'File {key} written to database.')

def s3_bucket_files(bucket_directory: str, bucket_name: str = settings.S3_BUCKET_NAME):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    return bucket.objects.filter(Prefix=bucket_directory)

def parse_files_from_s3_bucket(event_identifier: str, bucket_directory: str, bucket_name: str = settings.S3_BUCKET_NAME):
    logger = logging.getLogger('parse_m2.parse_files_from_s3_bucket')

    # Create a new Metro2Event. All records parsed will be associated with this Event.
    event = Metro2Event(name=event_identifier)
    event.save()

    logger.info(f"Finding all files in S3 bucket with prefix: {bucket_directory}")
    for file in s3_bucket_files(bucket_directory, bucket_name):
        logger.info(f"Encountered file: {file.key}")
        # TODO: Handle errors connecting to bucket and opening files
        parse_s3_file(file, event)
