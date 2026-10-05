import logging

from django.core.management.base import BaseCommand, CommandError

from evaluate_m2.evaluate import Evaluate
from parse_m2.models import Metro2Event


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py resume_evals -e [event_id]
    """
    help =  (
        "Check this event for any evaluators that haven't been run. Run those "
        "evaluators and leave existing results unchanged. This uses the same "
        "evaluator process as the evaluate command, and results in "
        "an EvaluatorResultSummary record for each evaluator "
        "and EvaluatorResult records for each hit. When S3_ENABLED==True, "
        "result files will be saved to the S3 bucket "
        "for evals with >0 hits."
    )

    def add_arguments(self, argparser):
        event_help = "The ID of the event record in the database"
        argparser.add_argument(
            "-e",
            "--event_id",
            nargs="?",
            required=True,
            help=event_help
        )

    def handle(self, *args, **options):
        logger = logging.getLogger('commands.evaluate')
        event_id = options["event_id"]

        # Fetch the Metro2Event
        try:
            event = Metro2Event.objects.get(id=event_id)
        except Metro2Event.DoesNotExist as e:
            # If the event doesn't exist, exit
            raise CommandError(f"No event found with id {event_id}. Exiting.") from e


        # Find which evals have already been run for this event
        evals_done = event.evaluatorresultsummary_set.values('evaluator_id')
        evals_done_names = [item['evaluator_id'] for item in evals_done]

        # Create a dict of evals to run, excluding items in evals_done
        evaluator = Evaluate()  # Instantiate an evaluator
        evals_to_run = {}
        for eval, func in evaluator.evaluators.items():
            if eval not in evals_done_names:
                evals_to_run[eval] = func

        if not evals_to_run:
            logger.info("No evals to run! Exiting.")
            return

        # Set those evals as the only ones to run
        logger.info(f"Evaluators to run: {evals_to_run.keys()}")
        evaluator.evaluators = evals_to_run

        logger.info(f"Resuming evaluators for event: {event_id}...")
        evaluator.run_evaluators(event)
        logger.info(
            self.style.SUCCESS(
                f"Finished remaining evaluators for event ID: {event_id}."
            )
        )
