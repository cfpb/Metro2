import django_filters.rest_framework

from evaluate_m2.models import EvaluatorResultMaterializedView


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
    """This filter set specifies `EvaluatorResultMaterializedView` fields to filter.

    Because the fields that we would filter `EvaluatorResult` objects by exist
    on their `source_record` relation, the fields here simply map the
    `source_record` field name to the correct field name for an
    `EvaluatorResult`.

    For example, the API might allow filtering `EvaluatorResults` by
    `acct_stat`, but the Django queryset will for `EvaluatorResults` will need
    to be filtered by `acct_stat`.
    """

    acct_type = django_filters.CharFilter(field_name="acct_type")
    acct_stat = AnyCharFilter(
        field_name="acct_stat",
    )
    compl_cond_cd = AnyCharFilter(field_name="compl_cond_cd")
    php = AnyCharFilter(field_name="php")
    php1 = AnyCharFilter(field_name="php1")
    pmt_rating = AnyCharFilter(field_name="pmt_rating")
    spc_com_cd = AnyCharFilter(field_name="spc_com_cd")
    terms_freq = AnyCharFilter(field_name="terms_freq")
    cons_info_ind = AnyCharFilter(field_name="cons_info_ind")
    cons_info_ind_assoc = AnyCharFilter(field_name="cons_info_ind_assoc")
    l1__change_ind = AnyCharFilter(field_name="change_ind")

    # Dates, as a boolean where the date either exists or does not
    dofd = django_filters.BooleanFilter(
        field_name="dofd",
        lookup_expr="isnull",
        exclude=True,
    )
    date_closed = django_filters.BooleanFilter(
        field_name="date_closed",
        lookup_expr="isnull",
        exclude=True,
    )

    # Amounts, as ranges of values with _max and _min fields
    amt_past_due = django_filters.RangeFilter(
        field_name="amt_past_due",
    )
    current_bal = django_filters.RangeFilter(
        field_name="current_bal",
    )
    smpa = django_filters.RangeFilter(
        field_name="smpa",
    )

    # Sort ordering filter for all the relevant fields from AccountActivity
    # This just maps sortable fields from the source_record on EvaluatorResult
    # to the field name on AccountActivity.
    sort = django_filters.OrderingFilter(
        fields=(
            ("activity_date", "activity_date"),
            ("cons_acct_num", "cons_acct_num"),
            ("port_type", "port_type"),
            ("acct_type", "acct_type"),
            ("date_open", "date_open"),
            ("credit_limit", "credit_limit"),
            ("hcola", "hcola"),
            ("id_num", "id_num"),
            ("terms_dur", "terms_dur"),
            ("terms_freq", "terms_freq"),
            ("smpa", "smpa"),
            ("actual_pmt_amt", "actual_pmt_amt"),
            ("acct_stat", "acct_stat"),
            ("pmt_rating", "pmt_rating"),
            ("php", "php"),
            ("php1", "php1"),
            ("spc_com_cd", "spc_com_cd"),
            ("compl_cond_cd", "compl_cond_cd"),
            ("current_bal", "current_bal"),
            ("amt_past_due", "amt_past_due"),
            ("orig_chg_off_amt", "orig_chg_off_amt"),
            ("doai", "doai"),
            ("dofd", "dofd"),
            ("date_closed", "date_closed"),
            ("dolp", "dolp"),
            ("int_type_ind", "int_type_ind"),
            ("cons_info_ind", "cons_info_ind"),
            ("ecoa", "ecoa"),
            ("cons_info_ind_assoc", "cons_info_ind_assoc"),
            ("ecoa_assoc", "ecoa_assoc"),
            ("first_name", "first_name"),
            ("surname", "surname"),

            # For all of these that are relations on the original models but
            # direct fields on the materialized view, we keep the original
            # Django __ related fieldname on the sort parameter side. That's
            # the name the front-end knows the field as.
            ("purch_sold_ind", "k2__purch_sold_ind"),
            ("purch_sold_name", "k2__purch_sold_name"),
            ("balloon_pmt_amt", "k4__balloon_pmt_amt"),
            ("change_ind", "l1__change_ind"),
            ("new_id_num", "l1__new_id_num"),
            ("new_acc_num", "l1__new_acc_num"),
            ("prior_cons_info_ind", "previous_values__cons_info_ind"),
            (
                "prior_cons_info_ind_assoc",
                "previous_values__cons_info_ind_assoc",
            ),
            ("prior_ecoa", "previous_values__ecoa"),
            ("prior_first_name", "previous_values__first_name"),
            ("prior_surname", "previous_values__surname"),
            ("prior_change_ind", "previous_values__l1__change_ind"),
            ("prior_new_acc_num", "previous_values__l1__new_acc_num"),
            ("prior_new_id_num", "previous_values__l1__new_id_num"),
            ("prior_activity_date", "previous_values__activity_date"),
            ("prior_port_type", "previous_values__port_type"),
            ("prior_acct_type", "previous_values__acct_type"),
            ("prior_date_open", "previous_values__date_open"),
            ("prior_acct_stat", "previous_values__acct_stat"),
            ("prior_pmt_rating", "previous_values__pmt_rating"),
            ("prior_current_bal", "previous_values__current_bal"),
            ("prior_orig_chg_off_amt", "previous_values__orig_chg_off_amt"),
            ("prior_dofd", "previous_values__dofd"),
            ("prior_date_closed", "previous_values__date_closed"),
            ("prior_id_num", "previous_values__id_num"),
        )
    )

    class Meta:
        model = EvaluatorResultMaterializedView
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
