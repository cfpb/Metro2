from django.contrib.auth.models import User
from django.test import TestCase
import os
from datetime import date, datetime

from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.models import (
    Metro2Event,
    M2DataFile, AccountHolder, AccountActivity,
    J1, J2, K1, K2, K3, K4, L1, N1
)


class ParserModelsTestCase(TestCase):
    def setUp(self):
        self.base_seg = os.path.join('parse_m2', 'tests','sample_files', 'base_segment_1.txt')  # noqa E501

        # Create the parent records for the AccountActivity data
        event = Metro2Event(name='test_exam')
        self.data_file = M2DataFile(event=event, file_name='file.txt')
        self.activity_date = datetime(2021, 1, 1)
        self.account_activity = AccountActivity(data_file = self.data_file,
                                                activity_date = self.activity_date)
        self.account_holder = AccountHolder(account_activity = self.account_activity,
                                            activity_date = self.activity_date)

    def create_exam_activity(self):
        acct_date=date(2019, 12, 31)
        # Create the Account Activities data
        activities = [
            {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_type': '12', 'credit_limit': 30, 'hcola': -5, 'port_type': 'I',
                'cons_info_ind': 'X', 'terms_dur': '15', 'terms_freq':'P'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
              'acct_type': '91', 'credit_limit': 40, 'hcola': -5, 'port_type': 'I',
              'cons_info_ind': 'W', 'terms_dur': '20', 'terms_freq':'D'
            }]
        # Create the parent records for the AccountActivity data for first event
        event = Metro2Event(name='test_exam')
        event.save()
        file = M2DataFile(event=event, file_name='file.txt')
        file.save()

        for item in activities:
            acct_record(file, item)

        # Create the second exam Account Activities data
        activities2 = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_type': '00', 'credit_limit': 10, 'hcola': -1, 'port_type': 'I',
                'cons_info_ind': 'Z', 'terms_dur': '5', 'terms_freq':'P'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
              'acct_type': '3A', 'credit_limit': 20, 'hcola': -1, 'port_type': 'M',
              'cons_info_ind': 'Y', 'terms_dur': '10', 'terms_freq':'W'
            }]
        # Create the parent records for the AccountActivity data for second event
        event_2 = Metro2Event(name='test_exam2')
        event_2.save()
        file2 = M2DataFile(event=event_2, file_name='file2.txt')
        file2.save()

        for item in activities2:
            acct_record(file2, item)

    def test_metro2_event_get_all_account_activity_returns_results(self):
        self.create_exam_activity()
        event = Metro2Event.objects.get(name='test_exam')
        result = event.get_all_account_activity()

        self.assertEqual(2, len(result))

    def test_get_all_account_activity_returns_no_results(self):
        self.create_exam_activity()
        event = Metro2Event(name="test_exam")
        result = event.get_all_account_activity()

        self.assertEqual(0, len(result))

    def test_parse_account_activity(self):
        with open(self.base_seg) as file:
            base_segment = file.readline()
            result = AccountActivity.parse_from_segment(base_segment, self.data_file, self.activity_date)
            self.assertIsInstance(result, AccountActivity)
            self.assertEqual(result.credit_limit, 210000)
            self.assertEqual(result.php, "222211000000000000010100")
            self.assertEqual(result.date_closed, None)
            self.assertEqual(result.doai, datetime(2023, 3, 31))

    def test_parse_account_holder(self):
        with open(self.base_seg) as file:
            base_segment = file.readline()
            result = AccountHolder.parse_from_segment(base_segment, self.account_activity, self.activity_date)
            self.assertIsInstance(result, AccountHolder)
            self.assertEqual(result.first_name, "FIRSTNAME1")
            self.assertEqual(result.country_cd, "US")
            self.assertEqual(result.phone_num, "3333334444")

    def test_parse_j1(self):
        filename = os.path.join('parse_m2', 'tests', 'sample_files', 'j1_segment.txt')
        with open(filename) as file:
            seg = file.readline()
            result = J1.parse_from_segment(seg, self.account_activity)
            self.assertIsInstance(result, J1)
            self.assertEqual(result.surname, "SURNAMEJ1")
            self.assertEqual(result.ssn, "333224444")

    def test_parse_j2(self):
        filename = os.path.join('parse_m2', 'tests', 'sample_files', 'j2_segment.txt')
        with open(filename) as file:
            seg = file.readline()
            result = J2.parse_from_segment(seg, self.account_activity)
            self.assertIsInstance(result, J2)
            self.assertEqual(result.dob, "11231977")
            self.assertEqual(result.addr_line_1, "1234 EXAMPLE BLVD")

    def test_parse_k1(self):
        filename = os.path.join('parse_m2', 'tests', 'sample_files', 'k1_segment.txt')
        with open(filename) as file:
            seg = file.readline()
            result = K1.parse_from_segment(seg, self.account_activity)
            self.assertIsInstance(result, K1)
            self.assertEqual(result.creditor_classification, "03")

    def test_parse_k2(self):
        filename = os.path.join('parse_m2', 'tests', 'sample_files', 'k2_segment.txt')
        with open(filename) as file:
            seg = file.readline()
            result = K2.parse_from_segment(seg, self.account_activity)
            self.assertIsInstance(result, K2)
            self.assertEqual(result.purch_sold_ind, "2")

    def test_parse_k3(self):
        filename = os.path.join('parse_m2', 'tests', 'sample_files', 'k3_segment.txt')
        with open(filename) as file:
            seg = file.readline()
            result = K3.parse_from_segment(seg, self.account_activity)
            self.assertIsInstance(result, K3)
            self.assertEqual(result.min, "MORTGAGEIDNUM")

    def test_parse_k4(self):
        filename = os.path.join('parse_m2', 'tests', 'sample_files', 'k4_segment.txt')
        with open(filename) as file:
            seg = file.readline()
            result = K4.parse_from_segment(seg, self.account_activity)
            self.assertIsInstance(result, K4)
            self.assertEqual(result.balloon_pmt_due_dt, datetime(2025, 2, 18))
            self.assertEqual(result.balloon_pmt_amt, 495000)

    def test_parse_l1(self):
        filename = os.path.join('parse_m2', 'tests', 'sample_files', 'l1_segment.txt')
        with open(filename) as file:
            seg = file.readline()
            result = L1.parse_from_segment(seg, self.account_activity)
            self.assertIsInstance(result, L1)
            self.assertEqual(result.new_acc_num, "NEWACCTNUMBER")

    def test_parse_n1(self):
        filename = os.path.join('parse_m2', 'tests', 'sample_files', 'n1_segment.txt')
        with open(filename) as file:
            seg = file.readline()
            result = N1.parse_from_segment(seg, self.account_activity)
            self.assertIsInstance(result, N1)
            self.assertEqual(result.occupation, "OCCUPATIONN1")


class TestMetro2EventAccess(TestCase):
    def setUp(self) -> None:
        # create users
        self.enf_user = User.objects.create(username="examiner", password="")
        self.sup_user = User.objects.create(username="other_user", password="")

        # Create events with only one user added
        self.enf_event = Metro2Event.objects.create(name="OfficialExam2023",)
        self.enf_event.members.add(self.enf_user)

        self.sup_event = Metro2Event.objects.create(name="SupervisionCase2022",)
        self.sup_event.members.add(self.sup_user)

    def test_access_true_for_assigned_users(self):
        # Enforcement user should only have access to the user that they are a member of
        self.assertTrue(self.enf_event.check_access_for_user(self.enf_user))
        self.assertFalse(self.sup_event.check_access_for_user(self.enf_user))

        # Supervision user should only have access to the user that they are a member of
        self.assertFalse(self.enf_event.check_access_for_user(self.sup_user))
        self.assertTrue(self.sup_event.check_access_for_user(self.sup_user))


class TestMetro2Eventset(TestCase):
    def setUp(self) -> None:
        self.name = "OfficialExam2023"
        self.event = Metro2Event.objects.create(name=self.name)

    def test_str_matches_name(self):
        self.assertEqual(self.name, str(self.event))
