from django.db.models import Q
from django.db import models


class AccountActivityQuerySet(models.QuerySet):
    def no_bankruptcy_indicators(self):
        return self.exclude(
            Q(j1__cons_info_ind__gt='') | \
            Q(j2__cons_info_ind__gt='') | \
            Q(account_holder__cons_info_ind__gt='')
        )
