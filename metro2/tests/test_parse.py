from unittest import TestCase
from unittest.mock import patch
from metro2.parse import parser

class TestParse(TestCase):
    @classmethod
    def set_up_class(cls):
        cls.valid_xlsx = "metro2/tests/test.xlsx"
        cls.valid_sheet = "test"
        cls.valid_sheet_with_data = "test2"
        cls.valid_colsegment = "A"
        cls.valid_colstart = "B"
        cls.valid_colend = "C"
        cls.valid_colfield = "D"
        cls.num_segments = 2
        cls.num_fields = 5
        cls.segment = "header"
        cls.problem = "There was a problem establishing the connection"

    # map fields should raise an excption if incorrect values are provided
    def test_map_fields_raises_exception_invalid_filename(self):
        self.assertRaises(
            FileNotFoundError,
            parser.map_fields,
            "fail.xlsx", "fail", "fail", "fail", "fail", "fail", "fail"
        )

    def test_map_fields_raises_exception_invalid_sheetname(self):
        self.assertRaises(
            KeyError,
            parser.map_fields,
            self.valid_xlsx, "fail", "fail", "fail", "fail", "fail", "fail"
        )

    def test_map_fields_raises_exception_invalid_column_name(self):
        self.assertRaises(
            ValueError,
            parser.map_fields,
            self.valid_xlsx, self.valid_sheet, "fail", "fail", "fail", "fail", "fail"
        )

    def test_map_fields_sets_values_on_empty_sheet(self):
        parser.mapping = dict()
        parser.map_fields(self.valid_xlsx, self.valid_sheet, self.valid_colsegment, self.valid_colstart, self.valid_colend, self.valid_colfield, None)
        self.assertEqual(0, len(parser.mapping))

    def test_map_fields_pass_with_valid_data(self):
        parser.mapping = dict()
        parser.map_fields(self.valid_xlsx, self.valid_sheet_with_data, self.valid_colsegment, self.valid_colstart, self.valid_colend, self.valid_colfield, None)
        self.assertEqual(self.num_segments, len(parser.mapping))
        self.assertEqual(self.num_fields, len(parser.mapping[self.segment]))

    # test that peek does not advance file pointer, and returns correct character
    def test_peek(self):
        valid_char = 't'
        seek_pos = 7
        file_to_read = "metro2/tests/test.txt"

        # open file and seek to byte 7
        fstream = open(file_to_read, 'r')
        fstream.seek(seek_pos)
        # peek byte 8
        peeked_char = parser.peek(fstream, 1)

        self.assertEqual(seek_pos, fstream.tell())
        fstream.close()

        self.assertEqual(valid_char, peeked_char)

    # test parsing a chunk of a file
    def test_parse_chunk_raises_exception_with_bad_filename(self):
        file_length = 10
        with self.assertRaises(SystemExit) as cm:
            parser.parse_chunk(0, file_length, "fail.json")

        self.assertEqual(cm.exception.code, 1)

    def test_parse_chunk_with_invalid_line(self):
        parser.mapping = dict()
        file_length = 45
        num_segments = 4
        file_to_read = "metro2/tests/test.txt"
        parser.mapping["header"] = [(1, 10)]
        parser.mapping["base"] = [(1, 5)]
        parser.mapping["J1"] = [(1, 2)]
        parser.mapping["trailer"] = [(1, 11)]
        parser.seg_length["header"] = 10
        parser.seg_length["base"] = 5
        parser.seg_length["J1"] = 2
        parser.seg_length["trailer"] = 11

        res = parser.parse_chunk(0, file_length, file_to_read)
        self.assertEqual(num_segments, len(res))

    # test files are broken down into chunks
    def test_construct_commands_raises_exception_with_bad_filename(self):
        self.assertRaises(FileNotFoundError, parser.construct_commands, "fail.txt")

    def test_construct_commands_adds_commands(self):
        parser.mapping = dict()
        file_to_read = "metro2/tests/test.txt"
        parser.mapping["header"] = [(1, 10)]
        parser.mapping["base"] = [(1, 5)]
        parser.mapping["J1"] = [(1, 2)]
        parser.mapping["trailer"] = [(1, 11)]
        parser.seg_length["header"] = 10
        parser.seg_length["base"] = 5
        parser.seg_length["J1"] = 2
        parser.seg_length["trailer"] = 11

        parser.construct_commands(file_to_read)
        self.assertEqual(1, len(parser.header_values))
        self.assertEqual(1, len(parser.base_values))
        self.assertEqual(1, len(parser.J1_values))
        self.assertEqual(1, len(parser.trailer_values))
