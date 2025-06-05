from datetime import timedelta
from django.utils import timezone

from django.contrib.auth.models import User
from django.test import TestCase


from users import task


class TestUsersView(TestCase):
    def setUp(self) -> None:
        self.priv_user1 = User.objects.create(
            id=1,
            username="user1",
            email="user1@fake.gov",
            last_login=timezone.now() - timedelta(days=91),
            is_active=True,
            is_superuser=True
        )
        self.non_priv_user2 = User.objects.create(
            id=2,
            username="user2",
            email="user2@fake.gov",
            last_login=timezone.now() - timedelta(days=91),
            is_active=True,
            is_superuser=False
        )
        self.non_priv_user3 = User.objects.create(
            id=3,
            username="user3",
            email="user3@fake.gov",
            last_login=timezone.now() - timedelta(days=91),
            is_active=False,
            is_superuser=False
        )

    def test_disable_non_privileged_inactive_users(self):
        active_non_priv_user = User.objects.filter(is_active=True, is_superuser=False)
        self.assertEqual(1, active_non_priv_user.count())
        self.assertEqual(active_non_priv_user[0].username, 'user2')

        total_deactivated = User.objects.filter(is_active=False, is_superuser=False)
        self.assertEqual(1, total_deactivated.count())

        task.disable_non_privileged_inactive_users()
        total_deactivated = User.objects.filter(is_active=False, is_superuser=False)
        self.assertEqual(total_deactivated.count(), 2)

    def test_disable_privileged_inactive_users(self):
        user = User.objects.create(
            id=4,
            username="user4",
            email="user4@fake.gov",
            last_login=timezone.now() - timedelta(days=46),
            is_active=True,
            is_superuser=True
        )

        active_priv_user = User.objects.filter(is_active=True, is_superuser=True)
        self.assertEqual(2, active_priv_user.count())
        self.assertEqual(active_priv_user[0].username, 'user1')
        self.assertEqual(active_priv_user[1].username, 'user4')

        total_deactivated = User.objects.filter(is_active=False, is_superuser=True)
        self.assertEqual(0, total_deactivated.count())

        task.disable_privileged_inactive_users()
        total_deactivated = User.objects.filter(is_active=False, is_superuser=True)
        self.assertEqual(total_deactivated.count(), 2)