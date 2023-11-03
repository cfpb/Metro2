from django.db import models


class M2DataFile(models.Model):
    exam_identifier = models.CharField(max_length=200)
    file_name = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

class UnparseableData(models.Model):
    data_file = models.ForeignKey(M2DataFile, on_delete=models.CASCADE)
    unparseable_line = models.CharField(max_length=2000)
    error_description = models.CharField(max_length=200)

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
    data_file = models.ForeignKey(M2DataFile, on_delete=models.CASCADE)
    activity_date = models.DateField()
    cons_acct_num = models.CharField(max_length=200)
    # Since this model inherits from the Person base class,
    # it automatically includes name, ssn, dob, ecoa, etc.

    # Since this model inherits from the Address base class,
    # it automatically has country_cd, addr, city, state, etc.

class AccountActivity(models.Model):
    # Note: Numeric fields are using models.IntegerField, which
    # has a limit of +/- 2.4 billion. Since the Metro2 format limits each of
    # these numeric fields to 9 characters, that size should be sufficient.
    # Also, it limits each numeric field to whole numbers only,
    # so no precision will be lost.

    # Note: Date fields that are not required in the CRRG use the option
    # null=True. For all required fields, this option defaults to null=False,
    # so they must have a value.

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
    doai = models.DateField()
    dofd = models.DateField(null=True)
    date_closed = models.DateField(null=True)
    dolp = models.DateField(null=True)
    int_type_ind = models.CharField(max_length=200)

class J1(Person):
    account_activity = models.ForeignKey(AccountActivity, on_delete=models.CASCADE)
    # Contains all fields from the Person abstract class

class J2(Person, Address):
    account_activity = models.ForeignKey(AccountActivity, on_delete=models.CASCADE)
    # Contains all fields from the Person and Address abstract classes

class K1(models.Model):
    account_activity = models.OneToOneField(AccountActivity, on_delete=models.CASCADE)
    orig_creditor_name = models.CharField(max_length=200)
    creditor_classification = models.CharField(max_length=200)

class K2(models.Model):
    account_activity = models.OneToOneField(AccountActivity, on_delete=models.CASCADE)
    purch_sold_ind = models.CharField(max_length=200)
    purch_sold_name = models.CharField(max_length=200)

class K3(models.Model):
    account_activity = models.OneToOneField(AccountActivity, on_delete=models.CASCADE)
    agency_id = models.CharField(max_length=200)
    agency_acct_num = models.CharField(max_length=200)
    min = models.CharField(max_length=200)

class K4(models.Model):
    account_activity = models.OneToOneField(AccountActivity, on_delete=models.CASCADE)
    spc_pmt_ind = models.CharField(max_length=200)
    deferred_pmt_st_dt = models.DateField(null=True)
    balloon_pmt_due_dt = models.DateField(null=True)
    balloon_pmt_amt = models.IntegerField()

class N1(models.Model):
    account_activity = models.OneToOneField(AccountActivity, on_delete=models.CASCADE)
    employer_name = models.CharField(max_length=200)
    employer_addr1 = models.CharField(max_length=200)
    employer_addr2 = models.CharField(max_length=200)
    employer_city = models.CharField(max_length=200)
    employer_state = models.CharField(max_length=200)
    employer_zip = models.CharField(max_length=200)
    occupation = models.CharField(max_length=200)
