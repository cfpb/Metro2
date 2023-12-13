from django.core.management.base import BaseCommand
from parse_m2.initiate_parsing import parse_files_from_local_filesystem
from parse_m2.models import Metro2Event
from django.conf import settings


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py parse_local -e [event_name] -d [local_data_directory]

    This command will fetch the files from the given directory, create an
    Event record, and parse the data into the database.
    """
    help = "Starts the parse process on a directory of files in the local filesystem"
    default_location = settings.LOCAL_EVENT_DATA

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

        self.stdout.write(
            f"Beginning event `{event_name}`. Parsing files from local filesystem in `{data_directory}` directory.")
        event_record: Metro2Event = parse_files_from_local_filesystem(event_name, data_directory)

        self.stdout.write(
            self.style.SUCCESS(f"Created event ID: {event_record.id}. Finished parsing data for event: {event_name}.")
        )
