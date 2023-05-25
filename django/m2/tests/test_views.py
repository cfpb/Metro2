from django.contrib.auth.models import Group, User
from django.test import TestCase


class TestSecuredViews(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(
            username="user1", password="pass",
        )
        return super().setUp()
    
    # TODO: The tests targeting `/secured` and `/unsecured` are proofs
    # of concept for testing secured views. Once we add real paths/
    # endpoints, we can update these tests to use real URLs.
    def test_unsecured_view_doesnt_require_auth(self):
        response = self.client.get("/unsecured/")
        self.assertEqual(response.status_code, 200)
    
    def test_secured_view_redirects_when_unauthenticated(self):
        response = self.client.get("/secured/")
        self.assertEqual(response.status_code, 302)

    def test_secured_view_doesnt_redirect_when_authenticated(self):
        self.client.force_login(self.user1)
        response = self.client.get("/secured/")
        self.assertEqual(response.status_code, 200)
