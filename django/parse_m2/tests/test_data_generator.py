import os
from django.test import TestCase
from datetime import date

from parse_m2 import data_generator
from parse_m2 import fields
from parse_m2.m2_parser import M2FileParser
from parse_m2.models import (
    Metro2Event, M2DataFile, AccountActivity, AccountHolder,
    J1, J2, K1, K2, K3, K4, L1, N1, UnparseableData
)
from evaluate_m2.tests.evaluator_test_helper import acct_record


class GenerateDataTestCase(TestCase):
    def xtest_do_the_thing(self):
        # Actually generate files
        for m in range(1,6):
            data_file = f"sample_data_20170{m}01.txt"
            activity_date = date(2017,m,1)
            data_generator.save_m2_file(data_file, 10000, activity_date)

    def test_save_generated_data(self):
        data_file = 'data_gen_output.txt'

        # Generate a data file
        activity_date = date(2017,1,1)
        data_generator.save_m2_file(data_file, size=10, activity_date=activity_date)

        # Parse it and check that all lines were parseable
        event = Metro2Event.objects.create(name='test_exam')
        parser = M2FileParser(event=event, filepath="file.txt")

        file_size = os.path.getsize(data_file)
        with open(data_file, mode='r') as filestream:
            parser.parse_file_contents(filestream, file_size)

            self.assertEqual(M2DataFile.objects.first().activity_date, activity_date)

            # The file contains the following segments:
            self.assertEqual(AccountHolder.objects.count(), 10)
            self.assertEqual(AccountActivity.objects.count(), 10)

            # The test file may contain some of these:
            # self.assertEqual(J1.objects.count(), 0)
            # self.assertEqual(J2.objects.count(), 0)
            # self.assertEqual(K4.objects.count(), 0)

            # The test file does not contain these:
            self.assertEqual(UnparseableData.objects.count(), 0)
            self.assertEqual(K1.objects.count(), 0)
            self.assertEqual(K2.objects.count(), 0)
            self.assertEqual(L1.objects.count(), 0)
            self.assertEqual(K3.objects.count(), 0)
            self.assertEqual(N1.objects.count(), 0)

        # Remove test file when finished
        os.remove(data_file)

    #######################################
    ## Methods for fabricating data
    #######################################
    def test_random_date(self):
        dt1 = data_generator.random_date(date(2001,1,1), date(2010,12,31))
        dt2 = data_generator.random_date(date(2001,1,1), date(2010,12,31))
        dt3 = data_generator.random_date(date(2001,1,1), date(2010,12,31))
        dt4 = data_generator.random_date(date(2001,1,1), date(2010,12,31))
        self.assertNotEqual(len({dt1, dt2, dt3, dt4}), 1)

    #######################################
    ## Methods for producing segments of M2 data
    #######################################
    def test_base_segment(self):
        # Base records to associate account activity with
        event = Metro2Event.objects.create(name="Test Event")
        m2df = M2DataFile.objects.create(event=event)

        # Create a record with default values
        r1_act = acct_record(m2df, {'cons_acct_num': 'ABCDEFGHIJ'})
        r1_holder = r1_act.account_holder

        # Serialize the record into M2 format
        serialized_r1 = data_generator.base_segment_data(r1_act, r1_holder)

        # Parse the serialized record so we can check that the values serialized correctly
        parsed_r1_act = AccountActivity.parse_from_segment(serialized_r1, m2df, date(2022,1,1))
        parsed_r1_holder = AccountHolder.parse_from_segment(serialized_r1, parsed_r1_act, date(2022,1,1))

        self.assertEqual(parsed_r1_act.acct_stat, r1_act.acct_stat)
        self.assertEqual(parsed_r1_holder.cons_acct_num, r1_holder.cons_acct_num)
        self.assertEqual(parsed_r1_act.doai, r1_act.doai)

    def test_j1(self):
        # Base record to associate account activity with
        r1_act = AccountActivity()

        j1 = J1(
            middle_name = "MIDDLENAME",
        )
        serialized_j1 = data_generator.j1_segment_data(j1)
        parsed_j1 = J1.parse_from_segment(serialized_j1, r1_act)
        self.assertEqual(parsed_j1.middle_name, "MIDDLENAME")

    def test_j2(self):
        # Base record to associate account activity with
        r1_act = AccountActivity()

        j2 = J2(
            city = "TESTCITY",
        )
        serialized_j2 = data_generator.j2_segment_data(j2)
        parsed_j2 = J2.parse_from_segment(serialized_j2, r1_act)
        self.assertEqual(parsed_j2.city, "TESTCITY")

    def test_k4(self):
        # Base record to associate account activity with
        r1_act = AccountActivity()

        k4 = K4(
            balloon_pmt_amt = 12345,
        )
        serialized_k4 = data_generator.k4_segment_data(k4)
        parsed_k4 = K4.parse_from_segment(serialized_k4, r1_act)
        self.assertEqual(parsed_k4.balloon_pmt_amt, 12345)

    def test_blank_segment(self):
        self.assertEqual(
            data_generator.blank_segment('K1'),
            "K1................................"
        )
        self.assertEqual(
            data_generator.blank_segment('k4'),
            "K4............................"
        )

    #######################################
    ## Helper methods for formatting individual fields
    #######################################
    def test_format_value_string(self):
        self.assertEqual(data_generator.format_str_value("hello", 10), "hello     ")
        self.assertEqual(data_generator.format_str_value("hello", 4), "hell")
        self.assertEqual(data_generator.format_str_value("hello", 5), "hello")

    def test_format_value_numeric(self):
        self.assertEqual(data_generator.format_num_value(123456, 10), "0000123456")
        self.assertEqual(data_generator.format_num_value(123456, 6), "123456")
        with self.assertRaises(Exception):
            data_generator.format_num_value(123456, 5)

    def test_format_value_date(self):
        self.assertEqual(data_generator.format_date_value(date(2011,1,1), 8), "01012011")
        self.assertEqual(data_generator.format_date_value(date(1980,4,29), 8), "04291980")
        with self.assertRaises(Exception):
            data_generator.format_date_value(date(2022,2,2), 5)

    def test_set_field_value_str(self):
        starting_seg = "......................."
        self.assertEqual(
            ".....timestam..........",
            data_generator.set_field_value(fields.base_fields, 'time_stamp', "timestamp", starting_seg)
        )

    def test_set_field_value_num(self):
        start_seg_2 = ".............................................................................................."
        self.assertEqual(
            "...................................................................................000000999..",
            data_generator.set_field_value(fields.base_fields, 'credit_limit', "999", start_seg_2)
        )