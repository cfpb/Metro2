import django_filters.rest_framework

from evaluate_m2.models import EvaluatorResult


class AnyCharFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    """Subclass CharFilter to allow multiple Char choices"""

    # If this value is given, filter on an empty sting.
    empty_value = "blank"

    # django-filter cannot filter on empty strings by default.
    # The documentaiton offers a couple of approaches to doing so, this is
    # based on one of them:
    # https://django-filter.readthedocs.io/en/stable/guide/tips.html#filtering-by-an-empty-string
    def filter(self, qs, value):
        if value is not None and self.empty_value in value:
            value = ["" if v == self.empty_value else v for v in value]
        return super().filter(qs, value)


class EvaluatorResultFilterSet(django_filters.rest_framework.FilterSet):
    """This filter set specifies `EvaluatorResult` fields to filter.

    Because the fields that we would filter `EvaluatorResult` objects by exist
    on their `source_record` relation, the fields here simply map the
    `source_record` field name to the correct field name for an
    `EvaluatorResult`.

    For example, the API might allow filtering `EvaluatorResults` by
    `acct_stat`, but the Django queryset will for `EvaluatorResults` will need
    to be filtered by `source_record__acct_stat`.
    """

    acct_type = django_filters.CharFilter(field_name="source_record__acct_type")
    acct_stat = AnyCharFilter(
        field_name="source_record__acct_stat",
    )
    compl_cond_cd = AnyCharFilter(field_name="source_record__compl_cond_cd")
    php = AnyCharFilter(field_name="source_record__php")
    php1 = AnyCharFilter(field_name="source_record__php1")
    pmt_rating = AnyCharFilter(field_name="source_record__pmt_rating")
    spc_com_cd = AnyCharFilter(field_name="source_record__spc_com_cd")
    terms_freq = AnyCharFilter(field_name="source_record__terms_freq")
    cons_info_ind = AnyCharFilter(
        field_name="source_record__cons_info_ind"
    )
    cons_info_ind_assoc = AnyCharFilter(
        field_name="source_record__cons_info_ind_assoc"
    )
    l1__change_ind = AnyCharFilter(field_name="source_record__l1__change_ind")

    # Dates, as a boolean where the date either exists or does not
    dofd = django_filters.BooleanFilter(
        field_name="source_record__dofd",
        lookup_expr="isnull",
        exclude=True,
    )
    date_closed = django_filters.BooleanFilter(
        field_name="source_record__date_closed",
        lookup_expr="isnull",
        exclude=True,
    )

    # Amounts, as ranges of values with _max and _min fields
    amt_past_due = django_filters.RangeFilter(
        field_name="source_record__amt_past_due",
    )
    current_bal = django_filters.RangeFilter(
        field_name="source_record__current_bal",
    )
    smpa = django_filters.RangeFilter(
        field_name="source_record__smpa",
    )

    # Sort ordering filter for all the relevant fields from AccountActivity
    # This just maps sortable fields from the source_record on EvaluatorResult
    # to the field name on AccountActivity.
    sort = django_filters.OrderingFilter(
        fields=(
            ("source_record__activity_date", "activity_date"),
            ("source_record__port_type", "port_type"),
            ("source_record__acct_type", "acct_type"),
            ("source_record__date_open", "date_open"),
            ("source_record__credit_limit", "credit_limit"),
            ("source_record__hcola", "hcola"),
            ("source_record__id_num", "id_num"),
            ("source_record__terms_dur", "terms_dur"),
            ("source_record__terms_freq", "terms_freq"),
            ("source_record__smpa", "smpa"),
            ("source_record__actual_pmt_amt", "actual_pmt_amt"),
            ("source_record__acct_stat", "acct_stat"),
            ("source_record__pmt_rating", "pmt_rating"),
            ("source_record__php", "php"),
            ("source_record__php1", "php1"),
            ("source_record__spc_com_cd", "spc_com_cd"),
            ("source_record__compl_cond_cd", "compl_cond_cd"),
            ("source_record__current_bal", "current_bal"),
            ("source_record__amt_past_due", "amt_past_due"),
            ("source_record__orig_chg_off_amt", "orig_chg_off_amt"),
            ("source_record__doai", "doai"),
            ("source_record__dofd", "dofd"),
            ("source_record__date_closed", "date_closed"),
            ("source_record__dolp", "dolp"),
            ("source_record__int_type_ind", "int_type_ind"),
            ("source_record__cons_info_ind", "cons_info_ind"),
            ("source_record__ecoa", "ecoa"),
            ("source_record__cons_info_ind_assoc", "cons_info_ind_assoc"),
            ("source_record__ecoa_assoc", "ecoa_assoc"),
            ("source_record__k2__purch_sold_ind", "k2__purch_sold_ind"),
            ("source_record__k2__purch_sold_name", "k2__purch_sold_name"),
            ("source_record__k4__balloon_pmt_amt", "k4__balloon_pmt_amt"),
            ("source_record__l1__change_ind", "l1__change_ind"),
            ("source_record__l1__new_id_num", "l1__new_id_num"),
            ("source_record__l1__new_acc_num", "l1__new_acc_num"),
        )
    )

    class Meta:
        model = EvaluatorResult
        fields = [
            "acct_type",
            "acct_stat",
            "compl_cond_cd",
            "php",
            "pmt_rating",
            "spc_com_cd",
            "terms_freq",
            "cons_info_ind",
            "l1__change_ind",
            "dofd",
            "date_closed",
            "amt_past_due",
            "current_bal",
            "smpa",
            "sort",
        ]
