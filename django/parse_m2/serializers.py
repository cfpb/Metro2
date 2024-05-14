from rest_framework import serializers

from evaluate_m2.evaluate_utils import get_activity_date_range
from .models import AccountActivity, AccountHolder, Metro2Event


class AccountActivitySerializer(serializers.ModelSerializer):
    inconsistencies = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = AccountActivity
        fields = ['id', 'inconsistencies', 'activity_date', 'port_type', 'acct_type',
                  'date_open', 'credit_limit', 'hcola', 'id_num', 'terms_dur',
                  'terms_freq', 'smpa', 'actual_pmt_amt', 'acct_stat', 'pmt_rating',
                  'php', 'spc_com_cd', 'compl_cond_cd', 'current_bal', 'amt_past_due',
                  'orig_chg_off_amt', 'doai', 'dofd', 'date_closed', 'dolp','int_type_ind']

    def get_inconsistencies(self, obj):
        eval_ids = obj.evaluatorresult_set.values_list('result_summary__evaluator__id')
        return [x[0] for x in eval_ids]

class AccountHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHolder
        exclude = ['data_file','activity_date']

class Metro2EventSerializer(serializers.ModelSerializer):
    date_range_start = serializers.SerializerMethodField(read_only=True)
    date_range_end = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Metro2Event
        fields = ['id','name', 'date_range_start', 'date_range_end']

    def get_date_range_start(self, obj):
        record_set = obj.get_all_account_activity()
        if record_set.exists():
            date_range = get_activity_date_range(record_set)
            return date_range["earliest"]

    def get_date_range_end(self, obj):
        record_set = obj.get_all_account_activity()
        if record_set.exists():
            date_range = get_activity_date_range(record_set)
            return date_range["latest"]
