import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from evaluate_m2.upload_utils import stream_results_files_to_s3
from parse_m2.models import Metro2Event


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py upload_results -e [event_id]
    """
    help =  (
        "For an event with eval hits, upload the full result CSVs to S3. "
        "Uploads one CSV for each eval with hits. "
        "This upload automatically happens after the eval process finishes, "
        "so this command will only need to be used under special circumstances. "
        "Evaluator Results Materialized View must be refreshed to include "
        "results before this can be run."
    )

    def add_arguments(self, argparser):
        event_help = "The ID of the event record in the database"
        argparser.add_argument(
            "-e",
            "--event_id",
            nargs="?",
            required=True,
            help=event_help
        )

    def handle(self, *args, **options):
        logger = logging.getLogger('commands.evaluate')
        event_id = options["event_id"]

        # Fetch the Metro2Event
        try:
            event = Metro2Event.objects.get(id=event_id)
        except Metro2Event.DoesNotExist as e:
            # If the event doesn't exist, exit
            raise CommandError(f"No event found with id {event_id}. Exiting.") from e

        if not settings.S3_ENABLED:
            msg = "Django setting S3_ENABLED must be set to use this command. Exiting."
            logger.info(msg)
            return

        logger.info(f"Beginning to upload result CSVs for event: {event_id}...")
        stream_results_files_to_s3(event)

        logger.info(
            self.style.SUCCESS(
                f"Finished uploading results for event ID: {event_id}."
            )
        )
