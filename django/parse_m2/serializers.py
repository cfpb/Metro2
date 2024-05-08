from rest_framework import serializers

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
        inconsistencies = []
        eval_results = obj.evaluatorresult_set.all()
        for er in eval_results:
            evaluator = er.result_summary.evaluator.id
            inconsistencies.append(evaluator)

        return inconsistencies

class AccountHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHolder
        exclude = ['data_file','activity_date']

class Metro2EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metro2Event
        fields = ['id','name']