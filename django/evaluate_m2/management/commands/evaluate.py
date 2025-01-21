from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from evaluate_m2.models import EvaluatorResultSummary
from evaluate_m2.evaluate import evaluator
from parse_m2.models import Metro2Event


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py evaluate -e [event_id]

    This command will run the evaluators on a dataset associated to an event,
    creates an EvaluatorResultSummary record for each evaluator that has a hit, and an EvaluatorResult record for each item returned from the evaluator.
    """
    help =  "Starts the evaluate process on the dataset linked to the Metro2Event " + \
            "record. If any EvaluatorResultSummary records exist for the Metro2Event " + \
            "record, the previous results will be deleted. The evaluate process " + \
            "will create a new EvaluatorResultSummary record for each evaluator, " + \
            "and EvaluatorResult records for each hit. When S3_ENABLED==True, " + \
            "result files will be saved to the S3 bucket " + \
            "for evals with >0 hits."

    def add_arguments(self, argparser):
        event_help = "The ID of the event record in the database"
        argparser.add_argument("-e", "--event_id", nargs="?", required=True, help=event_help)

    def handle(self, *args, **options):
        event_id = options["event_id"]

        # Fetch the Metro2Event
        try:
            event = Metro2Event.objects.get(id=event_id)
        except Metro2Event.DoesNotExist:
            # If the event doesn't exist, exit
            raise CommandError(f"No event found with id {event_id}. Exiting.")

        # Delete results of previous evaluator run
        self.stdout.write(f"Checking if EvaluatorResultSummary records exist for event ID: {event_id}.")
        eval_results = EvaluatorResultSummary.objects.filter(event=event)
        if eval_results.exists():
            self.stdout.write(f"Deleting results of {eval_results.count()} evaluators from previous run of this event.")
            eval_results.delete()

        self.stdout.write(f"Beginning evaluators for event: {event.name}...")
        evaluator.run_evaluators(event)
        self.stdout.write(
            self.style.SUCCESS(f"Finished running evaluators for event ID: {event_id} and saving results.")
        )
