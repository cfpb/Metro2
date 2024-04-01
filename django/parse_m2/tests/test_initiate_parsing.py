import os
from django.test import TestCase

from parse_m2.initiate_parsing_local import parse_files_from_local_filesystem
from parse_m2.initiate_parsing_s3 import parse_files_from_s3_bucket
from parse_m2.models import Metro2Event, M2DataFile, AccountHolder, UnparseableData


class InitiateLocalParsingTestCase(TestCase):
    def setUp(self):
        # this directory has two Metro2 files: m2_file_small and m2_file_small_with_error
        # and one file that doesn't end in .txt, so it won't get parsed
        self.test_local_data_directory = os.path.join(
            'parse_m2', 'tests','sample_files', 'test_local_data'
            )

    def test_open_local_files(self):
        parse_files_from_local_filesystem("exam Z", self.test_local_data_directory)

        # Should create one event
        self.assertEqual(Metro2Event.objects.count(), 1)
        event = Metro2Event.objects.first()
        self.assertEqual(event.name, "exam Z")

        # one M2DataFile object for each file
        self.assertEqual(M2DataFile.objects.count(), 3)
        # 3 records in the first file, 2 in the second
        self.assertEqual(AccountHolder.objects.count(), 5)

    def test_directory_does_not_exist(self):
        # Since this would only happen in the event of programmer error, it's fine that
        # this exception is uncaught.
        with self.assertRaises(FileNotFoundError):
            parse_files_from_local_filesystem("exam A", "/directory/that/does/not/exist")

    def test_open_zipfiles(self):
        test_zip_location = os.path.join(
            'parse_m2', 'tests','sample_files', 'test_local_zipped')
        parse_files_from_local_filesystem("exam ZIP", test_zip_location)
        # the zip contained 1 file
        self.assertEqual(M2DataFile.objects.count(), 1)
        # the file contained 1997 parseable records
        self.assertEqual(AccountHolder.objects.count(), 1997)


class InitiateS3ParsingTestCase(TestCase):
    # Test for parsing files from the S3 bucket. Only run when testing manually.
    # Before running, make sure S3 env vars are in place.
    def xtest_fetch_s3(self):
        parse_files_from_s3_bucket("exam B", "test-tiny")

        # Should create one event
        self.assertEqual(Metro2Event.objects.count(), 1)
        event = Metro2Event.objects.first()
        self.assertEqual(event.name, "exam B")

        # The test directory in S3 should contain one file
        self.assertEqual(M2DataFile.objects.count(), 1)
        file = M2DataFile.objects.first()
        self.assertEqual(file.file_name, "s3:test-tiny/m2_2k_lines_deidentified.TXT")

        # The test file should contain 1998 base segments
        self.assertEqual(AccountHolder.objects.count(), 1998)

    def xtest_fetch_s3_zip(self):
        parse_files_from_s3_bucket("exam B", "test-zipped/")

        # Should create one event
        self.assertEqual(Metro2Event.objects.count(), 1)
        event = Metro2Event.objects.first()
        self.assertEqual(event.name, "exam B")

        # The test directory in S3 should contain one file
        self.assertEqual(M2DataFile.objects.count(), 1)
        file = M2DataFile.objects.first()
        expected_name = "s3:test-zipped/one_small_file.zip:m2_2k_lines_deidentified.TXT"
        self.assertEqual(file.file_name, expected_name)

        # The test file should contain 1997 valid base segments and one unparseable
        self.assertEqual(AccountHolder.objects.count(), 1997)
        self.assertEqual(UnparseableData.objects.count(), 1)
