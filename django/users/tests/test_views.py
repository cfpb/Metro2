from django.contrib.auth.models import Group, User
from django.test import TestCase

from users.models import Dataset
from unittest import mock


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


class TestDatasetListView(TestCase):
    def setUp(self) -> None:
        self.exam_group = Group.objects.create(name="Exam2023")

        self.dataset = Dataset.objects.create(name="OfficialExam2023",
                                              user_group=self.exam_group)

        self.examiner = User.objects.create(
            username="examiner", password="",
        )
        self.examiner.groups.set([self.exam_group])
        self.user_without_group = User.objects.create(
            username="other_user", password="",
        )
        return super().setUp()

    def test_datasets_list_view_redirects_when_not_authorized(self):
        self.client.logout()
        response = self.client.get("/datasets/")
        self.assertEqual(response.status_code, 302)

    def test_datasets_list_view_shows_allowed_datasets(self):
        self.client.force_login(self.examiner)
        response = self.client.get("/datasets/")
        self.assertContains(response, "OfficialExam2023", status_code=200)

    def test_datasets_list_view_when_no_datasets_allowed(self):
        self.client.force_login(self.user_without_group)
        response = self.client.get("/datasets/")
        self.assertNotContains(response, "OfficialExam2023", status_code=200)


class TestIndividualDatasetView(TestCase):
    def setUp(self) -> None:
        self.dataset = Dataset.objects.create(name="TestExamABC")
        self.user = User.objects.create(
            username="examiner", password="",
        )
        return super().setUp()

    def test_single_dataset_view_contains_info_when_authorized(self):
        self.client.force_login(self.user)
        with mock.patch.object(Dataset, "check_access_for_user") as access_check:
            # Mock the dataset.check_access_for_user method to return True
            access_check.return_value = True
            response = self.client.get(f"/datasets/{self.dataset.id}/")
            access_check.assert_called_once()
            self.assertContains(response, "TestExamABC", status_code=200)

    def test_single_dataset_view_returns_404_when_not_authorized(self):
        self.client.force_login(self.user)
        with mock.patch.object(Dataset, "check_access_for_user") as access_check:
            # Mock the dataset.check_access_for_user method to return False
            access_check.return_value = False
            response = self.client.get(f"/datasets/{self.dataset.id}/")
            access_check.assert_called_once()
            self.assertEqual(response.status_code, 404)


class TestUsersView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username="examiner",
            password="",
            email="examiner@fake.gov"
        )
        group = Group.objects.create(name="group1")
        group.user_set.add(self.user)
        group2 = Group.objects.create(name="group2")
        group2.user_set.add(self.user)

    def test_users_view(self):
        expected = {
            "is_admin": False,
            "username": "examiner",
            "assigned_events": [
                { "id": 1, "name": "group1" },
                { "id": 2, "name": "group2" }
            ]
        }
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_users_view_returns_404_when_not_found(self):
        response = self.client.get('/users/2')
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertContains(response, 'User ID: 2 does not exist.', status_code=404)