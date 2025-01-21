from django.core.management.base import BaseCommand, CommandError
from parse_m2.models import Metro2Event, M2DataFile


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py delete_event_data -e [event_id]
    """
    help = "Delete one Metro2 data file, by filename, for a specific event record. " + \
            "Do this when the parser failed or errored on a single file and you " + \
            "want to remove it and try again. " + \
            "WARNING: This shouldn't be used after evals have run, since it makes " + \
            "eval results invalid. WARNING: This can't be used after post_parse " + \
            "has been run, since prior_values prevent deleting a file."

    def add_arguments(self, argparser):
        event_help = "The ID of the event record"
        argparser.add_argument("-e", "--event_id", nargs="?", required=True, help=event_help)

        filename_help = "The file_name value of the file to delete"
        argparser.add_argument("-f", "--file_name", nargs="?", required=True, help=filename_help)

    def handle(self, *args, **options):
        event_id = options["event_id"]
        file_name = options["file_name"]

        # Fetch the Metro2Event
        try:
            event = Metro2Event.objects.get(id=event_id)
        except Metro2Event.DoesNotExist:
            # If the event doesn't exist, exit
            raise CommandError(f"No event found with id {event_id}. Exiting.")

        # Fetch the M2DataFile record
        try:
            datafile = M2DataFile.objects.get(event=event, file_name=file_name)
        except M2DataFile.DoesNotExist:
            # If the file doesn't exist, exit
            raise CommandError(f"No file found with name `{file_name}` for event id {event_id}. Exiting.")

        # Delete the file
        datafile.delete()

        self.stdout.write(
            self.style.SUCCESS(f"Finished deleting `{file_name}` for event: {event.name}.")
        )
