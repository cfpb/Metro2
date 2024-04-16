from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist. " + \
           "Adds the user to a permissions group given by the --group argument"

    def add_arguments(self, parser):
        parser.add_argument('--username', help="Admin's username")
        parser.add_argument('--password', help="Admin's password")
        parser.add_argument('--group', help="Auth group to add the user to")

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        group_name = options['group']

        try:
            usr = User.objects.get(username=username)
            self.stdout.write(f"An existing user account was found for username `{username}`.")
            self.stdout.write("Ensuring the user account has admin permissions... ", ending="")
            usr.is_active = True
            usr.is_staff = True
            usr.is_superuser = True
            usr.save()
            self.stdout.write("Done.")
        except User.DoesNotExist:
            self.stdout.write(f"Creating admin user account for username `{username}`... ", ending="")
            usr = User.objects.create_superuser(username=username,
                                                email='', password=options['password'])
            self.stdout.write("Done.")
        self.stdout.write(f"Admin user ID: {usr.id}.")

        try:
            grp = Group.objects.get(name=group_name)
            self.stdout.write(f"Auth group exists with name {group_name}.")
        except Group.DoesNotExist:
            grp = Group.objects.create(name=group_name)
            self.stdout.write(f"Created auth group with name {group_name}.")

        self.stdout.write(f"Adding user `{username}` to group `{group_name}`.")
        usr.groups.add(grp)
        self.stdout.write(self.style.SUCCESS(f"Success: Admin user `{username}` exists with correct group permissions."))
