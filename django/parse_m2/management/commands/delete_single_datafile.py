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

        # Fetch the Metro2Event
        try:
            event = Metro2Event.objects.get(id=event_id)
        except Metro2Event.DoesNotExist:
            # If the event doesn't exist, exit
            raise CommandError(f"No event found with id {event_id}. Exiting.")

        # Fetch the M2DataFile record
        try:
            if file_id:
                logger.info(f"Searching for file with file_id {file_id} for event {event.id}...")
                datafile =  M2DataFile.objects.get(event=event, id=file_id)
            elif file_name:
                logger.info(f"Searching for file with file_name {file_name} for event {event.id}...")
                datafile =  M2DataFile.objects.get(event=event, file_name=file_name)
            else:
                raise CommandError("Either file name or file ID must be provided. Exiting.")
        except M2DataFile.DoesNotExist:
            raise CommandError(f"No such file found. Exiting.")

        # Delete the file
        datafile.delete()

        logger.info(
            self.style.SUCCESS(f"Finished deleting `{file_name}` for event: {event.name}.")
        )
