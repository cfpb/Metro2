from parse_m2.models import Metro2Event
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Adds an auth group to an existing event. " + \
           "Errors if no event exists with the given event name."

    def add_arguments(self, parser):
        parser.add_argument('--event', help="The name of the event to modify")
        parser.add_argument('--group', help="Auth group to add the event to")

    def handle(self, *args, **options):
        group_name = options['group']
        event_name = options['event']

        # Get the event object
        # If the event name doesn't exist, the command will fail
        evt = Metro2Event.objects.get(name=event_name)

        # Get or create the Group object
        try:
            grp = Group.objects.get(name=group_name)
            self.stdout.write(f"Auth group exists with name {group_name}.")
        except Group.DoesNotExist:
            grp = Group.objects.create(name=group_name)
            self.stdout.write(f"Created auth group with name {group_name}.")

        self.stdout.write(f"Modifying event `{event_name}` to use auth group `{group_name}`.")
        evt.user_group = grp
        evt.save()
        self.stdout.write(self.style.SUCCESS(f"Event `{event_name}` now uses the auth group `{group_name}`"))
