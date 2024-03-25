import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument('--username', help="Admin's username")
        parser.add_argument('--email', help="Admin's email")
        parser.add_argument('--password', help="Admin's password")
        parser.add_argument('--no-input', help="Read options from the environment",
                            action='store_true')

    def handle(self, *args, **options):
        User = get_user_model()

        if not User.objects.filter(username=options['username']).exists():
            self.stdout.write(f"An admin user account was not found for username: {options['username']}")
            User.objects.create_superuser(username=options['username'],
                                          email=options['email'],
                                          password=options['password'])
            self.stdout.write(
                self.style.SUCCESS(f"Finished creating admin user with username: {options['username']}.")
            )
        else:
            self.stdout.write(f"An existing admin user account was found for username: {options['username']}")