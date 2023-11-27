from django.test import TestCase
from datetime import datetime

from parse_m2 import parse_utils


class ParserUtilsTestCase(TestCase):
    def test_get_field_value_errors_when_field_nonexistent(self):
        with self.assertRaises(parse_utils.UnreadableLineException):
            parse_utils.get_field_value((1,30), "string")

    def test_cast_field_to_value_for_int_type(self):
        result = parse_utils.cast_to_type("123", "numeric")
        self.assertEqual(result, 123)

        result = parse_utils.cast_to_type("0000000000", "numeric")
        self.assertEqual(result, 0)

        result = parse_utils.cast_to_type("0000000123", "numeric")
        self.assertEqual(result, 123)

        with self.assertRaises(parse_utils.UnreadableLineException):
            parse_utils.cast_to_type("", "numeric")

        with self.assertRaises(parse_utils.UnreadableLineException):
            parse_utils.cast_to_type("123.45", "numeric")

    def test_cast_field_to_value_for_required_date_type(self):
        result = parse_utils.cast_to_type("12312011", "date")
        self.assertEqual(result, datetime(2011, 12, 31))

        result = parse_utils.cast_to_type("10252020", "date")
        self.assertEqual(result, datetime(2020, 10, 25))

        with self.assertRaises(parse_utils.UnreadableLineException):
            parse_utils.cast_to_type("00000000", "date")

        with self.assertRaises(parse_utils.UnreadableLineException):
            # error when input string is too short
            parse_utils.cast_to_type("1301202", "date")

    def test_cast_field_to_value_for_optional_date_type(self):
        result = parse_utils.cast_to_type("12312011", "date optional")
        self.assertEqual(result, datetime(2011, 12, 31))

        result = parse_utils.cast_to_type("10252020", "date optional")
        self.assertEqual(result, datetime(2020, 10, 25))

        result = parse_utils.cast_to_type("00000000", "date optional")
        self.assertEqual(result, None)

        with self.assertRaises(parse_utils.UnreadableLineException):
            # error when input string is too short
            parse_utils.cast_to_type("1301202", "date")

    def test_cast_field_to_value_string_type(self):
        result = parse_utils.cast_to_type("here's a string", "string")
        self.assertEqual(result, "here's a string")

        result = parse_utils.cast_to_type("padded string      ", "string")
        self.assertEqual(result, "padded string")

        result = parse_utils.cast_to_type("   left-padded", "string")
        self.assertEqual(result, "left-padded")

        result = parse_utils.cast_to_type("     ", "string")
        self.assertEqual(result, "")

        result = parse_utils.cast_to_type("", "string")
        self.assertEqual(result, "")

    def test_get_field_value_gets_correct_string(self):
        str = "test1234"
        result = parse_utils.get_field_value((1,4), str)
        self.assertEqual(result, "test")

        result = parse_utils.get_field_value((4,7), str)
        self.assertEqual(result, "t123")

        result = parse_utils.get_field_value((1,1), str)
        self.assertEqual(result, "t")

    def test_get_field_value_casts_to_types(self):
        str = "    test1234"
        result = parse_utils.get_field_value((1,8, "string"), str)
        self.assertEqual(result, "test")

        result = parse_utils.get_field_value((11,12, "numeric"), str)
        self.assertEqual(result, 34)

        str = "test03111901"
        result = parse_utils.get_field_value((5,12, "date"), str)
        self.assertEqual(result, datetime(1901, 3, 11))
