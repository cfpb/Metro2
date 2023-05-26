from django.contrib.auth.models import Group, User
from django.test import TestCase
from m2.models import Dataset


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


class TestDatasetAuthorization(TestCase):
    def setUp(self) -> None:
        self.exam_group = Group.objects.create(name="Exam2023")
        self.exam_group.save()

        self.dataset = Dataset.objects.create(name="OfficialExam2023",
                                              user_group=self.exam_group)
        self.dataset.save()

        self.examiner = User.objects.create(
            username="examiner", password="pass",
        )
        self.examiner.groups.set([self.exam_group])
        self.examiner.save()

        self.user_without_group = User.objects.create(
            username="other_user", password="pass",
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

    def test_single_dataset_view_contains_info_when_authorized(self):
        self.client.force_login(self.examiner)
        response = self.client.get("/datasets/OfficialExam2023/")
        self.assertContains(response, "OfficialExam2023", status_code=200)

    # TODO
    def xtest_single_dataset_view_redirects_when_not_authorized(self):
        self.client.force_login(self.user_without_group)
        response = self.client.get("/datasets/OfficialExam2023/")
        self.assertEqual(response.status_code, 302)