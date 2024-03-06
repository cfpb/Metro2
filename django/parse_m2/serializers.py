from rest_framework import serializers

from .models import AccountActivity


class AccountActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountActivity
        exclude = ['account_holder','cons_acct_num']
