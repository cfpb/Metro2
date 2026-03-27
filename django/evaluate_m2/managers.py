from django.db import models
from django.db.models import Q


class AccountActivityQuerySet(models.QuerySet):
    def no_previous_bankruptcy_indicators(self):
        return self.filter((
                Q(previous_values__cons_info_ind_assoc__exact=[]) |
                Q(previous_values__cons_info_ind_assoc__isnull=True)
            ) & Q(previous_values__cons_info_ind='')
        )
