import logging
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management import call_command
from django.utils import timezone

from django_apscheduler import util


@util.close_old_connections
def disable_non_privileged_inactive_users():
    logger = logging.getLogger('users.tasks.disable_non_privileged_inactive_users')
    inactive_users = User.objects.filter(
        last_login__lt=timezone.now() - timedelta(days=90),
        is_active=True, is_superuser=False)
    logger.info(f'Deactivating {inactive_users.count()} non-privileged users.')
    inactive_users.update(is_active=False)

@util.close_old_connections
def disable_privileged_inactive_users():
    logger = logging.getLogger('users.tasks.disable_privileged_inactive_users')
    inactive_users = User.objects.filter(
        last_login__lt=timezone.now() - timedelta(days=45),
        is_active=True, is_superuser=True)
    logger.info(f'Deactivating {inactive_users.count()} privileged users.')
    inactive_users.update(is_active=False)

@util.close_old_connections
def clear_expired_sessions():
    logger = logging.getLogger('users.tasks.clear_expired_sessions')
    logger.info("Removing expired session records from the database.")
    call_command('clearsessions')
