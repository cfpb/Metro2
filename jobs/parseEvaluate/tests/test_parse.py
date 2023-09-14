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
        result = parser.peek(self.temp, 2)
        self.assertEqual(expected_pos, self.temp.tell())
        self.assertEqual(result, 'te')

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
            # A base segment must meet both criteria: first four characters are digits, and
            # fifth character is a 1
            t4.write('87761xxxxxxxxx')
            t4.seek(0)
            self.assertEqual(parser.determine_segment(t4), 'base')

        # When none of the patterns match, it's unparseable; return none.
        with tempfile.TemporaryFile(mode='w+') as t5:
            t5.write('12345xxxxxxxxx')
            t5.seek(0)
            # 12345 looks like a base segment but it isn't valid. Return None.
            self.assertEqual(parser.determine_segment(t5), None)

        with tempfile.TemporaryFile(mode='w+') as t6:
            t6.write('N3xxxxxxxxxxxx')
            t6.seek(0)
            # N3 looks like an extra segment name but it isn't valid. Return None.
            self.assertEqual(parser.determine_segment(t6), None)


    def test_parse_segment_values_with_header_segment(self):
        # header_segment_1.txt is a one-line test file with a realistic header segment
        with open(os.path.join('tests','sample_files', 'header_segment_1.txt')) as file:
            result = parser.parse_segment_values(file, 'header')
            expected_values = [
                '1xxx', 'HEADER', '3C', '4INNOVISID',
                '5EQUIFAXID', '6EXPE', '7TRANSUNIO', '12312023',
                '01012022', '07042020', '07052020',
                '12REPORTERNAME',
                '13REPORTERADDRESS',
                '14TELEPHON',
                '15VENDORNAME',
                '16VER', '17MBPRBCID', ''
            ]
            self.assertEqual(result['values'], expected_values)

            expected_names = [
                'rdw_header', 'record_identifier_header', 'cycle_identifier_header',
                'innovis_program_identifier', 'equifax_program_identifier',
                'experian_program_identifier', 'transunion_program_identifier',
                'activity_date', 'date_created', 'program_date',
                'program_revision_date', 'reporter_name', 'reporter_address',
                'reporter_telephone_number', 'software_vendor_name', 'software_version_number',
                'microbilt_prbc_program_identifier', 'reserved_header'
            ]
            self.assertEqual(result['names'], expected_names)

    def test_parse_segment_values_with_base_segment(self):
        # base_segment_1.txt is a one-line test file with a realistic base segment
        with open(os.path.join('tests','sample_files', 'base_segment_1.txt')) as f:
            expected_values = [
                '0006', '1', '12312022', '235958', '0', 'FURNISHERID',
                'CY', 'ACCTNUMBER1', 'C', '47', '11302017',
                '000210000', '000019123', 'LOC', 'M', '000000200', '000000190',
                '71', '1', '222211000000000000010100', '', 'XG', '000000498',
                '000000198', '000000000', '03312023', '09292022', '00000000',
                '10312023', 'V', '', 'SURNAME1',
                'FIRSTNAME1', 'MIDDLENAME1', 'J', '333224444',
                '05221967', '3333334444', '1', '', 'US', '123 EXAMPLE ST. N.',
                'APT. 200', 'HOUSTON',
                'TX', '77000', 'C', 'R',
            ]
            result = parser.parse_segment_values(f, 'base')
            self.assertEqual(result['values'], expected_values)

            expected_names = [
                'rdw', 'proc_ind', 'time_stamp', 'throw_out_hms', 'reserved_base',
                'id_num', 'cycle_id', 'cons_acct_num', 'port_type', 'acct_type',
                'date_open', 'credit_limit', 'hcola', 'terms_dur', 'terms_freq',
                'smpa', 'actual_pmt_amt', 'acct_stat', 'pmt_rating', 'php',
                'spc_com_cd', 'compl_cond_cd', 'current_bal', 'amt_past_due',
                'orig_chg_off_amt', 'doai', 'dofd', 'date_closed', 'dolp',
                'int_type_ind', 'reserved_base_2', 'surname', 'first_name',
                'middle_name', 'gen_code', 'ssn', 'dob', 'phone_num', 'ecoa',
                'cons_info_ind', 'country_cd', 'addr_line_1', 'addr_line_2', 'city',
                'state', 'zip', 'addr_ind', 'res_cd',
            ]
            self.assertEqual(result['names'], expected_names)

    def test_parse_segment_values_removes_whitespace(self):
        with tempfile.TemporaryFile(mode='w+') as tf:
            # Write a K1 segment where "creditor name" is blank
            tf.write('K1                              09')
            tf.seek(0)
            result = parser.parse_segment_values(tf, 'k1')

            # The "creditor name" field should be an empty string,
            # not a string of 30 blank spaces.
            expected_values = ['K1', '', '09']
            self.assertEqual(result['values'], expected_values)
            expected_names = ['k1_seg_id', 'k1_orig_creditor_name', 'k1_creditor_classification',]
            self.assertEqual(result['names'], expected_names)

        with tempfile.TemporaryFile(mode='w+') as tf2:
            # Write a K1 segment where "creditor name" is blank
            tf2.write('K1CREDITOR                      09')
            tf2.seek(0)
            result = parser.parse_segment_values(tf2, 'k1')

            # The "creditor name" field should have no empty spaces at the end.
            expected_values = ['K1', 'CREDITOR', '09']
            self.assertEqual(result['values'], expected_values)

    def test_parse_chunk_finds_all_segments_in_chunk(self):
        with open(os.path.join('tests','sample_files', 'm2_file_small.txt')) as f:
            file_size = os.path.getsize(f.name)
            result = parser.parse_chunk(start=0, end=file_size, fstream=f)

            # The test file has 8 total segments in it
            self.assertEqual(len(result), 8)

    def test_parse_chunk_adds_segment_name_to_parsed_values(self):
        with open(os.path.join('tests','sample_files', 'm2_file_small.txt')) as f:
            file_size = os.path.getsize(f.name)
            result = parser.parse_chunk(start=0, end=file_size, fstream=f)
            # parse_chunk appends the segment name to the end of each parsed segment
            # In our test file, the first segment is a header
            self.assertEqual(result[0][-1], 'header')
            # The next segment is a base without any extra segments
            self.assertEqual(result[1][-1], 'base')
            # Next segment is a base with a K1 and K2 segment
            self.assertEqual(result[2][-1], 'base')
            self.assertEqual(result[3][-1], 'k1')
            self.assertEqual(result[4][-1], 'k2')
            # next segment is a base with a L1 segment
            self.assertEqual(result[5][-1], 'base')
            self.assertEqual(result[6][-1], 'l1')
            # last is a trailer
            self.assertEqual(result[7][-1], 'trailer')

    def test_parse_chunk(self):
        self.temp.write('00001'.ljust(426, '0'))
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
        str = 'bogus segment that does not match a metro2 segment type'
        self.temp.write(str)
        self.temp.seek(0)

        with patch('parse.logging.warning') as mock:
            parser.parse_chunk(0, os.path.getsize(self.temp.name), self.temp)
            mock.assert_called_with(f'unread data: {str}')

    def test_break_file_into_chunks(self):
        with open(os.path.join('tests','sample_files', 'm2_file_small.txt')) as f:
            # TODO: When this number is 4 or 5, this method becomes nonresponsive. WTF.
            chunk_endpoints = parser.break_file_into_chunks(f, 2)

            # break_file_into_chunks shouldn't break up lines of the file,
            # so each chunk should end with a \n
            _, first_chunk_endpoint = chunk_endpoints[0]
            f.seek(first_chunk_endpoint - 1)
            self.assertEqual(f.read(1), "\n")

            _, second_chunk_endpoint = chunk_endpoints[1]
            f.seek(second_chunk_endpoint - 1)
            self.assertEqual(f.read(1), "\n")

            # Test that the actual chunks match what's expected.
            # If the test file changes, this will need to change.
            expected = [(0, 1349), (1349, 2238)]
            self.assertEqual(chunk_endpoints, expected)

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
        with open(os.path.join('tests','sample_files', 'm2_file_small.txt')) as f:
            file_size = os.path.getsize(f.name)
            parser.parse_chunk(start=0, end=file_size, fstream=f)

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
