from operator import attrgetter

from rest_framework import serializers

from parse_m2.models import AccountActivity, Metro2Event


class OptionalRelatedField(serializers.Field):
    """A dotted-path attribute lookup on related object fields"""
    def __init__(self, path, **kwargs):
        self._getter = attrgetter(path)
        # Pass the entire object to to_representation()
        kwargs["source"] = "*"
        # This field is only ever read-only
        kwargs["read_only"] = True
        super().__init__(**kwargs)

    def to_representation(self, obj):
        try:
            return self._getter(obj)
        except AttributeError:
            return None


class AccountActivitySerializer(serializers.ModelSerializer):
    inconsistencies = serializers.SerializerMethodField(read_only=True)
    k1__orig_creditor_name = OptionalRelatedField("k1.orig_creditor_name")
    k1__creditor_classification = OptionalRelatedField("k1.creditor_classification")
    k2__purch_sold_ind = OptionalRelatedField("k2.purch_sold_ind")
    k2__purch_sold_name = OptionalRelatedField("k2.purch_sold_name")
    k3__agency_id = OptionalRelatedField("k3.agency_id")
    k3__agency_acct_num = OptionalRelatedField("k3.agency_acct_num")
    k3__min = OptionalRelatedField("k3.min")
    k4__spc_pmt_ind = OptionalRelatedField("k4.spc_pmt_ind")
    k4__deferred_pmt_st_dt = OptionalRelatedField("k4.deferred_pmt_st_dt")
    k4__balloon_pmt_due_dt = OptionalRelatedField("k4.balloon_pmt_due_dt")
    k4__balloon_pmt_amt = OptionalRelatedField("k4.balloon_pmt_amt")
    l1__change_ind = OptionalRelatedField("l1.change_ind")
    l1__new_acc_num = OptionalRelatedField("l1.new_acc_num")
    l1__new_id_num = OptionalRelatedField("l1.new_id_num")
    n1__employer_name = OptionalRelatedField("n1.employer_name")
    n1__employer_addr1 = OptionalRelatedField("n1.employer_addr1")
    n1__employer_addr2 = OptionalRelatedField("n1.employer_addr2")
    n1__employer_city = OptionalRelatedField("n1.employer_city")
    n1__employer_state = OptionalRelatedField("n1.employer_state")
    n1__employer_zip = OptionalRelatedField("n1.employer_zip")
    n1__occupation = OptionalRelatedField("n1.occupation")
    previous_values = serializers.HiddenField(default=None)
    previous_values__first_name = OptionalRelatedField("previous_values.first_name")
    previous_values__surname = OptionalRelatedField("previous_values.surname")
    previous_values__activity_date = OptionalRelatedField(
        "previous_values.activity_date"
    )
    previous_values__id_num = OptionalRelatedField("previous_values.id_num")
    previous_values__port_type = OptionalRelatedField("previous_values.port_type")
    previous_values__acct_type = OptionalRelatedField("previous_values.acct_type")
    previous_values__date_open = OptionalRelatedField("previous_values.date_open")
    previous_values__acct_stat = OptionalRelatedField("previous_values.acct_stat")
    previous_values__pmt_rating = OptionalRelatedField(
        "previous_values.pmt_rating"
    )
    previous_values__current_bal = OptionalRelatedField("previous_values.current_bal")
    previous_values__orig_chg_off_amt = OptionalRelatedField(
        "previous_values.orig_chg_off_amt"
    )
    previous_values__dofd = OptionalRelatedField("previous_values.dofd")
    previous_values__date_closed = OptionalRelatedField("previous_values.date_closed")
    previous_values__cons_info_ind = OptionalRelatedField(
        "previous_values.cons_info_ind"
    )
    previous_values__cons_info_ind_assoc = OptionalRelatedField(
        "previous_values.cons_info_ind_assoc"
    )
    previous_values__ecoa = OptionalRelatedField("previous_values.ecoa")
    previous_values__l1__change_ind = OptionalRelatedField(
        "previous_values.l1.change_ind"
    )
    previous_values__l1__new_acc_num = OptionalRelatedField(
        "previous_values.l1.new_acc_num"
    )
    previous_values__l1__new_id_num = OptionalRelatedField(
        "previous_values.l1.new_id_num"
    )

    class Meta:
        model = AccountActivity
        fields = '__all__'
        default_fields = [
            "id",
            "inconsistencies",
            "activity_date",
            "surname",
            "first_name",
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
            "cons_info_ind",
            "ecoa",
            "cons_info_ind_assoc",
            "ecoa_assoc",
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


class AccountHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountActivity
        fields = ['id', 'surname', 'first_name', 'middle_name', 'gen_code',
                  'ssn', 'dob', 'phone_num', 'ecoa', 'cons_info_ind',
                  'country_cd', 'addr_line_1', 'addr_line_2', 'city', 'state',
                  'zip', 'addr_ind', 'res_cd', 'cons_acct_num']

class Metro2EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metro2Event
        fields = ['id','name', 'portfolio', 'eid_or_matter_num',
                  'other_descriptor', 'date_range_start', 'date_range_end']
