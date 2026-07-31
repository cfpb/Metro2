from unittest import mock

from django.db.models import Q
from django.test import SimpleTestCase

from evaluate_m2.filters import (
    AnyCharFilter,
)


class AnyCharFilterTestCase(SimpleTestCase):
    def test_filtering_empty_string(self):
        qs = mock.Mock(spec=["filter"])
        f = AnyCharFilter("test_field")
        expected_q = (
            Q(test_field__isnull=True) |
            Q(test_field__in=["value", "other"])
        )
        result = f.filter(qs, ["value", "blank", "other"])
        qs.filter.assert_called_once_with(expected_q)
        self.assertNotEqual(qs, result)
