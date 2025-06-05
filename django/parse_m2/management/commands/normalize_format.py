import logging

from django.core.management.base import BaseCommand
from parse_m2.normalize_format import update_S3_directory_files_format


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py normalize_format -i input_dir -o output_dir
    """
    help = "Iterate through the files in the input_dir S3 bucket directory, " + \
            "run a format correction script on each one, and upload the " + \
            "corrected files to the output_dir location in the S3 bucket. " + \
            "Only run this on files that need to be corrected."

    def add_arguments(self, argparser):
        input_help = "The directory location in the S3 bucket containing files to normalize."
        argparser.add_argument("-i", "--input_dir", nargs="?", required=True, help=input_help)
        output_help = "The location in the S3 bucket to save normalized files."
        argparser.add_argument("-o", "--output_dir", nargs="?", required=True, help=output_help)

    def handle(self, *args, **options):
        logger = logging.getLogger('commands.normalize_format')
        input_dir = options["input_dir"]
        output_dir = options["output_dir"]

        # Run the format normalization
        logger.info(f"Normalizing files from {input_dir} directory...")
        update_S3_directory_files_format(input_dir, output_dir)

        logger.info(
            self.style.SUCCESS(f"Finished normalizing data in directory: {input_dir}.")
        )
