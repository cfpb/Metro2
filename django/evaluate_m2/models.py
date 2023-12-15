import logging

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import JSONField

from parse_m2.models import AccountActivity, Metro2Event


class EvaluatorMetaData(models.Model):
    name = models.CharField(max_length=200, blank=False)
    func: any
    event: str

    def set_func(self, func = None):
        self.func = func

    def set_metro2_event(self, event = None):
        self.event = event


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
