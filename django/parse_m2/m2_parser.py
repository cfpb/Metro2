import io
import re


from parse_m2 import fields
from parse_m2.models import (
    Metro2Event,
    M2DataFile, UnparseableData,
    AccountHolder, AccountActivity,
    J1, J2, K1, K2, K3, K4, L1, N1
)
from parse_m2 import parse_utils


class M2FileParser():
    chunk_size = 2000  # TODO: determine a good number for this
    header_format = r'.{4}HEADER$'
    trailer_format = r'.{4}TRAILER$'

    def __init__(self, event: Metro2Event, filepath: str) -> None:
        """
        - file_record: the M2DataFile that represents the file that the
                    line of data came from. Used as a foreign key when
                    saving the records in the line.
        """
        self.file_record: M2DataFile = M2DataFile(event=event, file_name=filepath)
        self.file_record.save()

    def get_activity_date_from_header(self, line: str):
        if re.match(self.header_format, line[:10]):
            # If the line is a header, get the activity_date
            return parse_utils.get_field_value(
                fields.header_fields["activity_date"],
                line,
            )
        else:
            raise parse_utils.UnreadableFileException("First line of file isn't a header")


    def parse_extra_segments(self, line: str, parsed: dict) -> dict:
        """
        Given a string with any number of extra segments, determine what the first
        segment is, parse its values, add the values to the `parsed` dict, and
        call this method again with whatever is left of the string.
        """
        if len(line) < 2:
            return parsed

        acct_activity = parsed["AccountActivity"]

        next_segment_indicator = line[:2]
        if re.match(r'J1', next_segment_indicator):
            seg_length = fields.seg_length["j1"]
            j1 = J1.parse_from_segment(line[:seg_length], acct_activity)
            if "j1" in parsed:
                parsed["j1"].append(j1)
            else:
                parsed["j1"] = [j1]

        elif re.match(r'J2', next_segment_indicator):
            seg_length = fields.seg_length["j2"]
            j2 = J2.parse_from_segment(line[:seg_length], acct_activity)
            if "j2" in parsed:
                parsed["j2"].append(j2)
            else:
                parsed["j2"] = [j2]

        elif re.match(r'K1', next_segment_indicator):
            seg_length = fields.seg_length["k1"]
            k1 = K1.parse_from_segment(line[:seg_length], acct_activity)
            parsed["k1"] = k1

        elif re.match(r'K2', next_segment_indicator):
            seg_length = fields.seg_length["k2"]
            k2 = K2.parse_from_segment(line[:seg_length], acct_activity)
            parsed["k2"] = k2

        elif re.match(r'K3', next_segment_indicator):
            seg_length = fields.seg_length["k3"]
            k3 = K3.parse_from_segment(line[:seg_length], acct_activity)
            parsed["k3"] = k3

        elif re.match(r'K4', next_segment_indicator):
            seg_length = fields.seg_length["k4"]
            k4 = K4.parse_from_segment(line[:seg_length], acct_activity)
            parsed["k4"] = k4

        elif re.match(r'L1', next_segment_indicator):
            seg_length = fields.seg_length["l1"]
            l1 = L1.parse_from_segment(line[:seg_length], acct_activity)
            parsed["l1"] = l1

        elif re.match(r'N1', next_segment_indicator):
            seg_length = fields.seg_length["n1"]
            n1 = N1.parse_from_segment(line[:seg_length], acct_activity)
            parsed["n1"] = n1

        else:
            msg = f"Extra segment indicator `{next_segment_indicator}`" + \
                " did not match any valid extra segment"
            raise parse_utils.UnreadableLineException(msg)

        if seg_length:
            self.parse_extra_segments(line[seg_length:], parsed)

        return parsed

    def parse_line(self, line: str, activity_date) -> dict:
        """
        Given a single line of a Metro2 file, parse all of the segments it contains
        into individual model records, and put them all into a dict.

        inputs:
        - line: the line of metro2 data, starting with a base segment
        - activity_date: date object, to be saved in the AccountHolder and
                        AccountActivity records for this line

        output:
        - If the line was a valid Metro2 line, a dict with the following keys:
        AccountHolder, AccountActivity, and optionally a key for each
        type of extra segment that was present in the line
        (j1, j2, k1, k2, k3, k4, l1, n1)
        - If the line was not valid (i.e. if any part of the parsing process
        threw an UnreadableLine exception), a dict with an 'UnparseableData' key.
        """
        if re.match(self.trailer_format, line[:11]):
            # If the line is a trailer, ignore it
            return

        try:
            parsed = {}
            # parse the base segment into AccountHolder and AccountActivity
            acct_holder = AccountHolder.parse_from_segment(
                line, self.file_record, activity_date)
            parsed["AccountHolder"] = acct_holder

            acct_activity = AccountActivity.parse_from_segment(
                line, acct_holder, activity_date)
            parsed["AccountActivity"] = acct_activity

            # parse the extra segments
            base_segment_length = fields.seg_length["header"]
            remaining_chars = line[base_segment_length:]
            parsed = self.parse_extra_segments(remaining_chars, parsed)
            return parsed

        except parse_utils.UnreadableLineException as e:
            # if any part of the line couldn't be parsed, don't save
            #  the segments; only save the line as UnparseableData
            return {"UnparseableData": UnparseableData(
                data_file=self.file_record,
                unparseable_line=line,
                error_description=str(e)
            )}

    def parse_chunk(self, f: io.TextIOWrapper, chunk_size: int, activity_date) -> dict:
        """
        Given a filestream of a Metro2 file, parse chunk_size lines from it and save them
        to a dict.

        inputs:
        - f: filestream of the Metro2 file
        - chunk_size: the number of lines to parse before returning
        - activity_date: date object, to be saved in the AccountHolder and
                        AccountActivity records for each line

        output:
        - a dict with the following keys: AccountHolder, AccountActivity,
        extra segment keys (if any were present), and UnparseableData (if any)
        """
        parsed_records = {
            "AccountHolder": [],
            "AccountActivity": [],
            "j1": [],
            "j2": [],
            "k1": [],
            "k2": [],
            "k3": [],
            "k4": [],
            "l1": [],
            "n1": [],
            "UnparseableData": [],
        }
        lines_parsed = 0
        while lines_parsed < chunk_size:
            line = f.readline()
            if not line:
                # If the file has ended, exit the parser
                break

            line_results = self.parse_line(line, activity_date)
            if line_results:
                if "UnparseableData" in line_results:
                    parsed_records["UnparseableData"].append(line_results["UnparseableData"])
                if "AccountHolder" in line_results:
                    parsed_records["AccountHolder"].append(line_results["AccountHolder"])
                if "AccountActivity" in line_results:
                    parsed_records["AccountActivity"].append(line_results["AccountActivity"])
                if "j1" in line_results:
                    parsed_records["j1"] = parsed_records["j1"] + line_results["j1"]
                if "j2" in line_results:
                    parsed_records["j2"] = parsed_records["j2"] + line_results["j2"]
                if "k1" in line_results:
                    parsed_records["k1"].append(line_results["k1"])
                if "k2" in line_results:
                    parsed_records["k2"].append(line_results["k2"])
                if "k3" in line_results:
                    parsed_records["k3"].append(line_results["k3"])
                if "k4" in line_results:
                    parsed_records["k4"].append(line_results["k4"])
                if "l1" in line_results:
                    parsed_records["l1"].append(line_results["l1"])
                if "n1" in line_results:
                    parsed_records["n1"].append(line_results["n1"])

            lines_parsed += 1

        return parsed_records

    def save_values_bulk(self, values: dict):
        UnparseableData.objects.bulk_create(values["UnparseableData"])
        AccountHolder.objects.bulk_create(values["AccountHolder"])
        AccountActivity.objects.bulk_create(values["AccountActivity"])
        J1.objects.bulk_create(values["j1"])
        J2.objects.bulk_create(values["j2"])
        K1.objects.bulk_create(values["k1"])
        K2.objects.bulk_create(values["k2"])
        K3.objects.bulk_create(values["k3"])
        K4.objects.bulk_create(values["k4"])
        L1.objects.bulk_create(values["l1"])
        N1.objects.bulk_create(values["n1"])

    def parse_file_contents(self, f: io.TextIOWrapper, file_size: int):
        """
        Parse a Metro2 file and save the records to the database.

        Inputs:
        `f` - file stream of the data file to be parsed
        `file_size` - the size of the file stream in bytes
        """
        # get first line
        header_line = f.readline()
        activity_date = self.get_activity_date_from_header(header_line)

        # parse the rest of the file until it is done
        while f.tell() < file_size:
            values = self.parse_chunk(f, self.chunk_size, activity_date)
            self.save_values_bulk(values)
