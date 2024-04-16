from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from io import StringIO

class GenerateAdminCommandTestCase(TestCase):
    def setUp(self) -> None:
        self.User = get_user_model()
        self.out = StringIO()

    def test_generate_admin_creates_user_when_needed(self):
        # Start with no users
        self.assertEqual(self.User.objects.count(), 0)

        # Run the command, which creates a user
        args = [
            "--username=test",
            "--password=test",
            "--group=test",
        ]
        call_command("generate_admin_user", *args, stdout=self.out)
        # User should exist now
        u1 = self.User.objects.get(username="test")
        self.assertTrue(u1.is_staff)
        # User should be in the 'test' group
        self.assertTrue(u1.groups.filter(name='test').exists())

    def test_generate_admin_upgrades_user_permissions_when_needed(self):
        # Start with a normal user with no permissions
        u1 = self.User.objects.create(username='test')
        self.assertFalse(u1.is_staff)

        # Run the command, which upgrades the user if it exists
        args = [
            "--username=test",
            "--password=test",
            "--group=test",
        ]
        call_command("generate_admin_user", *args, stdout=self.out)
        # Fetch the test user again
        u1 = self.User.objects.get(username="test")
        # User should be admin now
        self.assertTrue(u1.is_staff)

    def test_generate_admin_uses_existing_auth_group_if_available(self):
        # Start with an existing auth group
        g1 = Group.objects.create(name="admin")

        # Run the command, which uses the existing group
        args = [
            "--username=admin",
            "--password=admin",
            "--group=admin",
        ]
        call_command("generate_admin_user", *args, stdout=self.out)
        # The user should have the auth group
        u1 = self.User.objects.get(username="admin")
        self.assertEqual(u1.groups.first(), g1)
