import zipfile
import os
import logging

from parse_m2.m2_parser import M2FileParser
from parse_m2.models import Metro2Event
from parse_m2.parse_utils import file_type_valid, zip_file


############################################
# Methods for parsing files from the local filesystem
def parse_local_file(event: Metro2Event, filepath):
    logger = logging.getLogger('parse_m2.parse_local_file')

    # Instantiate a parser
    parser = M2FileParser(event, f"local:{filepath}")

    logger.debug(f"Parsing local file: {filepath}")
    try:
        fstream = open(filepath, 'r')
        file_size = os.path.getsize(filepath)
        # Parse the file
        parser.parse_file_contents(fstream, file_size)
        logger.info(f'File {os.path.basename(fstream.name)} written to database.')
    except FileNotFoundError as e:
        logger.error(f"There was an error opening the file: {e}")
    finally:
        if fstream:
            fstream.close()

def parse_zip_file(zip_path: str, event: Metro2Event):
    logger = logging.getLogger('parse_m2.parse_zipfile')
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for f in zipf.filelist:
            filename = f.filename
            logger.info(f"Encountered file in zipfile: {filename}")
            if file_type_valid(filename):
                parser = M2FileParser(event, f"local:ZIP:{zip_path}:{filename}")
                fstream = zipf.open(filename)
                file_size = f.file_size
                parser.parse_file_contents(fstream, file_size)
                logger.info(f"file written to db")
            else:
                logger.info(f"Skipping file within zip. Does not match an allowed file type.")


def parse_files_from_local_filesystem(event_identifier: str, data_directory: str) -> Metro2Event:
    logger = logging.getLogger('parse_m2.parse_files_from_local_filesystem')

    # Create a new Metro2Event. All records parsed will be associated with this Event.
    event = Metro2Event(name=event_identifier)
    event.save()

    # iterate over files in LOCAL_EVENT_DATA directory
    for filename in os.listdir(data_directory):
        logger.info(f"Encountered file in local data path: {filename}")
        filepath = os.path.join(data_directory, filename)

        if os.path.isfile(filepath):
            if file_type_valid(filename):
                if zip_file(filename):
                    parse_zip_file(filepath, event)
                else:
                    parse_local_file(event, filepath)
            else:
                logger.info(f"Skipping. Does not match an allowed file type.")

    return event
