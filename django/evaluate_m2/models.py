
import logging

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import JSONField

from parse_m2.models import AccountActivity


class EvaluatorMetaData(models.Model):
    name = models.CharField(max_length=200, blank=False)
    func: any
    longitudinal_func: any

    def set_evaluator_properties(self, func = None, longitudinal_func = None):
        self.func = func
        self.longitudinal_func = longitudinal_func


    # def all_account_activity(self):
    #     return self.objects.evaluator.source_record__set.all()
    def exec_custom_func(self) -> list[dict]:
        # returns a list of results from running a query
        logger = logging.getLogger('evaluator.exec_custom_func')
        res = list()
        if self.longitudinal_func:
            res = self.longitudinal_func
        else:
            res = list(self.func)

        return res

class EvaluatorResultSummary(models.Model):
    evaluator_name = models.ForeignKey(EvaluatorMetaData, on_delete=models.CASCADE)
    hits = models.IntegerField()

class EvaluatorResult(models.Model):
    result_summary = models.ForeignKey(EvaluatorResultSummary, on_delete=models.CASCADE)
    date = models.DateField()
    field_values = JSONField(encoder=DjangoJSONEncoder)
    source_record = models.ForeignKey(AccountActivity, on_delete=models.CASCADE)
    acct_num = models.CharField(max_length=30)
