import os
from datetime import date

from django.test import TestCase

from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.initiate_parsing_local import parse_files_from_local_filesystem
from parse_m2.initiate_post_parsing import (
    _associate_prior_records_single_datafile,
    associate_previous_records,
    post_parse,
    report_on_prior_record_outcome,
)
from parse_m2.models import AccountActivity, M2DataFile, Metro2Event


class InitiatePostParsingTestCase(TestCase):
    def setUp(self):
        # this directory has three Metro2 files: jan-2018, feb-2018 and mar-2018
        self.test_local_data_directory = os.path.join(
            'parse_m2', 'tests','sample_files', 'test_previous_records'
            )

        self.event = Metro2Event.objects.create(
            name="exam Z", directory=self.test_local_data_directory
        )
        parse_files_from_local_filesystem(self.event)

    def test_post_parse_date_range(self):
        post_parse(self.event)

        # Event date range should be set
        self.assertEqual(date(2018, 3, 31), self.event.date_range_end)
        self.assertEqual(date(2018, 1, 31), self.event.date_range_start)

    def test_post_parse_total_tradelines(self):
        # total_tradelines defaults to zero
        self.assertEqual(self.event.total_tradelines, 0)

        post_parse(self.event)
        # post_parse updates total_tradelines value
        self.assertEqual(self.event.total_tradelines, 6)

    def test_associate_previous_records_no_previous_records(self):
        associate_previous_records(self.event)
        # Retrieve any record with activity_date 2018-01-31
        record = AccountActivity.objects.filter(activity_date='2018-01-31').first()

        # There are no record prior to Jan-2018
        self.assertEqual(None, record.previous_values)

    def test_associate_previous_records_lag_method(self):
        # For a small event, 'lag' and 'chunk' methods are identical
        associate_previous_records(self.event, strategy='lag')

        # Retrieve any record with activity_date 2018-02-28
        feb_record = AccountActivity.objects.filter(activity_date='2018-02-28').first()
        prev_feb_record = AccountActivity.objects.get(
            cons_acct_num=feb_record.cons_acct_num,
            activity_date='2018-01-31'
        )

        # Retrieve any record with activity_date 2018-03-31
        mar_record = AccountActivity.objects.filter(activity_date='2018-03-31').first()
        prev_mar_record = AccountActivity.objects.get(
            cons_acct_num=mar_record.cons_acct_num, activity_date='2018-02-28'
        )

        self.assertEqual(prev_feb_record, feb_record.previous_values)
        self.assertEqual(prev_mar_record, mar_record.previous_values)

    def test_associate_previous_records_chunk_method(self):
        # For a small event, 'lag' and 'chunk' methods are identical
        associate_previous_records(self.event, strategy='chunk')

        # Retrieve any record with activity_date 2018-02-28
        feb_record = AccountActivity.objects.filter(activity_date='2018-02-28').first()
        prev_feb_record = AccountActivity.objects.get(
            cons_acct_num=feb_record.cons_acct_num,
            activity_date='2018-01-31'
        )

        # Retrieve any record with activity_date 2018-03-31
        mar_record = AccountActivity.objects.filter(activity_date='2018-03-31').first()
        prev_mar_record = AccountActivity.objects.get(
            cons_acct_num=mar_record.cons_acct_num, activity_date='2018-02-28'
        )

        self.assertEqual(prev_feb_record, feb_record.previous_values)
        self.assertEqual(prev_mar_record, mar_record.previous_values)

    def test_report_prior_record_outcome(self):
        associate_previous_records(self.event)
        # event.prior_records_associated defaults to 0, then is updated
        self.assertEqual(self.event.prior_records_associated, 0)
        report_on_prior_record_outcome(self.event)
        self.assertEqual(self.event.prior_records_associated, 4)


class AssociatePriorRecordsByFileOrderTestCase(TestCase):
    def setUp(self):
        self.event = Metro2Event.objects.create(name="event")
        self.file1 = M2DataFile.objects.create(
            event = self.event, file_name="f1", activity_date=date(2022, 1, 1))
        self.file2 = M2DataFile.objects.create(
            event = self.event, file_name="f2", activity_date=date(2022, 2, 1),
            previous_file=self.file1)
        self.file3 = M2DataFile.objects.create(
            event = self.event, file_name="f3", activity_date=date(2022, 3, 1),
            previous_file=self.file2)

        self.a11 = acct_record(self.file1, {'id': 11, 'cons_acct_num': 'A'})
        self.a12 = acct_record(self.file1, {'id': 12, 'cons_acct_num': 'B'})
        self.a13 = acct_record(self.file1, {'id': 13, 'cons_acct_num': 'C'})

        self.a21 = acct_record(self.file2, {'id': 21, 'cons_acct_num': 'A'})
        self.a22 = acct_record(self.file2, {'id': 22, 'cons_acct_num': 'B'})

        self.a31 = acct_record(self.file3, {'id': 31, 'cons_acct_num': 'A'})
        self.a32 = acct_record(self.file3, {'id': 32, 'cons_acct_num': 'B'})
        self.a33 = acct_record(self.file3, {'id': 33, 'cons_acct_num': 'C'})

        return super().setUp()

    def test_associate_records_by_file(self):
        _associate_prior_records_single_datafile(self.file2, self.file1)
        self.a21.refresh_from_db()
        self.a22.refresh_from_db()
        self.assertEqual(self.a21.previous_values, self.a11)
        self.assertEqual(self.a22.previous_values, self.a12)

    def test_associate_records_by_file_2(self):
        _associate_prior_records_single_datafile(self.file3, self.file2)
        self.a31.refresh_from_db()
        self.a32.refresh_from_db()
        self.a33.refresh_from_db()
        self.assertEqual(self.a31.previous_values, self.a21)
        self.assertEqual(self.a32.previous_values, self.a22)
        self.assertEqual(self.a33.previous_values, None)

    def test_file_strategy_for_prior_records_full_event(self):
        associate_previous_records(self.event, strategy= 'file')
        records = [self.a11, self.a12, self.a13, self.a21, self.a22,
                   self.a31, self.a32, self.a33]
        [r.refresh_from_db() for r in records]
        self.assertEqual(self.a11.previous_values, None)
        self.assertEqual(self.a12.previous_values, None)
        self.assertEqual(self.a13.previous_values, None)
        self.assertEqual(self.a21.previous_values, self.a11)
        self.assertEqual(self.a22.previous_values, self.a12)
        self.assertEqual(self.a31.previous_values, self.a21)
        self.assertEqual(self.a32.previous_values, self.a22)
        self.assertEqual(self.a33.previous_values, None)