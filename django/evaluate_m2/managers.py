from django.db.models import Q
from django.db import models


class AccountActivityQuerySet(models.QuerySet):
    def no_bankruptcy_indicators(self):
        return self.filter((
                Q(previous_values__account_holder__cons_info_ind_assoc__exact=[]) |
                Q(previous_values__account_holder__cons_info_ind_assoc__isnull=True)
            ) & Q(previous_values__account_holder__cons_info_ind='')
        )
