from django.test import TestCase
from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.models import Metro2Event, M2DataFile, AccountActivity, J1, J2


class AccountActivityQuerySetTest(TestCase):
    def setUp(self) -> None:
        event = Metro2Event.objects.create(name = "test")
        self.file = M2DataFile.objects.create(event=event, file_name="test")

    def test_base_has_bankruptcy_indicators(self):
        acct_record(self.file, {"cons_info_ind": "x"})
        result = AccountActivity.objects.no_bankruptcy_indicators().count()
        self.assertEqual(result, 0)

    def test_base_has_no_bankruptcy_indicators(self):
        acct_record(self.file, {"cons_info_ind": ""})
        result = AccountActivity.objects.no_bankruptcy_indicators().count()
        self.assertEqual(result, 1)

    def test_j1_has_no_bankruptcy_indicators(self):
        a = acct_record(self.file, {"cons_info_ind": ""})
        J1.objects.create(account_activity=a, cons_info_ind="")
        J1.objects.create(account_activity=a, cons_info_ind="")
        result = AccountActivity.objects.no_bankruptcy_indicators().count()
        # I think ideally we would only return one result, since
        # it's only one AccountActivity. Is that possible?
        self.assertEqual(result, 1)

    def test_j1_has_bankruptcy_indicators(self):
        a = acct_record(self.file, {"cons_info_ind": ""})
        J1.objects.create(account_activity=a, cons_info_ind="x")
        result = AccountActivity.objects.no_bankruptcy_indicators().count()
        self.assertEqual(result, 0)

    def test_j2_has_no_bankruptcy_indicators(self):
        a = acct_record(self.file, {"cons_info_ind": ""})
        J2.objects.create(account_activity=a, cons_info_ind="")
        J2.objects.create(account_activity=a, cons_info_ind="")
        result = AccountActivity.objects.no_bankruptcy_indicators().count()
        # I think ideally we would only return one result, since
        # it's only one AccountActivity. Is that possible?
        self.assertEqual(result, 1)

    def test_j2_has_bankruptcy_indicators(self):
        a = acct_record(self.file, {"cons_info_ind": ""})
        J2.objects.create(account_activity=a, cons_info_ind="x")
        result = AccountActivity.objects.no_bankruptcy_indicators().count()
        self.assertEqual(result, 0)

    def test_has_multiple_j1_but_only_one_bankruptcy_indicator(self):
        a = acct_record(self.file, {"cons_info_ind": ""})
        J1.objects.create(account_activity=a, cons_info_ind="x")
        J1.objects.create(account_activity=a, cons_info_ind="")
        result = AccountActivity.objects.no_bankruptcy_indicators().count()
        # I think this should not return any results, since the account does
        # have bankruptcy indicators. Is that possible? IDK
        self.assertEqual(result, 0)

    def test_has_multiple_j2_but_only_one_bankruptcy_indicator(self):
        a = acct_record(self.file, {"cons_info_ind": ""})
        J2.objects.create(account_activity=a, cons_info_ind="x")
        J2.objects.create(account_activity=a, cons_info_ind="")
        result = AccountActivity.objects.no_bankruptcy_indicators().count()
        # I think this should not return any results, since the account does
        # have bankruptcy indicators. Is that possible?
        self.assertEqual(result, 0)
