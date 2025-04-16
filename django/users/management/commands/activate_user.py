import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Updates a user's is_active flag to True. Use this when " + \
        "an administrator's account has been deactivated, so they can't " + \
        "re-activate it via the admin interface."

    def add_arguments(self, argparser):
        user_help = "The user name (which is usually also the email address) " + \
            "of the user to mark as active."
        argparser.add_argument("-u", "--username", nargs="?", required=True, help=user_help)

    def handle(self, *args, **options):
        logger = logging.getLogger('commands.activate_user')
        User = get_user_model()
        username = options['username']

        usr = User.objects.get(username=username)
        logger.info(f"An existing user account was found for username `{username}`.")
        logger.info("Ensuring the user account is active... ")
        usr.is_active = True
        usr.save()
        logger.info(self.style.SUCCESS(f"Success: `{username}` has been activated."))

