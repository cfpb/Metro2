from datetime import date

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import DEFERRED, JSONField

from django_prose_editor.fields import ProseEditorField

from parse_m2.models import AccountActivity, Metro2Event


class EvaluatorMetadata(models.Model):
    class Meta:
        verbose_name_plural = "Evaluator Metadata"

    _richtext_basic_options = {
        "Bold": True,
        "Italic": True,
        "BulletList": True,
        "OrderedList": True,
        "ListItem": True,
        "Link": True,
        "Blockquote": True
    }

    _last_modified_never = date(1900,1,1)

    # Use the identifier as the primary key instead of an auto_numbered ID.
    # id values may not be blank and must be unique
    id = models.CharField(max_length=200, primary_key=True)
    category = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)  # short plain language description
    long_description = ProseEditorField(
        extensions={
            "Bold": True,
            "Italic": True,
            "BulletList": True,
            "OrderedList": True,
            "ListItem": True,
            "Link": True,
            "Heading": {
                "levels": [4]
            },
        },
        sanitize=True,  # Built-in server side sanitization
        blank=True,
    )
    fields_used = JSONField(encoder=DjangoJSONEncoder, null=True)
    fields_display = JSONField(encoder=DjangoJSONEncoder, null=True)
    crrg_reference = ProseEditorField(
        extensions=_richtext_basic_options,
        sanitize=True,
        blank=True,
    )
    potential_harm = ProseEditorField(
        extensions=_richtext_basic_options,
        sanitize=True,
        blank=True,
    )
    rationale = ProseEditorField(
        extensions=_richtext_basic_options,
        sanitize=True,
        blank=True,
    )
    alternate_explanation = ProseEditorField(
        extensions=_richtext_basic_options,
        sanitize=True,
        blank=True,
    )
    interpret_fields_last_modified = models.DateField(default=_last_modified_never)
    additional_notes = ProseEditorField(
        extensions=_richtext_basic_options,
        sanitize=True,
        blank=True,
    )
    additional_notes_last_modified = models.DateField(default=_last_modified_never)

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
        'php1',
        'pmt_rating',
        'spc_com_cd',
        'terms_freq',
        'cons_info_ind',
        'cons_info_ind_assoc',
        'l1__change_ind',
        'dofd',
        'date_closed',
        'amt_past_due',
        'current_bal',
    ]

    _from_bulk_import: bool = False
    _loaded_values: dict = {}

    def __init__(self, *args, **kwargs):
        # When records are initialized from the EvaluatorMetadataSerializer
        # (i.e. from csv import), _from_bulk_import is True
        if 'from_bulk_import' in kwargs:
            self._from_bulk_import = kwargs.pop('from_bulk_import')
        super().__init__(*args, **kwargs)

    @classmethod
    def from_db(cls, db, field_names, values):
        # When loading a record from the db, cache the loaded values
        # so we can compare them to the new values upon save. Source:
        # https://docs.djangoproject.com/en/5.2/ref/models/instances/
        instance = super().from_db(db, field_names, values)
        instance._loaded_values = dict(
            zip(
                field_names,
                (value for value in values if value is not DEFERRED),
                strict=False,
            )
        )
        return instance

    _interpret_fields = ['crrg_reference', 'potential_harm',
                         'rationale', 'alternate_explanation']
    _additional_fields = ['additional_notes']
    def _values_modified(self, field_names):
        for f in field_names:
            if self._loaded_values[f] != self.__getattribute__(f):
                return True
        return False

    def save(self, *args, **kwargs):
        # If modifying an existing record manually (not with a bulk import),
        # update the _last_modified fields if necessary
        if self._loaded_values and not self._from_bulk_import:
            if self._values_modified(self._interpret_fields):
                self.interpret_fields_last_modified = date.today()
            if self._values_modified(self._additional_fields):
                self.additional_notes_last_modified = date.today()
        return super().save(*args, **kwargs)

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

    def sample_of_results(
        self,
        sample_size: int = settings.M2_RESULT_SAMPLE_SIZE
    ) -> list[int]:
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
