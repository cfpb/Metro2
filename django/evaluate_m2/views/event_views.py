import logging

from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from evaluate_m2.exception_utils import (
    get_evaluate_m2_not_found_exception,
)
from evaluate_m2.models import (
    EvaluatorResultSummary,
)
from evaluate_m2.serializers import (
    EventsViewSerializer,
)
from evaluate_m2.views.views_utils import (
    has_permissions_for_request,
)
from parse_m2.models import Metro2Event

@api_view()
def events_view(request, event_id):
    logger = logging.getLogger("views.evaluator_results_view")
    try:
        event = Metro2Event.objects.get(id=event_id)
        if not has_permissions_for_request(request, event):
            return HttpResponse("Unauthorized", status=401)

        eval_result_summaries = (
            EvaluatorResultSummary.objects.filter(event=event, hits__gt=0)
            .select_related("evaluator")
            .order_by("evaluator__id")
        )
        evaluator_metadata_serializer = EventsViewSerializer(
            eval_result_summaries, many=True, context={"event": event}
        )
        result = {
            "id": event.id,
            "name": event.name,
            "portfolio": event.portfolio,
            "eid_or_matter_num": event.eid_or_matter_num,
            "other_descriptor": event.other_descriptor,
            "directory": event.directory,
            "date_range_start": event.date_range_start,
            "date_range_end": event.date_range_end,
            "total_tradelines": event.total_tradelines,
            "total_accounts": event.total_accounts,
            "evaluators": evaluator_metadata_serializer.data,
        }
        return Response(result)
    except (Metro2Event.DoesNotExist, EvaluatorResultSummary.DoesNotExist) as e:
        error = get_evaluate_m2_not_found_exception(
            str(e), event_id, None, request.path
        )
        logger.error(error["message"])
        return Response(error, status=status.HTTP_404_NOT_FOUND)
