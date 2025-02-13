import io

from smart_open import open
from django.conf import settings

from parse_m2.parse_utils import decode_if_needed, is_header_line, get_next_line
from django_application.s3_utils import s3_bucket_files, s3_session


# todo: check that s3 is enabled in settings?
def update_S3_directory_files_format(source_directory: str, destination_dir: str):
    if not settings.S3_ENABLED:
        print("sorry, s3 must be enabled for this to work")
        return

    # Destination_dir shouldn't end with a slash
    for file in s3_bucket_files(source_directory):

        source_fstream = file.get()["Body"]
        dest_path = destination_path(file.key, destination_dir)

        upload_modified_s3_file(source_fstream, dest_path, {'client': s3_session()})

def destination_path(file_key: str, destination_dir: str) -> str:
    # Destination_dir shouldn't end with a slash
    bucket_name = settings.S3_BUCKET_NAME
    return f"s3://{bucket_name}/{destination_dir}/{get_filename(file_key)}"

def get_filename(file_key:str) -> str:
    return file_key.split("/")[-1]

def upload_modified_s3_file(source_fstream, destination: str, transport_params: dict):
    """
    Stream source_file from the S3 bucket. For each row, make any
    corrections needed. Upload the corrected version to destination.
    """
    with open(destination, 'w', transport_params=transport_params) as dest_file:
        # If the first row is a header segment, write it as-is to the destination file
        # If not, treat it as a normal row.
        first_line = get_next_line(source_fstream)
        if not is_header_line(first_line):
            first_line = modify_individual_line(first_line)
        dest_file.write(first_line)

        # Then handle all of the remaining rows of the file. All remaining rows
        # should be base+extra segments (a.k.a normal rows), and safe to modify.
        # (Except the final row, which should be a trailer, which the parser ignores)
        for l in source_fstream:
            line = decode_if_needed(l)
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
