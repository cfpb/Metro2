import logging
import os
import zipfile

from parse_m2.initiate_parsing_utils import (
    is_data_file,
    is_zip_file,
    log_invalid_file_extension,
    parse_file_from_zip,
    parsed_file_exists,
)
from parse_m2.m2_parser import M2FileParser
from parse_m2.models import Metro2Event


############################################
# Methods for parsing files from the local filesystem
def parse_local_file(
    event: Metro2Event,
    filepath: str,
    collection: str = None
):
    logger = logging.getLogger('parse_m2.parse_local_file')

    parser = M2FileParser(event, full_name, collection)

    logger.info(f"Parsing local file: {filepath}")
    try:
        with open(filepath) as fstream:
            file_size = os.path.getsize(filepath)
            parser.parse_file_contents(fstream, file_size)
            logger.debug("Parsing completed")
    except FileNotFoundError as e:
        logger.error(f"There was an error opening the file: {e}")

def parse_zip_file_contents(
    zip_path: str, event: Metro2Event, collection: str = None
):
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for f in zipf.filelist:
            full_name = f"local:ZIP:{zip_path}:{f.filename}"

            # If this file already exists on this event, don't parse it again.
            if parsed_file_exists(event, full_name):
                logger = logging.getLogger('parse_m2.local.parse_zip_file_contents')
                logger.debug(f"Skipping existing file {full_name}")
                return

            parse_file_from_zip(f, zipf, full_name, event, collection)

def parse_files_from_local_filesystem(
    event: Metro2Event, directory: str = None, collection: str = None
):
    """
    Parse all files in the local filesystem location indicated by
    event.directory, and save them to event. For any files that look like
    zip files, iterate through each file in the zip and parse each one.

    The parser will not parse a file if one with a matching name already exists.
    """
    logger = logging.getLogger('parse_m2.parse_files_from_local_filesystem')

    data_directory: str = event.directory

    # Iterate over files in the directory
    for filename in os.listdir(data_directory):
        logger.debug(f"Encountered file in local data path: {filename}")
        filepath = os.path.join(data_directory, filename)

        if os.path.isfile(filepath):
            if is_zip_file(filename):
                parse_zip_file_contents(
                    filepath, event, collection
                )
            elif parsed_file_exists(event, file_name_local(filepath)):
                # If this file already exists on this event, don't parse it again.
                logger.debug(
                    f"Skipping existing file {file_name_local(filepath)}"
                )
            elif is_data_file(filename):
                parse_local_file(event, filepath, collection)
            else:
                # If the file is neither zip nor datafile, log an error and skip
                logger.info("Skipping. Does not match an allowed file type.")
                log_invalid_file_extension(event, filename)
