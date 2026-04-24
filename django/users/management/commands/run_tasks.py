import datetime
import logging

from django.core.management.base import BaseCommand

from users.task import (
    clear_expired_sessions,
    disable_non_privileged_inactive_users,
    disable_privileged_inactive_users,
)


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Runs 3 recurring jobs. Intended to be run daily.\n" +\
        " - Deactivate inactive users (privileged)\n" + \
        " - Deactivate inactive users (non-privileged)\n" + \
        " - Clear expired Django sessions (only runs on Mondays)"

    def handle(self, *args, **options):
        logger.info("Starting tasks...")
        disable_non_privileged_inactive_users()
        disable_privileged_inactive_users()
        if datetime.date.today().weekday() == 0:
            clear_expired_sessions()

        logger.info(
            self.style.SUCCESS("Finished running all tasks.")
        )
