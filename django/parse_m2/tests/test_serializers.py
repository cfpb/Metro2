from datetime import date
from django.test import TestCase
from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.models import J1, K4, L1, Metro2Event, M2DataFile, AccountHolder, AccountActivity
from rest_framework.renderers import JSONRenderer
from parse_m2.serializers import (
    AccountActivitySerializer,
    AccountHolderSerializer,
    Metro2EventSerializer
)

class AccountActivitySerializerTestCase(TestCase):
    def setUp(self) -> None:
        # Create an AccountActivity record
        event = Metro2Event(name="tst")
        event.save()
        file = M2DataFile(event=event, file_name="tst.txt")
        file.save()
        acct_holder = AccountHolder(
            data_file=file,activity_date=date(2023, 11, 30), cons_acct_num="98765",
            cons_info_ind_assoc=["1A", "B"], ecoa_assoc=["2", "1"])
        acct_holder.save()
        self.acct_activity = AccountActivity(
            account_holder=acct_holder,
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
        self.acct_activity.save()
        k4 = K4(account_activity=self.acct_activity, balloon_pmt_amt=11854)
        k4.save()
        l1 = L1(account_activity=self.acct_activity, change_ind="2")
        l1.save()
        self.json_representation = {
            "id": self.acct_activity.id,
            "inconsistencies": [],
            "activity_date": "2023-11-20",
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
            "cons_info_ind": '',
            "ecoa": '',
            "cons_info_ind_assoc": ["1A", "B"],
            "ecoa_assoc": ["2", "1"],
            "purch_sold_ind": None,
            "balloon_pmt_amt": 11854,
            "change_ind": "2"
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
        event = Metro2Event(name="test")
        event.save()
        file = M2DataFile(event=event, file_name="test.txt")
        file.save()
        self.acct_holder = AccountHolder(
            data_file=file,
            activity_date=date(2023, 11, 30),
            cons_acct_num="12345",
            surname="Doe",
            first_name="Jane",
            middle_name="A",
            gen_code="F",
            ssn="012345678",
            dob=date(2000, 1, 1),
            phone_num="0123456789",
            ecoa="0",
            cons_info_ind="Z"
        )
        self.acct_holder.save()


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
