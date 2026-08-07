import io
import re
from datetime import date

from parse_m2 import fields, parse_utils
from parse_m2.models import (
    J1,
    J2,
    K1,
    K2,
    K3,
    K4,
    L1,
    N1,
    AccountActivity,
    M2DataFile,
    Metro2Event,
    UnparseableData,
)


class M2FileParser:
    # Parser version is saved on each file record.
    # Increment this version for all updates to parser functionality.
    parser_version = "3.1.3"

    chunk_size = 2000  # TODO: determine a good number for this
    any_non_whitespace = r'\S'

    activity_date = None

    def __init__(
        self, event: Metro2Event, filepath: str, collection: str = None
    ) -> None:
        """
        - file_record: the M2DataFile that represents the file that the
                    line of data came from. Used as a foreign key when
                    saving the records in the line.
        """
        self.file_record: M2DataFile = M2DataFile(
            event=event,
            file_name=filepath,
            parsing_status="In progress",
            parser_version=self.parser_version,
            # Collection, if present, will be prepended to consumer account number
            # for all records in this file
            collection=collection,
        )
        self.file_record.save()

    def update_file_record(self, status=None, msg=None) -> None:
        """
        Update the file record with the given status and error message.
        """
        file = self.file_record
        if status:
            file.parsing_status = status
        if msg:
            file.error_message = msg
        file.save()

    def get_activity_date_from_header(self, line: str) -> date:
        try:
            return parse_utils.get_field_value(
                fields.header_fields, "activity_date", line,
            )
        except parse_utils.UnreadableLineException as e:
            message = "First line is a header, but activity_date couldn't be parsed"
            if len(line) > 2000:
                line = line[:1500] + "..."
            error_message = f"{message}. {e}. Source line: `{line}`"
            # if the header couldn't be parsed, don't try to parse the rest of the file
            raise parse_utils.UnreadableFileException(error_message) from e

    def handle_first_line_and_return_activity_date(self, first_line:str) -> date:
        if parse_utils.is_header_line(first_line):
            # If it's a header, get the activity date
            return self.get_activity_date_from_header(first_line)
        else:
            # If header is missing, first save a message to inform users
            message = (
                "First line of file isn't a header. Using DOAI in place of activity "
                "date."
            )
            self.update_file_record(msg=message)

            # Next, parse the first line as a tradeline and save the results
            # (self.activity_date=None signals the parser to use DOAI as activity_date)
            line_results = self.parse_line(line=first_line)
            if line_results:
                parsed_records = self.prepare_results_for_bulk_save(line_results)
                self.save_values_bulk(parsed_records)
            return None

    def parse_extra_segments(self, line: str, parsed: dict) -> dict:
        """
        Given a string with any number of extra segments, determine what the first
        segment is, parse its values, add the values to the `parsed` dict, and
        call this method again with whatever is left of the string.
        """
        # If there's only whitespace left in this line, return
        if not re.match(self.any_non_whitespace, line):
            return parsed
        acct_activity = parsed["AccountActivity"]

        next_segment_indicator = line[:2]
        if next_segment_indicator == "J1":
            segment = line[:fields.seg_length["j1"]]
            if parse_utils.segment_has_contents(segment):
                j1 = J1.parse_from_segment(segment, acct_activity)
                if "j1" in parsed:
                    parsed["j1"].append(j1)
                else:
                    parsed["j1"] = [j1]
                if j1.cons_info_ind:
                    parsed["cons_info_ind_assoc"].append(j1.cons_info_ind)
                if j1.ecoa:
                    parsed["ecoa_assoc"].append(j1.ecoa)

        elif next_segment_indicator == "J2":
            segment = line[:fields.seg_length["j2"]]
            if parse_utils.segment_has_contents(segment):
                j2 = J2.parse_from_segment(segment, acct_activity)
                if "j2" in parsed:
                    parsed["j2"].append(j2)
                else:
                    parsed["j2"] = [j2]
                if j2.cons_info_ind:
                    parsed["cons_info_ind_assoc"].append(j2.cons_info_ind)
                if j2.ecoa:
                    parsed["ecoa_assoc"].append(j2.ecoa)

        elif next_segment_indicator == "K1":
            segment = line[:fields.seg_length["k1"]]
            if parse_utils.segment_has_contents(segment):
                k1 = K1.parse_from_segment(segment, acct_activity)
                parsed["k1"] = k1

        elif next_segment_indicator == "K2":
            segment = line[:fields.seg_length["k2"]]
            if parse_utils.segment_has_contents(segment):
                k2 = K2.parse_from_segment(segment, acct_activity)
                parsed["k2"] = k2

        elif next_segment_indicator == "K3":
            segment = line[:fields.seg_length["k3"]]
            if parse_utils.segment_has_contents(segment):
                k3 = K3.parse_from_segment(segment, acct_activity)
                parsed["k3"] = k3

        elif next_segment_indicator == "K4":
            segment = line[:fields.seg_length["k4"]]
            if parse_utils.segment_has_contents(segment):
                k4 = K4.parse_from_segment(segment, acct_activity)
                parsed["k4"] = k4

        elif next_segment_indicator == "L1":
            segment = line[:fields.seg_length["l1"]]
            if parse_utils.segment_has_contents(segment):
                l1 = L1.parse_from_segment(segment, acct_activity)
                parsed["l1"] = l1

        elif next_segment_indicator == "N1":
            segment = line[:fields.seg_length["n1"]]
            if parse_utils.segment_has_contents(segment):
                n1 = N1.parse_from_segment(segment, acct_activity)
                parsed["n1"] = n1

        else:
            msg = f"Extra segment indicator `{next_segment_indicator}`" + \
                " did not match any valid extra segment"
            raise parse_utils.UnreadableLineException(msg)

        if segment:
            seg_length = len(segment)
            self.parse_extra_segments(line[seg_length:], parsed)

        return parsed

    def parse_line(self, line: str) -> dict:
        """
        Given a single line of a Metro2 file, parse all of the segments it contains
        into individual model records, and put them all into a dict.

        inputs:
        - line: the line of metro2 data, starting with a base segment

        output:
        - If the line was a valid Metro2 line, a dict with the following keys:
        AccountActivity, and optionally a key for each
        type of extra segment that was present in the line
        (j1, j2, k1, k2, k3, k4, l1, n1)
        - If the line was not valid (i.e. if any part of the parsing process
        threw an UnreadableLine exception), a dict with an 'UnparseableData' key.
        """
        try:
            parsed = {}
            parsed["cons_info_ind_assoc"] = []
            parsed["ecoa_assoc"] = []

            # parse the base segment into AccountActivity
            acct_activity = AccountActivity.parse_from_segment(
                line, self.file_record, self.activity_date)
            parsed["AccountActivity"] = acct_activity

            # parse the extra segments
            base_segment_length = fields.seg_length["header"]
            remaining_chars = line[base_segment_length:]
            parsed = self.parse_extra_segments(remaining_chars, parsed)

            # Take the fields that are aggregated from the extra segments and
            # save them to the AccountActivity record
            if "cons_info_ind_assoc" in parsed:
                acct_activity.cons_info_ind_assoc = parsed["cons_info_ind_assoc"]
            if "ecoa_assoc" in parsed:
                acct_activity.ecoa_assoc = parsed["ecoa_assoc"]

            return parsed

        except parse_utils.UnreadableLineException as e:
            if re.match(parse_utils.trailer_format, line[:11]):
                # If the line is a trailer, ignore it
                return
            else:
                # if any part of the line couldn't be parsed, don't save
                #  the segments; only save the line as UnparseableData
                return self.unparseable_data(line, e)

    def unparseable_data(self, line, error):
        if len(line) > 2000:
            line = line[:1997] + "..."
        return {"UnparseableData": UnparseableData(
            data_file=self.file_record,
            unparseable_line=line,
            error_description=str(error)
        )}

    def parse_chunk(self, f: io.TextIOWrapper, chunk_size: int) -> dict:
        """
        Given a filestream of a Metro2 file, parse chunk_size lines from it and save
        them to a dict.

        inputs:
        - f: filestream of the Metro2 file
        - chunk_size: the number of lines to parse before returning

        output:
        - a dict with the following keys: AccountActivity,
        extra segment keys (if any were present), and UnparseableData (if any)
        """
        lines_parsed = 0
        parsed_records = None

        while lines_parsed < chunk_size:
            try:
                line = parse_utils.get_next_line(f)
                if not line:
                    # If the file has ended, exit the parser
                    break
                line_results = self.parse_line(line)
            except parse_utils.UnreadableLineException as e:
                # if get_next_line fails, save as unparseable
                line_results = self.unparseable_data("", e)

            if line_results:
                parsed_records = self.prepare_results_for_bulk_save(
                    line_results, parsed_records
                )

            lines_parsed += 1

        return parsed_records

    def prepare_results_for_bulk_save(
        self, line_results: dict, parsed_records: dict = None
    ) -> dict:
        """
        Take the results of parsing a single line (with the parse_line method) and
        add them to a dict of parser results organized by model, so we can use the
        save_values_bulk method on it.
        """
        if not parsed_records:
            parsed_records = {
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
        if "UnparseableData" in line_results:
            parsed_records["UnparseableData"].append(line_results["UnparseableData"])
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

        return parsed_records

    def save_values_bulk(self, values: dict):
        UnparseableData.objects.bulk_create(values["UnparseableData"])
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
        Before exiting, update the file record to show the outcome of the parsing
        process: "Not parsed" (if it errored out) or "Finished" (if it completed
        successfully)

        Inputs:
        `f` - file stream of the data file to be parsed
        `file_size` - the size of the file stream in bytes
        """
        # handle the first line of the file
        try:
            first_line = parse_utils.get_next_line(f)
            self.activity_date = self.handle_first_line_and_return_activity_date(
                first_line
            )
            self.file_record.activity_date = self.activity_date
        except (parse_utils.UnreadableFileException,
                parse_utils.UnreadableLineException) as e:
            # If it fails to parse, record the failure, and
            # don't try to parse the rest of the file
            self.update_file_record(status="Not parsed", msg=str(e))
            return

        # parse the rest of the file until it is done
        while f.tell() < file_size:
            values = self.parse_chunk(f, self.chunk_size)
            if values:
                self.save_values_bulk(values)

        self.update_file_record(status="Finished")
