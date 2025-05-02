from django.test import TestCase, override_settings

from parse_m2.normalize_format import update_S3_directory_files_format, get_filename

class TestFormatNormalization(TestCase):
    # Test for adjusting each line of a Metro2 file to correct format errors

    def test_get_filename(self):
        result = get_filename("Supervision/event_directory/my_filename.TXT")
        self.assertEqual(result, "my_filename.TXT")

@override_settings(S3_ENABLED=True)
class TestS3FormatNormalization(TestCase):
    # Test for creating modified versions of files by streaming them
    # from S3 and uploading new versions to a separate directory
    # Before running, make sure S3 env vars are in place (see settings/local.py)

    def test_directory_s3(self):
        test_dir = 'test-tiny'
        destination_dir = 'tmp-normalized-result'

        update_S3_directory_files_format(test_dir, destination_dir)
