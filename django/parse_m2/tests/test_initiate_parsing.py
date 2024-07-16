import os
from django.test import TestCase

from parse_m2.initiate_parsing_local import parse_files_from_local_filesystem
from parse_m2.initiate_parsing_s3 import parse_files_from_s3_bucket
from parse_m2.initiate_parsing_utils import parsed_file_exists
from parse_m2.models import Metro2Event, M2DataFile, AccountHolder, UnparseableData


class InitiateLocalParsingTestCase(TestCase):
    def setUp(self):
        # this directory has two Metro2 files: m2_file_small and m2_file_small_with_error
        # and one file that doesn't end in .txt, so it won't get parsed
        self.test_local_data_directory = os.path.join(
            'parse_m2', 'tests','sample_files', 'test_local_data'
            )

        self.event = Metro2Event.objects.create(
            name="exam Z", directory=self.test_local_data_directory
        )

    def test_open_local_files(self):
        parse_files_from_local_filesystem(self.event)

        # one M2DataFile object for each file
        self.assertEqual(M2DataFile.objects.count(), 3)
        # 3 records in the first file, 2 in the second
        self.assertEqual(AccountHolder.objects.count(), 5)

    def test_file_with_bad_extension(self):
        parse_files_from_local_filesystem(self.event)
        bad_file = M2DataFile.objects.get(file_name__endswith="without_extension")
        self.assertIn("invalid file extension", bad_file.error_message)
        self.assertEqual("Not parsed", bad_file.parsing_status)

    def test_directory_does_not_exist(self):
        # If the user enters a bad directory, they get an error.
        # TODO: How can we message this issue to the user more clearly?
        exam_with_typo = Metro2Event.objects.create(name="x", directory="/directory/that/does/not/exist")
        with self.assertRaises(FileNotFoundError):
            parse_files_from_local_filesystem(exam_with_typo)

    def test_open_zipfiles(self):
        test_zip_location = os.path.join(
            'parse_m2', 'tests','sample_files', 'test_local_zipped')
        zip_event = Metro2Event.objects.create(
            name="zipped exam", directory=test_zip_location
        )
        parse_files_from_local_filesystem(zip_event)
        # the zip contained 1 file
        self.assertEqual(M2DataFile.objects.count(), 1)
        # the file contained 1997 parseable records
        self.assertEqual(AccountHolder.objects.count(), 1997)


from unittest.mock import patch

class InitiateS3ParsingTestCase(TestCase):
    # Test for parsing files from the S3 bucket. Only run when testing manually.
    # Before running, make sure S3 env vars are in place.

    def xtest_fetch_s3(self):
        with patch.dict('os.environ', {'AWS_PROFILE': 'prof'}):
            exam_s3 = Metro2Event.objects.create(name="s3 exam", directory="test-tiny/")
            parse_files_from_s3_bucket(exam_s3)

            # The test directory in S3 should contain one file
            self.assertEqual(M2DataFile.objects.count(), 1)
            file = M2DataFile.objects.first()
            self.assertEqual(file.file_name, "s3:test-tiny/m2_2k_lines_deidentified.TXT")

            # The test file should contain 1998 base segments
            self.assertEqual(AccountHolder.objects.count(), 1998)

    def xtest_fetch_s3_zip(self):
        with patch.dict('os.environ', {'AWS_PROFILE': 'prof'}):
            exam_s3 = Metro2Event.objects.create(name="other s3 exam", directory="test-zipped/")
            parse_files_from_s3_bucket(exam_s3)

            # The test directory in S3 should contain one file
            self.assertEqual(M2DataFile.objects.count(), 1)
            file = M2DataFile.objects.first()
            expected_name = "s3:test-zipped/one_small_file.zip:m2_2k_lines_deidentified.TXT"
            self.assertEqual(file.file_name, expected_name)

            # The test file should contain 1997 valid base segments and one unparseable
            self.assertEqual(AccountHolder.objects.count(), 1997)
            self.assertEqual(UnparseableData.objects.count(), 1)

class InitiateParsingUtilsTestCase(TestCase):
    def setUp(self) -> None:
        self.event = Metro2Event.objects.create(name="util-test")
        self.filename1 = "s3://files/event-files/my-data.txt"
        M2DataFile.objects.create(event=self.event, file_name=self.filename1)

    def test_file_exists(self):
        self.assertTrue(parsed_file_exists(self.event, self.filename1))
        self.assertFalse(parsed_file_exists(self.event, "s3://files/event-files/my-data.txt2"))
        other_event = Metro2Event.objects.create(name="red herring")
        self.assertFalse(parsed_file_exists(other_event, self.filename1))