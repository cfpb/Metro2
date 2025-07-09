from datetime import date
from io import StringIO

from django.core.management import call_command
from django.contrib.auth.models import User
from django.db.models import F
from django.test import TestCase

from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.models import Metro2Event, M2DataFile, AccountActivity

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

class UpdateActivityDateToDOAITestCase(TestCase):
    def setUp(self):
        self.event = Metro2Event.objects.create()
        self.file = M2DataFile.objects.create(event=self.event)
        return super().setUp()

    def test_set_values_using_f(self):
        acct_record(self.file,
            {'id': 3, 'activity_date': date(2025,2,14), 'doai': date(2023,9,30)})
        acct_record(self.file,
            {'id': 4, 'activity_date': date(2025,2,14), 'doai': date(2023,8,20)})
        acct_record(self.file,
            {'id': 5, 'activity_date': date(2025,2,14), 'doai': date(2021,3,31)})

        for file in self.event.m2datafile_set.all():
            file.accountactivity_set.update(activity_date=F('doai'))

        r1 = AccountActivity.objects.get(id=3)
        self.assertEqual(r1.activity_date, date(2023,9,30))

        r2 = AccountActivity.objects.get(id=4)
        self.assertEqual(r2.activity_date, date(2023,8,20))

        r3 = AccountActivity.objects.get(id=5)
        self.assertEqual(r3.activity_date, date(2021,3,31))