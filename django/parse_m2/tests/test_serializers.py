from datetime import date
from django.test import TestCase
from parse_m2.initiate_post_parsing import post_parse
from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.models import K2, K4, L1, Metro2Event, M2DataFile, AccountHolder, AccountActivity
from rest_framework.renderers import JSONRenderer
from parse_m2.serializers import (
    AccountActivitySerializer,
    AccountHolderSerializer,
    Metro2EventSerializer
)

class AccountActivitySerializerTestCase(TestCase):
    def setUp(self) -> None:
        # Create an AccountActivity record
        event = Metro2Event.objects.create(name="tst")
        file = M2DataFile.objects.create(event=event, file_name="tst.txt")
        self.acct_activity = AccountActivity.objects.create(
            data_file=file,
            event=event,
            activity_date=date(2023,11,20),
            cons_acct_num="98765",
            port_type="port_type",
            acct_type="acct_type",
            date_open=date(2020,3,17),
            credit_limit=9000,
            hcola=90210,
            terms_dur="terms_dur",
            terms_freq="terms_freq",
            smpa=5,
            actual_pmt_amt=201,
            acct_stat="acct_stat",
            pmt_rating="pmt_rating",
            php="php",
            spc_com_cd="spc_com_cd",
            compl_cond_cd="compl_cond_cd",
            current_bal=12345,
            amt_past_due=111,
            orig_chg_off_amt=0,
            doai=date(2023,11,3),
            dofd=None,
            date_closed=None,
            dolp=date(2023,1,1),
            int_type_ind="int_type_ind",
        )
        AccountHolder.objects.create(
            account_activity=self.acct_activity, activity_date=date(2023, 11, 30),
            surname="Doe", first_name="Jane", cons_acct_num="98765",
            cons_info_ind_assoc=["1A", "B"], ecoa_assoc=["2", "1"])
        K2.objects.create(account_activity=self.acct_activity, purch_sold_name="Fake")
        K4.objects.create(account_activity=self.acct_activity, balloon_pmt_amt=11854)
        L1.objects.create(account_activity=self.acct_activity, change_ind="2",
                new_id_num="0032", new_acc_num="32")
        self.json_representation = {
            "id": self.acct_activity.id,
            "inconsistencies": [],
            "activity_date": "2023-11-20",
            "account_holder__surname": "Doe",
            "account_holder__first_name": "Jane",
            "port_type": "port_type",
            "acct_type": "acct_type",
            "date_open": "2020-03-17",
            "credit_limit": 9000,
            "hcola": 90210,
            "id_num": "",
            "terms_dur": "terms_dur",
            "terms_freq": "terms_freq",
            "smpa": 5,
            "actual_pmt_amt": 201,
            "acct_stat": "acct_stat",
            "pmt_rating": "pmt_rating",
            "php": "php",
            "spc_com_cd": "spc_com_cd",
            "compl_cond_cd": "compl_cond_cd",
            "current_bal": 12345,
            "amt_past_due": 111,
            "orig_chg_off_amt": 0,
            "doai": "2023-11-03",
            "dofd": None,
            "date_closed": None,
            "dolp": "2023-01-01",
            "int_type_ind": "int_type_ind",
            "account_holder__cons_info_ind": '',
            "account_holder__ecoa": '',
            "account_holder__cons_info_ind_assoc": ["1A", "B"],
            "account_holder__ecoa_assoc": ["2", "1"],
            "k2__purch_sold_ind": '',
            "k2__purch_sold_name": "Fake",
            "k4__balloon_pmt_amt": 11854,
            "l1__change_ind": "2",
            "l1__new_id_num": "0032",
            "l1__new_acc_num": "32",
        }

    def test_account_activity_serializer(self):
        serializer = AccountActivitySerializer(self.acct_activity)
        self.assertEqual(serializer.data, self.json_representation)

    def test_account_activity_serializer_many_true(self):
        activity_records = [self.acct_activity]
        serializer = AccountActivitySerializer(activity_records, many=True)
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render([self.json_representation])
        self.assertEqual(json_output, expected)

class AccountHolderSerializerTestCase(TestCase):
    def setUp(self) -> None:
        # Create an AccountActivity record
        test_date = date(2023, 11, 30)
        event = Metro2Event(name="test")
        event.save()
        file = M2DataFile.objects.create(event=event, file_name="test.txt")
        acct_activity = acct_record(file, {
            "activity_date": test_date,
            "cons_acct_num": "12345",
            "surname": "Doe",
            "first_name": "Jane",
            "middle_name": "A",
            "gen_code": "F",
            "ssn": "012345678",
            "dob": date(2000, 1, 1),
            "phone_num": "0123456789",
            "ecoa": "0",
            "cons_info_ind": "Z"
        })

        self.acct_holder = acct_activity.account_holder

        self.json_representation = {
            "id": self.acct_holder.id,
            "surname": "Doe",
            "first_name": "Jane",
            "middle_name": "A",
            "gen_code": "F",
            "ssn": "012345678",
            "dob": "2000-01-01",
            "phone_num": "0123456789",
            "ecoa": "0",
            "cons_info_ind": "Z",
            "country_cd": "",
            "addr_line_1": "",
            "addr_line_2": "",
            "city": "",
            "state": "",
            "zip": "",
            "addr_ind": "",
            "res_cd": "",
            "cons_acct_num": "12345"
        }

    def test_account_holder_serializer(self):
        serializer = AccountHolderSerializer(self.acct_holder)
        self.assertEqual(serializer.data, self.json_representation)

    def test_account_holder_serializer_many_true(self):
        acct_holders = [self.acct_holder]
        serializer = AccountHolderSerializer(acct_holders, many=True)
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render([self.json_representation])
        self.assertEqual(json_output, expected)

class Metro2EventSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.event = Metro2Event.objects.create(id=1, name='test_exam')
        self.data_file = M2DataFile.objects.create(event=self.event, file_name='file.txt')
        self.json_representation = {
            'id': 1, 'name': 'test_exam', 'portfolio': '',
            'eid_or_matter_num': '', 'other_descriptor': '',
            'date_range_start': '2011-07-31', 'date_range_end': '2020-12-31'
        }
        self.activities = [
            { 'id': 32, 'activity_date': date(2011, 7, 31), 'cons_acct_num': '0032', },
            { 'id': 33, 'activity_date': date(2012, 10, 31), 'cons_acct_num': '0033', },
            { 'id': 34, 'activity_date': date(2013, 11, 30), 'cons_acct_num': '0034', },
            { 'id': 35, 'activity_date': date(2020, 12, 31), 'cons_acct_num': '0035', }]
        for item in self.activities:
            acct_record(self.data_file, item)
        post_parse(self.event)  # Ensure the event record has the date range saved

    def test_metro2_event_serializer(self):
        serializer = Metro2EventSerializer(self.event)
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render(self.json_representation)
        self.assertEqual(json_output, expected)

    def test_metro2_event_serializer_many_true(self):
        events = [self.event]
        serializer = Metro2EventSerializer(events, many=True)
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render([self.json_representation])
        self.assertEqual(json_output, expected)
