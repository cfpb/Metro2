from django.core.management import call_command
from django.contrib.auth.models import Group
from parse_m2.models import Metro2Event
from django.test import TestCase
from io import StringIO

class AddAuthToEventCommandTestCase(TestCase):
    def setUp(self) -> None:
        self.out = StringIO()

    def test_generate_admin_creates_user_when_needed(self):
        # Start with an event
        Metro2Event.objects.create(name="my event")
        # Run the command, which creates an event if needed
        args = [
            "--group=test group",
            "--event=my event"
        ]
        call_command("add_auth_group_to_event", *args, stdout=self.out)
        gr = Group.objects.get(name="test group")
        ev = Metro2Event.objects.get(name="my event")
        self.assertEqual(ev.user_group, gr)

