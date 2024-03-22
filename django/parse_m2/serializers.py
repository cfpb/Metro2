from rest_framework import serializers

from .models import AccountActivity, AccountHolder, Metro2Event


class AccountActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountActivity
        exclude = ['account_holder','cons_acct_num']

class AccountHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHolder
        exclude = ['data_file','activity_date']

class Metro2EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metro2Event
        fields = ['id','name']