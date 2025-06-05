import os
import io

from django.test import TestCase

from parse_m2.normalize_format import (
    get_filename,
    modify_individual_line,
    normalize_file_format
)


class TestFormatNormalization(TestCase):
    # Test for adjusting each line of a Metro2 file to correct format errors

    def test_get_filename(self):
        result = get_filename("Supervision/event_directory/my_filename.TXT")
        self.assertEqual(result, "my_filename.TXT")

    def test_modify_single_line(self):
        str = "123456789"
        result = modify_individual_line(str)
        self.assertEqual(result, "....123456789")

    def test_normalize_file_format(self):
        sample_files_dir = os.path.join('parse_m2', 'tests','sample_files',)
        input_file = os.path.join(sample_files_dir, 'm2_file_small.txt')

        expected_output = os.path.join(sample_files_dir, 'test_normalize_format',
                                   'small_after_normalization.txt')

        with open(input_file, 'r') as input:
            with open(expected_output, 'r') as expected:
                with io.StringIO() as output:
                    normalize_file_format(input, output)
                    output.seek(0)
                    self.assertEqual(output.read(), expected.read())
