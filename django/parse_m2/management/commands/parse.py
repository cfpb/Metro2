from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from parse_m2.initiate_parsing_s3 import parse_files_from_s3_bucket
from parse_m2.initiate_parsing_local import parse_files_from_local_filesystem
from parse_m2.models import Metro2Event, M2DataFile
from parse_m2.initiate_updating_records import update_event_records
from evaluate_m2.models import EvaluatorResultSummary


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py parse -e [event_id]
    """
    help = "Starts the parse process for the given event. " + \
            "Checks the SSO_ENABLED setting to determine whether to use local or S3 files. " + \
            "Uses all files in the `directory` field on the event. " + \
            "Deletes all results of previous parse and evaluate runs for this event."

    def add_arguments(self, argparser):
        event_help = "The ID of the event record"
        argparser.add_argument("-e", "--event_id", nargs="?", required=True, help=event_help)

    def handle(self, *args, **options):
        event_id = options["event_id"]

        # Fetch the Metro2Event
        try:
            event = Metro2Event.objects.get(id=event_id)
        except Metro2Event.DoesNotExist:
            # If the event doesn't exist, exit
            raise CommandError(f"No event found with id {event_id}. Exiting.")

        # Delete results of previous parse
        self.stdout.write(f"Checking if M2DataFile records exist for event ID: {event_id}.")
        parsed_files = M2DataFile.objects.filter(event=event)
        if parsed_files.exists():
            self.stdout.write(f"Deleting {parsed_files.count()} existing files.")
            parsed_files.delete()

        # Delete results of previous evaluator run
        self.stdout.write(f"Checking if EvaluatorResultSummary records exist for event ID: {event_id}.")
        eval_results = EvaluatorResultSummary.objects.filter(event=event)
        if eval_results.exists():
            self.stdout.write(f"Deleting results of {eval_results.count()} evaluators from previous run of this event.")
            eval_results.delete()

        # Parse the data
        self.stdout.write(f"Parsing files from {event.directory} directory...")
        if settings.SSO_ENABLED:
            parse_files_from_s3_bucket(event)
        else:
            parse_files_from_local_filesystem(event)
        update_event_records(event)
        self.stdout.write(
            self.style.SUCCESS(f"Finished parsing data for event: {event.name}.")
        )
