from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from rest_framework.test import APITestCase


class TestBadRequestView(TestCase):

    def test_bad_request_view(self):
        response = self.client.get('/api/fake/')
        self.assertEqual(response.status_code, 400)

    def test_does_not_return_bad_request(self):
        response = self.client.get('/api/all-evaluator-metadata/')
        self.assertNotEqual(response.status_code, 400)


class TestVersionEndpoint(APITestCase):

    def test_unauth_does_not_get_version(self):
        response = self.client.get("/api/version/")
        self.assertEqual(response.status_code, 403)

    @override_settings(VERSION="testversion")
    def test_gets_version(self):
        user = get_user_model().objects.create_user(username="testuser")
        self.client.force_authenticate(user=user)

        response = self.client.get("/api/version/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"version": "testversion"})
