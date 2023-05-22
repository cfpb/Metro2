from django.contrib.auth.models import Group
from django.db import models


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    user_group = models.ForeignKey(Group, blank=True, on_delete=models.CASCADE)
    # etc.

    def __str__(self) -> str:
        return self.name