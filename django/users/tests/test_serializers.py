from django.contrib.auth.models import Group, User
from django.test import TestCase

from parse_m2.models import Metro2Event
from users.serializers import UserViewSerializer


class UserViewSerializerTestCase(TestCase):
    def setUp(self) -> None:
        # Create a User record
        self.user = User.objects.create(
            username="examiner",
            password="",
            email="examiner@fake.gov"
        )
        self.group = Group.objects.create(name="event1")
        self.group.user_set.add(self.user)
        event = Metro2Event(id=1, name='test_exam', user_group=self.group)
        event.save()
        event2 = Metro2Event(id=2, name='another_exam', user_group=self.group)
        event2.save()

        self.json_representation = {
            "is_admin": False,
            "username": "examiner",
            "assigned_events": [
                { "id": 1, "name": "test_exam" }, { "id": 2, "name": "another_exam" }
            ]
        }

    def test_user_view_serializer(self):
        serializer = UserViewSerializer(self.user)
        self.assertEqual(serializer.data, self.json_representation)
