import logging

from django.core.management.base import BaseCommand, CommandError
from django.db.models import F
from parse_m2.models import Metro2Event


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py doai_activity_date -e event_id
    """
    help = "For all files on an event that have an activity_date set, " \
            "update each AccountActivity record so " + \
            "the account_activity value matches the DOAI. " + \
            "This is needed to correct a specific dataset, which " + \
            "included incorrect activity date values in provided data."

    def add_arguments(self, argparser):
        event_help = "The ID of the event record"
        argparser.add_argument("-e", "--event_id", nargs="?", required=True, help=event_help)

    def handle(self, *args, **options):
        logger = logging.getLogger('commands.doai_activity_date')
        event_id = options["event_id"]

        # Fetch the Metro2Event
        try:
            event = Metro2Event.objects.get(id=event_id)
        except Metro2Event.DoesNotExist:
            # If the event doesn't exist, exit
            raise CommandError(f"No event found with id {event_id}. Exiting.")

        for df in event.m2datafile_set.all():
            if df.activity_date:
                logger.info(f"Updating file {df.file_name}")
                df.accountactivity_set.update(activity_date=F('doai'))
            else:
                # For files that have activity_date=None, the DOAI is already used as
                # activity_date for the AccountActivity records. So, only update files
                # that have an activity date.
                logger.debug(f"Skipping file {df.file_name} since it already uses DOAI.")

        logger.info(
            self.style.SUCCESS(f"Finished updating Account Activity data for event: {event_id}.")
        )
