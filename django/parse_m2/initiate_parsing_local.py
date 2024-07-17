import zipfile
import os
import logging

from parse_m2.m2_parser import M2FileParser
from parse_m2.models import Metro2Event
from parse_m2.initiate_parsing_utils import data_file, zip_file, get_extension, parse_file_from_zip, parsed_file_exists


############################################
# Methods for parsing files from the local filesystem
def parse_local_file(event: Metro2Event, filepath: str, skip_existing: bool):
    logger = logging.getLogger('parse_m2.parse_local_file')
    full_name = f"local:{filepath}"

    if skip_existing:
        # If the skip_existing flag is set to True, and this file
        # already exists on this event, don't parse it again.
        if parsed_file_exists(event, full_name):
            return

    # Instantiate a parser
    parser = M2FileParser(event, full_name)

    logger.debug(f"Parsing local file: {filepath}")
    try:
        with open(filepath, 'r') as fstream:
            file_size = os.path.getsize(filepath)
            # Parse the file
            parser.parse_file_contents(fstream, file_size)
            logger.info(f'File {os.path.basename(fstream.name)} written to database.')
    except FileNotFoundError as e:
        logger.error(f"There was an error opening the file: {e}")

def parse_zip_file_contents(zip_path: str, event: Metro2Event, skip_existing: bool):
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for f in zipf.filelist:
            full_name = f"local:ZIP:{zip_path}:{f.filename}"

            if skip_existing:
                # If the skip_existing flag is set to True, and this file
                # already exists on this event, don't parse it again.
                if parsed_file_exists(event, full_name):
                    return

            parse_file_from_zip(f, zipf, full_name, event)

def parse_files_from_local_filesystem(event: Metro2Event, skip_existing: bool = True):
    """
    Parse all files in the local filesystem location indicated by
    event.directory, and save them to event. For any files that look like
    zip files, iterate through each file in the zip and parse each one.

    If skip_existing is True, the parser will not parse a file if one with
    a matching name already exists.
    """
    logger = logging.getLogger('parse_m2.parse_files_from_local_filesystem')

    data_directory: str = event.directory

    # iterate over files in the directory
    for filename in os.listdir(data_directory):
        logger.info(f"Encountered file in local data path: {filename}")
        filepath = os.path.join(data_directory, filename)

        if os.path.isfile(filepath):
            if zip_file(filename):
                parse_zip_file_contents(filepath, event, skip_existing)
            elif data_file(filename):
                parse_local_file(event, filepath, skip_existing)
            else:
                file_ext = get_extension(filename)
                error_message = f"File skipped because of invalid file extension: .{file_ext}"
                M2FileParser(event, filepath).update_file_record(status="Not parsed", msg=error_message)
                logger.info("Skipping. Does not match an allowed file type.")
