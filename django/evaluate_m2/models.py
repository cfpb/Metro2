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
    description = models.TextField(blank=True)  # short plain language description
    long_description = models.TextField(blank=True)
    fields_used = JSONField(encoder=DjangoJSONEncoder, null=True)
    fields_display = JSONField(encoder=DjangoJSONEncoder, null=True)
    crrg_reference = models.TextField(blank=True)
    potential_harm = models.TextField(blank=True)
    rationale = models.TextField(blank=True)
    alternate_explanation = models.TextField(blank=True)

    func: any

    def __str__(self) -> str:
        return self.id

class EvaluatorResultSummary(models.Model):
    class Meta:
        verbose_name_plural = "Evaluator Result Summaries"
    event = models.ForeignKey(Metro2Event, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(EvaluatorMetadata, on_delete=models.CASCADE)
    hits = models.IntegerField()
    accounts_affected = models.IntegerField(null=True)
    inconsistency_start = models.DateField(null=True)
    inconsistency_end = models.DateField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Event: {self.event} - {self.evaluator}"


class EvaluatorResult(models.Model):
    class Meta:
        verbose_name_plural = "Evaluator Results"
        indexes = [ models.Index(fields=['acct_num',])]
    result_summary = models.ForeignKey(EvaluatorResultSummary, on_delete=models.CASCADE)
    date = models.DateField()
    field_values = JSONField(encoder=DjangoJSONEncoder)
    source_record = models.ForeignKey(AccountActivity, on_delete=models.CASCADE)
    acct_num = models.CharField(max_length=30)

    def create_csv_header(self):
        csv_header = list(self.field_values.keys())
        csv_header.insert(0, 'event_name')
        return csv_header

    def create_csv_row_data(self):
        response = [
            self.result_summary.event.name,
            ] + list(self.field_values.values())
        return response
