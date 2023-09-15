##############################################################################
# This file reads in a metro2 mapping file and converts the raw data to fields
# in a database. DB connection is currently only for use in local development.
# Secrets should be used in a production or prod-like environment.
##############################################################################

import os
import re
import sys
import logging
import multiprocessing as mp

from fields import fields, seg_length
from iterator_file import IteratorFile
from tables import connect
from psycopg2 import OperationalError

# check if tool is set to run locally
try:
    METRO2ENV = os.environ['METRO2ENV']
except KeyError as e:
    logging.error(f"Environment (local, prod, etc.) not found: {e}")
    sys.exit(1)
except:
    logging.error("Unexpected error, quitting...")
    sys.exit(1)

# quit if not local
if METRO2ENV != 'local':
    logging.error("Metro2 evaluator tool is not configured to run in production. \
        Quitting...")
    sys.exit(1)

# add any fields to be removed to this list. To skip these fields, import this
# and pass it as the skip argument to initializing the parser.
pii_to_remove = {
    "cycle_identifier_header",
    "innovis_program_identifier",
    "equifax_program_identifier",
    "experian_program_identifier",
    "transunion_program_identifier",
    "reporter_name",
    "reporter_address",
    "reporter_telephone_number",
    "software_vendor_name",
    "software_version_number",
    "microbilt_prbc_program_identifier",
    "surname",
    "first_name",
    "middle_name",
    "ssn",
    "dob",
    "phone_num",
    "addr_line_1",
    "addr_line_2",
    "zip",
    "surname_j1",
    "first_name_j1",
    "middle_name_j1",
    "ssn_j1",
    "dob_j1",
    "phone_num_j1",
    "surname_j2",
    "first_name_j2",
    "middle_name_j2",
    "ssn_j2",
    "dob_j2",
    "phone_num_j2",
    "addr_line_1_j2",
    "addr_line_2_j2",
    "zip_j2",
    "k1_orig_creditor_name",
    "k2_purch_sold_name",
    "n1_employer_name",
    "employer_addr1",
    "employer_addr2",
    "employer_zip"
}

class Parser():
    def __init__(self, skip=None):
        # imports segment schema
        self.skip = list()
        if skip:
            self.skip = skip
        self.mapping = fields
        self.commands = dict()
        self.parsed_values = {
            "header": list(),
            "trailer": list(),
            "base": list(),
            "j1": list(),
            "j2": list(),
            "k1": list(),
            "k2": list(),
            "k3": list(),
            "k4": list(),
            "l1": list(),
            "n1": list(),
        }
        self.field_names = dict()
        self.seg_length = seg_length

    # returns the requested bytes without advancing the iterator
    def peek(self, filestream, bytes_to_read):
        # store current position of iterator
        pos = filestream.tell()
        # read and then seek back to original position
        result = filestream.read(bytes_to_read)
        filestream.seek(pos)

        return result

    # TODO: This method is not tested.
    def generate_guid(self, file_name, file_position):
        # generate GUID that will be unique between chunks and files
        return hash(f'{file_name}-{file_position}')

    def file_identifier(self, file_name):
        return hash(f'{file_name}')

    def determine_segment(self, fstream):
        # the order here is very important since regex is expensive.
        # base will be the most common segment in any file so we want to test that first
        # extra segments will be the next most common, so we want to test those second
        # header and trailer are one per file, so we test those last
        if re.match(r'\d{4}1', self.peek(fstream, 5)):
            segment = "base"
        elif re.match(r'J1|J2|K1|K2|K3|K4|L1|N1', self.peek(fstream, 2)):
            # convert segment name to lowercase to match fields.py
            segment = self.peek(fstream, 2).lower()
        elif re.match(r'.{4}HEADER$', self.peek(fstream, 10)):
            segment = "header"
        elif re.match(r'.{4}TRAILER$', self.peek(fstream, 11)):
            segment = "trailer"
        else:
            # catch unreadable lines
            segment = None

        return segment


    def parse_segment_values(self, fstream, segment, default_values=None):
        values = list()
        if default_values:
            values += default_values
        names = list()

        prev_field_end = 0
        for field_name, (field_start, field_end) in self.mapping[segment].items():
            if field_name not in self.skip:
                names.append(field_name)

            # if field skipped, skip that many characters in the stream
            skip = (int(field_start) - 1) - int(prev_field_end)
            if skip > 0:
                fstream.read(skip)

            length = int(field_end) - (int(field_start) - 1)
            found_value = fstream.read(length).strip()
            values.append(found_value)
            # update prev_field_end
            prev_field_end = field_end

        # in case the last field is skipped
        if prev_field_end != self.seg_length[segment]:
            skip_last = self.seg_length[segment] - prev_field_end
            fstream.read(skip_last)

        return {'values': values, 'names': names}


    # TODO: This method is not tested.
    def create_commands(self, values, segment):
        sub = list()
        sub.append('{}')
        # add two to values for the guid and file
        command = '\t'.join(sub * (len(values) + 2))
        # segment needs to be lower so it matches table names
        self.commands[segment.lower()] = command


    # parse a chunk of a file given the byte offset and endpoint
    def parse_chunk(self, start, end, fstream):
        values_list = list()
        # get just the file name from the stream
        file_name = os.path.basename(fstream.name)
        fstream.seek(start)
        pos = fstream.tell()
        guid = self.generate_guid(file_name, str(pos))
        # this remains consistent for the chunk
        file = self.file_identifier(file_name)

        # read until the end of the chunk is reached
        while pos < end:
            # read to the end of this line
            while pos < end and self.peek(fstream, 1) != '\n':
                # determine what kind of segment is next
                segment = self.determine_segment(fstream)
                if not segment:
                    logging.warning(f"unread data: {fstream.readline()}")
                    pos = fstream.tell()
                    # seek back one for the newline
                    fstream.seek(pos - 1)
                    break


                # read in entire segment
                parsed_segment = self.parse_segment_values(fstream, segment, default_values=[guid, file])
                values = parsed_segment['values']
                names = parsed_segment['names']

                # update commands
                self.create_commands(values, segment)

                # add names to field_names dict
                self.field_names[segment] = names

                # add segment to the end of the values list
                values.append(segment)
                # update pos
                pos = fstream.tell()
                values_list.append(values)

            # read newline
            fstream.read(1)
            pos = fstream.tell()
            # update guid
            guid = self.generate_guid(file_name, str(pos))

        return values_list

    def break_file_into_chunks(self, fstream, max_chunks):
        file_size = os.path.getsize(fstream.name)
        if file_size == 0:
            logging.error(f'Encountered empty file: {fstream.name}')
            return

        # seek to the beginning of the file stream
        fstream.seek(0)

        # doesn't matter if we lose a decimal value here since the last chunk is "the rest"
        chunk_size = int(file_size / max_chunks)

        # find first newline after each chunk size
        chunk_endpoints = list()
        offset = 0
        chunk_start = 0
        for _ in range(max_chunks - 1):
            # just in case we have less lines than workers
            if chunk_start < file_size:
                # Position the cursor {chunk_size} characters after {chunk_start}
                fstream.seek(chunk_start + chunk_size)

                offset += chunk_size
                # find the first newline after offset and append the position to chunk_endpoints
                while fstream.read(1) != '\n':
                    offset+=1
                # add one more to offset for the newline we found
                offset+=1
                chunk_endpoints.append((chunk_start, offset))
                # next chunk will start at the next byte
                chunk_start = offset

        # just in case we have less lines than workers
        if chunk_start < file_size:
            # add the last chunk
            chunk_endpoints.append((chunk_start, file_size))

        return chunk_endpoints

    # constructs commands to feed to exec_commands method with parallel processing
    def construct_commands(self, fstream):
        # TODO: use an async processing library to parallelize the parsing process
        # For now, I'm leaving this code here, in case it's useful in the future:
        # num_workers = mp.cpu_count()
        # logging.info(f'{num_workers} workers available to parse data')

        num_workers = 3
        chunk_endpoints = self.break_file_into_chunks(fstream, num_workers)

        # If the file is empty, stop processing this file.
        if not chunk_endpoints:
            return

        for chunk in chunk_endpoints:
            start, end = chunk
            parsed_result = self.parse_chunk(start, end, fstream)
            for parsed_segment in parsed_result:
                segment_name = parsed_segment.pop()  # get the segment name from the end of the list of values
                # Add the segment's parsed values as a tuple to self.parsed_values
                self.parsed_values[segment_name].append(tuple(parsed_segment))

    def write_to_database(self, values, segment, connection, cursor, max_block_size=2000):
        # Gives good performance relative to other potential block sizes.

        block_start = 0
        block_end = max_block_size
        commands = self.commands[segment]
        cols = list(self.field_names[segment])

        # process statements in blocks
        while block_end < len(values):
            # split values
            val_list = values[block_start:block_end]

            copy_str = IteratorFile((commands.format(*vals) for vals in val_list))

            # execute block
            cursor.copy_from(copy_str, segment, columns=cols)

            # persist changes
            connection.commit()

            # update block start and block end
            block_start += max_block_size
            block_end += max_block_size

        # execute final command
        # split values
        val_list = values[block_start:len(values)]

        copy_str = IteratorFile((commands.format(*vals) for vals in val_list))

        # execute block
        cursor.copy_from(copy_str, segment, columns=cols)

        cursor.close()

        # persist changes
        connection.commit()

    # establish connection to postgres database
    def exec_commands(self):
        conn = None

        try:
            conn = connect()

            # create a cursor
            cur = conn.cursor()

            # write each segment to database
            self.write_to_database(self.parsed_values["header"], "header", conn, cur)
            self.write_to_database(self.parsed_values["trailer"], "trailer", conn, cur)
            self.write_to_database(self.parsed_values["base"], "base", conn, cur)
            self.write_to_database(self.parsed_values["j1"], "j1", conn, cur)
            self.write_to_database(self.parsed_values["j2"], "j2", conn, cur)
            self.write_to_database(self.parsed_values["k1"], "k1", conn, cur)
            self.write_to_database(self.parsed_values["k2"], "k2", conn, cur)
            self.write_to_database(self.parsed_values["k3"], "k3", conn, cur)
            self.write_to_database(self.parsed_values["k4"], "k4", conn, cur)
            self.write_to_database(self.parsed_values["l1"], "l1", conn, cur)
            self.write_to_database(self.parsed_values["n1"], "n1", conn, cur)

        except OperationalError as e:
            logging.error(f"There was a problem establishing the connection: {e}")
        finally:
            if conn is not None:
                conn.close()

# create instance of parser
parser = Parser()
