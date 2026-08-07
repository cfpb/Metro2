import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from evaluate_m2.evaluate import evaluator
from evaluate_m2.models import EvaluatorResultMaterializedView
from parse_m2.initiate_parsing_local import parse_files_from_local_filesystem
from parse_m2.initiate_post_parsing import post_parse
from parse_m2.models import Metro2Event


class Command(BaseCommand):
    """
    This command will check if an Event record has been created for the provided
    event_name.  If it does not exist, it will call the command that will fetch the
    files from the given directory, create an Event record and parse the data into the
    database. Then will call the command to run the evaluators.
    """
    default_location = settings.LOCAL_EVENT_DATA
    help = (
        "This command is used to add sample data in local development "
        "environments. It will create a new Metro2Event record with the "
        "provided event name if it does not exist or will quit if it exists."
    )

    def add_arguments(self, argparser):
        event_help = "A name to identify this event record"
        argparser.add_argument(
            "-e",
            "--event_name",
            nargs="?",
            required=True,
            help=event_help
        )

        dir_help = (
            "Location is relative to the `/django` directory. "
            "Defaults to the LOCAL_EVENT_DATA setting in this environment: "
        ) + str(self.default_location)
        argparser.add_argument(
            "-d",
            "--data_directory",
            nargs="?",
            required=False,
            help=dir_help
        )

    def handle(self, *args, **options):
        logger = logging.getLogger('commands.single_evaluator')
        event_name = options["event_name"]
        data_directory = options["data_directory"]

        if not data_directory:
            logger.info(
                "Using default file location for Metro2 files: "
                f"`{self.default_location}`."
            )
            data_directory = self.default_location

        if Metro2Event.objects.filter(name=event_name).exists():
            logger.info(
                f"An event record already exists for event name: {event_name}. No "
                "new seed data will be added."
            )
            # Still make sure the evaluator results materialized view exists.
            EvaluatorResultMaterializedView.create_or_refresh_materialized_view()

        else:
            # Create a new Metro2Event. All records parsed will be associated
            # with this event.
            event = Metro2Event(name=event_name, directory=data_directory)
            event.save()
            logger.info(
                f"Created an event record with name {event_name}. ID: {event.id}"
            )

            logger.info(
                f"Parsing files from local filesystem in `{data_directory}` directory."
            )
            parse_files_from_local_filesystem(event)

            logger.info(f"Beginning post parsing process for event: {event.name}.")
            post_parse(event)
            logger.info(f"Beginning evaluators for event: {event.name}.")
            evaluator.run_evaluators(event)
            logger.info(
                self.style.SUCCESS("Finished running evaluators and saving results."))
