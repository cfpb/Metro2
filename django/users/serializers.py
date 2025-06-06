from rest_framework import serializers
from django.contrib.auth.models import User

from parse_m2.serializers import Metro2EventSerializer


class UserViewSerializer(serializers.ModelSerializer):
    assigned_events = serializers.SerializerMethodField(read_only=True)
    is_admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['is_admin','username', 'assigned_events']

    def get_assigned_events(self, obj: User):
        events = obj.metro2event_set.order_by('-id')
        eventSerializer = Metro2EventSerializer(events, many=True)
        return eventSerializer.data

    def get_is_admin(self, obj) -> bool:
        return obj.is_superuser == 1
