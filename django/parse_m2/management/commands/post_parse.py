import logging

from django.core.management.base import BaseCommand, CommandError
from parse_m2.initiate_post_parsing import post_parse
from parse_m2.models import Metro2Event


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py post_parse -e [event_id]
    """
    help = "After all files have been parsed for this event, run this command " + \
            "to prepare for running evaluators. It does two things: (1) calculate " + \
            "the date range of this event's data (for display), and (2) populate " + \
            "the 'previous values' field for all records, which allows progressive" + \
            "evaluators to work."

    def add_arguments(self, argparser):
        event_help = "The ID of the event record in the database"
        argparser.add_argument("-e", "--event_id", nargs="?", required=True, help=event_help)

    def handle(self, *args, **options):
        logger = logging.getLogger('commands.post_parse')
        event_id = options["event_id"]

        # Fetch the Metro2Event
        try:
            event = Metro2Event.objects.get(id=event_id)
        except Metro2Event.DoesNotExist:
            # If the event doesn't exist, exit
            raise CommandError(f"No event found with id {event_id}. Exiting.")

        logger.info(f"Beginning post-parse process for event: {event.name}.")
        post_parse(event)

        logger.info(f"Done. Generating report...")

        record_set = event.get_all_account_activity()

        total_updated = record_set.filter(previous_values_id__isnull=False).count()
        logger.info(f"Records with a previous record associated: {total_updated}")

        total_not_updated = record_set.filter(previous_values_id__isnull=True).count()
        logger.info(f"Records with NO previous record associated: {total_not_updated}")

        logger.info(
            self.style.SUCCESS(f"Finished post-parse for event ID: {event_id}.")
        )
