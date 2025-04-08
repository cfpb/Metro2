from unittest import mock

from django.test import SimpleTestCase

from evaluate_m2.filters import (
    AnyCharFilter,
)


class AnyCharFilterTestCase(SimpleTestCase):
    def test_filtering(self):
        qs = mock.Mock(spec=["filter"])
        f = AnyCharFilter()
        result = f.filter(qs, ["value", "blank", "other"])
        qs.filter.assert_called_once_with(None__in=["value", "", "other"])
        self.assertNotEqual(qs, result)
