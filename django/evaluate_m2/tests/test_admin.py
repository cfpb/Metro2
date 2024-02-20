from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from evaluate_m2.admin import (
    EvaluatorMetadataAdmin,
    EvaluatorResultSummaryAdmin,
    EvaluatorResultAdmin
)
from evaluate_m2.models import (
    EvaluatorMetadata,
    EvaluatorResult,
    EvaluatorResultSummary
)


class MockRequest:
    pass

class EvaluatorMetadataAdminTestCase(TestCase):
    def setUp(self):
        self.request = MockRequest()
        self.ma = EvaluatorMetadataAdmin(EvaluatorMetadata, AdminSite())

    def test_add_permission_is_false(self):
        self.assertFalse(self.ma.has_add_permission(self.request))

    def test_view_permission_is_true(self):
        self.assertTrue(self.ma.has_view_permission(self.request))

    def test_change_permission_is_true(self):
        self.assertTrue(self.ma.has_change_permission(self.request))

    def test_delete_permission_is_false(self):
        self.assertFalse(self.ma.has_delete_permission(self.request))

class EvaluatorResultSummaryAdminTestCase(TestCase):
    def setUp(self):
        self.request = MockRequest()
        self.ma = EvaluatorResultSummaryAdmin(EvaluatorResultSummary, AdminSite())

    def test_add_permission_is_false(self):
        self.assertFalse(self.ma.has_add_permission(self.request))

    def test_view_permission_is_true(self):
        self.assertTrue(self.ma.has_view_permission(self.request))

    def test_change_permission_is_false(self):
        self.assertFalse(self.ma.has_change_permission(self.request))

    def test_delete_permission_is_false(self):
        self.assertFalse(self.ma.has_delete_permission(self.request))

class EvaluatorResultAdminTestCase(TestCase):
    def setUp(self):
        self.request = MockRequest()
        self.ma = EvaluatorResultAdmin(EvaluatorResult, AdminSite())

    def test_add_permission_is_false(self):
        self.assertFalse(self.ma.has_add_permission(self.request))

    def test_view_permission_is_true(self):
        self.assertTrue(self.ma.has_view_permission(self.request))

    def test_change_permission_is_false(self):
        self.assertFalse(self.ma.has_change_permission(self.request))

    def test_delete_permission_is_false(self):
        self.assertFalse(self.ma.has_delete_permission(self.request))
