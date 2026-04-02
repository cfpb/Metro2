from datetime import date
from unittest.mock import Mock

from django.test import SimpleTestCase, TestCase

from rest_framework.renderers import JSONRenderer

from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.initiate_post_parsing import post_parse
from parse_m2.models import (
    K1,
    K2,
    K3,
    K4,
    L1,
    N1,
    AccountActivity,
    M2DataFile,
    Metro2Event,
)
from parse_m2.serializers import (
    AccountActivitySerializer,
    AccountHolderSerializer,
    Metro2EventSerializer,
    OptionalRelatedField,
)


class OptionalRelatedFieldTestCase(SimpleTestCase):
    def setUp(self) -> None:
        # Object to test relations one level deep
        self.shallow_obj = Mock(spec=[])
        self.shallow_obj.related = Mock(spec=[], f="hello", g="world")

        # Object to test relations multiple levels deep
        self.deep_obj = Mock(spec=[])
        self.deep_obj.a = Mock(spec=[])
        self.deep_obj.a.b = Mock(spec=[], c=42)

        # Object to test empty relations
        self.empty_obj = Mock(spec=[])

    def test_simple_related_path(self):
        field = OptionalRelatedField("related.f")
        self.assertEqual(field.to_representation(self.shallow_obj), "hello")

    def test_missing_related_object(self):
        field = OptionalRelatedField("related.f")
        self.assertIsNone(field.to_representation(self.empty_obj))

    def test_missing_related_object_path(self):
        field = OptionalRelatedField("related.h")
        self.assertIsNone(field.to_representation(self.empty_obj))

    def test_deep_related_path(self):
        field = OptionalRelatedField("a.b.c")
        self.assertEqual(field.to_representation(self.deep_obj), 42)


class AccountActivitySerializerTestCase(TestCase):
    def setUp(self) -> None:
        # Create an AccountActivity record
        event = Metro2Event.objects.create(name="tst")
        file = M2DataFile.objects.create(event=event, file_name="tst.txt")

        self.prev_acct_activity = AccountActivity.objects.create(
            data_file=file,
            event=event,
            activity_date=date(2023, 10, 1),
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
            dofd=date(2023,1,1),
            date_closed=date(2023,2,1),
            dolp=date(2023,1,1),
            int_type_ind="int_type_ind",
            surname="Doe",
            first_name="Jane",
            cons_info_ind_assoc=["1A", "B"],
            ecoa_assoc=["2", "1"],
        )
        L1.objects.create(
            account_activity=self.prev_acct_activity,
            change_ind="",
            new_id_num="",
            new_acc_num=""
        )

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
            dofd=date(2023,1,1),
            date_closed=date(2023,2,1),
            dolp=date(2023,1,1),
            int_type_ind="int_type_ind",
            surname="Doe",
            first_name="Jane",
            cons_info_ind_assoc=["1A", "B"],
            ecoa_assoc=["2", "1"],
            previous_values=self.prev_acct_activity,
        )
        K1.objects.create(
            account_activity=self.acct_activity,
            orig_creditor_name="OrigCred",
            creditor_classification="CC",
        )
        K2.objects.create(
            account_activity=self.acct_activity,
            purch_sold_ind="",
            purch_sold_name="Fake",
        )
        K3.objects.create(
            account_activity=self.acct_activity,
            agency_id="AG1",
            agency_acct_num="AG_ACCT",
            min="MIN1",
        )
        K4.objects.create(
            account_activity=self.acct_activity,
            balloon_pmt_amt=11854,
            balloon_pmt_due_dt=date(2023,5,1),
            deferred_pmt_st_dt=date(2023,4,1),
        )
        L1.objects.create(
            account_activity=self.acct_activity,
            change_ind="2",
            new_id_num="0032",
            new_acc_num="32"
        )
        N1.objects.create(
            account_activity=self.acct_activity,
            employer_name="Acme",
            employer_addr1="123 Main",
            employer_addr2="Ste 4",
            employer_city="Springfield",
            employer_state="IL",
            employer_zip="62704",
            occupation="Engineer",
        )

        self.json_representation = {
            "id": self.acct_activity.id,
            "inconsistencies": [],
            "activity_date": "2023-11-20",
            "surname": "Doe",
            "first_name": "Jane",
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
            "php1": "p",
            "spc_com_cd": "spc_com_cd",
            "compl_cond_cd": "compl_cond_cd",
            "current_bal": 12345,
            "amt_past_due": 111,
            "orig_chg_off_amt": 0,
            "doai": "2023-11-03",
            "dofd": "2023-01-01",
            "date_closed": "2023-02-01",
            "dolp": "2023-01-01",
            "int_type_ind": "int_type_ind",
            "cons_info_ind": '',
            "ecoa": '',
            "cons_info_ind_assoc": ["1A", "B"],
            "ecoa_assoc": ["2", "1"],
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
        self.assertEqual(serializer.data, [self.json_representation])

    def test_account_activity_limited_fields(self):
        include_fields = ["id", "acct_type"]
        serializer = AccountActivitySerializer(
            self.acct_activity, include_fields=include_fields
        )
        self.assertEqual(
            serializer.data,
            {k: v for k, v in self.json_representation.items() if k in include_fields},
        )

    def test_includes_all_fields(self):
        # Pass `include_fields=None` will ensure all possible fields are serialized
        serializer = AccountActivitySerializer(
            self.acct_activity,
            include_fields=None
        )
        fields_that_are_none = {
            k for k, v in serializer.data.items()
            if v is None
        }
        self.assertEqual(fields_that_are_none, set())


class AccountHolderSerializerTestCase(TestCase):
    def setUp(self) -> None:
        # Create an AccountActivity record
        test_date = date(2023, 11, 30)
        event = Metro2Event(name="test")
        event.save()
        file = M2DataFile.objects.create(event=event, file_name="test.txt")
        self.acct_activity = acct_record(file, {
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

        self.json_representation = {
            "id": self.acct_activity.id,
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
        serializer = AccountHolderSerializer(self.acct_activity)
        self.assertEqual(serializer.data, self.json_representation)

    def test_account_holder_serializer_many_true(self):
        acct_holders = [self.acct_activity]
        serializer = AccountHolderSerializer(acct_holders, many=True)
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render([self.json_representation])
        self.assertEqual(json_output, expected)

class Metro2EventSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.event = Metro2Event.objects.create(id=1, name='test_exam')
        self.data_file = M2DataFile.objects.create(
            event=self.event,
            file_name='file.txt'
        )
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
