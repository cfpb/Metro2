from django.db import models
from django.db.models import JSONField

class Evaluator():
    date_format = "MMDDYYYY"
    strptime_format = "%m%d%Y"
    name = models.CharField(max_length=200)


    def __init__(self, name, func=None, longitudinal_func=None):
        self.name = name
    # Do we need fields?
    #   self.fields = fields
        self.func = func
        self.longitudinal_func = longitudinal_func
    class Meta:
        # abstract = True means Evaulator is not a table in the
        # database, instead we can use these fields as results
        # of another model, e.g. Results or Metadata below.
        abstract = True

    def exec_custom_func(self):
        # returns a list of results from running a query
        res = list()
        if self.longitudinal_func:
            res = self.longitudinal_func
        else:
            res = self.func

        # returns a list of dicts from the results
        res_set = [dict(zip(row._mapping.keys(), row)) for row in res]

        return res_set

class Metadata(models.Model):
    evaluator_name = models.CharField(max_length=200, unique=True)
    hits = models.IntegerField()

class Results(models.Model):
    evaluator_name = models.CharField(max_length=200)
    date = models.DateField()
    field_values = JSONField()
    record_id = models.CharField(max_length=24, unique=True)
    acct_num = models.CharField(max_length=30)
