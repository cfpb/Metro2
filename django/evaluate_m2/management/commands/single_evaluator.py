import logging

from django.core.management.base import BaseCommand, CommandError
from evaluate_m2.models import EvaluatorResultSummary
from evaluate_m2.evaluate import Evaluate
from parse_m2.models import Metro2Event


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py single_evaluator -e [event_id] -n [evaluator_name]
    """
    help =  "Runs one evaluator on the dataset linked to the Metro2Event record." + \
            "If any EvaluatorResultSummary records exist for this eval for the Metro2Event " + \
            "record, the previous results will be deleted. The evaluate process " + \
            "will create new result records for any hits."

    def add_arguments(self, argparser):
        event_help = "The ID of the event record in the database"
        argparser.add_argument("-e", "--event_id", nargs="?", required=True, help=event_help)
        name_help = "The ID of the eval to run"
        argparser.add_argument("-n", "--eval_name", nargs="?", required=False, help=name_help)

    def handle(self, *args, **options):
        logger = logging.getLogger('commands.single_evaluator')
        event_id = options["event_id"]
        eval_name = options["eval_name"]

        if not eval_name:
            eval_name = "Rating-APD-1"

        # Fetch the Metro2Event
        try:
            event = Metro2Event.objects.get(id=event_id)
        except Metro2Event.DoesNotExist:
            # If the event doesn't exist, exit
            raise CommandError(f"No event found with id {event_id}. Exiting.")

        evaluator = Evaluate()  # Instantiate an evaluator

        # Find the evaluator to run
        try:
            func = evaluator.evaluators[eval_name]
        except KeyError:
            # If it doesn't exist, exit
            raise CommandError(f"No evaluator with name {eval_name}. Exiting.")

        evaluator.evaluators = {eval_name: func}  # Set that eval as the only one to run

        # Delete results of previous evaluator run
        logger.info(f"Checking if EvaluatorResultSummary records exist for event ID: {event_id}.")
        eval_results = EvaluatorResultSummary.objects.filter(event=event, evaluator__id=eval_name)
        if eval_results.exists():
            logger.info("Deleting results from previous run of this evaluator.")
            eval_results.delete()

        logger.info(f"Beginning to run {eval_name}...")
        evaluator.run_evaluators(event)
        logger.info(
            self.style.SUCCESS(f"Finished running evaluator {eval_name} for event ID: {event_id} and saving results.")
        )
