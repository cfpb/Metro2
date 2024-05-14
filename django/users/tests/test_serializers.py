from datetime import date
from django.contrib.auth.models import Group, User
from django.test import TestCase

from evaluate_m2.tests.evaluator_test_helper import acct_record
from rest_framework.renderers import JSONRenderer
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
        self.group = Group.objects.create(name="event1")
        self.group.user_set.add(self.user)
        event = Metro2Event(id=1, name='test_exam', user_group=self.group)
        event.save()
        event2 = Metro2Event(id=2, name='another_exam', user_group=self.group)
        self.data_file = M2DataFile(event=event, file_name='file.txt')
        self.data_file.save()
        event2.save()
        self.data_file2 = M2DataFile(event=event2, file_name='file.txt')
        self.data_file2.save()
        self.activities = [
            {
                'id': 32, 'activity_date': date(2011, 7, 31), 'cons_acct_num': '0032',
            }, {
                'id': 33, 'activity_date': date(2012, 10, 31), 'cons_acct_num': '0033',
            }, {
                'id': 34, 'activity_date': date(2013, 11, 30), 'cons_acct_num': '0034',
            }, {
                'id': 35, 'activity_date': date(2020, 12, 31), 'cons_acct_num': '0035',
            }]
        self.json_representation = {
            'is_admin': False,
            'username': 'examiner',
            'assigned_events': [
                {
                    'id': 1, 'name': 'test_exam', 'date_range_start': '2011-07-31',
                    'date_range_end': '2020-12-31',
                }, {
                     'id': 2, 'name': 'another_exam', 'date_range_start': None,
                     'date_range_end': None,
                }
            ]
        }
    def test_user_view_serializer(self):
        for item in self.activities:
            acct_record(self.data_file, item)
        serializer = UserViewSerializer(self.user)
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render(self.json_representation)
        self.assertEqual(json_output, expected)
