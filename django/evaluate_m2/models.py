from django.db import models
from django.db.models import JSONField

from parse_m2.models import AccountActivity

class EvaluatorMetaData(models.Model):
    evaluator_name = models.CharField(max_length=200, unique=True)
    hits = models.IntegerField()

class EvaluatorResult(models.Model):
    evaluator = models.ForeignKey(EvaluatorMetaData, on_delete=models.CASCADE)
    date = models.DateField()
    field_values = JSONField()
    source_record = models.ForeignKey(AccountActivity, on_delete=models.CASCADE)
    acct_num = models.CharField(max_length=30)
