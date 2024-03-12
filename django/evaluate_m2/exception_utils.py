from datetime import datetime
from rest_framework import status

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
    else:
        msg = f'Evaluator result does not exist for event ID {event_id} or evaluator ID {evaluator_id}.'
    error= {
        'timestamp': datetime.now(),
        'status': status.HTTP_404_NOT_FOUND,
        'error': 'Not Found',
        'message': msg,
        'path': path
    }

    return error