import logging

from django.core.management.base import BaseCommand

from evaluate_m2.models import EvaluatorResultMaterializedView


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py materialized_view
    """
    help =  (
        "Creates the materialized view that connects with the "
        "EvaluatorResultMaterializedView model, if it doesn't exist. "
        "This is what allows the evaluator results view to work. "
        "If the materialized view does exist, this command refreshes "
        "it to incorporate any new evaluator results."
    )


    def handle(self, *args, **options):
        logger = logging.getLogger('commands.single_evaluator')

        EvaluatorResultMaterializedView.create_or_refresh_materialized_view()

        logger.info(
            self.style.SUCCESS(
                "Success: Evaluator Result materialized view now exists"
                " and contains all evaluator results"
            )
        )