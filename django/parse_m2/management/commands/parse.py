import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from parse_m2.initiate_parsing_local import parse_files_from_local_filesystem
from parse_m2.initiate_parsing_s3 import parse_files_from_s3_bucket
from parse_m2.models import Metro2Event


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py parse -e [event_id] -c [collection_name]
    """
    help = (
        "Checks all files in the S3 directory for this event, and parses any that "
        "haven't already been parsed. "
        "Can be used to resume parsing on an event that already has some files parsed. "
        "Does not run the post_parse function, so it will need to be run manually. "
        "Checks the S3_ENABLED setting to determine whether to use local or S3 files. "
    )

    def add_arguments(self, argparser):
        event_help = "The ID of the event record. (required)"
        argparser.add_argument(
            "-e",
            "--event_id",
            nargs="?",
            required=True,
            help=event_help
        )

        directory_help = (
            "The directory to find files for parsing. When present, overrides "
            "the 'directory' value on the Metro2Event model. Useful for when "
            "an event has files in multiple directories that need to be parsed "
            "separately. (optional)"
        )
        argparser.add_argument(
            "-d", "--directory",
            nargs="?", required=False,
            help=directory_help,
        )

        collection_help = (
            "A string to differentiate records from different sources "
            "or 'collections'. Used to prevent overlapping account numbers within "
            "a dataset. Will be applied to all files parsed by this run of the parser. "
            "(optional)"
        )
        argparser.add_argument(
            "-c",
            "--collection",
            nargs="?",
            required=False,
            help=collection_help
        )

    def handle(self, *args, **options):
        logger = logging.getLogger('commands.parse')
        event_id = options["event_id"]
        directory = options["directory"]
        collection = options["collection"]

        # Fetch the Metro2Event
        try:
            event = Metro2Event.objects.get(id=event_id)
        except Metro2Event.DoesNotExist as e:
            # If the event doesn't exist, exit
            raise CommandError(f"No event found with id {event_id}. Exiting.") from e

        # Parse the data
        logger.info(f"Parsing files from {event.directory} directory...")
        if settings.S3_ENABLED:
            parse_files_from_s3_bucket(
                event,
                directory=directory,
                collection=collection
            )
        else:
            parse_files_from_local_filesystem(
                event,
                directory=directory,
                collection=collection
            )

        logger.info(
            self.style.SUCCESS(f"Finished parsing data for event: {event_id}.")
        )
