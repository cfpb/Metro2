import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

def disable_non_privileged_inactive_users():
    logger = logging.getLogger('users.tasks.disable_non_privileged_inactive_users')
    inactive_users = User.objects.filter(
        last_login__lt=timezone.now() - timedelta(days=90),
        is_active=True, is_superuser=False)
    logger.info(f'{inactive_users.count()} non-privileged users will be deactivated and written to the database.')
    inactive_users.update(is_active=False)

def disable_privileged_inactive_users():
    logger = logging.getLogger('users.tasks.disable_privileged_inactive_users')
    inactive_users = User.objects.filter(
        last_login__lt=timezone.now() - timedelta(days=45),
        is_active=True, is_superuser=True)
    logger.info(f'{inactive_users.count()} privileged users will be deactivated and written to the database.')
    inactive_users.update(is_active=False)

def start():
        scheduler = BackgroundScheduler()
        scheduler.add_job(disable_non_privileged_inactive_users, 'interval', days=1)
        scheduler.add_job(disable_privileged_inactive_users, 'interval', days=1)
        scheduler.start()
