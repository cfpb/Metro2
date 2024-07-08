from rest_framework import serializers

from .models import AccountActivity, AccountHolder, Metro2Event


class AccountActivitySerializer(serializers.ModelSerializer):
    inconsistencies = serializers.SerializerMethodField(read_only=True)
    cons_info_ind = serializers.SerializerMethodField(read_only=True)
    ecoa = serializers.SerializerMethodField(read_only=True)
    cons_info_ind_assoc = serializers.SerializerMethodField(read_only=True)
    ecoa_assoc = serializers.SerializerMethodField(read_only=True)
    purch_sold_ind = serializers.SerializerMethodField(read_only=True)
    balloon_pmt_amt = serializers.SerializerMethodField(read_only=True)
    change_ind = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = AccountActivity
        fields = ['id', 'inconsistencies', 'activity_date', 'port_type', 'acct_type',
                  'date_open', 'credit_limit', 'hcola', 'id_num', 'terms_dur',
                  'terms_freq', 'smpa', 'actual_pmt_amt', 'acct_stat', 'pmt_rating',
                  'php', 'spc_com_cd', 'compl_cond_cd', 'current_bal', 'amt_past_due',
                  'orig_chg_off_amt', 'doai', 'dofd', 'date_closed', 'dolp','int_type_ind',
                  'cons_info_ind', 'ecoa', 'cons_info_ind_assoc', 'ecoa_assoc',
                  'purch_sold_ind', 'balloon_pmt_amt', 'change_ind']

    def get_inconsistencies(self, obj):
        eval_ids = obj.evaluatorresult_set.values_list('result_summary__evaluator__id')
        return [x[0] for x in eval_ids]

    def get_cons_info_ind(self, obj):
        return obj.account_holder.cons_info_ind

    def get_ecoa(self, obj):
        return obj.account_holder.ecoa

    def get_cons_info_ind_assoc(self, obj):
        return obj.account_holder.cons_info_ind_assoc

    def get_ecoa_assoc(self, obj):
        return obj.account_holder.ecoa_assoc

    def get_purch_sold_ind(self, obj):
        if hasattr(obj, 'k2'):
            return obj.k2.purch_sold_ind

    def get_balloon_pmt_amt(self, obj):
        if hasattr(obj, 'k4'):
            return obj.k4.balloon_pmt_amt

    def get_change_ind(self, obj):
        if hasattr(obj, 'l1'):
            return obj.l1.change_ind

class AccountHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHolder
        exclude = ['data_file','activity_date','cons_info_ind_assoc', 'ecoa_assoc']

class Metro2EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metro2Event
        fields = ['id','name', 'portfolio', 'eid_or_matter_num',
                  'other_descriptor', 'date_range_start', 'date_range_end']
