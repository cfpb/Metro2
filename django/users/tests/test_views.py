import json
import os
from unittest import mock
from django.contrib.auth.models import Group, User
from django.test import RequestFactory, TestCase

from parse_m2.models import Metro2Event
from users.views import users_view

class TestUsersView(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        # Create a User record
        self.user = User.objects.create(
            id=1,
            username="examiner",
            email="examiner@fake.gov"
        )
        group = Group.objects.create(name="event1")
        group.user_set.add(self.user)
        event = Metro2Event(id=1, name='test_exam', user_group=group)
        event.save()
        event2 = Metro2Event(id=2, name='test_exam2', user_group=group)
        event2.save()

    def test_users_view(self):
        expected = {
            "is_admin": False,
            "username": "examiner",
            "assigned_events": [
                { "id": 1, "name": "test_exam" },
                { "id": 2, "name": "test_exam2" }
            ]
        }
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
        with mock.patch.dict(os.environ, {"ENABLE_SSO": 'enabled'}):
            request = self.factory.get('/api/users/')
            request.user = current_user
            response = users_view(request)
            data = json.loads(response.content)
            self.assertEqual(data['username'], 'sso_user')
            self.assertEqual(response.headers['Content-Type'], 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_users_view_without_sso_enabled_returns_response(self):
         with mock.patch.dict(os.environ, {"ENABLE_SSO": 'not enabled'}):
            request = self.factory.get('/api/users/')
            response = users_view(request)
            data = json.loads(response.content)
            self.assertEqual(data['username'], 'examiner')
            self.assertEqual(response.headers['Content-Type'], 'application/json')
            self.assertEqual(response.status_code, 200)
