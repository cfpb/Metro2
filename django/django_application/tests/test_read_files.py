from django.conf import settings
from os import path
from django.test import TestCase
from django_application.file_utils import get_file_contents, get_json_file_contents


class TestReadFilesystemFiles(TestCase):
    file_path = path.join(settings.BASE_DIR, 'django_application', 'tests', 'sample_file.json')

    def test_read_plaintext_file(self):
        result = get_file_contents(self.file_path)
        self.assertEqual(result,
            '{"NAME":"myName","USER":"myUser","PASSWORD":"password123456","PORT":9876,"HOST":"myHost.sample.example.gov"}')

    def test_read_json_file(self):
        result = get_json_file_contents(self.file_path)
        keys = sorted(list(result.keys()))
        self.assertEqual(keys, ['HOST', 'NAME', 'PASSWORD', 'PORT', 'USER'])