from django.conf import settings
from django.http import JsonResponse

from rest_framework.pagination import PageNumberPagination


class EvaluatorResultsPaginator(PageNumberPagination):
    page_size = settings.M2_RESULT_SAMPLE_SIZE

    def get_paginated_response(self, data):
        return JsonResponse({
            "count": self.page.paginator.count,
            "hits": data
        })

