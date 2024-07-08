from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from parse_m2.models import Metro2Event


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py update_event_records -e [event_id]
    """
    help = "Starts the process to update previous_values on all records " + \
           "for the given event. "

    def add_arguments(self, argparser):
        event_help = "The ID of the event record in the database"
        argparser.add_argument("-e", "--event_id", nargs="?", required=True, help=event_help)

    def handle(self, *args, **options):
        event_id = options["event_id"]

        # Fetch the Metro2Event
        try:
            event = Metro2Event.objects.get(id=event_id)
        except Metro2Event.DoesNotExist:
            # If the event doesn't exist, exit
            raise CommandError(f"No event found with id {event_id}. Exiting.")

        event.post_parse()
        self.stdout.write(f"All records updated for event: {event.name}...")
