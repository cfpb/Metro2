from parse_m2.models import Metro2Event
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Adds a user as a member to an existing event. " + \
           "Errors if no event name or username does not exist."

    def add_arguments(self, parser):
        parser.add_argument('--event', help="The name of the event to modify")
        parser.add_argument('--user', help="Username of user to add to the event")

    def handle(self, *args, **options):
        username_input = options['user']
        event_name = options['event']

        # Get the event object
        # If the event name doesn't exist, the command will fail
        evt = Metro2Event.objects.get(name=event_name)

        # Get the user object
        # If the user with this username doesn't exist, the command will fail
        usr = User.objects.get(username=username_input)

        # Add the user to the event
        evt.members.add(usr)

        self.stdout.write(self.style.SUCCESS(f"User {username_input} is now a member of event {event_name}"))
