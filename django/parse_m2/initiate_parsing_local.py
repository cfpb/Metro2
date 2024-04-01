import zipfile
import os
import logging

from parse_m2.m2_parser import M2FileParser
from parse_m2.models import Metro2Event
from parse_m2.parse_utils import data_file, zip_file, get_extension


############################################
# Methods for parsing files from the local filesystem
def parse_local_file(event: Metro2Event, filepath):
    logger = logging.getLogger('parse_m2.parse_local_file')

    # Instantiate a parser
    parser = M2FileParser(event, f"local:{filepath}")

    logger.debug(f"Parsing local file: {filepath}")
    try:
        with open(filepath, 'r') as fstream:
            file_size = os.path.getsize(filepath)
            # Parse the file
            parser.parse_file_contents(fstream, file_size)
            logger.info(f'File {os.path.basename(fstream.name)} written to database.')
    except FileNotFoundError as e:
        logger.error(f"There was an error opening the file: {e}")

def parse_zip_file(zip_path: str, event: Metro2Event):
    logger = logging.getLogger('parse_m2.parse_zipfile')
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for f in zipf.filelist:
            filename = f.filename
            logger.info(f"Encountered file in zipfile: {filename}")
            full_name = f"local:ZIP:{zip_path}:{filename}"
            parser = M2FileParser(event, full_name)
            if not f.is_dir():
                if data_file(filename):
                    with zipf.open(filename) as fstream:
                        logger.debug(f"Parsing file {full_name}...")
                        parser.parse_file_contents(fstream, f.file_size)
                        logger.info("file written to db")
                else:
                    file_ext = get_extension(filename)
                    error_message = f"File skipped because of invalid file extension: .{file_ext}"
                    parser.record_unparseable_file(error_message)
                    logger.info("Skipping file within zip. Does not match an allowed file type.")


def parse_files_from_local_filesystem(event_identifier: str, data_directory: str) -> Metro2Event:
    """
    Create a Metro2Event record. Parse all files in the <data_directory> folder
    in the local filesystem and save them to the event. For any files that look like
    zip files, iterate through each file in the zip and parse each one.

    Return the Metro2Event file associated with the parsed records.
    """
    logger = logging.getLogger('parse_m2.parse_files_from_local_filesystem')

    # Create a new Metro2Event. All records parsed will be associated with this Event.
    event = Metro2Event(name=event_identifier)
    event.save()

    # iterate over files in LOCAL_EVENT_DATA directory
    for filename in os.listdir(data_directory):
        logger.info(f"Encountered file in local data path: {filename}")
        filepath = os.path.join(data_directory, filename)

        if os.path.isfile(filepath):
            if zip_file(filename):
                parse_zip_file(filepath, event)
            elif data_file(filename):
                parse_local_file(event, filepath)
            else:
                file_ext = get_extension(filename)
                error_message = f"File skipped because of invalid file extension: .{file_ext}"
                M2FileParser(event, filepath).record_unparseable_file(error_message)
                logger.info("Skipping. Does not match an allowed file type.")

    return event
