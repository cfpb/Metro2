from django.core.management.base import BaseCommand
from django.conf import settings

from evaluate_m2.evaluate import evaluator
from parse_m2.initiate_parsing_local import parse_files_from_local_filesystem
from parse_m2.models import Metro2Event

class Command(BaseCommand):
    """
    This command will check if an Event record has been created for the provided
    event_name.  If it does not exist, it will call the command that will fetch the
    files from the given directory, create an Event record and parse the data into the
    database. Then will call the command to run the evaluators.
    """
    default_location = settings.LOCAL_EVENT_DATA
    help = "This command is used to add sample data in local development " + \
           "environments. It will create a new Metro2Event record with the " + \
           "provided event name if it does not exist or will quit if it exists."

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

        if not data_directory:
            self.stdout.write(f"Using default file location for Metro2 files: `{self.default_location}`.")
            data_directory = self.default_location

        if not Metro2Event.objects.filter(name=event_name).exists():
            self.stdout.write(f"Event Record does not exist for event name: {event_name}.")

            # Create a new Metro2Event. All records parsed will be associated with this Event.
            event = Metro2Event(name=event_name, directory=data_directory)
            event.save()
            self.stdout.write( f"Created an event record with name {event_name}. ID: {event.id}")

            self.stdout.write(f"Parsing files from local filesystem in `{data_directory}` directory.")
            parse_files_from_local_filesystem(event)
            event.post_parse()
            self.stdout.write(f"Beginning evaluators for event: {event.name}.")
            evaluator.run_evaluators(event)
            self.stdout.write(
                self.style.SUCCESS(f"Finished running evaluators and saving results."))

        else:
            self.stdout.write(f"An event record already exists for event name: {event_name}. No changes will be made.")
