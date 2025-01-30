import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist. "

    def add_arguments(self, parser):
        parser.add_argument('--username', help="Admin's username")
        parser.add_argument('--password', help="Admin's password")

    def handle(self, *args, **options):
        logger = logging.getLogger('commands.generate_admin_user')
        User = get_user_model()
        username = options['username']

        try:
            usr = User.objects.get(username=username)
            logger.info(f"An existing user account was found for username `{username}`.")
            logger.info("Ensuring the user account has admin permissions... ")
            usr.is_active = True
            usr.is_staff = True
            usr.is_superuser = True
            usr.save()
            logger.info("Done.")
        except User.DoesNotExist:
            logger.info(f"Creating admin user account for username `{username}`... ")
            usr = User.objects.create_superuser(username=username,
                                                email='', password=options['password'])
            logger.info("Done.")
        logger.info(f"Admin user ID: {usr.id}.")

        logger.info(self.style.SUCCESS(f"Success: Admin user `{username}` exists."))
