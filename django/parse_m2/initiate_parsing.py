import os
import logging
from django.conf import settings

from parse_m2.m2_parser import M2FileParser
from parse_m2.models import Metro2Event


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


def parse_files_from_local_filesystem(event_identifier: str, data_directory: str = settings.LOCAL_EVENT_DATA):
    logger = logging.getLogger('parse_m2.parse_files_from_local_filesystem')

    # Create a new Metro2Event. All records parsed will be associated with this Event.
    event = Metro2Event(name=event_identifier)
    event.save()

    # iterate over files in LOCAL_EVENT_DATA directory
    for filename in os.listdir(data_directory):
        logger.info(f"Encountered file in local data path: {filename}")
        filepath = os.path.join(data_directory, filename)

        # Only use files ending in .txt
        if os.path.isfile(filepath) and filename.lower().endswith('.txt'):
            parse_local_file(event, filepath)
