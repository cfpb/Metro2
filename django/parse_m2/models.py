from django.contrib.auth.models import Group
from django.db import models
from django.core.management import call_command

from parse_m2.parse_utils import get_field_value
from parse_m2 import fields
from evaluate_m2.managers import AccountActivityQuerySet


class Metro2Event(models.Model):
    class Meta:
        verbose_name_plural = "Metro2 Events"
    name = models.CharField(max_length=300)
    user_group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.name

    def get_all_account_activity(self):
        return AccountActivity.objects.filter(
            account_holder__data_file__event=self)

    def evaluate(self):
        call_command('run_evaluators', event_id=self.id)

    def check_access_for_user(self, user) -> bool:
        """
        Utility method for checking authorization. Returns True if
        the user is assigned to the correct user group to have
        access to this event.
        """
        return self.user_group in user.groups.all()

class M2DataFile(models.Model):
    class Meta:
        verbose_name_plural = "Metro2 Data Files"
    event = models.ForeignKey(Metro2Event, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    parsing_status = models.CharField(max_length=200, default="Not started")
    error_message = models.CharField(max_length=2000, blank=True)

    def __str__(self) -> str:
        return self.file_name

class UnparseableData(models.Model):
    class Meta:
        verbose_name_plural = "Unparseable Data"
    data_file = models.ForeignKey(M2DataFile, on_delete=models.CASCADE)
    unparseable_line = models.CharField(max_length=2000)
    error_description = models.CharField(max_length=2000)

class Person(models.Model):
    surname = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    gen_code = models.CharField(max_length=200)
    ssn = models.CharField(max_length=200)
    dob = models.CharField(max_length=200)
    phone_num = models.CharField(max_length=200)
    ecoa = models.CharField(max_length=200)
    cons_info_ind = models.CharField(max_length=200)

    class Meta:
        # abstract = True means Person is not a table in the
        # database, instead we can use these fields as part
        # of another model, e.g. AccountHolder below.
        abstract = True

class Address(models.Model):
    country_cd = models.CharField(max_length=200)
    addr_line_1 = models.CharField(max_length=200)
    addr_line_2 = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.CharField(max_length=200)
    addr_ind = models.CharField(max_length=200)
    res_cd = models.CharField(max_length=200)

    class Meta:
        # abstract = True means Address is not a table in the
        # database, instead we can use these fields as part
        # of another model, e.g. AccountHolder below.
        abstract = True

class AccountHolder(Person, Address):
    class Meta:
        verbose_name_plural = "Account Holders"
    data_file = models.ForeignKey(M2DataFile, on_delete=models.CASCADE)
    activity_date = models.DateField()
    cons_acct_num = models.CharField(max_length=200)
    # Since this model inherits from the Person base class,
    # it automatically includes name, ssn, dob, ecoa, etc.
    # Since this model inherits from the Address base class,
    # it automatically has country_cd, addr, city, state, etc.

    def __str__(self) -> str:
        return f"AccountHolder {self.id} (File ID: {self.data_file.id})"

    @classmethod
    def parse_from_segment(cls, base_seg: str, m2_data_file: M2DataFile, activity_date):
        return cls(
            data_file = m2_data_file,
            activity_date = activity_date,
            cons_acct_num = get_field_value(fields.base_fields, "cons_acct_num", base_seg),

            # Person-related values
            surname = get_field_value(fields.base_fields, "surname", base_seg),
            first_name = get_field_value(fields.base_fields, "first_name", base_seg),
            middle_name = get_field_value(fields.base_fields, "middle_name", base_seg),
            gen_code = get_field_value(fields.base_fields, "gen_code", base_seg),
            ssn = get_field_value(fields.base_fields, "ssn", base_seg),
            dob = get_field_value(fields.base_fields, "dob", base_seg),
            phone_num = get_field_value(fields.base_fields, "phone_num", base_seg),
            ecoa = get_field_value(fields.base_fields, "ecoa", base_seg),
            cons_info_ind = get_field_value(fields.base_fields, "cons_info_ind", base_seg),

            # Address-related values
            country_cd = get_field_value(fields.base_fields, "country_cd", base_seg),
            addr_line_1 = get_field_value(fields.base_fields, "addr_line_1", base_seg),
            addr_line_2 = get_field_value(fields.base_fields, "addr_line_2", base_seg),
            city = get_field_value(fields.base_fields, "city", base_seg),
            state = get_field_value(fields.base_fields, "state", base_seg),
            zip = get_field_value(fields.base_fields, "zip", base_seg),
            addr_ind = get_field_value(fields.base_fields, "addr_ind", base_seg),
            res_cd = get_field_value(fields.base_fields, "res_cd", base_seg),
        )

class AccountActivity(models.Model):
    objects = AccountActivityQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "Account Activities"
        indexes = [ models.Index(fields=['cons_acct_num',])]
    # Note: Numeric fields are using models.IntegerField, which
    # has a limit of +/- 2.4 billion. Since the Metro2 format limits each of
    # these numeric fields to 9 characters, that size should be sufficient.
    # Also, it limits each numeric field to whole numbers only,
    # so no precision will be lost.

    # Note: Date fields that are not required in the CRRG use the option
    # null=True. For all required fields, this option defaults to null=False,
    # so they must have a value.

    def __str__(self) -> str:
        return f"AccountActivity {self.id} (File ID: {self.account_holder.data_file.id})"

    account_holder = models.OneToOneField(AccountHolder, on_delete=models.CASCADE)
    activity_date = models.DateField()
    cons_acct_num = models.CharField(max_length=200)
    port_type = models.CharField(max_length=200)
    acct_type = models.CharField(max_length=200)
    date_open = models.DateField()
    credit_limit = models.IntegerField()
    hcola = models.IntegerField()
    terms_dur = models.CharField(max_length=200)
    terms_freq = models.CharField(max_length=200)
    smpa = models.IntegerField()
    actual_pmt_amt = models.IntegerField()
    acct_stat = models.CharField(max_length=200)
    pmt_rating = models.CharField(max_length=200)
    php = models.CharField(max_length=200)
    spc_com_cd = models.CharField(max_length=200)
    compl_cond_cd = models.CharField(max_length=200)
    current_bal = models.IntegerField()
    amt_past_due = models.IntegerField()
    orig_chg_off_amt = models.IntegerField()
    doai = models.DateField(null=True)
    dofd = models.DateField(null=True)
    date_closed = models.DateField(null=True)
    dolp = models.DateField(null=True)
    int_type_ind = models.CharField(max_length=200)

    @classmethod
    def parse_from_segment(cls, base_seg: str, acct_holder: AccountHolder, activity_date):
        return cls(
            account_holder = acct_holder,
            activity_date = activity_date,
            cons_acct_num = get_field_value(fields.base_fields, "cons_acct_num", base_seg),

            port_type = get_field_value(fields.base_fields, "port_type", base_seg),
            acct_type = get_field_value(fields.base_fields, "acct_type", base_seg),
            date_open = get_field_value(fields.base_fields, "date_open", base_seg),
            credit_limit = get_field_value(fields.base_fields, "credit_limit", base_seg),
            hcola = get_field_value(fields.base_fields, "hcola", base_seg),
            terms_dur = get_field_value(fields.base_fields, "terms_dur", base_seg),
            terms_freq = get_field_value(fields.base_fields, "terms_freq", base_seg),
            smpa = get_field_value(fields.base_fields, "smpa", base_seg),
            actual_pmt_amt  = get_field_value(fields.base_fields, "actual_pmt_amt", base_seg),
            acct_stat = get_field_value(fields.base_fields, "acct_stat", base_seg),
            pmt_rating = get_field_value(fields.base_fields, "pmt_rating", base_seg),
            php  = get_field_value(fields.base_fields, "php", base_seg),
            spc_com_cd = get_field_value(fields.base_fields, "spc_com_cd", base_seg),
            compl_cond_cd = get_field_value(fields.base_fields, "compl_cond_cd", base_seg),
            current_bal = get_field_value(fields.base_fields, "current_bal", base_seg),
            amt_past_due = get_field_value(fields.base_fields, "amt_past_due", base_seg),
            orig_chg_off_amt = get_field_value(fields.base_fields, "orig_chg_off_amt", base_seg),
            doai = get_field_value(fields.base_fields, "doai", base_seg),
            dofd = get_field_value(fields.base_fields, "dofd", base_seg),
            date_closed = get_field_value(fields.base_fields, "date_closed", base_seg),
            dolp = get_field_value(fields.base_fields, "dolp", base_seg),
            int_type_ind = get_field_value(fields.base_fields, "int_type_ind", base_seg),
        )

class J1(Person):
    class Meta:
        verbose_name_plural = "J1 Segment Associated Consumer - Same Address"
    account_activity = models.ForeignKey(AccountActivity, on_delete=models.CASCADE)
    # Contains all fields from the Person abstract class

    def __str__(self) -> str:
        return f"J1 {self.id} (File ID: {self.account_activity.account_holder.data_file.id})"

    @classmethod
    def parse_from_segment(cls, segment: str, account_activity: AccountActivity):
        return cls(
            account_activity = account_activity,
            # Person-related values
            surname = get_field_value(fields.j1_fields, "surname_j1", segment),
            first_name = get_field_value(fields.j1_fields, "first_name_j1", segment),
            middle_name = get_field_value(fields.j1_fields, "middle_name_j1", segment),
            gen_code = get_field_value(fields.j1_fields, "gen_code_j1", segment),
            ssn = get_field_value(fields.j1_fields, "ssn_j1", segment),
            dob = get_field_value(fields.j1_fields, "dob_j1", segment),
            phone_num = get_field_value(fields.j1_fields, "phone_num_j1", segment),
            ecoa = get_field_value(fields.j1_fields, "ecoa_j1", segment),
            cons_info_ind = get_field_value(fields.j1_fields, "cons_info_ind_j1", segment),
        )

class J2(Person, Address):
    class Meta:
        verbose_name_plural = "J2 Segment Associated Consumer - Different Address"
    account_activity = models.ForeignKey(AccountActivity, on_delete=models.CASCADE)
    # Contains all fields from the Person and Address abstract classes

    def __str__(self) -> str:
        return f"J2 {self.id} (File ID: {self.account_activity.account_holder.data_file.id})"

    @classmethod
    def parse_from_segment(cls, segment: str, account_activity: AccountActivity):
        return cls(
            account_activity = account_activity,
            # Person-related values
            surname = get_field_value(fields.j2_fields, "surname_j2", segment),
            first_name = get_field_value(fields.j2_fields, "first_name_j2", segment),
            middle_name = get_field_value(fields.j2_fields, "middle_name_j2", segment),
            gen_code = get_field_value(fields.j2_fields, "gen_code_j2", segment),
            ssn = get_field_value(fields.j2_fields, "ssn_j2", segment),
            dob = get_field_value(fields.j2_fields, "dob_j2", segment),
            phone_num = get_field_value(fields.j2_fields, "phone_num_j2", segment),
            ecoa = get_field_value(fields.j2_fields, "ecoa_j2", segment),
            cons_info_ind = get_field_value(fields.j2_fields, "cons_info_ind_j2", segment),

            # Address-related values
            country_cd = get_field_value(fields.j2_fields, "country_cd_j2", segment),
            addr_line_1 = get_field_value(fields.j2_fields, "addr_line_1_j2", segment),
            addr_line_2 = get_field_value(fields.j2_fields, "addr_line_2_j2", segment),
            city = get_field_value(fields.j2_fields, "city_j2", segment),
            state = get_field_value(fields.j2_fields, "state_j2", segment),
            zip = get_field_value(fields.j2_fields, "zip_j2", segment),
            addr_ind = get_field_value(fields.j2_fields, "addr_ind_j2", segment),
            res_cd = get_field_value(fields.j2_fields, "res_cd_j2", segment),
        )

class K1(models.Model):
    class Meta:
        verbose_name_plural = "K1 Segment Original Creditor Name"
    account_activity = models.OneToOneField(AccountActivity, on_delete=models.CASCADE)
    orig_creditor_name = models.CharField(max_length=200)
    creditor_classification = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"K1 {self.id} (File ID: {self.account_activity.account_holder.data_file.id})"

    @classmethod
    def parse_from_segment(cls, segment: str, account_activity: AccountActivity):
        return cls(
            account_activity = account_activity,
            orig_creditor_name = get_field_value(fields.k1_fields, "k1_orig_creditor_name", segment),
            creditor_classification = get_field_value(fields.k1_fields, "k1_creditor_classification", segment),
        )

class K2(models.Model):
    class Meta:
        verbose_name_plural = "K2 Segment Purchased From/Sold To"
    account_activity = models.OneToOneField(AccountActivity, on_delete=models.CASCADE)
    purch_sold_ind = models.CharField(max_length=200)
    purch_sold_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"K2 {self.id} (File ID: {self.account_activity.account_holder.data_file.id})"

    @classmethod
    def parse_from_segment(cls, segment: str, account_activity: AccountActivity):
        return cls(
            account_activity = account_activity,
            purch_sold_ind = get_field_value(fields.k2_fields, "k2_purch_sold_ind", segment),
            purch_sold_name = get_field_value(fields.k2_fields, "k2_purch_sold_name", segment),
        )

class K3(models.Model):
    class Meta:
        verbose_name_plural = "K3 Segment Mortgage Information"
    account_activity = models.OneToOneField(AccountActivity, on_delete=models.CASCADE)
    agency_id = models.CharField(max_length=200)
    agency_acct_num = models.CharField(max_length=200)
    min = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"K3 {self.id} (File ID: {self.account_activity.account_holder.data_file.id})"

    @classmethod
    def parse_from_segment(cls, segment: str, account_activity: AccountActivity):
        return cls(
            account_activity = account_activity,
            agency_id = get_field_value(fields.k3_fields, "k3_agcy_id", segment),
            agency_acct_num = get_field_value(fields.k3_fields, "k3_agcy_acct_num", segment),
            min = get_field_value(fields.k3_fields, "k3_min", segment),
        )

class K4(models.Model):
    class Meta:
        verbose_name_plural = "K4 Segment Specialized Payment Information"
    account_activity = models.OneToOneField(AccountActivity, on_delete=models.CASCADE)
    spc_pmt_ind = models.CharField(max_length=200)
    deferred_pmt_st_dt = models.DateField(null=True)
    balloon_pmt_due_dt = models.DateField(null=True)
    balloon_pmt_amt = models.IntegerField(null=True)

    def __str__(self) -> str:
        return f"K4 {self.id} (File ID: {self.account_activity.account_holder.data_file.id})"

    @classmethod
    def parse_from_segment(cls, segment: str, account_activity: AccountActivity):
        return cls(
            account_activity = account_activity,
            spc_pmt_ind = get_field_value(fields.k4_fields, "k4_spc_pmt_ind", segment),
            deferred_pmt_st_dt = get_field_value(fields.k4_fields, "k4_deferred_pmt_st_dt", segment),
            balloon_pmt_due_dt = get_field_value(fields.k4_fields, "k4_balloon_pmt_due_dt", segment),
            balloon_pmt_amt = get_field_value(fields.k4_fields, "k4_balloon_pmt_amt", segment),
        )

class L1(models.Model):
    class Meta:
        verbose_name_plural = "L1 Segment Account Number/Identification Number Change"
    account_activity = models.OneToOneField(AccountActivity, on_delete=models.CASCADE)
    change_ind = models.CharField(max_length=200)
    new_acc_num = models.CharField(max_length=200)
    new_id_num = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"L1 {self.id} (File ID: {self.account_activity.account_holder.data_file.id})"

    @classmethod
    def parse_from_segment(cls, segment: str, account_activity: AccountActivity):
        return cls(
            account_activity = account_activity,
            change_ind = get_field_value(fields.l1_fields, "l1_change_ind", segment),
            new_acc_num = get_field_value(fields.l1_fields, "l1_new_acc_num", segment),
            new_id_num = get_field_value(fields.l1_fields, "l1_new_id_num", segment),
        )

class N1(models.Model):
    class Meta:
        verbose_name_plural = "N1 Segment Employment"
    account_activity = models.OneToOneField(AccountActivity, on_delete=models.CASCADE)
    employer_name = models.CharField(max_length=200)
    employer_addr1 = models.CharField(max_length=200)
    employer_addr2 = models.CharField(max_length=200)
    employer_city = models.CharField(max_length=200)
    employer_state = models.CharField(max_length=200)
    employer_zip = models.CharField(max_length=200)
    occupation = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"N1 {self.id} (File ID: {self.account_activity.account_holder.data_file.id})"

    @classmethod
    def parse_from_segment(cls, segment: str, account_activity: AccountActivity):
        return cls(
            account_activity = account_activity,
            employer_name = get_field_value(fields.n1_fields, "n1_employer_name", segment),
            employer_addr1 = get_field_value(fields.n1_fields, "employer_addr1", segment),
            employer_addr2 = get_field_value(fields.n1_fields, "employer_addr2", segment),
            employer_city = get_field_value(fields.n1_fields, "employer_city", segment),
            employer_state = get_field_value(fields.n1_fields, "employer_state", segment),
            employer_zip = get_field_value(fields.n1_fields, "employer_zip", segment),
            occupation = get_field_value(fields.n1_fields, "occupation", segment),
        )
