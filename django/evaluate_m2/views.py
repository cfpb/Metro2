import csv
import json
import logging
import botocore

from datetime import date
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import get_list_or_404
from django.core.exceptions import FieldError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django_application.s3_utils import s3_session
from evaluate_m2.views_utils import (
    get_object,
    has_permissions_for_request,
)
from evaluate_m2.exception_utils import get_evaluate_m2_not_found_exception
from evaluate_m2.models import EvaluatorMetadata, EvaluatorResult, EvaluatorResultSummary
from evaluate_m2.serializers import (
    EvaluatorMetadataSerializer,
    EventsViewSerializer)
from evaluate_m2 import upload_utils
from parse_m2.models import AccountActivity, AccountHolder, Metro2Event
from parse_m2.serializers import AccountActivitySerializer, AccountHolderSerializer


@api_view(('GET',))
def download_evaluator_metadata_csv(request):
    # Documentation on returning CSV: https://docs.djangoproject.com/en/4.2/howto/outputting-csv/
    filename = f"evaluator-metadata-{date.today()}.csv"
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

    eval_metadata_serializer = EvaluatorMetadataSerializer(
        EvaluatorMetadata.objects.all(), many=True
    )
    header = EvaluatorMetadataSerializer.Meta.fields
    # Add the header to the CSV response
    writer = csv.DictWriter(response, fieldnames=header)
    writer.writeheader()

    # Add all evaluators to the response
    for row in eval_metadata_serializer.data:
        writer.writerow(row)

    return response

@api_view(('GET',))
def download_evaluator_results_csv(request, event_id, evaluator_id):
    logger = logging.getLogger('views.download_evaluator_results_csv')
    try:
        event = Metro2Event.objects.get(id=event_id)
        evaluator = EvaluatorMetadata.objects.get(id=evaluator_id)
        eval_result_summary = EvaluatorResultSummary.objects.get(
            event=event, evaluator=evaluator)

        if not has_permissions_for_request(request, event):
            return HttpResponse('Unauthorized', status=401)

        if settings.S3_ENABLED:
            return fetch_csv_results_from_s3(request, event_id, evaluator_id)

        # TODO: fall back on generating the response if the fetch from S3 fails
        else:
            filename = f"{event.name}_{evaluator.id}.csv"
            response = HttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
            return upload_utils.generate_full_csv(eval_result_summary, response)
    except (
        Metro2Event.DoesNotExist,
        EvaluatorMetadata.DoesNotExist,
        EvaluatorResultSummary.DoesNotExist
    ) as e:
        error = get_evaluate_m2_not_found_exception(
            str(e), event_id, evaluator_id, request.path)
        logger.error(error['message'])
        return Response(error, status=status.HTTP_404_NOT_FOUND)

@api_view()
def evaluator_results_view(request, event_id, evaluator_id):
    logger = logging.getLogger('views.evaluator_results_view')
    try:
        event = Metro2Event.objects.get(id=event_id)
        evaluator = EvaluatorMetadata.objects.get(id=evaluator_id)
        eval_result_summary = EvaluatorResultSummary.objects.get(
            event=event, evaluator=evaluator)

        if not has_permissions_for_request(request, event):
            return HttpResponse('Unauthorized', status=401)

        if settings.S3_ENABLED:
            return fetch_json_results_from_s3(request, event_id, evaluator_id)

        # TODO: fall back on generating the response if the fetch from S3 fails
        else:
            records = event.get_all_account_activity()
            sample_json = upload_utils.generate_json_sample(eval_result_summary, records)
            return JsonResponse(sample_json)

    except (
        Metro2Event.DoesNotExist,
        EvaluatorMetadata.DoesNotExist,
        EvaluatorResultSummary.DoesNotExist
    ) as e:
        error = get_evaluate_m2_not_found_exception(
            str(e), event_id, evaluator_id, request.path)
        logger.error(error['message'])
        return Response(error, status=status.HTTP_404_NOT_FOUND)
    except FieldError as e:
        # TODO: update the metadata importer to ensure that
        # result_summary_fields are always valid AccountActivity field names
        err = f"Metadata for {evaluator.id} has incorrect field name: {e}"
        return Response(err, status=status.HTTP_404_NOT_FOUND)

@api_view(('GET',))
def account_summary_view(request, event_id, account_number):
    logger = logging.getLogger('views.account_summary_view')
    try:
        event = Metro2Event.objects.get(id=event_id)
        if not has_permissions_for_request(request, event):
            return HttpResponse('Unauthorized', status=401)
        event_activities=get_list_or_404(event.get_all_account_activity().filter(
            cons_acct_num=account_number).order_by('activity_date'))
        if not event_activities:
            raise Http404()
        activities_serializer = AccountActivitySerializer(event_activities, many=True)
        eval_results = EvaluatorResult.objects.filter(
            acct_num=account_number,
            result_summary__event=event)
        eval_metadata=[]
        for e in eval_results:
            eval=e.result_summary.evaluator.id
            if eval not in eval_metadata:
                eval_metadata.append(eval)
        data = {'cons_acct_num': account_number,
                'inconsistencies': eval_metadata,
                'account_activity': activities_serializer.data}
        return JsonResponse(data)
    except (
        Http404,
        Metro2Event.DoesNotExist,
        EvaluatorMetadata.DoesNotExist,
        EvaluatorResult.DoesNotExist,
        AccountActivity.DoesNotExist
    ) as e:
        error = get_evaluate_m2_not_found_exception(
            str(e), event_id, None, request.path, account_number)
        logger.error(error['message'])
        return Response(error, status=status.HTTP_404_NOT_FOUND)

@api_view(('GET',))
def account_pii_view(request, event_id, account_number):
    logger = logging.getLogger('views.account_pii_view')
    try:
        event = Metro2Event.objects.get(id=event_id)
        if not has_permissions_for_request(request, event):
            return HttpResponse('Unauthorized', status=401)
        latest_acct_activity = AccountActivity.objects.filter(
            data_file__event=event,
            cons_acct_num=account_number).latest('activity_date')
        result = latest_acct_activity.account_holder
        acct_holder_serializer = AccountHolderSerializer(result)
        return JsonResponse(acct_holder_serializer.data)
    except (
        Metro2Event.DoesNotExist,
        AccountHolder.DoesNotExist
    ) as e:
        error = get_evaluate_m2_not_found_exception(
            str(e), event_id, None, request.path, account_number)
        logger.error(error['message'])
        return Response(error, status=status.HTTP_404_NOT_FOUND)

@api_view()
def events_view(request, event_id):
    logger = logging.getLogger('views.evaluator_results_view')
    try:
        event = Metro2Event.objects.get(id=event_id)
        if not has_permissions_for_request(request, event):
            return HttpResponse('Unauthorized', status=401)
        eval_result_summary = EvaluatorResultSummary.objects \
            .filter(event=event, hits__gt=0).order_by('evaluator__id')
        evaluators = [ers.evaluator for ers in eval_result_summary]
        evaluator_metadata_serializer = EventsViewSerializer(
            evaluators, many=True, context={'event': event})
        result = {
            'id': event.id,
            'name': event.name,
            'portfolio': event.portfolio,
            'eid_or_matter_num': event.eid_or_matter_num,
            'other_descriptor': event.other_descriptor,
            'directory': event.directory,
            'date_range_start': event.date_range_start,
            'date_range_end': event.date_range_end,
            'evaluators': evaluator_metadata_serializer.data
        }
        return JsonResponse(result)
    except (
        Metro2Event.DoesNotExist,
        EvaluatorResultSummary.DoesNotExist
    ) as e:
        error = get_evaluate_m2_not_found_exception(
            str(e), event_id, None, request.path)
        logger.error(error['message'])
        return Response(error, status=status.HTTP_404_NOT_FOUND)

###########################################
## Helper methods for eval results when S3_ENABLED == True
def fetch_csv_results_from_s3(request, event_id, evaluator_id):
    logger = logging.getLogger('views.fetch_csv_results_from_s3')
    filename = upload_utils.s3_filename(evaluator_id, "csv")
    key = upload_utils.s3_bucket_key(event_id, evaluator_id, "csv")
    try:
        response = StreamingHttpResponse(
            get_object(s3_session(), settings.S3_BUCKET_NAME, key),
            status=200,
            content_type="text/csv",
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            error = get_evaluate_m2_not_found_exception(
            e.response['Error']['Message'], event_id, evaluator_id, request.path, None)
            logger.error(error['message'])
            return Response(error, status=status.HTTP_404_NOT_FOUND)

def fetch_json_results_from_s3(request, event_id, evaluator_id):
    logger = logging.getLogger('views.fetch_json_results_from_s3')
    s3 = s3_session()
    key = upload_utils.s3_bucket_key(event_id, evaluator_id, "json")
    try:
        file = s3.get_object(Bucket=settings.S3_BUCKET_NAME, Key=key)
        file_data = file['Body'].read().decode('utf-8')
        return JsonResponse(json.loads(file_data))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            error = get_evaluate_m2_not_found_exception(
            e.response['Error']['Message'], event_id, evaluator_id, request.path, None)
            logger.error(error['message'])
            return Response(error, status=status.HTTP_404_NOT_FOUND)
