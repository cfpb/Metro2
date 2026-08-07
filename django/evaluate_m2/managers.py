from django.db import models
from django.db.models import Count, IntegerField, OuterRef, Q, Subquery, Value
from django.db.models.functions import Coalesce


class AccountActivityQuerySet(models.QuerySet):
    def no_previous_bankruptcy_indicators(self):
        return self.filter(
            (
                Q(previous_values__cons_info_ind_assoc__exact=[])
                | Q(previous_values__cons_info_ind_assoc__isnull=True)
            )
            & Q(previous_values__cons_info_ind="")
        )

    def with_hit_count(self, event):
        from evaluate_m2.models import EvaluatorResult

        # Subquery for the number of evaluators hit for
        # each account
        subquery = (
            EvaluatorResult.objects.filter(
                result_summary__event=event,
                acct_num=OuterRef("cons_acct_num"),
            )
            .order_by()
            .values("acct_num")
            .annotate(
                n=Count("id"),
            )
            .values("n")[:1]
        )

        return self.annotate(
            total_hits=Coalesce(
                Subquery(subquery, output_field=IntegerField()),
                Value(0),
            ),
        )

    def with_record_count(self, event):
        subquery = (
            self.model._default_manager.filter(
                data_file__event=event,
                cons_acct_num=OuterRef("cons_acct_num"),
            )
            .order_by()
            .values("cons_acct_num")
            .annotate(
                n=Count("id"),
            )
            .values("n")[:1]
        )

        return self.annotate(
            total_records=Coalesce(
                Subquery(subquery, output_field=IntegerField()),
                Value(0),
            )
        )

    def distinct_accounts(self):
        return self.order_by(
            "cons_acct_num",
            "-activity_date",
        ).distinct("cons_acct_num")
