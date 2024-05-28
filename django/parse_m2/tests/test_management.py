from django.core.management import call_command
from django.contrib.auth.models import User
from parse_m2.models import Metro2Event
from django.test import TestCase
from io import StringIO

class AddAuthToEventCommandTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="Jane Smith")
        self.out = StringIO()

    def test_generate_admin_creates_user_when_needed(self):
        # Start with an event
        Metro2Event.objects.create(name="my event")
        # Run the command, which creates an event if needed
        args = [
            "--user=Jane Smith",
            "--event=my event"
        ]
        call_command("add_user_to_event", *args, stdout=self.out)
        ev = Metro2Event.objects.get(name="my event")
        self.assertIn(self.user, ev.members.all())

