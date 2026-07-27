from datetime import datetime

from rest_framework import status


def format_error(status: int, error_string: str, message: str, path: str):
    return {
        "timestamp": datetime.now(),
        "status": status,
        "error": error_string,
        "message": message,
        "path": path,
    }


def get_evaluate_m2_not_found_exception(
        error_string:str, event_id: str, evaluator_id: str, path: str, acct_num=''):
    msg = ''

    if 'Metro2Event' in error_string:
        msg = f'Event ID: {event_id} does not exist.'
    elif 'EvaluatorMetadata' in error_string:
        msg = f'Evaluator: {evaluator_id} does not exist.'
    elif 'AccountHolder' in error_string:
        msg = f'AccountHolder record(s) not found for account number {acct_num}.'
    elif 'AccountActivity' in error_string:
        msg = f'AccountActivity record(s) not found for account number {acct_num}.'
    elif 'EvaluatorResultSummary' in error_string:
        msg = f'EvaluatorResultSummary record(s) not found for event ID {event_id}.'
    else:
        msg = (
            f'Evaluator result does not exist for event ID {event_id} or '
            f'evaluator ID {evaluator_id}.'
        )

    return format_error(status.HTTP_404_NOT_FOUND, 'Not Found', msg, path)
