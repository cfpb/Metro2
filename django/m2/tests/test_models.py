from django.contrib.auth.models import Group, User
from django.test import TestCase
from m2.models import Dataset


class TestDataset(TestCase):
    def setUp(self) -> None:
        group1 = Group.objects.create(name="Exam2023")
        group2 = Group.objects.create(name="OtherGroup")

        self.dataset1 = Dataset.objects.create(
            name="OfficialExam2023", user_group=group1)
        self.dataset2 = Dataset.objects.create(
            name="OtherExam", user_group=group2)

        self.examiner = User.objects.create(username="examiner", password="")
        self.examiner.groups.set([group1, group2])
        self.user_without_group = User.objects.create(
            username="other_user", password="")
        return super().setUp()
    
    def test_access_true_for_user_in_correct_group(self):
        """
        When dataset.user_group contains the user,
        dataset.check_access_for_user should return True.
        """
        self.assertTrue(self.dataset1.check_access_for_user(self.examiner))
        self.assertTrue(self.dataset2.check_access_for_user(self.examiner))

    def test_access_false_for_user_without_correct_group(self):
        """
        When dataset.user_group does not contain the user, 
        dataset.check_access_for_user should return False.
        """
        self.assertFalse(self.dataset1.check_access_for_user(self.user_without_group))
        self.assertFalse(self.dataset2.check_access_for_user(self.user_without_group))