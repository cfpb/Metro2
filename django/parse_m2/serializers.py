from rest_framework import serializers

from .models import AccountActivity, AccountHolder, Metro2Event


class AccountActivitySerializer(serializers.ModelSerializer):
    inconsistencies = serializers.SerializerMethodField(read_only=True)
    account_holder__ecoa_assoc = serializers.SerializerMethodField()
    account_holder__surname = serializers.SerializerMethodField()
    account_holder__first_name = serializers.SerializerMethodField()
    account_holder__middle_name = serializers.SerializerMethodField()
    account_holder__gen_code = serializers.SerializerMethodField()
    account_holder__ssn = serializers.SerializerMethodField()
    account_holder__dob = serializers.SerializerMethodField()
    account_holder__phone_num = serializers.SerializerMethodField()
    account_holder__ecoa = serializers.SerializerMethodField()
    account_holder__cons_info_ind = serializers.SerializerMethodField()
    account_holder__cons_info_ind_assoc = serializers.SerializerMethodField()
    account_holder__country_cd = serializers.SerializerMethodField()
    account_holder__addr_line_1 = serializers.SerializerMethodField()
    account_holder__addr_line_2 = serializers.SerializerMethodField()
    account_holder__city = serializers.SerializerMethodField()
    account_holder__state = serializers.SerializerMethodField()
    account_holder__zip = serializers.SerializerMethodField()
    account_holder__addr_ind = serializers.SerializerMethodField()
    account_holder__res_cd = serializers.SerializerMethodField()
    k1__orig_creditor_name = serializers.SerializerMethodField()
    k1__creditor_classification = serializers.SerializerMethodField()
    k2__purch_sold_ind = serializers.SerializerMethodField(read_only=True)
    k2__purch_sold_name = serializers.SerializerMethodField(read_only=True)
    k3__agency_id = serializers.SerializerMethodField()
    k3__agency_acct_num = serializers.SerializerMethodField()
    k3__min = serializers.SerializerMethodField()
    k4__spc_pmt_ind = serializers.SerializerMethodField()
    k4__deferred_pmt_st_dt = serializers.SerializerMethodField()
    k4__balloon_pmt_due_dt = serializers.SerializerMethodField()
    k4__balloon_pmt_amt = serializers.SerializerMethodField()
    l1__change_ind = serializers.SerializerMethodField()
    l1__new_acc_num = serializers.SerializerMethodField()
    l1__new_id_num = serializers.SerializerMethodField()
    n1__employer_name = serializers.SerializerMethodField()
    n1__employer_addr1 = serializers.SerializerMethodField()
    n1__employer_addr2 = serializers.SerializerMethodField()
    n1__employer_city = serializers.SerializerMethodField()
    n1__employer_state = serializers.SerializerMethodField()
    n1__employer_zip = serializers.SerializerMethodField()
    n1__occupation = serializers.SerializerMethodField()

    class Meta:
        model = AccountActivity
        fields = '__all__'
        default_fields = [
            "id",
            "inconsistencies",
            "activity_date",
            "account_holder__surname",
            "account_holder__first_name",
            "port_type",
            "acct_type",
            "date_open",
            "credit_limit",
            "hcola",
            "id_num",
            "terms_dur",
            "terms_freq",
            "smpa",
            "actual_pmt_amt",
            "acct_stat",
            "pmt_rating",
            "php",
            "php1",
            "spc_com_cd",
            "compl_cond_cd",
            "current_bal",
            "amt_past_due",
            "orig_chg_off_amt",
            "doai",
            "dofd",
            "date_closed",
            "dolp",
            "int_type_ind",
            "account_holder__cons_info_ind",
            "account_holder__ecoa",
            "account_holder__cons_info_ind_assoc",
            "account_holder__ecoa_assoc",
            "k2__purch_sold_ind",
            "k2__purch_sold_name",
            "k4__balloon_pmt_amt",
            "l1__change_ind",
            "l1__new_id_num",
            "l1__new_acc_num",
        ]

    def __init__(self, *args, **kwargs):
        if "include_fields" in kwargs:
            include_fields = kwargs.pop("include_fields")
        else:
            include_fields = self.Meta.default_fields

        super().__init__(*args, **kwargs)

        if include_fields is not None:
            # If we were given fields to include, drop any that are not in
            # that set.
            # Based on the DRF example here: https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
            all_fields = set(self.fields)
            for field_name in all_fields - set(include_fields):
                self.fields.pop(field_name)

    def get_inconsistencies(self, obj):
        eval_ids = obj.evaluatorresult_set.values_list('result_summary__evaluator__id')
        return [x[0] for x in eval_ids]

    def get_account_holder__ecoa_assoc(self, obj):
        return obj.account_holder.ecoa_assoc

    def get_account_holder__surname(self, obj):
        return obj.account_holder.surname

    def get_account_holder__first_name(self, obj):
        return obj.account_holder.first_name

    def get_account_holder__middle_name(self, obj):
        return obj.account_holder.middle_name

    def get_account_holder__gen_code(self, obj):
        return obj.account_holder.gen_code

    def get_account_holder__ssn(self, obj):
        return obj.account_holder.ssn

    def get_account_holder__dob(self, obj):
        return obj.account_holder.dob

    def get_account_holder__phone_num(self, obj):
        return obj.account_holder.phone_num

    def get_account_holder__ecoa(self, obj):
        return obj.account_holder.ecoa

    def get_account_holder__cons_info_ind(self, obj):
        return obj.account_holder.cons_info_ind

    def get_account_holder__cons_info_ind_assoc(self, obj):
        return obj.account_holder.cons_info_ind_assoc

    def get_account_holder__country_cd(self, obj):
        return obj.account_holder.country_cd

    def get_account_holder__addr_line_1(self, obj):
        return obj.account_holder.addr_line_1

    def get_account_holder__addr_line_2(self, obj):
        return obj.account_holder.addr_line_2

    def get_account_holder__city(self, obj):
        return obj.account_holder.city

    def get_account_holder__state(self, obj):
        return obj.account_holder.state

    def get_account_holder__zip(self, obj):
        return obj.account_holder.zip

    def get_account_holder__addr_ind(self, obj):
        return obj.account_holder.addr_ind

    def get_account_holder__res_cd(self, obj):
        return obj.account_holder.res_cd

    def get_k1__orig_creditor_name(self, obj):
        if hasattr(obj, "k1"):
            return obj.k1.orig_creditor_name

    def get_k1__creditor_classification(self, obj):
        if hasattr(obj, "k1"):
            return obj.k1.creditor_classification

    def get_k2__purch_sold_ind(self, obj):
        if hasattr(obj, 'k2'):
            return obj.k2.purch_sold_ind

    def get_k2__purch_sold_name(self, obj):
        if hasattr(obj, 'k2'):
            return obj.k2.purch_sold_name

    def get_k3__agency_id(self, obj):
        if hasattr(obj, "k3"):
            return obj.k3.agency_id

    def get_k3__agency_acct_num(self, obj):
        if hasattr(obj, "k3"):
            return obj.k3.agency_acct_num

    def get_k3__min(self, obj):
        if hasattr(obj, "k3"):
            return obj.k3.min

    def get_k4__spc_pmt_ind(self, obj):
        if hasattr(obj, "k4"):
            return obj.k4.spc_pmt_ind

    def get_k4__deferred_pmt_st_dt(self, obj):
        if hasattr(obj, "k4"):
            return obj.k4.deferred_pmt_st_dt

    def get_k4__balloon_pmt_due_dt(self, obj):
        if hasattr(obj, "k4"):
            return obj.k4.balloon_pmt_due_dt

    def get_k4__balloon_pmt_amt(self, obj):
        if hasattr(obj, "k4"):
            return obj.k4.balloon_pmt_amt

    def get_l1__change_ind(self, obj):
        if hasattr(obj, "l1"):
            return obj.l1.change_ind

    def get_l1__new_id_num(self, obj):
        if hasattr(obj, "l1"):
            return obj.l1.new_id_num

    def get_l1__new_acc_num(self, obj):
        if hasattr(obj, "l1"):
            return obj.l1.new_acc_num

    def get_n1__employer_name(self, obj):
        if hasattr(obj, "n1"):
            return obj.n1.employer_name

    def get_n1__employer_addr1(self, obj):
        if hasattr(obj, "n1"):
            return obj.n1.employer_addr1

    def get_n1__employer_addr2(self, obj):
        if hasattr(obj, "n1"):
            return obj.n1.employer_addr2

    def get_n1__employer_city(self, obj):
        if hasattr(obj, "n1"):
            return obj.n1.employer_city

    def get_n1__employer_state(self, obj):
        if hasattr(obj, "n1"):
            return obj.n1.employer_state

    def get_n1__employer_zip(self, obj):
        if hasattr(obj, "n1"):
            return obj.n1.employer_zip

    def get_n1__occupation(self, obj):
        if hasattr(obj, "n1"):
            return obj.n1.occupation


class AccountHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHolder
        fields = ['id', 'surname', 'first_name', 'middle_name', 'gen_code',
                  'ssn', 'dob', 'phone_num', 'ecoa', 'cons_info_ind',
                  'country_cd', 'addr_line_1', 'addr_line_2', 'city', 'state',
                  'zip', 'addr_ind', 'res_cd', 'cons_acct_num']

class Metro2EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metro2Event
        fields = ['id','name', 'portfolio', 'eid_or_matter_num',
                  'other_descriptor', 'date_range_start', 'date_range_end']
