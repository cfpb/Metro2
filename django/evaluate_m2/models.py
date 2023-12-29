from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import JSONField

from parse_m2.models import AccountActivity, Metro2Event


class EvaluatorMetadata(models.Model):
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

    def __str__(self) -> str:
        return self.name

    @classmethod
    def create_from_dict(cls, json: dict):
        # using .create means we don't have to call .save manually
        return cls.objects.create(
            name=json["name"],
            description=json["description"],
            long_description=json["long_description"],
            fields_used=json["fields_used"].split(";"),
            fields_display=json["fields_display"].split(";"),
            ipl=json["ipl"],
            crrg_topics=json["crrg_topics"],
            crrg_page=json["crrg_page"],
            pdf_page=json["pdf_page"],
            use_notes=json["use_notes"],
            alternative_explanation=json["alternative_explanation"],
            risk_level=json["risk_level"],
        )

    csv_header = [
            "name",
            "description",
            "long_description",
            "fields_used",
            "fields_display",
            "ipl",
            "crrg_topics",
            "crrg_page",
            "pdf_page",
            "use_notes",
            "alternative_explanation",
            "risk_level",
        ]

    def serialize(self):
        if self.fields_used:
            fields_used = ";".join(self.fields_used)
        else:
            fields_used = ""

        if self.fields_display:
            fields_display = ";".join(self.fields_display)
        else:
            fields_display = ""

        return [
            self.name,
            self.description,
            self.long_description,
            fields_used,
            fields_display,
            self.ipl,
            self.crrg_topics,
            self.crrg_page,
            self.pdf_page,
            self.use_notes,
            self.alternative_explanation,
            self.risk_level,
        ]


class EvaluatorResultSummary(models.Model):
    event = models.ForeignKey(Metro2Event, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(EvaluatorMetadata, on_delete=models.CASCADE)
    hits = models.IntegerField()


class EvaluatorResult(models.Model):
    result_summary = models.ForeignKey(EvaluatorResultSummary, on_delete=models.CASCADE)
    date = models.DateField()
    field_values = JSONField(encoder=DjangoJSONEncoder)
    source_record = models.ForeignKey(AccountActivity, on_delete=models.CASCADE)
    acct_num = models.CharField(max_length=30)
