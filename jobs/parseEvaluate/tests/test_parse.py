import tempfile
import os

from unittest import TestCase
from unittest.mock import patch
from parse import parser
from tests.fixtures import Pool, Connect

class TestParse(TestCase):
    def setUp(self):
        self.temp = tempfile.NamedTemporaryFile(mode='w+')

    def tearDown(self):
        self.temp.close()

    def test_peek(self):
        # writes 'test' to a temp file, then uses peek to get the first
        # two characters, and makes sure the position in the file has
        # not advanced.
        self.temp.write('test')
        self.temp.seek(0)
        expected_pos = self.temp.tell()
        expected_res = 'te'
        actual_res = parser.peek(self.temp, 2)
        self.assertEqual(expected_pos, self.temp.tell())
        self.assertEqual(expected_res, actual_res)

    def test_determine_segment(self):
        # For this test, all characters that don't matter for
        # determine_segment are filled in with x.
        with tempfile.TemporaryFile(mode='w+') as t1:
            t1.write('xxxxHEADERxxxxxxx')
            t1.seek(0)  # return the filestream position to the start of the string
            self.assertEqual(parser.determine_segment(t1), 'header')

        with tempfile.TemporaryFile(mode='w+') as t2:
            t2.write('xxxxTRAILERxxxxx')
            t2.seek(0)
            self.assertEqual(parser.determine_segment(t2), 'trailer')

        with tempfile.TemporaryFile(mode='w+') as t3:
            t3.write('J1xxxxxxxxxxxx')
            t3.seek(0)
            # For extra segments, return the segment name in lower case
            self.assertEqual(parser.determine_segment(t3), 'j1')

        with tempfile.TemporaryFile(mode='w+') as t4:
            t4.write('N3xxxxxxxxxxxx')
            t4.seek(0)
            # N3 looks like an extra segment name but it isn't valid. Return None.
            self.assertEqual(parser.determine_segment(t4), None)

        with tempfile.TemporaryFile(mode='w+') as t5:
            # When the first five characters are all digits, it's a base segment
            t5.write('87766xxxxxxxxx')
            t5.seek(0)
            self.assertEqual(parser.determine_segment(t5), 'base')

        with tempfile.TemporaryFile(mode='w+') as t6:
            # When none of the patterns match, it's unparseable; return none.
            t6.write('NNxxxxxxxxxxxx')
            t6.seek(0)
            self.assertEqual(parser.determine_segment(t6), None)

    def test_parse_chunk(self):
        self.temp.write('00000'.ljust(426, '0'))
        self.temp.write('\nJ1'.ljust(101, '0'))
        self.temp.write('\n0000HEADER'.ljust(427, '0'))
        self.temp.write('\n0000TRAILER'.ljust(427, '0'))
        self.temp.seek(0)

        # four value lists should be created. The base value list should
        # contain 51 fields. The J1 value list should contain 15 fields.
        # The header value list should contain 21 fields. The trailer value
        # list should contain 50 fields.
        expected_elements = 4
        expected_base_fields = 51
        expected_J1_fields = 15
        expected_header_fields = 21
        expected_trailer_fields = 50

        # result will be a list of value lists
        result = parser.parse_chunk(0, os.path.getsize(self.temp.name), self.temp)

        self.assertEqual(len(result), expected_elements)
        self.assertEqual(len(result[0]), expected_base_fields)
        self.assertEqual(len(result[1]), expected_J1_fields)
        self.assertEqual(len(result[2]), expected_header_fields)
        self.assertEqual(len(result[3]), expected_trailer_fields)

    def test_parse_chunk_unreadable(self):
        # unreadable line
        self.temp.write('test')
        self.temp.seek(0)

        with patch('parse.logging.warn') as mock:
            parser.parse_chunk(0, os.path.getsize(self.temp.name), self.temp)
            mock.assert_called_with('unread data: ', 'test')

    @patch('parse.mp.Pool')
    @patch.object(parser, 'parse_chunk')
    def test_construct_commands(self, mock_parse_chunk, mock_pool):
        mock_pool.return_value = Pool()
        # write something to the file so we're not trying to read an empty file
        self.temp.write('\n')
        self.temp.seek(0)
        
        # expected value is what we should see from parser.header_values
        expected = tuple(('success',))

        # make sure each segment's values contain the expected value
        return_val = list([['success', 'header']])
        mock_parse_chunk.return_value = return_val
        parser.construct_commands(self.temp)
        # parsed_values is a dict where each entry is a list of values for
        # the corresponding segment. Therefore, when we access
        # parsed_values["segment"][0], we are accessing the first element
        # of the values list for that segment. We expect that to be
        # a tuple of just the string 'success'.
        self.assertEqual(parser.parsed_values["header"][0], expected)
        return_val = list([['success', 'trailer']])
        mock_parse_chunk.return_value = return_val
        parser.construct_commands(self.temp)
        self.assertEqual(parser.parsed_values["trailer"][0], expected)
        return_val = list([['success', 'base']])
        mock_parse_chunk.return_value = return_val
        parser.construct_commands(self.temp)
        self.assertEqual(parser.parsed_values["base"][0], expected)
        return_val = list([['success', 'J1']])
        mock_parse_chunk.return_value = return_val
        parser.construct_commands(self.temp)
        self.assertEqual(parser.parsed_values["j1"][0], expected)
        return_val = list([['success', 'J2']])
        mock_parse_chunk.return_value = return_val
        parser.construct_commands(self.temp)
        self.assertEqual(parser.parsed_values["j2"][0], expected)
        return_val = list([['success', 'K1']])
        mock_parse_chunk.return_value = return_val
        parser.construct_commands(self.temp)
        self.assertEqual(parser.parsed_values["k1"][0], expected)
        return_val = list([['success', 'K2']])
        mock_parse_chunk.return_value = return_val
        parser.construct_commands(self.temp)
        self.assertEqual(parser.parsed_values["k2"][0], expected)
        return_val = list([['success', 'K3']])
        mock_parse_chunk.return_value = return_val
        parser.construct_commands(self.temp)
        self.assertEqual(parser.parsed_values["k3"][0], expected)
        return_val = list([['success', 'K4']])
        mock_parse_chunk.return_value = return_val
        parser.construct_commands(self.temp)
        self.assertEqual(parser.parsed_values["k4"][0], expected)
        return_val = list([['success', 'L1']])
        mock_parse_chunk.return_value = return_val
        parser.construct_commands(self.temp)
        self.assertEqual(parser.parsed_values["l1"][0], expected)
        return_val = list([['success', 'N1']])
        mock_parse_chunk.return_value = return_val
        parser.construct_commands(self.temp)
        self.assertEqual(parser.parsed_values["n1"][0], expected)

    def test_construct_commands_empty_file(self):
        # if the program encounters an empty file, it should log the file
        # as an error.
        with patch('parse.logging.error') as mock:
            parser.construct_commands(self.temp)
            mock.assert_called_with('Encountered empty file: ' + self.temp.name)

    def test_write_to_database(self):
        # asserts that the list of values triggers the while loop twice
        # and then a final call is made to IteratorFile. It would be more
        # useful to test the contents of IteratorFile, but what we pass
        # to that is an iterator, not a string, so it's hard to do a
        # comparison.
        conn = Connect()
        cur = conn.cursor()

        expected_command = "{}\t{}"
        parser.commands['header'] = expected_command

        values = [
            tuple(['value1', 'value2']),
            tuple(['value3', 'value4']),
            tuple(['value5', 'value6']),
            tuple(['value7', 'value8']),
            tuple(['value9', 'value10'])
        ]
        with patch('parse.IteratorFile') as mock:
            parser.write_to_database(values, 'header', conn, cur, 2)
            self.assertEqual(3, mock.call_count)
