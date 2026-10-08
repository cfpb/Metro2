import logging

from django.core.management.base import BaseCommand, CommandError

from parse_m2.initiate_post_parsing import post_parse
from parse_m2.models import Metro2Event


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py post_parse -e [event_id]
    > python manage.py post_parse -e [event_id] --file_strategy
    """
    help = (
        "After all files have been parsed for this event, run this command "
        "to prepare for running evaluators. It does two things: (1) calculate "
        "stats about this event's data (for display), and (2) populate "
        "the 'previous values' field for all records, which allows progressive "
        "evaluators to work."
        "In order to use the --file_strategy flag, you must first use the Django "
        "admin to indicate 'prior' files for all relevant files."
    )

    def add_arguments(self, argparser):
        event_help = "The ID of the event record in the database"
        argparser.add_argument(
            "-e",
            "--event_id",
            nargs="?",
            required=True,
            help=event_help,
        )

        strategy_help = (
            "The strategy to use when associating prior records. "
            "Options are: lag, chunk, file. "
            "If not present, will default to 'chunk'. "
            "See code for explanation of each option. "
        )
        argparser.add_argument(
            "-s",
            "--strategy",
            nargs="?",
            required=False,
            help=strategy_help,
        )

    def handle(self, *args, **options):
        logger = logging.getLogger('commands.post_parse')
        event_id = options["event_id"]
        strategy = options['strategy']

        # Fetch the Metro2Event
        try:
            event = Metro2Event.objects.get(id=event_id)
        except Metro2Event.DoesNotExist as e:
            # If the event doesn't exist, exit
            raise CommandError(f"No event found with id {event_id}. Exiting.") from e

        logger.info(f"Beginning post-parse process for event: {event_id}.")
        post_parse(event, strategy)

        logger.info(
            self.style.SUCCESS(f"Finished post-parse for event ID: {event_id}.")
        )
