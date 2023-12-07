import os
from django.test import TestCase
from unittest.mock import patch

from parse_m2.initiate_parsing import parse_files_from_local_filesystem
from parse_m2.models import M2DataFile, AccountHolder


class InitiateParsingTestCase(TestCase):
    def setUp(self):
        # this directory has two files: m2_file_small and m2_file_small_with_error
        self.test_local_data_directory = os.path.join(
            'parse_m2', 'tests','sample_files', 'test_local_data'
            )

    def test_open_local_files(self):
        exam_id = "examination A"
        parse_files_from_local_filesystem(exam_id, self.test_local_data_directory)
        # one M2DataFile object for each file that was opened
        self.assertEqual(M2DataFile.objects.count(), 2)
        # 3 records in the first file, 2 in the second
        self.assertEqual(AccountHolder.objects.count(), 5)
