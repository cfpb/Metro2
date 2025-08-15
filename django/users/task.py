import logging

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.utils import timezone

def disable_non_privileged_inactive_users():
    logger = logging.getLogger('users.tasks.disable_non_privileged_inactive_users')
    inactive_users = User.objects.filter(
        last_login__lt=timezone.now() - timedelta(days=90),
        is_active=True, is_superuser=False)
    logger.info(f'Deactivating {inactive_users.count()} non-privileged users.')
    inactive_users.update(is_active=False)

def disable_privileged_inactive_users():
    logger = logging.getLogger('users.tasks.disable_privileged_inactive_users')
    inactive_users = User.objects.filter(
        last_login__lt=timezone.now() - timedelta(days=45),
        is_active=True, is_superuser=True)
    logger.info(f'Deactivating {inactive_users.count()} privileged users.')
    inactive_users.update(is_active=False)

def clear_expired_sessions():
    logger = logging.getLogger('users.tasks.clear_expired_sessions')
    logger.info("Removing expired session records from the database.")
    call_command('clearsessions')

def start():
        scheduler = BackgroundScheduler()
        if settings.SSO_ENABLED:
            scheduler.add_job(disable_non_privileged_inactive_users, 'interval', days=1)
            scheduler.add_job(disable_privileged_inactive_users, 'interval', days=1)
        scheduler.add_job(clear_expired_sessions, 'interval', weeks=1)
        scheduler.start()
