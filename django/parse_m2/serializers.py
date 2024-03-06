from rest_framework import serializers

from .models import AccountHolder


class AccountHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHolder
        exclude = ['data_file','activity_date']
