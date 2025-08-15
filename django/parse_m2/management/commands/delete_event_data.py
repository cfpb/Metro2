import logging

from django.core.management.base import BaseCommand, CommandError
from parse_m2.models import Metro2Event, M2DataFile
from evaluate_m2.models import EvaluatorResultSummary


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py delete_event_data -e [event_id]
    """
    help = "Delete all Metro2 data for a specific event record. Do this " + \
            "when you receive corrected data for an event, and all previous " + \
            "data and results for that event are no longer valid. This deletes " + \
            "all evaluator results and parsed files."

    def add_arguments(self, argparser):
        event_help = "The ID of the event record"
        argparser.add_argument("-e", "--event_id", nargs="?", required=True, help=event_help)

    def handle(self, *args, **options):
        logger = logging.getLogger('commands.delete_event_data')
        event_id = options["event_id"]

        # Fetch the Metro2Event
        try:
            event = Metro2Event.objects.get(id=event_id)
        except Metro2Event.DoesNotExist:
            # If the event doesn't exist, exit
            raise CommandError(f"No event found with id {event_id}. Exiting.")

        # Delete results of previous evaluator run
        logger.info(f"Checking if EvaluatorResultSummary records exist for event ID: {event_id}.")
        eval_results = EvaluatorResultSummary.objects.filter(event=event)
        if eval_results.exists():
            logger.info(f"Deleting results of {eval_results.count()} evaluators from previous run of this event.")
            eval_results.delete()

        # Delete results of previous parse
        logger.info(f"Checking if M2DataFile records exist for event ID: {event_id}.")
        parsed_files = M2DataFile.objects.filter(event=event)
        if parsed_files.exists():
            # Remove all "previous values" associations, since they prevent deleting files
            event.get_all_account_activity().update(previous_values_id=None)

            logger.info(f"Deleting {parsed_files.count()} existing files.")
            parsed_files.delete()

        logger.info(
            self.style.SUCCESS(f"Finished deleting data for event: {event_id}.")
        )
