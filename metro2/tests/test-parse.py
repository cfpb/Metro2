from unittest import mock, TestCase
from unittest.mock import patch
import os

from io import StringIO
from metro2.parse import parser

class ParseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid_xlsx = "metro2/tests/test.xlsx"
        cls.valid_sheet = "test"
        cls.valid_sheet_with_data = "test2"
        cls.valid_colsegment = "A"
        cls.valid_colstart = "B"
        cls.valid_colend = "C"
        cls.num_segments = 2
        cls.num_fields = 5
        cls.segment = "header"
        cls.problem = "There was a problem establishing the connection"

    # map fields should raise an excption if incorrect values are provided
    def testMapFieldsRaisesExceptionInvalidFilename(self):
        self.assertRaises(
            FileNotFoundError,
            parser.map_fields,
            "fail.xlsx", "fail", "fail", "fail", "fail"
        )

    def testMapFieldsRaisesExceptionInvalidSheetname(self):
        self.assertRaises(
            KeyError,
            parser.map_fields,
            self.valid_xlsx, "fail", "fail", "fail", "fail"
        )

    def testMapFieldsRaisesExceptionInvalidColumnName(self):
        self.assertRaises(
            ValueError,
            parser.map_fields,
            self.valid_xlsx, self.valid_sheet, "fail", "fail", "fail"
        )

    def testMapFieldsSetsValuesOnEmptySheet(self):
        parser.mapping = dict()
        parser.map_fields(self.valid_xlsx, self.valid_sheet, self.valid_colsegment, self.valid_colstart, self.valid_colend)
        self.assertEqual(0, len(parser.mapping))

    def testMapFieldsPassWithValidData(self):
        parser.mapping = dict()
        parser.map_fields(self.valid_xlsx, self.valid_sheet_with_data, self.valid_colsegment, self.valid_colstart, self.valid_colend)
        self.assertEqual(self.num_segments, len(parser.mapping))
        self.assertEqual(self.num_fields, len(parser.mapping[self.segment]))

    # test that peek does not advance file pointer, and returns correct character
    def testPeek(self):
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
    def testParseChunkRaisesExceptionWithBadFilename(self):
        file_length = 10
        self.assertRaises(
            FileNotFoundError,
            parser.parse_chunk,
            0, file_length, "fail"
        )

    def testParseChunkWithInvalidLine(self):
        parser.mapping = dict()
        file_length = 45
        num_segments = 4
        file_to_read = "metro2/tests/test.txt"
        parser.mapping["header"] = [(1, 10)]
        parser.mapping["base"] = [(1, 5)]
        parser.mapping["J1"] = [(1, 2)]
        parser.mapping["trailer"] = [(1, 11)]

        res = parser.parse_chunk(0, file_length, file_to_read)
        self.assertEqual(num_segments, len(res))

    # test files are broken down into chunks
    def testConstructCommandsRaisesExceptionWithBadFilename(self):
        self.assertRaises(FileNotFoundError, parser.construct_commands, "fail")

    def testConstructCommandsAddsCommands(self):
        parser.mapping = dict()
        file_to_read = "metro2/tests/test.txt"
        parser.mapping["header"] = [(1, 10)]
        parser.mapping["base"] = [(1, 5)]
        parser.mapping["J1"] = [(1, 2)]
        parser.mapping["trailer"] = [(1, 11)]

        parser.construct_commands(file_to_read)
        self.assertEqual(1, len(parser.header_values))
        self.assertEqual(1, len(parser.base_values))
        self.assertEqual(1, len(parser.J1_values))
        self.assertEqual(1, len(parser.trailer_values))

    # Test that exec_commands is called
    @mock.patch('psycopg2.connect', return_value=None)
    def testExecCommandsFailsOnBadConnection(self, _):
        with patch('sys.stdout', new = StringIO()) as mock:
            parser.exec_commands(None)
            self.assertIn(self.problem, mock.getvalue())

    # test that if any one of the environment variables are wront, connection
    # will fail.
    @mock.patch.dict(os.environ, {"PGHOST": "fail"}, clear=True)
    def testExecCommandsFailsOnPGHOST(self):
        with patch('sys.stdout', new = StringIO()) as mock:
            parser.exec_commands(None)
            self.assertIn(self.problem, mock.getvalue())

    @mock.patch.dict(os.environ, {"PGPORT": "fail"}, clear=True)
    def testExecCommandsFailsOnPGPORT(self):
        with patch('sys.stdout', new = StringIO()) as mock:
            parser.exec_commands(None)
            self.assertIn(self.problem, mock.getvalue())

    @mock.patch.dict(os.environ, {"PGDATABASE": "fail"}, clear=True)
    def testExecCommandsFailsOnPGDATABASE(self):
        with patch('sys.stdout', new = StringIO()) as mock:
            parser.exec_commands(None)
            self.assertIn(self.problem, mock.getvalue())

    @mock.patch.dict(os.environ, {"PGUSER": "fail"}, clear=True)
    def testExecCommandsFailsOnPGUSER(self):
        with patch('sys.stdout', new = StringIO()) as mock:
            parser.exec_commands(None)
            self.assertIn(self.problem, mock.getvalue())

    @mock.patch.dict(os.environ, {"PGPASSWORD": "fail"}, clear=True)
    def testExecCommandsFailsOnPGPASSWORD(self):
        with patch('sys.stdout', new = StringIO()) as mock:
            parser.exec_commands(None)
            self.assertIn(self.problem, mock.getvalue())
