from evaluate_m2.models import EvaluatorResult

import django_filters.rest_framework


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
    account_holder__cons_info_ind = AnyCharFilter(
        field_name="source_record__account_holder__cons_info_ind"
    )
    account_holder__cons_info_ind_assoc = AnyCharFilter(
        field_name="source_record__account_holder__cons_info_ind_assoc"
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
            "account_holder__cons_info_ind",
            "l1__change_ind",
            "dofd",
            "date_closed",
            "amt_past_due",
            "current_bal",
            "smpa",
        ]
