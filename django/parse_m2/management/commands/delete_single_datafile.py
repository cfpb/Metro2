import logging

from django.core.management.base import BaseCommand, CommandError
from parse_m2.models import Metro2Event, M2DataFile


class Command(BaseCommand):
    """
    Run this command in one of the following ways:
    > python manage.py delete_single_datafile -e [event_id] -f [file_name]
    > python manage.py delete_single_datafile -e [event_id] -i [file_id]
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
        argparser.add_argument("-f", "--file_name", nargs="?", required=False, help=filename_help)

        file_id_help = "The ID of the file to delete"
        argparser.add_argument("-i", "--file_id", nargs="?", required=False, help=file_id_help)


    def handle(self, *args, **options):
        logger = logging.getLogger('commands.delete_single_datafile')
        event_id = options["event_id"]
        file_name = options["file_name"]
        file_id = options["file_id"]

        # Check params for validity
        if file_name and file_id:
            raise CommandError("Either file name or file ID must be provided, not both. Exiting.")
        if not file_name and not file_id:
            raise CommandError("Either file name or file ID must be provided. Exiting.")

        # Fetch the Metro2Event
        try:
            event = Metro2Event.objects.get(id=event_id)
        except Metro2Event.DoesNotExist:
            # If the event doesn't exist, exit
            raise CommandError(f"No event found with id {event_id}. Exiting.")

        # Fetch the M2DataFile record
        try:
            if file_id:
                datafile =  M2DataFile.objects.get(event=event, id=file_id)
            elif file_name:
                datafile =  M2DataFile.objects.get(event=event, file_name=file_name)
        except M2DataFile.DoesNotExist:
            if file_id:
                msg = f"file ID `{file_id}`"
            else:
                msg = f"file name `{file_name}`"
            raise CommandError(f"No file found with {msg}. Exiting.")

        # Delete the file
        datafile.delete()

        logger.info(
            self.style.SUCCESS(f"Successfully deleted file {datafile.file_name} for event: {event.name}.")
        )
