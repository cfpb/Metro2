from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase

from evaluate_m2.tests.evaluator_test_helper import acct_record
from rest_framework.renderers import JSONRenderer
from parse_m2.initiate_post_parsing import post_parse
from parse_m2.models import M2DataFile, Metro2Event
from users.serializers import UserViewSerializer


class UserViewSerializerTestCase(TestCase):
    def setUp(self) -> None:
        # Create a User record
        self.user = User.objects.create(
            username="examiner",
            password="",
            email="examiner@fake.gov"
        )
        event = Metro2Event.objects.create(id=1, name='test_exam')
        event.members.add(self.user)
        event2 = Metro2Event.objects.create(id=2, name='another_exam',
                                            eid_or_matter_num='123-345667', portfolio="mortgage loans",
                                            other_descriptor="exam")
        event2.members.add(self.user)
        self.data_file = M2DataFile.objects.create(event=event, file_name='file.txt')

        # Create account records for event 1
        [acct_record(self.data_file, item) for item in [
            { 'id': 32, 'activity_date': date(2011, 7, 31), 'cons_acct_num': '0032', },
            { 'id': 33, 'activity_date': date(2012, 10, 31), 'cons_acct_num': '0033', },
            { 'id': 34, 'activity_date': date(2013, 11, 30), 'cons_acct_num': '0034', },
            { 'id': 35, 'activity_date': date(2020, 12, 31), 'cons_acct_num': '0035', }]]
        post_parse(event)  # Ensure the event record has the date range saved

        self.json_representation = {
            'is_admin': False,
            'username': 'examiner',
            'assigned_events': [
                {
                    'id': 1, 'name': 'test_exam', 'portfolio': '',
                    'eid_or_matter_num': '', 'other_descriptor': '',
                    'date_range_start': '2011-07-31', 'date_range_end': '2020-12-31',
                }, {
                     'id': 2, 'name': 'another_exam', 'portfolio': 'mortgage loans',
                     'eid_or_matter_num': '123-345667', 'other_descriptor': 'exam',
                     'date_range_start': None, 'date_range_end': None,
                }
            ]
        }

    def test_user_view_serializer(self):
        serializer = UserViewSerializer(self.user)
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render(self.json_representation)
        self.assertEqual(json_output, expected)
