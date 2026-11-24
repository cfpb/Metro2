import logging

from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError

from evaluate_m2.models import EvaluatorResultMaterializedView, EvaluatorResultSummary
from evaluate_m2.views.eval_results_views import EvaluatorResultsFacetsView
from parse_m2.models import Metro2Event


class Command(BaseCommand):
    """
    Run this command by running the following:
    > python manage.py initial_filter_counts -e [event_id]
    """
    help =  (
        "If evaluators have been run for this event, this command saves "
        "filter counts for every evaluator that has results. Do this by requesting "
        "the filter facets endpoint for each evaluator, which saves the calculated "
        "values to the Django cache. "
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

        eval_results = EvaluatorResultSummary.objects.filter(event=event, hits__gt=0)
        if eval_results.exists():
            for eval_summary in eval_results:
                self.save_facets(
                    event.id,
                    eval_summary.evaluator_id,
                    logger
                )
        else:
            logger.info(f"No evaluators found with hits for event {event_id}.")

        logger.info(
            self.style.SUCCESS(
                f"Finished caching initial facet counts for event ID: {event_id}."
            )
        )

    def save_facets(self, event_id: int, eval_id: str, logger):
        cache_key = f"/api/events/{event_id}/evaluator/{eval_id}/facets/?"  # noqa: E501
        logger.info(f"Saving facets for {eval_id}.")
        queryset = EvaluatorResultMaterializedView.objects.filter(
            event_id=event_id,
            evaluator_id=eval_id,
        )
        facets = EvaluatorResultsFacetsView.calculate_facets(queryset)
        year_in_seconds = 365 * 24 * 60 * 60
        cache.add(key=cache_key, value=facets, timeout=year_in_seconds)
