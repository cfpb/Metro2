from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import JSONField

from parse_m2.models import AccountActivity, Metro2Event


class EvaluatorMetaData(models.Model):
    # id is auto-numbered
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True)  # plain language description
    long_description = models.TextField(blank=True)
    fields_used = JSONField(encoder=DjangoJSONEncoder, null=True)
    fields_display = JSONField(encoder=DjangoJSONEncoder, null=True)
    ipl = models.CharField(max_length=200, blank=True)
    # category -- tbd how to model this
    # filters -- tbd how to model this
    crrg_topics = models.CharField(max_length=200, blank=True)
    crrg_page = models.CharField(max_length=200, blank=True)
    pdf_page = models.CharField(max_length=200, blank=True)
    use_notes = models.TextField(blank=True)
    alternative_explanation = models.TextField(blank=True)
    risk_level = models.CharField(max_length=200, blank=True)

    func: any

    def set_func(self, func = None):
        self.func = func

class EvaluatorResultSummary(models.Model):
    event = models.ForeignKey(Metro2Event, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(EvaluatorMetaData, on_delete=models.CASCADE)
    hits = models.IntegerField()

class EvaluatorResult(models.Model):
    result_summary = models.ForeignKey(EvaluatorResultSummary, on_delete=models.CASCADE)
    date = models.DateField()
    field_values = JSONField(encoder=DjangoJSONEncoder)
    source_record = models.ForeignKey(AccountActivity, on_delete=models.CASCADE)
    acct_num = models.CharField(max_length=30)
