from datetime import date

from django.test import TestCase

from evaluate_m2.tests.evaluator_test_helper import acct_record, evaluator_result_record
from parse_m2.models import AccountActivity, M2DataFile, Metro2Event


class AccountActivityQuerySetTest(TestCase):
    def setUp(self) -> None:
        event = Metro2Event.objects.create(name = "test")
        self.prev_file = M2DataFile.objects.create(event=event, file_name="test1")
        self.file = M2DataFile.objects.create(event=event, file_name="test")

    def test_base_has_no_previous_bankruptcy_indicators(self):
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
        result = AccountActivity.objects.no_previous_bankruptcy_indicators().count()
        self.assertEqual(result, 1)

    def test_base_has_bankruptcy_indicators(self):
        prior_acct = acct_record(self.prev_file, {
            "id":"1",
            "activity_date": date(2022, 5, 31),
            "cons_acct_num": "0032",
            "cons_info_ind": "a",
            "previous_values":None
            })
        acct_record(self.file, {
            "id":"2",
            "cons_acct_num": "0032",
            "activity_date": date(2022, 6, 30),
            "cons_info_ind": "a",
            "previous_values":prior_acct
            })
        result = AccountActivity.objects.no_previous_bankruptcy_indicators().count()
        self.assertEqual(result, 0)

    def test_j_segment_has_no_previous_bankruptcy_indicators(self):
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

        result = AccountActivity.objects.no_previous_bankruptcy_indicators().count()
        self.assertEqual(result, 1)

    def test_j1_has_one_previous_bankruptcy_indicators(self):
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

        result = AccountActivity.objects.no_previous_bankruptcy_indicators().count()
        self.assertEqual(result, 0)

    def test_j1_has_previous_bankruptcy_indicators(self):
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

        result = AccountActivity.objects.no_previous_bankruptcy_indicators().count()
        self.assertEqual(result, 0)


class AccountActivityQuerySetAnnotationsTest(TestCase):
    def setUp(self) -> None:
        self.event = Metro2Event.objects.create(name = "test")
        self.file = M2DataFile.objects.create(event=self.event, file_name="test")

    def test_inconsistency_counts(self):
        acct = acct_record(
            self.file, {
                "id":"1",
                "activity_date": date(2022, 5, 31),
                "cons_acct_num": "0032",
            }
        )
        evaluator_result_record(self.event, "Sample-1", acct)
        evaluator_result_record(self.event, "Sample-2", acct)

        qs = AccountActivity.objects.with_inconsistency_counts(self.event)
        query_acct = qs.filter(cons_acct_num=acct.cons_acct_num).first()
        self.assertEqual(query_acct.total_inconsistencies, 2)

    def test_inconsistency_counts_same_eval(self):
        acct1 = acct_record(
            self.file, {
                "id":"1",
                "activity_date": date(2022, 5, 31),
                "cons_acct_num": "0032",
            }
        )
        acct2 = acct_record(
            self.file, {
                "id":"2",
                "activity_date": date(2022, 6, 30),
                "cons_acct_num": "0032",
            }
        )
        # One hit across two months
        evaluator_result_record(self.event, "Sample-1", acct1)
        evaluator_result_record(self.event, "Sample-1", acct2)

        qs = AccountActivity.objects.with_inconsistency_counts(self.event)
        query_acct = qs.filter(cons_acct_num=acct1.cons_acct_num).first()
        self.assertEqual(query_acct.total_inconsistencies, 2)

    def test_months_of_data(self):
        acct_record(
            self.file, {
                "id":"1",
                "activity_date": date(2022, 6, 5),
                "cons_acct_num": "0032",
            }
        )
        acct_record(
            self.file, {
                "id":"2",
                "activity_date": date(2022, 6, 20),
                "cons_acct_num": "0032",
            }
        )
        acct_record(
            self.file, {
                "id":"3",
                "activity_date": date(2022, 8, 1),
                "cons_acct_num": "0032",
            }
        )

        qs = AccountActivity.objects.with_months_of_data(self.event)
        query_acct = qs.filter(cons_acct_num="0032").first()
        # June + August
        self.assertEqual(query_acct.months_of_data, 2)
