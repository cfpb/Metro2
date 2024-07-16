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
