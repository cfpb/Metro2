import logging
from zipfile import ZipFile, ZipInfo

from parse_m2.m2_parser import M2FileParser
from parse_m2.models import Metro2Event


def is_data_file(filename: str) -> bool:
    data_file_extensions = ['txt']
    return get_extension(filename) in data_file_extensions

def is_zip_file(filename: str) -> bool:
    zip_file_extensions = ['zip']
    return get_extension(filename) in zip_file_extensions

def get_extension(filename: str) -> str:
    return filename.split('.')[-1].lower()

def parse_file_from_zip(
    f: ZipInfo,
    zip_file: ZipFile,
    full_name: str,
    event: Metro2Event,
    collection: str = None
):
    logger = logging.getLogger('parse_m2.parse_file_from_zip')
    filename = f.filename
    logger.debug(f"Encountered file in zipfile: {filename}")
    if not f.is_dir():
        if is_data_file(filename):
            parser = M2FileParser(event, full_name, collection)
            try:
                with zip_file.open(filename) as fstream:
                    logger.info(f"Parsing file {full_name}")
                    parser.parse_file_contents(fstream, f.file_size)
                    logger.debug("Parsing completed.")
            except NotImplementedError as e:
                parser.update_file_record(status="Not parsed", msg=f"File skipped: {e}")
        else:
            log_invalid_file_extension(event, full_name)
            logger.debug(
                "Skipping file within zip. Does not match an allowed file type."
            )

def parsed_file_exists(event: Metro2Event, filename: str) -> bool:
    """
    If the given Metro2Event already has an associated M2DataFile record
    with the given filename, return True. Otherwise return False.

    We use this method to ensure we don't parse duplicate file records
    when adding more files to an existing event, or when
    the parser is running in parallel in multiple processes.
    """
    file = event.m2datafile_set.filter(file_name=filename)
    return file.exists()

def log_invalid_file_extension(
    event: Metro2Event, filename: str,
):
    """
    For the given file, create a M2DataFile record with status
    'Not parsed' and informative error message, which will show
    up in the list of files for the event.
    """
    error_message = (
        "File skipped because of invalid file extension: "
        f".{get_extension(filename)}"
    )
    M2FileParser(event, filename).update_file_record(
        status="Not parsed", msg=error_message
    )
