from django.db import models
from django.db.models import Count, IntegerField, OuterRef, Q, Subquery, Value
from django.db.models.functions import Coalesce, TruncMonth


class AccountActivityQuerySet(models.QuerySet):
    def no_previous_bankruptcy_indicators(self):
        return self.filter((
                Q(previous_values__cons_info_ind_assoc__exact=[]) |
                Q(previous_values__cons_info_ind_assoc__isnull=True)
            ) & Q(previous_values__cons_info_ind='')
        )

    def with_inconsistency_counts(self, event):
        from evaluate_m2.models import EvaluatorResult

        # Subquery for the number of inconsistencies (evaluators hit) for
        # each account. This is just a count of hits.
        subquery = EvaluatorResult.objects.filter(
            result_summary__event=event,
            acct_num=OuterRef("cons_acct_num"),
        ).order_by().values("acct_num").annotate(
            n=Count("result_summary__evaluator_id", distinct=True),
        ).values("n")[:1]

        return self.annotate(
            total_inconsistencies=Coalesce(
                Subquery(subquery, output_field=IntegerField()),
                Value(0),
            ),
        )

    def with_months_of_data(self, event):
        # Subquery for the number of months of data. This counts **distinct**
        # months, not the number of months in the total range.
        # I.e. if there's data for Feb, March, and May, but not April, that's
        # three months of data, not four.
        subquery = self.model._default_manager.filter(
            data_file__event=event,
            cons_acct_num=OuterRef("cons_acct_num"),
        ).order_by().annotate(
            month=TruncMonth("activity_date"),
        ).values("cons_acct_num").annotate(
            n=Count("month", distinct=True),
        ).values("n")[:1]

        return self.annotate(
            months_of_data=Coalesce(
                Subquery(subquery, output_field=IntegerField()),
                Value(0),
            )
        )

    def distinct_accounts(self):
        return self.order_by(
            "cons_acct_num",
            "-activity_date",
        ).distinct("cons_acct_num")
