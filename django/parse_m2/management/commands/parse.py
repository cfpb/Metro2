import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from parse_m2.initiate_parsing_s3 import parse_files_from_s3_bucket
from parse_m2.initiate_parsing_local import parse_files_from_local_filesystem
from parse_m2.models import Metro2Event


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py parse -e [event_id]
    """
    help = "Checks all files in the S3 directory for this event, and parses any that " + \
            "haven't already been parsed. " + \
            "Can be used to resume parsing on an event that already has some files parsed. " + \
            "Does not run the post_parse function, so it will need to be run manually. " + \
            "Checks the S3_ENABLED setting to determine whether to use local or S3 files. "

    def add_arguments(self, argparser):
        event_help = "The ID of the event record"
        argparser.add_argument("-e", "--event_id", nargs="?", required=True, help=event_help)

    def handle(self, *args, **options):
        logger = logging.getLogger('commands.parse')
        event_id = options["event_id"]

        # Fetch the Metro2Event
        try:
            event = Metro2Event.objects.get(id=event_id)
        except Metro2Event.DoesNotExist:
            # If the event doesn't exist, exit
            raise CommandError(f"No event found with id {event_id}. Exiting.")

        # Parse the data
        logger.info(f"Parsing files from {event.directory} directory...")
        if settings.S3_ENABLED:
            parse_files_from_s3_bucket(event, skip_existing=True)
        else:
            parse_files_from_local_filesystem(event, skip_existing=True)

        logger.info(
            self.style.SUCCESS(f"Finished parsing data for event: {event.name}.")
        )
