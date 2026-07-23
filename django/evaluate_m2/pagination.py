from django.conf import settings

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class EvaluatorResultsPaginator(PageNumberPagination):
    page_size = settings.M2_RESULT_SAMPLE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "hits": data
        })
