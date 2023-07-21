##############################################################################
# This file reads in a metro2 mapping file and converts the raw data to fields
# in a database. DB connection is currently only for use in local development.
# Secrets should be used in a production or prod-like environment.
##############################################################################

import os
import re
import multiprocessing as mp
import openpyxl as xl

from iterator_file import IteratorFile
from tables import create, connect, connect_res, meta, res_meta

# check if tool is set to run locally
try:
    METRO2ENV = os.environ['METRO2ENV']
except KeyError as e:
    print("Environment (local, prod, etc.) not found: %s", e)
    exit(1)
except:
    print("Unexpected error, quitting...")
    exit(1)

# quit if not local
if METRO2ENV != 'local':
    print("Metro2 evaluator tool is not configured to run in production. \
        Quitting...")
    exit(1)

class Parser():
    def __init__(self):
        #create empty DataFrame used for mapping
        self.mapping = dict()
        self.commands = dict()
        self.header_values = list()
        self.trailer_values = list()
        self.base_values = list()
        self.J1_values = list()
        self.J2_values = list()
        self.K1_values = list()
        self.K2_values = list()
        self.K3_values = list()
        self.K4_values = list()
        self.L1_values = list()
        self.N1_values = list()
        self.field_names = dict()
        self.seg_length = dict()

    # maps fixed width fields in each segment from mapping file
    def map_fields(self, mapfile, sheetname, colsegment, colstart, colend, colfield, skip):
        # load workbook and strip out data we need
        wb = xl.load_workbook(mapfile)
        sheet = wb[sheetname]
        segments = sheet[colsegment]
        starts = sheet[colstart]
        ends = sheet[colend]
        fieldnames = sheet[colfield]

        # start at 1 to skip the xlsx column header
        iterator = 1
        num_rows = len(segments)
        # first segment will always be header
        segment = "header"
        # iterate over data and save to mapping dict
        while iterator < num_rows:
            values = list()
            # each table starts with id and file fields not included in the mapping file
            fields = list(["id", "file"])
            while iterator < num_rows and segment == segments[iterator].value:
                if not skip or fieldnames[iterator].value.lower() not in skip:
                    values.append((starts[iterator].value, ends[iterator].value))
                    fields.append(fieldnames[iterator].value.lower())
                iterator+=1
            # save values and update segment
            self.mapping[segment] = values
            # segment needs to be lower so it matches table names
            self.field_names[segment.lower()] = fields
            # seg length will be the last value of the ends column
            self.seg_length[segment] = ends[iterator - 1].value

            # update commands
            sub = list()
            sub.append('{}')
            # add two to values for the guid and file (added later)
            command = '\t'.join(sub * (len(values) + 2))
            # segment needs to be lower so it matches table names
            self.commands[segment.lower()] = command

            # if there's another segment to map
            if iterator < num_rows and segments[iterator].value != None:
                segment = segments[iterator].value

        wb.close()

    # returns the requested bytes without advancing the iterator
    def peek(self, filestream, bytes_to_read):
        # store current position of iterator
        pos = filestream.tell()
        # read and then seek back to original position
        result = filestream.read(bytes_to_read)
        filestream.seek(pos)

        return result

    # parse a chunk of a file given the byte offset and endpoint
    def parse_chunk(self, start, end, file_name):
        values_list = list()
        fstream = None
        try:
            fstream = open(file_name, 'r')
            fstream.seek(start)
            pos = fstream.tell()
            # generate GUID that will be unique between chunks and files
            str_pos = str(pos)
            guid = hash(f'{file_name}-{str_pos}')
            # this remains consistent for the chunk
            file = hash(f'{file_name}')

            # read until the end of the chunk is reached
            while pos < end:
                while pos < end and self.peek(fstream, 1) != '\n':
                    segment = ""
                    # determine segment
                    # the order here is very important since regex is expensive.
                    # base will be the most common segment in any file so we want to test that first
                    # extra segments will be the next most common, so we want to test those second
                    # header and trailer are one per file, so we test those last
                    if re.match(r'\d{5}', self.peek(fstream, 5)):
                        segment = "base"
                    elif re.match(r'[A-Z][1-4]', self.peek(fstream, 2)):
                        segment = self.peek(fstream, 2)
                    elif re.match(r'.*HEADER$', self.peek(fstream, 10)):
                        segment = "header"
                    elif re.match(r'.*TRAILER$', self.peek(fstream, 11)):
                        segment = "trailer"
                    # catch unreadable lines
                    else:
                        print("error: encountered unreadable line...")
                        print("unread data: ", fstream.readline())
                        pos = fstream.tell()
                        # seek back one for the newline
                        fstream.seek(pos - 1)
                        break

                    # read in entire segment
                    values = list()

                    # add guid and file to beginning of values list
                    values.append(guid)
                    values.append(file)

                    prev_field_end = 0
                    for field_start, field_end in self.mapping[segment]:
                        # in case there's a segment that was skipped
                        skip = (int(field_start) - 1) - int(prev_field_end)
                        if skip > 0:
                            fstream.read(skip)
                        
                        length = int(field_end) - (int(field_start) - 1)
                        values.append(fstream.read(length))
                        # update prev_field_end
                        prev_field_end = field_end

                    # in case the last field is skipped
                    if prev_field_end != self.seg_length[segment]:
                        skip_last = self.seg_length[segment] - prev_field_end
                        fstream.read(skip_last)

                    # add segment to the end of the values list
                    values.append(segment)
                    # update pos
                    pos = fstream.tell()
                    values_list.append(values)

                # read newline
                fstream.read(1)
                pos = fstream.tell()
                # update guid
                str_pos = str(pos)
                guid = hash(f'{file_name}-{str_pos}')

        except Exception as e:
            print("encountered an error opening file", e)
            exit(1)
        finally:
            if fstream is not None:
                fstream.close() 
        
        return values_list

    # constructs commands to feed to exec_commands method with parallel processing
    def construct_commands(self, file_name):
        file_size = os.path.getsize(file_name)

        # break down file into chunks
        num_workers = mp.cpu_count()
        print(f'{num_workers} workers available to parse data')
        # doesn't matter if we lose a decimal value here since the last chunk is "the rest"
        chunk_size = int(file_size / num_workers)

        # open file and find first newline after each chunk size
        fstream = None
        try:
            fstream = open(file_name, 'rb')
            chunk_endpoints = list()
            offset = 0
            chunk_start = 0
            for _ in range(num_workers - 1):
                # 1 for the second argument means we are starting from the current read position
                fstream.seek(chunk_size, 1)
                offset += chunk_size
                # find the first newline after offset and append the position to chunk_endpoints
                while fstream.read(1) != b'\n':
                    offset+=1
                # add one more to offset for the newline we found
                offset+=1
                chunk_endpoints.append((chunk_start, offset))
                # next chunk will start at the next byte
                chunk_start = offset
            
            # add the last chunk
            chunk_endpoints.append((chunk_start, file_size - 1))
        except Exception as e:
            print("encountered an error opening file: ", e)
            exit(1)
        finally:
            if fstream is not None:
                fstream.close()

        print("Parsing...")
        pool = mp.Pool(num_workers)
        async_results = list(pool.apply_async(self.parse_chunk, args=(start, endpoint, file_name,)) for start, endpoint in chunk_endpoints)
        completed_results = [result.get() for result in async_results]

        # combine results
        for result in completed_results:
            for values in result:
                # pop segment off the end of the values list
                segment = values.pop()
                
                # add to values
                val_tup = tuple(values)
                if segment == "header":
                    self.header_values.append(val_tup)
                elif segment == "trailer":
                    self.trailer_values.append(val_tup)
                elif segment == "base":
                    self.base_values.append(val_tup)
                elif segment == "J1":
                    self.J1_values.append(val_tup)
                elif segment == "J2":
                    self.J2_values.append(val_tup)
                elif segment == "K1":
                    self.K1_values.append(val_tup)
                elif segment == "K2":
                    self.K2_values.append(val_tup)
                elif segment == "K3":
                    self.K3_values.append(val_tup)
                elif segment == "K4":
                    self.K4_values.append(val_tup)
                elif segment == "L1":
                    self.L1_values.append(val_tup)
                elif segment == "N1":
                    self.N1_values.append(val_tup)

        pool.close()
        pool.join()

        print("Parsing complete.")

    # establish connection to postgres database
    def exec_commands(self, values=None, segment=None):
        max_block_size = 2000
        conn = None

        try:
            conn = connect()

            # create a cursor
            cur = conn.cursor()
            
            # execute commands
            if values and segment:
                block_start = 0
                block_end = max_block_size
                commands = self.commands[segment]
                cols = list(self.field_names[segment])
                
                # process statements in blocks
                while block_end < len(values) - block_start:
                    # split values
                    val_list = values[block_start:block_end]

                    copy_str = IteratorFile((commands.format(*vals) for vals in val_list))

                    # execute block
                    cur.copy_from(copy_str, segment, columns=cols)

                    # persist changes
                    conn.commit()

                    # update block start and block end
                    block_start += max_block_size
                    block_end += max_block_size

                # execute final command
                # split values
                val_list = values[block_start:len(values)]

                copy_str = IteratorFile((commands.format(*vals) for vals in val_list))

                # execute block
                cur.copy_from(copy_str, segment, columns=cols)

                cur.close()

                # persist changes
                conn.commit()

        except Exception as e:
            print("There was a problem establishing the connection: ", e)
        finally:
            if conn is not None:
                conn.close()

    # creates database tables
    def create_tables(self):
        create(meta, connect)
        create(res_meta, connect_res)

# create instance of parser
parser = Parser()
