import logging
from zipfile import ZipInfo, ZipFile

from parse_m2.models import Metro2Event
from parse_m2.m2_parser import M2FileParser


def data_file(filename: str) -> bool:
    data_file_extensions = ['txt']
    return get_extension(filename) in data_file_extensions

def zip_file(filename: str) -> bool:
    zip_file_extensions = ['zip']
    return get_extension(filename) in zip_file_extensions

def get_extension(filename: str) -> str:
    return filename.split('.')[-1].lower()

def parse_file_from_zip(f: ZipInfo, zip_file: ZipFile, full_name: str, event: Metro2Event):
    logger = logging.getLogger('parse_m2.parse_file_from_zip')
    filename = f.filename
    logger.info(f"Encountered file in zipfile: {filename}")
    if not f.is_dir():
        parser = M2FileParser(event, full_name)
        if data_file(filename):
            try:
                with zip_file.open(filename) as fstream:
                    logger.debug(f"Parsing file {full_name}...")
                    parser.parse_file_contents(fstream, f.file_size)
                    logger.info("file written to db")
            except NotImplementedError as e:
                parser.update_file_record(status="Not parsed", msg=f"File skipped: {e}")
        else:
            file_ext = get_extension(filename)
            error_message = f"File skipped because of invalid file extension: .{file_ext}"
            parser.update_file_record(status="Not parsed", msg=error_message)
            logger.info("Skipping file within zip. Does not match an allowed file type.")

def parsed_file_exists(event: Metro2Event, filename: str) -> bool:
    """
    If the given Metro2Event already has an associated M2DataFile record
    with the given filename, return True. Otherwise return False.

    We use this method to ensure we don't parse duplicate file records
    when adding more files to an existing event, or (future state) when
    the parser is running in parallel in multiple processes.
    """
    file = event.m2datafile_set.filter(file_name=filename)
    return file.exists()

def log_invalid_file_extension(event: Metro2Event, filename: str, skip_existing: bool, logger):
    if parsed_file_exists(event, filename) and skip_existing:
        # If the skip_existing flag is set to True, and this file
        # already exists on this event, don't log it again.
        logger.debug(f"Skipping existing file {filename}, because skip_existing = True")
    else:
        # If no skip_existing flag or it hasn't been logged before, log it.
        error_message = f"File skipped because of invalid file extension: .{get_extension(filename)}"
        M2FileParser(event, filename).update_file_record(status="Not parsed", msg=error_message)
        logger.info("Skipping. Does not match an allowed file type.")
