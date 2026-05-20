import os

from django.test import TestCase

from parse_m2.initiate_parsing_local import parse_files_from_local_filesystem
from parse_m2.initiate_parsing_utils import parsed_file_exists
from parse_m2.models import AccountActivity, M2DataFile, Metro2Event


class InitiateLocalParsingTestCase(TestCase):
    def setUp(self):
        # this directory has two Metro2 files: m2_file_small and
        # m2_file_small_with_error and one file that doesn't end in .txt, so it won't
        # get parsed
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
        self.assertEqual(AccountActivity.objects.count(), 5)

    def test_file_with_bad_extension(self):
        parse_files_from_local_filesystem(self.event)
        bad_file = M2DataFile.objects.get(file_name__endswith="without_extension")
        self.assertIn("invalid file extension", bad_file.error_message)
        self.assertEqual("Not parsed", bad_file.parsing_status)

    def test_directory_does_not_exist(self):
        # If the user enters a bad directory, they get an error.
        # TODO: How can we message this issue to the user more clearly?
        exam_with_typo = Metro2Event.objects.create(
            name="x",
            directory="/directory/that/does/not/exist"
        )
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
        self.assertEqual(AccountActivity.objects.count(), 1997)

    def test_prepend_collection_onto_account_num(self):
        parse_files_from_local_filesystem(self.event, collection="HEALTH")

        # one M2DataFile object for each file
        self.assertEqual(M2DataFile.objects.count(), 3)
        # 3 records in the first file, 2 in the second
        self.assertEqual(
            AccountActivity.objects.filter(
                cons_acct_num__startswith="HEALTH."
            ).count(),
            5
        )

    def test_prepend_collection_on_zipfile(self):
        test_zip_location = os.path.join(
            'parse_m2', 'tests','sample_files', 'test_local_zipped')
        zip_event = Metro2Event.objects.create(
            name="zipped exam", directory=test_zip_location
        )
        parse_files_from_local_filesystem(zip_event, collection="ZIP_EVENT")
        # the zip contained 1 file
        self.assertEqual(M2DataFile.objects.count(), 1)
        # the file contained 1997 parseable records
        self.assertEqual(
            AccountActivity.objects.filter(
                cons_acct_num__startswith="ZIP_EVENT"
            ).count(),
            1997
        )


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
