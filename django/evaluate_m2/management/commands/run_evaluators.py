from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from evaluate_m2.models import EvaluatorResultSummary
from evaluate_m2.evaluate import evaluator
from parse_m2.models import Metro2Event



class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py run_evaluators -e [event_id]

    This command will run the evaluators on a dataset associated to an event,
    creates an EvaluatorResultSummary record for each evaluator that has a hit, and an EvaluatorResult record for each item returned from the evaluator.
    """
    help =  "Starts the evaluate process on the dataset linked to the Metro2Event " + \
            "record. If an EvaluatorResultSummary record exists for the Metro2Event " + \
            "record, the previous results will be deleted. The evaluate process " + \
            "will continue and create a new EvaluatorResultSummary record for " + \
            "each evaluator that returns a result list, and EvaluatorResult records " + \
            "for each item in the results list."

    def add_arguments(self, argparser):
        event_help = "The ID of the event record in the database"
        argparser.add_argument("-e", "--event_id", nargs="?", required=True, help=event_help)

    def handle(self, *args, **options):
        event_id = options["event_id"]

        self.stdout.write(f"Retrieve the Metro2Event record for event ID: {event_id}.")
        try:
            event_record: Metro2Event = Metro2Event.objects.get(pk=event_id)
            self.stdout.write(f"Checking if EvaluatorResultSummary records exist for event ID: {event_id}.")

            event_results = EvaluatorResultSummary.objects.filter(event=event_record)
            if event_results.exists():
                self.stdout.write(f"Deleting results of {event_results.count()} evaluators from previous run of this event.")
                event_results.delete()

            self.stdout.write(f"Beginning evaluators for event: {event_record.name}.")
            evaluator.run_evaluators(event_record)
            self.stdout.write(
                self.style.SUCCESS(f"Finished running evaluators for event ID: {event_id} and saving results.")
            )
        except ObjectDoesNotExist:
            self.stdout.write(f"No Metro2Event record for: {event_id}.")
