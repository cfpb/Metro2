from django.core.management.base import BaseCommand
from evaluate_m2.models import EvaluatorResultSummary
from evaluate_m2.evaluate import evaluator
from parse_m2.models import Metro2Event


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py run_evaluators -e [event_ID]

    This command will run the evaluators on a dataset associated to an event,
    creates an EvaluatorResultSummary record for each evaluator that has a hit, and an EvaluatorResult record for each item returned from the evaluator.
    """
    help =  "Starts the evaluate process on the dataset linked to the Metro2Event " + \
            "record. Creates a new EvaluatorResultSummary record for each evaluator " + \
            "that returns a results list, and EvaluatorResult records for each item " + \
            "in the results list."

    def add_arguments(self, argparser):
        event_help = "An ID to identify this event record"
        argparser.add_argument("-e", "--event_ID", nargs="?", required=True, help=event_help)

    def handle(self, *args, **options):
        event_ID = options["event_ID"]

        self.stdout.write(f"Retrieve the Metro2Event record for event ID: {event_ID}.")
        if Metro2Event.objects.filter(pk=event_ID).exists():
            event_record: Metro2Event = Metro2Event.objects.get(pk=event_ID)
            self.stdout.write(f"Checking if EvaluatorResultSummary records exist for event ID: {event_ID}.")
            if EvaluatorResultSummary.objects.filter(event=event_record).exists():
                self.stdout.write(f"Deleting results from previous run for event ID:{event_ID}.")
                EvaluatorResultSummary.objects.filter(event=event_record).delete()

            self.stdout.write(f"Beginning evaluators for event: {event_record.name}.")
            evaluator.run_evaluators(event_record)
            self.stdout.write(
                self.style.SUCCESS(f"Finished running evaluators for event ID: {event_ID} and saving results.")
            )
        else:
            self.stdout.write(f"No Metro2Event record for: {event_ID}.")
