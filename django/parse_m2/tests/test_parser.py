from django.test import TestCase
import os
from datetime import datetime

from parse_m2.m2_parser import M2FileParser
from parse_m2 import parse_utils
from parse_m2.models import (
    Metro2Event, UnparseableData,
    AccountHolder, AccountActivity,
    J1, J2, K1, K2, K3, K4, L1, N1
)

class ParserTestCase(TestCase):
    def setUp(self):
        self.header_seg = os.path.join('parse_m2', 'tests','sample_files', 'header_segment_1.txt')
        self.base_seg = os.path.join('parse_m2', 'tests','sample_files', 'base_segment_1.txt')
        self.tiny_file = os.path.join('parse_m2', 'tests','sample_files', 'm2_file_small.txt')
        self.missing_header = os.path.join('parse_m2', 'tests','sample_files', 'm2_file_small_no_header.txt')
        self.error_file = os.path.join('parse_m2', 'tests','sample_files', 'm2_file_small_with_error.txt')

        self.extras_str = "K1ORIGNALCREDITORNAME           03K22SOLDTONAME                     L12NEWACCTNUMBER                                      "

        event = Metro2Event(name='test_exam')
        event.save()
        self.parser = M2FileParser(event=event, filepath="file.txt")
        self.activity_date = datetime(2021, 1, 1)
        self.account_holder = AccountHolder(
            data_file = self.parser.file_record, activity_date = self.activity_date)
        self.account_activity = AccountActivity(
            account_holder = self.account_holder, activity_date = self.activity_date)

    ############################
    # Tests for the whole parsing process
    def test_parse(self):
        # Test the whole parsing process for a file
        file_size = os.path.getsize(self.tiny_file)

        with open(self.tiny_file, mode='r') as filestream:
            self.parser.parse_file_contents(filestream, file_size)

            # The test file contains the following segments:
            self.assertEqual(AccountHolder.objects.count(), 3)
            self.assertEqual(AccountActivity.objects.count(), 3)
            self.assertEqual(J1.objects.count(), 2)
            self.assertEqual(J2.objects.count(), 1)
            self.assertEqual(K1.objects.count(), 1)
            self.assertEqual(K2.objects.count(), 1)
            self.assertEqual(L1.objects.count(), 1)

            # The test file does not contain these:
            self.assertEqual(UnparseableData.objects.count(), 0)
            self.assertEqual(K3.objects.count(), 0)
            self.assertEqual(K4.objects.count(), 0)
            self.assertEqual(N1.objects.count(), 0)

    def test_parse_file_without_header_line(self):
        file_size = os.path.getsize(self.missing_header)
        with open(self.missing_header, mode='r') as filestream:
            self.parser.parse_file_contents(filestream, file_size)

            # Because the file is missing a header, the parser
            # uses the DOAI value as the activity_date
            for aa in AccountActivity.objects.all():
                doai = aa.doai
                self.assertEqual(doai, aa.activity_date)
                self.assertEqual(doai, aa.account_holder.activity_date)

    def test_aggregate_fields(self):
        # Test the whole parsing process for a file
        file_size = os.path.getsize(self.tiny_file)
        with open(self.tiny_file, mode='r') as filestream:
            self.parser.parse_file_contents(filestream, file_size)

            # The test file contains the following segments:
            self.assertEqual(AccountHolder.objects.count(), 3)
            self.assertEqual(J1.objects.count(), 2)
            self.assertEqual(J2.objects.count(), 1)

            account_1 = AccountHolder.objects.get(cons_acct_num='ACCTNUMBER1')
            account_2 = AccountHolder.objects.get(cons_acct_num='ACCTNUMBER2')
            account_3 = AccountHolder.objects.get(cons_acct_num='ACCTNUMBER3')

            # The test file first row contains multiple J1 segments
            self.assertEqual(account_1.cons_info_ind_assoc, ['1A', 'A'])
            self.assertEqual(account_1.ecoa_assoc, ['2','2'])

            # The test file second row contains no J1/J2 segments
            self.assertEqual(account_2.cons_info_ind_assoc, [])
            self.assertEqual(account_2.ecoa_assoc, [])

            # The test file third row contains J2 segment
            self.assertEqual(account_3.cons_info_ind_assoc, [])
            self.assertEqual(account_3.ecoa_assoc, ['2'])

    def test_report_file_outcome(self):
        file_size = os.path.getsize(self.tiny_file)

        with open(self.tiny_file, mode='r') as filestream:
            self.parser.parse_file_contents(filestream, file_size)
            file = self.parser.file_record
            self.assertEqual(file.parsing_status, "Finished")

    def test_parse_file_with_error(self):
        # error_file is identical to _tiny_file except that one line was modified
        # to make it unparseable
        file_size = os.path.getsize(self.error_file)
        with open(self.error_file, mode='r') as filestream:
            self.parser.parse_file_contents(filestream, file_size)

            # The test file contains the following segments:
            self.assertEqual(UnparseableData.objects.count(), 1)
            self.assertEqual(AccountHolder.objects.count(), 2)
            self.assertEqual(AccountActivity.objects.count(), 2)
            self.assertEqual(K1.objects.count(), 1)
            self.assertEqual(K2.objects.count(), 1)

    ############################
    # Tests for handling unparseable data in the body of the file
    def test_unparseable_data_in_line(self):
        line = "this is a bad line of data"
        result = self.parser.parse_line(line, self.activity_date)
        # result contains an instance of UnparseableData
        unparseable = result["UnparseableData"]
        self.assertEqual(unparseable.unparseable_line, line)
        self.assertIn("Segment too short", unparseable.error_description)

        # since the line was unparseable, no segments were added to result
        self.assertNotIn("j1", result)
        self.assertNotIn("j2", result)
        self.assertNotIn("k1", result)
        self.assertNotIn("k2", result)
        self.assertNotIn("k3", result)
        self.assertNotIn("k4", result)
        self.assertNotIn("l1", result)
        self.assertNotIn("n1", result)

    ############################
    # Tests for parsing extra segments
    def test_parsing_extra_segments(self):
        records = {"AccountActivity": self.account_activity}
        result = self.parser.parse_extra_segments(self.extras_str, records)
        self.assertNotIn("j1", result)
        self.assertNotIn("j2", result)
        self.assertEqual(result["k1"].orig_creditor_name, "ORIGNALCREDITORNAME")
        self.assertEqual(result["k2"].purch_sold_name, "SOLDTONAME")
        self.assertEqual(result["l1"].new_acc_num, "NEWACCTNUMBER")
        self.assertNotIn("k4", result)
        self.assertNotIn("n1", result)

    def test_no_extra_segments_exist(self):
        records = {"AccountActivity": self.account_activity}
        result = self.parser.parse_extra_segments("", records)
        self.assertEqual(result, records)

    def test_extra_segment_too_short(self):
        records = {"AccountActivity": self.account_activity}
        str = "K2 but is too short for a k2"
        with self.assertRaises(parse_utils.UnreadableLineException):
            self.parser.parse_extra_segments(str, records)

    def test_extra_segment_doesnt_match_any_type(self):
        records = {"AccountActivity": self.account_activity}
        str = "W2 is not a type of extra segment"
        with self.assertRaises(parse_utils.UnreadableLineException):
            self.parser.parse_extra_segments(str, records)

    def test_extra_whitespace_at_end(self):
        # Extra segment has extra whitespace at the end
        extra_space_str = "K1ORIGNALCREDITORNAME                                  "
        records = {"AccountActivity": self.account_activity}
        result = self.parser.parse_extra_segments(extra_space_str, records)
        self.assertNotIn("j1", result)
        self.assertNotIn("j2", result)
        self.assertEqual(result["k1"].orig_creditor_name, "ORIGNALCREDITORNAME")
        self.assertNotIn("k2", result)
        self.assertNotIn("l1", result)
        self.assertNotIn("k4", result)
        self.assertNotIn("n1", result)

    ############################
    # Tests for parsing the header
    def test_header_doesnt_match_format(self):
        bad_str = "this string is not a header segment"
        with self.assertRaises(parse_utils.UnreadableFileException):
            self.parser.get_activity_date_from_header(bad_str)

    def test_header_with_malformed_activity_date(self):
        # 99-99-2023 is not a valid date
        bad_str = "xxxxHEADERxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx99992023xxxxxxxxxxxx"
        with self.assertRaises(parse_utils.UnreadableFileException):
            self.parser.get_activity_date_from_header(bad_str)

    def test_header_too_short(self):
        bad_str = "xxxxHEADER with insufficient characters"
        with self.assertRaises(parse_utils.UnreadableFileException):
            self.parser.get_activity_date_from_header(bad_str)

    def test_get_activity_date_from_header(self):
        with open(self.header_seg, mode='r') as file:
            header_row = file.readline()
            activity_date = self.parser.get_activity_date_from_header(header_row)
            self.assertEqual(activity_date, datetime(2023, 12, 31, 0, 0))

    def test_parser_saves_header_as_unparseable(self):
        # First line of bad_header_file matches the header format, but doesn't
        # have a valid activity_date
        bad_header_file = os.path.join('parse_m2', 'tests','sample_files', 'm2_file_bad_header.txt')
        file_size = os.path.getsize(bad_header_file)

        with open(bad_header_file, mode='r') as filestream:
            self.parser.parse_file_contents(filestream, file_size)

            # The file record should show that the parsing failed
            file = self.parser.file_record
            self.assertEqual(file.parsing_status, "Not parsed")
            self.assertIn("activity_date couldn't be parsed", file.error_message)
            self.assertIn("HEADERWRONG", file.error_message)

            # Everything else should be empty
            self.assertEqual(UnparseableData.objects.count(), 0)
            self.assertEqual(AccountHolder.objects.count(), 0)
            self.assertEqual(AccountActivity.objects.count(), 0)
            self.assertEqual(K1.objects.count(), 0)
            self.assertEqual(K2.objects.count(), 0)
            self.assertEqual(L1.objects.count(), 0)
            self.assertEqual(J1.objects.count(), 0)
            self.assertEqual(J2.objects.count(), 0)
            self.assertEqual(K3.objects.count(), 0)
            self.assertEqual(K4.objects.count(), 0)
            self.assertEqual(N1.objects.count(), 0)
