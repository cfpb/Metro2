from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from evaluate_m2.views_utils import (
    get_randomizer,
    has_permissions_for_request
)
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
        self.event = Metro2Event.objects.create(id=1, name='test_exam')
        self.event.members.add(self.user)
        self.event2 = Metro2Event.objects.create(id=2, name='another_exam')

    def test_has_permissions_for_request_sso_not_enabled(self):
        with self.settings(SSO_ENABLED = False):
            output = has_permissions_for_request(self.client.get('/'), self.event)
            self.assertEqual(output, True)

    def test_has_permissions_for_request_sso_enabled(self):
        with self.settings(SSO_ENABLED = True):
            request = self.factory.get('/api_call')
            request.user = self.user
            output = has_permissions_for_request(request, self.event)
            self.assertEqual(output, True)

    def test_has_permissions_for_request_sso_enabled_no_permission(self):
        with self.settings(SSO_ENABLED = True):
            request = self.factory.get('/api_call')
            request.user = self.user
            output = has_permissions_for_request(request, self.event2)
            self.assertEqual(output, False)

    def test_get_randomizer_less_than_page_size(self):
        total = 19
        page_total = 20
        output = get_randomizer(total, page_total)
        # 19/20 = 0
        self.assertEqual(output, 1)

    def test_get_randomizer_more_than_page_size(self):
        total = 74
        page_total = 20
        output = get_randomizer(total, page_total)
        # 74 / 20 = 3.7
        self.assertEqual(output, 3)