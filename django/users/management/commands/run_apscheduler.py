# runapscheduler.py
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from users.task import (
    clear_expired_sessions,
    disable_non_privileged_inactive_users,
    disable_privileged_inactive_users
)

logger = logging.getLogger(__name__)


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way. 
@util.close_old_connections
def delete_old_job_executions(max_age=1_209_600):
  """
  This job deletes APScheduler job execution entries older than `max_age` from the database.
  It helps to prevent the database from filling up with old historical records that are no
  longer useful.
  
  :param max_age: The maximum length of time to retain historical job execution records.
                  Defaults to 14 days.
  """
  DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
  help = "Runs APScheduler."

  def handle(self, *args, **options):
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        disable_non_privileged_inactive_users,
        trigger=CronTrigger(
            hour="00", minute="00"
        ),  # daily at Midnight
        id="non_privileged_users",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added job 'non_privileged_users'.")

    scheduler.add_job(
        disable_privileged_inactive_users,
        trigger=CronTrigger(
            hour="00", minute="05"
        ),  # daily at 12:05am
        id="privileged_users",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added job 'privileged_users'.")

    scheduler.add_job(
        clear_expired_sessions,
        trigger=CronTrigger(
            day_of_week="mon", hour="02", minute="00"
        ),  # 2:00am on Monday
        id="clear_expired_sessions",
        replace_existing=True,
    )
    logger.info("Added job 'clear_expired_sessions'.")

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(
            day_of_week="mon", hour="01", minute="00"
        ),  # 1:00am on Monday
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )
    logger.info(
      "Added weekly job: 'delete_old_job_executions'."
    )

    # Todo: should it remove the jobs when it's not running?

    try:
      logger.info("Starting scheduler...")
      scheduler.start()
    except KeyboardInterrupt:
      logger.info("Stopping scheduler...")
      scheduler.shutdown()
      logger.info("Scheduler shut down successfully!")
