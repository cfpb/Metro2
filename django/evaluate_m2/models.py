import logging
from datetime import date

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection, models
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
        extensions= {
            "Bold": True,
            "Italic": True,
            "BulletList": True,
            "OrderedList": True,
            "ListItem": True,
            "Link": True,
            "Blockquote": True,
            "Heading": {
                "levels": [4]
            },
        },
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
    hits = models.IntegerField(default=0)
    accounts_affected = models.IntegerField(default=0)
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

    @classmethod
    def initialize(cls, event: Metro2Event, eval_id: str, eval_version: str):
        """
        Before the evaluator runs, create an EvaluatorResultsSummary object
        to associate hits with.
        """
        eval, _ = EvaluatorMetadata.objects.get_or_create(id=eval_id)

        return cls.objects.create(
            event = event,
            evaluator = eval,
            evaluator_version = eval_version,
        )

    def summarize_eval_results(self):
        """
        After the evaluator runs, if there were any hits, update the
        summary of info about the hits.
        """
        data = self.evaluatorresult_set
        if data.exists():
            hits = data.count()
            accounts_affected = data.values('acct_num').distinct().count()
            earliest_date = data.order_by('date').first().date
            latest_date = data.order_by('-date').first().date

            self.hits = hits
            self.accounts_affected = accounts_affected
            self.inconsistency_start = earliest_date
            self.inconsistency_end = latest_date
            self.save()

            self._generate_sample_of_results().update(sample=True)

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
    # Indicate whether this result is included in the set of random sample results
    sample = models.BooleanField(default=False)

    def create_csv_row_data(self, fields_list: list[str]):
        field_values = AccountActivity.objects \
                    .values_list(*fields_list) \
                    .get(id=self.source_record.id)
        response = [
            self.result_summary.event.name,
            ] + list(field_values)
        return response


class EvaluatorResultMaterializedView(models.Model):
    class Meta:
        managed = False
        db_table = 'mv_all_evaluator_results'
        verbose_name_plural = "Evaluator Result Materialized View"

    table_name = 'mv_all_evaluator_results'

    @classmethod
    def create_or_refresh_materialized_view(cls):
        lg = logging.getLogger('eval_mv.create_or_refresh_materialized_view')
        if cls.materialized_view_exists():
            lg.info("Refreshing the evaluator results materialized view...")
            with connection.cursor() as c:
                c.execute(cls.refresh_view_command)
        else:
            lg.info("Creating the evaluator results materialized view...")
            with connection.cursor() as c:
                c.execute(cls.create_view_command)
                c.execute(cls.create_index_command)
        lg.info("... Done.")

    @classmethod
    def materialized_view_exists(cls) -> bool:
        with connection.cursor() as c:
            command = "select * from pg_matviews where matviewname = %s"
            result = c.execute(command, [cls.table_name])
            return result.rowcount > 0

    # The fields on this model correspond to the
    # column names in the materialized view
    id = models.IntegerField(db_column="id", primary_key=True)
    event_id = models.IntegerField(db_column="event_id")
    evaluator_id = models.CharField(db_column="evaluator_id")
    source_record_id = models.IntegerField(db_column="source_record_id")
    sample = models.BooleanField(db_column="sample")
    # account activity fields
    activity_date = models.DateField(db_column="activity_date")
    cons_acct_num = models.CharField(db_column="cons_acct_num")
    port_type = models.CharField(db_column="port_type")
    acct_type = models.CharField(db_column="acct_type")
    date_open = models.DateField(db_column="date_open")
    credit_limit = models.IntegerField(db_column="credit_limit")
    hcola = models.IntegerField(db_column="hcola")
    id_num = models.CharField(db_column="id_num")
    terms_dur = models.CharField(db_column="terms_dur")
    terms_freq = models.CharField(db_column="terms_freq")
    smpa = models.IntegerField(db_column="smpa")
    actual_pmt_amt = models.IntegerField(db_column="actual_pmt_amt")
    acct_stat = models.CharField(db_column="acct_stat")
    pmt_rating = models.CharField(db_column="pmt_rating")
    php = models.CharField(db_column="php")
    php1 = models.CharField(db_column="php1")
    spc_com_cd = models.CharField(db_column="spc_com_cd")
    compl_cond_cd = models.CharField(db_column="compl_cond_cd")
    current_bal = models.IntegerField(db_column="current_bal")
    amt_past_due = models.IntegerField(db_column="amt_past_due")
    orig_chg_off_amt = models.IntegerField(db_column="orig_chg_off_amt")
    doai = models.DateField(db_column="doai")
    dofd = models.DateField(db_column="dofd")
    date_closed = models.DateField(db_column="date_closed")
    dolp = models.DateField(db_column="dolp")
    int_type_ind = models.CharField(db_column="int_type_ind")
    surname = models.CharField(db_column="surname")
    first_name = models.CharField(db_column="first_name")
    middle_name = models.CharField(db_column="middle_name")
    gen_code = models.CharField(db_column="gen_code")
    ssn = models.CharField(db_column="ssn")
    dob = models.CharField(db_column="dob")
    phone_num = models.CharField(db_column="phone_num")
    ecoa = models.CharField(db_column="ecoa")
    ecoa_assoc = models.JSONField(
        encoder=DjangoJSONEncoder, db_column="ecoa_assoc")
    cons_info_ind = models.CharField(db_column="cons_info_ind")
    cons_info_ind_assoc = models.JSONField(
        encoder=DjangoJSONEncoder, db_column="cons_info_ind_assoc")
    addr_line_1 = models.CharField(db_column="addr_line_1")
    addr_line_2 = models.CharField(db_column="addr_line_2")
    city = models.CharField(db_column="city")
    state = models.CharField(db_column="state")
    zip = models.CharField(db_column="zip")
    addr_ind = models.CharField(db_column="addr_ind")
    res_cd = models.CharField(db_column="res_cd")
    # extra segment columns
    purch_sold_ind = models.CharField(db_column="purch_sold_ind")
    purch_sold_name = models.CharField(db_column="purch_sold_name")
    spc_pmt_ind = models.CharField(db_column="spc_pmt_ind")
    deferred_pmt_st_dt = models.DateField(db_column="deferred_pmt_st_dt")
    balloon_pmt_due_dt = models.DateField(db_column="balloon_pmt_due_dt")
    balloon_pmt_amt = models.IntegerField(db_column="balloon_pmt_amt")
    change_ind = models.CharField(db_column="change_ind")
    new_acc_num = models.CharField(db_column="new_acc_num")
    new_id_num = models.CharField(db_column="new_id_num")
    # prior record values
    prior_activity_date = models.DateField(db_column="prior_activity_date")
    prior_port_type = models.CharField(db_column="prior_port_type")
    prior_acct_type = models.CharField(db_column="prior_acct_type")
    prior_date_open = models.DateField(db_column="prior_date_open")
    prior_id_num = models.CharField(db_column="prior_id_num")
    prior_acct_stat = models.CharField(db_column="prior_acct_stat")
    prior_pmt_rating = models.CharField(db_column="prior_pmt_rating")
    prior_current_bal = models.IntegerField(db_column="prior_current_bal")
    prior_orig_chg_off_amt = models.IntegerField(db_column="prior_orig_chg_off_amt")
    prior_dofd = models.DateField(db_column="prior_dofd")
    prior_date_closed = models.DateField(db_column="prior_date_closed")
    prior_surname = models.CharField(db_column="prior_surname")
    prior_first_name = models.CharField(db_column="prior_first_name")
    prior_ecoa = models.CharField(db_column="prior_ecoa")
    prior_ecoa_assoc = models.JSONField(
        encoder=DjangoJSONEncoder, db_column="prior_ecoa_assoc")
    prior_cons_info_ind = models.CharField(db_column="prior_cons_info_ind")
    prior_cons_info_ind_assoc = models.JSONField(
        encoder=DjangoJSONEncoder, db_column="prior_cons_info_ind_assoc")
    prior_change_ind = models.CharField(db_column="prior_change_ind")
    prior_new_acc_num = models.CharField(db_column="prior_new_acc_num")
    prior_new_id_num = models.CharField(db_column="prior_new_id_num")

    refresh_view_command = """
        REFRESH MATERIALIZED VIEW mv_all_evaluator_results;
    """
    create_index_command = """
        CREATE INDEX idx_event_id_evaluator_id
        ON mv_all_evaluator_results (event_id, evaluator_id);
    """

    # The column names in the materialized view correspond to the
    # fields on the model
    create_view_command = """
        CREATE MATERIALIZED VIEW mv_all_evaluator_results AS (
        SELECT
            r.id,
            a.event_id,
            s.evaluator_id,
            a.id as source_record_id,
            r.sample,

            a.activity_date,
            a.cons_acct_num,
            a.port_type,
            a.acct_type,
            a.date_open,
            a.credit_limit,
            a.hcola,
            a.id_num,
            a.terms_dur,
            a.terms_freq,
            a.smpa,
            a.actual_pmt_amt,
            a.acct_stat,
            a.pmt_rating,
            a.php,
            a.php1,
            a.spc_com_cd,
            a.compl_cond_cd,
            a.current_bal,
            a.amt_past_due,
            a.orig_chg_off_amt,
            a.doai,
            a.dofd,
            a.date_closed,
            a.dolp,
            a.int_type_ind,
            a.surname,
            a.first_name,
            a.middle_name,
            a.gen_code,
            a.ssn,
            a.dob,
            a.phone_num,
            a.ecoa,
            a.ecoa_assoc,
            a.cons_info_ind,
            a.cons_info_ind_assoc,
            a.addr_line_1,
            a.addr_line_2,
            a.city,
            a.state,
            a.zip,
            a.addr_ind,
            a.res_cd,

            k2.purch_sold_ind,
            k2.purch_sold_name,
            k4.spc_pmt_ind,
            k4.deferred_pmt_st_dt,
            k4.balloon_pmt_due_dt,
            k4.balloon_pmt_amt,
            l1.change_ind,
            l1.new_acc_num,
            l1.new_id_num,

            prev.activity_date as prior_activity_date,
            prev.port_type as prior_port_type,
            prev.acct_type as prior_acct_type,
            prev.date_open as prior_date_open,
            prev.id_num as prior_id_num,
            prev.acct_stat as prior_acct_stat,
            prev.pmt_rating as prior_pmt_rating,
            prev.current_bal as prior_current_bal,
            prev.orig_chg_off_amt as prior_orig_chg_off_amt,
            prev.dofd as prior_dofd,
            prev.date_closed as prior_date_closed,
            prev.surname as prior_surname,
            prev.first_name as prior_first_name,
            prev.ecoa as prior_ecoa,
            prev.ecoa_assoc as prior_ecoa_assoc,
            prev.cons_info_ind as prior_cons_info_ind,
            prev.cons_info_ind_assoc as prior_cons_info_ind_assoc,
            prev_l1.change_ind as prior_change_ind,
            prev_l1.new_acc_num as prior_new_acc_num,
            prev_l1.new_id_num as prior_new_id_num

        FROM
            parse_m2_accountactivity as a
            INNER JOIN evaluate_m2_evaluatorresult as r
            on r.source_record_id = a.id
            INNER JOIN evaluate_m2_evaluatorresultsummary as s
            on r.result_summary_id = s.id
            LEFT JOIN parse_m2_k2 as k2
            on a.id = k2.account_activity_id
            LEFT JOIN parse_m2_k4 as k4
            on a.id = k4.account_activity_id
            LEFT JOIN parse_m2_l1 as l1
            on a.id = l1.account_activity_id
            LEFT JOIN parse_m2_accountactivity as prev
            on a.previous_values_id = prev.id
            LEFT JOIN parse_m2_l1 as prev_l1
            on prev.id = prev_l1.account_activity_id
        );
    """
