from rest_framework import serializers

from .models import AccountActivity, AccountHolder


class AccountHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHolder
        exclude = ['data_file','activity_date']


class AccountActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountActivity
        exclude = ['account_holder','cons_acct_num']
