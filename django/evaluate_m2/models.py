from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import JSONField

from parse_m2.models import AccountActivity, Metro2Event


class EvaluatorMetadata(models.Model):
    class Meta:
        verbose_name_plural = "Evaluator Metadata"

    # Use the identifier as the primary key instead of an auto_numbered ID.
    # id values may not be blank and must be unique
    id = models.CharField(max_length=200, primary_key=True)
    category = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)  # short plain language description
    long_description = models.TextField(blank=True)
    fields_used = JSONField(encoder=DjangoJSONEncoder, null=True)
    fields_display = JSONField(encoder=DjangoJSONEncoder, null=True)
    crrg_reference = models.TextField(blank=True)
    potential_harm = models.TextField(blank=True)
    rationale = models.TextField(blank=True)
    alternate_explanation = models.TextField(blank=True)

    func: any

    # Fields that should always be present in the evaluator results view
    identifying_fields = [
        'id',
        'activity_date',
        'cons_acct_num',
        'doai',
    ]

    filterable_fields = [
        'acct_stat',
        'compl_cond_cd',
        'php',
        'pmt_rating',
        'spc_com_cd',
        'terms_freq',
        'account_holder__cons_info_ind',
        'account_holder__cons_info_ind_assoc',
        'l1__change_ind',
        'dofd',
        'date_closed',
        'amt_past_due',
        'current_bal',
    ]

    def __str__(self) -> str:
        return self.id

    def result_summary_fields(self) -> list[str]:
        """
        Return the list of AccountActivity fields (and fields on related
        records) that should be shown in the evaluator result view API
        endpoint.

        Fields are listed in the following order (but with duplicates removed):
        - identifying fields (consistent for every evaluator)
        - fields_used and fields_display (evaluator-dependent)
        - filterable fields (consistent for every evaluator)
        """
        fieldset = self.identifying_fields + \
            self.fields_used + \
            self.fields_display + \
            self.filterable_fields

        dups_removed = [*dict.fromkeys(fieldset)]
        return dups_removed



class EvaluatorResultSummary(models.Model):
    class Meta:
        verbose_name_plural = "Evaluator Result Summaries"
    event = models.ForeignKey(Metro2Event, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(EvaluatorMetadata, on_delete=models.CASCADE)
    hits = models.IntegerField()
    accounts_affected = models.IntegerField(null=True)
    inconsistency_start = models.DateField(null=True)
    inconsistency_end = models.DateField(null=True)
    evaluator_version = models.CharField(max_length=200, blank=True)
    sample_ids = models.JSONField(encoder=DjangoJSONEncoder, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Event: {self.event} - {self.evaluator}"

    def create_csv_header(self):
        csv_header = list(self.evaluator.result_summary_fields())
        csv_header.insert(0, 'event_name')
        return csv_header

    def sample_of_results(self, sample_size: int = settings.M2_RESULT_SAMPLE_SIZE) -> list[int]:
        """
        Return a list of IDs of AccountActivity records that are hits
        for this evaluator.
        If this eval has more than sample_size hits, the list is a
        RANDOM sample of this eval's hits. Otherwise, return a list
        of all hits.
        """
        data = self.evaluatorresult_set

        if not data.exists():
            return []
        if self.hits <= sample_size:
            small_aa_set = data.values_list('source_record_id')
            return [val[0] for val in small_aa_set]
        else:
            # Since all hits for an eval are added to the EvaluatorResults table
            # in one transaction and the ID column is auto-generated, we can
            # assume the ID values will be sequential. In that case, we can select
            # the sample as numbers from the numeric range of IDs, which is
            # computationally easier than selecting records from the table.
            import random

            first_id = data.order_by("id").first().id
            last_id = data.order_by("-id").first().id
            random_ids = random.sample(range(first_id, last_id + 1), sample_size)

            random_aa_set = data.filter(id__in=random_ids) \
                .values_list('source_record_id')

            return [val[0] for val in random_aa_set]


class EvaluatorResult(models.Model):
    class Meta:
        verbose_name_plural = "Evaluator Results"
        indexes = [ models.Index(fields=['acct_num',])]
    result_summary = models.ForeignKey(EvaluatorResultSummary, on_delete=models.CASCADE)
    date = models.DateField()
    source_record = models.ForeignKey(AccountActivity, on_delete=models.CASCADE)
    acct_num = models.CharField(max_length=30)

    def create_csv_row_data(self, fields_list: list[str]):
        field_values = AccountActivity.objects \
                    .values_list(*fields_list) \
                    .get(id=self.source_record.id)
        response = [
            self.result_summary.event.name,
            ] + list(field_values)
        return response
