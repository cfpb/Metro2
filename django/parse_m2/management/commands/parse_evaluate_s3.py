from django.core.management.base import BaseCommand
from parse_m2.initiate_parsing import parse_files_from_s3_bucket
from parse_m2.models import Metro2Event


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py parse_evaluate_s3 -e [event_name] -d [s3_folder]

    This command will use the S3 connection variables provided in this environment's
    settings file. It will fetch the files from the given directory of this
    environment's S3 bucket, create an Event record, parse the data into the
    database, and run the evaluators on the dataset.
    """
    help = "Starts the parse and evaluate process on a directory of Metro2 files"

    def add_arguments(self, argparser):
        event_help = "A name to identify this event record"
        argparser.add_argument("-e", "--event_name", nargs="?", required=True, help=event_help)
        argparser.add_argument("-d", "--s3_directory", nargs="?", required=True)

    def handle(self, *args, **options):
        event_name = options["event_name"]
        s3_directory = options["s3_directory"]

        self.stdout.write(
            f"Beginning event `{event_name}`. Parsing files from S3 bucket in {s3_directory} directory.")

        event_record: Metro2Event = parse_files_from_s3_bucket(event_name, s3_directory)

        self.stdout.write(
            self.style.SUCCESS(f"Created event ID: {event_record.id}. Finished parsing data for event: {event_name}.")
        )

        # self.stdout.write(f"Beginning evaluators for {event_name}.")
        # run_evaluators(event_record)
        # self.stdout.write(
        #     self.style.SUCCESS(f"Finished running evaluators for {event_name} and saving results.")
        # )
