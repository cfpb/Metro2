from django.db.models import Q
from django.db import models


class AccountActivityQuerySet(models.QuerySet):
    def no_bankruptcy_indicators(self):
        return self.filter(
            Q(j1__isnull=True) | Q(j1__cons_info_ind=''),
            Q(j2__isnull=True) | Q(j2__cons_info_ind=''),
            account_holder__cons_info_ind=''
        )
