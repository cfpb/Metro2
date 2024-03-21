from datetime import datetime
from rest_framework import status

def get_users_not_found_exception(user_id: str, path: str):
    msg = f'User ID: {user_id} does not exist.'

    error= {
        'timestamp': datetime.now(),
        'status': status.HTTP_404_NOT_FOUND,
        'error': 'Not Found',
        'message': msg,
        'path': path
    }

    return error