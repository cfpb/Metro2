import logging

from smart_open import open
from django.conf import settings

from parse_m2.initiate_parsing_utils import data_file
from parse_m2.parse_utils import is_header_line, get_next_line
from django_application.s3_utils import s3_bucket_files, s3_session


def update_S3_directory_files_format(source_dir: str, destination_dir: str):
    """
    Iterate through the files in the source_dir S3 bucket. For each
    one that looks like a Metro2 file, use the normalize_file_format method
    to generate a new file with updated format. Upload the files to
    destination_dir.
    Parameters:
    - source_dir: the S3 bucket prefix containing the files to normalize
    - destination_dir: the S3 bucket path to save generated files in.
                       Shouldn't end with a slash.
    """
    logger = logging.getLogger("update_files_format")

    if not settings.S3_ENABLED:
        logger.error("S3 must be enabled to use format normalization")
        return

    # Iterate through the bucket directory
    for file in s3_bucket_files(source_dir):
        logger.debug(f"file: {file.key}")

        if data_file(file.key):
            logger.debug("processing...")
            source_fstream = file.get()["Body"]
            destination = destination_path(file.key, destination_dir)
            with open(destination, 'w', transport_params={'client': s3_session()}) as dest_file:
                normalize_file_format(source_fstream, dest_file)

        else:
            # Don't process the file if it obviously isn't a Metro2 file
            # (e.g. zip, docx, or csv file extensions)
            logger.debug("Invalid file extension. Skipping.")

def destination_path(file_key: str, destination_dir: str) -> str:
    # Destination_dir shouldn't end with a slash
    bucket_name = settings.S3_BUCKET_NAME
    return f"s3://{bucket_name}/{destination_dir}/{get_filename(file_key)}"

def get_filename(file_key:str) -> str:
    return file_key.split("/")[-1]

def normalize_file_format(source_fstream, dest_file):
    """
    For a Metro2 file, update each row using the modify_individual_line method.
    If the first row is a header segment, don't update it.
    """
    # If the first row is a header segment, write it as-is to the destination file
    # If not, treat it as a normal row.
    first_line = get_next_line(source_fstream)
    if not is_header_line(first_line):
        first_line = modify_individual_line(first_line)
    dest_file.write(first_line)

    # Next, handle the rest the file. All remaining rows should be base+extra
    # segments (a.k.a normal rows), and therefore safe to modify.
    # (Except the final row, which should be a trailer, which the parser ignores)
    while True:
        line = get_next_line(source_fstream)
        if len(line) == 0:
            break  # if the file has ended, exit
        line = modify_individual_line(line)
        dest_file.write(line)


def modify_individual_line(line) -> str:
    line = off_by_four_correction(line)
    # eventually, we may add more file correction methods here
    # or use options to turn individual modifications on/off
    return line

def off_by_four_correction(line: str):
    """
    This corrects the "off by four" type of malformed row, where the RDW
    column (positions 1-4 of the base segment) is missing. To correct it,
    we shift the row to the right by four characters. This column is not
    used by the parser, so the contents don't matter. We use `....`.

    This correction should only be used on non-header rows. (Since our parser
    ignores trailer rows, it's fine to use it on the trailer.)
    """
    return f"....{line}"
