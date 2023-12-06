from django.test import TestCase
import os
from datetime import datetime

from parse_m2.models import (
    Metro2Event,
    M2DataFile, AccountHolder, AccountActivity,
    J1, J2, K1, K2, K3, K4, L1, N1
)


class ParserUtilsTestCase(TestCase):
    def setUp(self):
        self.base_seg = os.path.join('parse_m2', 'tests','sample_files', 'base_segment_1.txt')  # noqa E501

        # Create the parent records for the AccountActivity data
        event = Metro2Event(name='test_exam')
        self.data_file = M2DataFile(event=event, file_name='file.txt')
        self.activity_date = datetime(2021, 1, 1)
        self.account_holder = AccountHolder(
            data_file = self.data_file, activity_date = self.activity_date)
        self.account_activity = AccountActivity(
            account_holder = self.account_holder, activity_date = self.activity_date)

    def test_parse_account_holder(self):
        with open(self.base_seg) as file:
            base_segment = file.readline()
            result = AccountHolder.parse_from_segment(base_segment, self.data_file, self.activity_date)
            self.assertIsInstance(result, AccountHolder)
            self.assertEqual(result.first_name, "FIRSTNAME1")
            self.assertEqual(result.country_cd, "US")
            self.assertEqual(result.phone_num, "3333334444")

    def test_parse_account_activity(self):
        with open(self.base_seg) as file:
            base_segment = file.readline()
            result = AccountActivity.parse_from_segment(base_segment, self.account_holder, self.activity_date)
            self.assertIsInstance(result, AccountActivity)
            self.assertEqual(result.credit_limit, 210000)
            self.assertEqual(result.php, "222211000000000000010100")
            self.assertEqual(result.date_closed, None)
            self.assertEqual(result.doai, datetime(2023, 3, 31))

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
