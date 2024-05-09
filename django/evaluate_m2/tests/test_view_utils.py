from django.contrib.auth.models import Group, User
from django.test import RequestFactory, TestCase

from evaluate_m2.views_utils import has_permissions_for_request
from parse_m2.models import Metro2Event


class ViewUtilsTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        # Create a User record
        self.user = User.objects.create(
            username="examiner",
            password="",
            email="examiner@fake.gov"
        )
        self.group = Group.objects.create(name="event1")
        self.group.user_set.add(self.user)
        self.event = Metro2Event(id=1, name='test_exam', user_group=self.group)
        self.event.save()
        self.event2 = Metro2Event(id=2, name='another_exam')
        self.event2.save()

    def test_has_permissions_for_request_sso_not_enabled(self):
        with self.settings(ENABLE_SSO='not_enabled'):
            output = has_permissions_for_request(self.client.get('/'), self.event)
            self.assertEqual(output, True)

    def test_has_permissions_for_request_sso_enabled(self):
        with self.settings(ENABLE_SSO='enabled'):
            request = self.factory.get('/api_call')
            request.user = self.user
            output = has_permissions_for_request(request, self.event)
            self.assertEqual(output, True)

    def test_has_permissions_for_request_sso_enabled_no_permission(self):
        with self.settings(ENABLE_SSO='enabled'):
            request = self.factory.get('/api_call')
            request.user = self.user
            output = has_permissions_for_request(request, self.event2)
            self.assertEqual(output, False)