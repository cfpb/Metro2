from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

from evaluate_m2.pagination import EvaluatorResultsPaginator


class TestPagination(SimpleTestCase):

    def setUp(self):
        self.paginator = EvaluatorResultsPaginator()
        self.queryset = range(1, 101)
        self.factory = APIRequestFactory()

    def test_paginated_response_no_page_number(self):
        request = Request(self.factory.get("/"))
        queryset = self.paginator.paginate_queryset(self.queryset, request)
        self.assertEqual(queryset, list(range(1, 21)))

        response = self.paginator.get_paginated_response(queryset)
        self.assertJSONEqual(
            str(response.content, encoding=response.charset),
            {
                "count": 100,
                "hits": list(range(1, 21)),
            },
        )

    def test_paginated_response_with_page_number(self):
        request = Request(self.factory.get("/", {"page": 2}))
        queryset = self.paginator.paginate_queryset(self.queryset, request)
        self.assertEqual(queryset, list(range(21, 41)))

        response = self.paginator.get_paginated_response(queryset)
        self.assertJSONEqual(
            str(response.content, encoding=response.charset),
            {
                "count": 100,
                "hits": list(range(21, 41)),
            },
        )


