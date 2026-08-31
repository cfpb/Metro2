from functools import reduce

from django.db.models import Q

import django_filters.rest_framework
from django_filters.constants import EMPTY_VALUES

from evaluate_m2.models import EvaluatorResultMaterializedView
from parse_m2.models import AccountActivity


class NullInclusiveFilterMixin:
    # If this value is given, filter on a null value
    null_value = "blank"
    match_empty_string = True

    def get_null_query(self, values, null_value="blank"):
        query = Q()

        if values is not None and self.null_value in values:
            # Construct values that do not include the the null placeholder
            # and add a null value query
            values = [v for v in values if v != self.null_value]
            query |= Q(**{f"{self.field_name}__isnull": True})
            if self.match_empty_string:
                query |= Q(**{self.field_name: ""})

        return values, query


class AnyCharFilter(django_filters.BaseInFilter, NullInclusiveFilterMixin):
    """Match any char value in a CharField"""

    # Override the filter method to construct a query that will filter for
    # values and null.
    def filter(self, qs, values):
        if values in EMPTY_VALUES:
            return qs

        # Pull out a null value as a separate query
        values, query = self.get_null_query(values)

        # Filter for remaining values
        if len(values) > 0:
            query |= Q(**{f"{self.field_name}__{self.lookup_expr}": values})

        return self.get_method(qs)(query)


class JSONArrayContainsFilter(django_filters.BaseCSVFilter, NullInclusiveFilterMixin):
    """Match any value in a JSONField array"""
    match_empty_string = False

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("lookup_expr", "contains")
        super().__init__(*args, **kwargs)

    def filter(self, qs, values):
        if values in EMPTY_VALUES:
            return qs

        # Pull out a null value as a separate query
        values, query = self.get_null_query(values)

        if len(values) > 0:
            # Construct a Q object for every potential value
            query |= reduce(
                Q.__or__,
                (Q(**{f"{self.field_name}__{self.lookup_expr}": [v]}) for v in values)
            )

        return self.get_method(qs)(query)


class EvaluatorResultFilterSet(django_filters.rest_framework.FilterSet):
    """This filter set specifies `EvaluatorResultMaterializedView` fields to filter.
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
    cons_info_ind_assoc = JSONArrayContainsFilter(field_name="cons_info_ind_assoc")
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


class AccountListFilterSet(django_filters.rest_framework.FilterSet):
    cons_acct_num = django_filters.BaseInFilter(
        field_name="cons_acct_num",
        lookup_expr="in"
    )

    class Meta:
        model = AccountActivity
        fields = ["cons_acct_num"]

    # Require a specific list of accounts to filter, otherwise this
    # filter will return an empty queryset.
    def filter_queryset(self, queryset):
        if not self.form.cleaned_data.get("cons_acct_num"):
            return queryset.none()
        return super().filter_queryset(queryset)
