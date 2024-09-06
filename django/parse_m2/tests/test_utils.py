from django.test import TestCase
from datetime import datetime

from parse_m2 import parse_utils


class ParserUtilsTestCase(TestCase):
    # Tests for cast_to_type
    # ========================
    def test_cast_field_to_value_for_int_type(self):
        result = parse_utils.cast_to_type("123", "numeric")
        self.assertEqual(result, 123)

        result = parse_utils.cast_to_type("0000000000", "numeric")
        self.assertEqual(result, 0)

        result = parse_utils.cast_to_type("0000000123", "numeric")
        self.assertEqual(result, 123)

        result = parse_utils.cast_to_type("-00000023", "numeric")
        self.assertEqual(result, -23)

        with self.assertRaises(parse_utils.UnreadableLineException):
            parse_utils.cast_to_type("", "numeric")

        with self.assertRaises(parse_utils.UnreadableLineException):
            parse_utils.cast_to_type("123.45", "numeric")

        with self.assertRaises(parse_utils.UnreadableLineException):
            parse_utils.cast_to_type("$1234", "numeric")

    def test_cast_field_to_value_for_optional_int_type(self):
        result = parse_utils.cast_to_type("123", "numeric optional")
        self.assertEqual(result, 123)

        result = parse_utils.cast_to_type("0000000000", "numeric optional")
        self.assertEqual(result, 0)

        result = parse_utils.cast_to_type("0000000123", "numeric optional")
        self.assertEqual(result, 123)

        result = parse_utils.cast_to_type("-00000023", "numeric optional")
        self.assertEqual(result, -23)

        result = parse_utils.cast_to_type("", "numeric optional")
        self.assertEqual(result, None)

        result = parse_utils.cast_to_type("123.45", "numeric optional")
        self.assertEqual(result, None)

        result = parse_utils.cast_to_type("$1234", "numeric optional")
        self.assertEqual(result, None)

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

    # Tests for get_field_value
    # ========================
    def test_get_field_value_gives_informative_error_msg(self):
        with self.assertRaises(parse_utils.UnreadableLineException)as e:
            parse_utils.get_field_value({"account_plan": (1,30)}, "account_plan", "string")
        self.assertIn("segment length is 6", str(e.exception))

        with self.assertRaises(parse_utils.UnreadableLineException)as e1:
            parse_utils.get_field_value({"test_date": (1,8, "date")}, "test_date", "33334444")
        self.assertIn("Indices: 1-8", str(e1.exception))

        with self.assertRaises(parse_utils.UnreadableLineException)as e2:
            parse_utils.get_field_value({"age": (1,3, "numeric")}, "age", "XYZ")
        self.assertIn("Field name: `age`", str(e2.exception))

    def test_get_field_value_gets_correct_string(self):
        str = "test1234"
        result = parse_utils.get_field_value({"x": (1,4)}, "x", str)
        self.assertEqual(result, "test")

        result = parse_utils.get_field_value({"x": (4,7)}, "x", str)
        self.assertEqual(result, "t123")

        result = parse_utils.get_field_value({"x": (1,1)}, "x", str)
        self.assertEqual(result, "t")

    def test_get_field_value_casts_to_types(self):
        str = "    test1234"
        result = parse_utils.get_field_value({"x": (1,8, "string")}, "x", str)
        self.assertEqual(result, "test")

        result = parse_utils.get_field_value({"x": (11,12, "numeric")}, "x", str)
        self.assertEqual(result, 34)

        str = "test03111901"
        result = parse_utils.get_field_value({"x": (5,12, "date")}, "x", str)
        self.assertEqual(result, datetime(1901, 3, 11))

    # Tests for decode_if_needed
    # ========================
    def test_decode_str(self):
        s = "hello"
        result = parse_utils.decode_if_needed(s)
        self.assertEqual(s, result)

    def test_decode_bytes(self):
        b = b'howdy'
        result = parse_utils.decode_if_needed(b)
        self.assertEqual("howdy", result)

    def test_decode_other(self):
        with self.assertRaises(parse_utils.UnreadableLineException):
            x = 123
            parse_utils.decode_if_needed(x)