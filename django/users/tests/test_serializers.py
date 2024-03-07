from datetime import date
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from rest_framework.renderers import JSONRenderer

from users.serializers import GroupSerializer

class GroupSerializerTestCase(TestCase):
    def setUp(self) -> None:
        # Create an AccountActivity record
        ct = ContentType.objects.get_for_model(User)
        self.group = Group.objects.create(name="group")
        permission = Permission.objects.create(codename='read',
                                   name='Can read',
                                   content_type=ct)
        self.group.permissions.add(permission)

        self.json_representation = {
            "id": self.group.id,
            "name": "group"
        }

    def test_group_serializer(self):
        serializer = GroupSerializer(self.group)
        self.assertEqual(serializer.data, self.json_representation)

    def test_group_serializer_many_true(self):
        groups = [self.group]
        serializer = GroupSerializer(groups, many=True)
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render([self.json_representation])
        self.assertEqual(json_output, expected)
