from django.core.management.base import BaseCommand
from django.conf import settings

from evaluate_m2.evaluate import evaluator
from parse_m2.initiate_parsing import parse_files_from_local_filesystem
from parse_m2.models import Metro2Event


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py parse_local_and_evaluate -e [event_name] -d [local_data_directory]

    This command will check if an Event record has been created for the provided
    event_name.  If it does not exist, it will call the command that will fetch the
    files from the given directory, create an Event record and parse the data into the
    database. Then will call the command to run the evaluators.
    """
    default_event = 'Sample-Dataset-007'
    default_location = settings.LOCAL_EVENT_DATA
    help = "Starts the parse process on a directory of files in the local filesystem. " + \
           "Creates a new Metro2Event record for these Metro2 records. If no directory " + \
           "argument is provided, defaults to the LOCAL_EVENT_DATA setting in this " + \
           f"env: {default_location}"

    def add_arguments(self, argparser):
        event_help = "A name to identify this event record"
        argparser.add_argument("-e", "--event_name", nargs="?", required=True, help=event_help)

        dir_help = "Location is relative to the `/django` directory. " + \
            "Defaults to the LOCAL_EVENT_DATA setting in this environment: " + \
            self.default_location
        argparser.add_argument("-d", "--data_directory", nargs="?", required=False, help=dir_help)

    def handle(self, *args, **options):
        event_name = options["event_name"]
        data_directory = options["data_directory"]
        if not event_name:
            self.stdout.write(f"Using default event name: `{self.default_event}`.")
            event_name = self.event_name
        if not data_directory:
            self.stdout.write(f"Using default file location for Metro2 files: `{self.default_location}`.")
            data_directory = self.default_location

        try:
            existing_event = Metro2Event.objects.get(name=event_name)
        except Metro2Event.DoesNotExist:
            self.stdout.write(
                f"Beginning event `{event_name}`. Parsing files from local filesystem in `{data_directory}` directory.")
            event_record: Metro2Event = parse_files_from_local_filesystem(event_name, data_directory)

            self.stdout.write(
                self.style.SUCCESS(f"Created event ID: {event_record.id}. Finished parsing data for event: {event_name}.")
            )

            self.stdout.write(f"Beginning evaluators for event: {event_record.name}.")
            evaluator.run_evaluators(event_record)
            self.stdout.write(
                self.style.SUCCESS(f"Finished running evaluators for event ID: {event_record.id} and saving results."))
