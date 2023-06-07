from django.contrib.auth.models import Group
from django.db import models


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    user_group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    # etc.

    def __str__(self) -> str:
        return self.name

    def check_access_for_user(self, user) -> bool:
        """
        Utility method for checking authorization. Returns True if
        the user is assigned to the correct user group to have
        access to this dataset.
        """
        return self.user_group in user.groups.all()