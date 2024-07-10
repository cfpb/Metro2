import json
from datetime import date

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase


from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.models import M2DataFile, Metro2Event
from parse_m2.initiate_post_parsing import post_parse
from users.views import users_view


class TestUsersView(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create(
            id=1,
            username="examiner",
            email="examiner@fake.gov"
        )
        event = Metro2Event.objects.create(id=1, name='test_exam')
        event.members.add(self.user)
        data_file = M2DataFile.objects.create(event=event, file_name='file.txt')

        # Create account activity records for Event 1
        [acct_record(data_file, item) for item in [
            { 'id': 32, 'activity_date': date(2019, 7, 31), 'cons_acct_num': '0032', },
            { 'id': 33, 'activity_date': date(2019, 10, 31), 'cons_acct_num': '0033', },
            { 'id': 34, 'activity_date': date(2019, 11, 30), 'cons_acct_num': '0034', },
            { 'id': 35, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0035', }]]
        post_parse(event)  # Ensure the event record has the date range saved

        e2 = Metro2Event.objects.create(id=2, name='test_exam2', eid_or_matter_num='887-656565',
                                   portfolio="credit cards", other_descriptor="2025")
        e2.members.add(self.user)

    def test_users_view(self):
        expected = {
            'is_admin': False,
            'username': 'examiner',
            'assigned_events': [
                {
                    'id': 1, 'name': 'test_exam', 'portfolio': '',
                    'eid_or_matter_num': '', 'other_descriptor': '',
                    'date_range_start': '2019-07-31', 'date_range_end': '2019-12-31',
                }, {
                     'id': 2, 'name': 'test_exam2', 'portfolio': 'credit cards',
                     'eid_or_matter_num': '887-656565', 'other_descriptor': '2025',
                     'date_range_start': None, 'date_range_end': None
                }]}

        response = self.client.get('/api/users/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_users_view_returns_404_when_not_found(self):
        response = self.client.get('/api/users/2/')
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertContains(response, 'User ID: 2 does not exist.', status_code=404)

    def test_users_view_with_sso_enabled_returns_response(self):
        current_user = User.objects.create(
            id=2,
            username="sso_user",
            email="sso_user@fake.gov"
        )
        with self.settings(SSO_ENABLED = True):
            request = self.factory.get('/api/users/')
            request.user = current_user
            response = users_view(request)
            data = json.loads(response.content)
            self.assertEqual(data['username'], 'sso_user')
            self.assertEqual(response.headers['Content-Type'], 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_users_view_without_sso_enabled_returns_response(self):
        with self.settings(SSO_ENABLED = False):
            request = self.factory.get('/api/users/')
            response = users_view(request)
            data = json.loads(response.content)
            self.assertEqual(data['username'], 'examiner')
            self.assertEqual(response.headers['Content-Type'], 'application/json')
            self.assertEqual(response.status_code, 200)
