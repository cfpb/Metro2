from datetime import date
from django.test import TestCase
from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.models import Metro2Event, M2DataFile, AccountActivity, J1, J2


class AccountActivityQuerySetTest(TestCase):
    def setUp(self) -> None:
        event = Metro2Event.objects.create(name = "test")
        self.prev_file = M2DataFile.objects.create(event=event, file_name="test1")
        self.file = M2DataFile.objects.create(event=event, file_name="test")

    def test_base_has_no_bankruptcy_indicators(self):
        prior_acct = acct_record(self.prev_file, {
            "id":"1",
            "activity_date": date(2022, 5, 31),
            "cons_acct_num": "0032",
            "cons_info_ind": "",
            "previous_values":None
            })
        acct_record(self.file, {
            "id":"2",
            "cons_acct_num": "0032",
            "activity_date": date(2022, 6, 30),
            "cons_info_ind": "a",
            "previous_values":prior_acct
            })
        result = AccountActivity.objects.no_bankruptcy_indicators().count()
        self.assertEqual(result, 1)

    def test_j_segment_has_no_bankruptcy_indicators(self):
        prior_acct = acct_record(self.prev_file, {
            "id":"1",
            "activity_date": date(2022, 5, 31),
            "cons_acct_num": "0032",
            "cons_info_ind": "",
            "previous_values":None,
            "cons_info_ind_assoc": []
            })

        acct_record(self.file, {
            "id":"2",
            "cons_acct_num": "0032",
            "activity_date": date(2022, 6, 30),
            "cons_info_ind": "a",
            "previous_values":prior_acct
            })

        result = AccountActivity.objects.no_bankruptcy_indicators().count()
        self.assertEqual(result, 1)

    def test_j1_has_one_bankruptcy_indicators(self):
        prior_acct = acct_record(self.prev_file, {
            "id":"1",
            "activity_date": date(2022, 5, 31),
            "cons_acct_num": "0032",
            "cons_info_ind": "",
            "previous_values":None,
            "cons_info_ind_assoc": ["x",""]
            })

        acct_record(self.file, {
            "id":"2",
            "cons_acct_num": "0032",
            "activity_date": date(2022, 6, 30),
            "cons_info_ind": "a",
            "previous_values":prior_acct
            })

        result = AccountActivity.objects.no_bankruptcy_indicators().count()
        self.assertEqual(result, 0)

    def test_j1_has_bankruptcy_indicators(self):
        prior_acct = acct_record(self.prev_file, {
            "id":"1",
            "activity_date": date(2022, 5, 31),
            "cons_acct_num": "0032",
            "cons_info_ind": "",
            "previous_values":None,
            "cons_info_ind_assoc": ["X"]
            })

        acct_record(self.file, {
            "id":"2",
            "cons_acct_num": "0032",
            "activity_date": date(2022, 6, 30),
            "cons_info_ind": "a",
            "previous_values":prior_acct
            })

        result = AccountActivity.objects.no_bankruptcy_indicators().count()
        self.assertEqual(result, 0)
