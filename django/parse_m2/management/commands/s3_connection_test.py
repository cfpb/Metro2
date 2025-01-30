import logging

from django.core.management.base import BaseCommand
from parse_m2.initiate_parsing_s3 import s3_bucket_files
from django.conf import settings


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py s3_connection_test -d [s3_folder]
    """
    help = "This command will use the S3 connection variables provided in this " + \
    "environment's settings file. It will list the files from the given directory " + \
    "of this environment's S3 bucket, or error if the connection is not set up correctly."

    def add_arguments(self, argparser):
        dir_help = "The directory within the S3 bucket, defaults to 'test-tiny'"
        argparser.add_argument("-d", "--s3_directory", nargs="?", required=False, help=dir_help)

    def handle(self, *args, **options):
        logger = logging.getLogger('commands.s3_connection_test')
        s3_directory = options["s3_directory"]
        if not s3_directory:
            s3_directory = 'test-tiny'

        bucket_name = settings.S3_BUCKET_NAME
        logger.info(f"Using S3 bucket defined in settings file: {bucket_name}")

        logger.info(f"Finding all files in S3 bucket with prefix: {s3_directory}")
        count = 0
        for file in s3_bucket_files(s3_directory):
            logger.info(f" * {file.key}")
            count += 1

        logger.info(f"Total files found: {count}")
        logger.info(
            self.style.SUCCESS("Successfully connected to the S3 bucket.")
        )
