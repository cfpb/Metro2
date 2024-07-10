from datetime import date
import os
from django.test import TestCase

from parse_m2.initiate_parsing_local import parse_files_from_local_filesystem
from parse_m2.initiate_post_parsing import post_parse, associate_previous_records

from parse_m2.models import AccountActivity, Metro2Event


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

    def test_associate_previous_records_no_previous_records(self):
        associate_previous_records(self.event)
        # Retrieve any record with activity_date 2018-01-31
        record = AccountActivity.objects.filter(activity_date='2018-01-31').first()

        # There are no record prior to Jan-2018
        self.assertEqual(None, record.previous_values)

    def test_associate_previous_records(self):
        associate_previous_records(self.event)

        # Retrieve any record with activity_date 2018-02-28
        feb_record = AccountActivity.objects.filter(activity_date='2018-02-28').first()
        prev_feb_record = AccountActivity.objects.get(cons_acct_num=feb_record.cons_acct_num, activity_date='2018-01-31')

        # Retrieve any record with activity_date 2018-03-31
        mar_record = AccountActivity.objects.filter(activity_date='2018-03-31').first()
        prev_mar_record = AccountActivity.objects.get(cons_acct_num=mar_record.cons_acct_num, activity_date='2018-02-28')

        self.assertEqual(prev_feb_record, feb_record.previous_values)
        self.assertEqual(prev_mar_record, mar_record.previous_values)