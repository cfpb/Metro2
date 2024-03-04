from datetime import datetime
from rest_framework import status

def get_evaluate_m2_not_found_exception(
        error:str, id: str, name: str, path: str):
    msg = ''

    if 'Metro2Event' in error:
        msg = f'Event ID: {id} does not exist.'
    elif 'EvaluatorMetadata' in error:
        msg = f'Evaluator: {name} does not exist.'
    elif 'AccountActivity' in error:
        msg = f'AccountActivity records not found for account number {id}.'
    else:
        msg = f'Evaluator result does not exist for event ID {id} or evaluator {name}.'
    error= {
        'timestamp': datetime.now(),
        'status': status.HTTP_404_NOT_FOUND,
        'error': 'Not Found',
        'message': msg,
        'path': path
    }

    return error