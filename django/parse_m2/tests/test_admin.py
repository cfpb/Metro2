
from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from parse_m2.admin import (
    AccountHolderAdmin, AccountActivityAdmin,
    J1Admin, J2Admin, K1Admin, K2Admin, K3Admin,
    K4Admin, L1Admin, N1Admin, Metro2EventAdmin,
    M2DataFileAdmin, UnparseableDataAdmin
)
from parse_m2.models import (
    AccountHolder, AccountActivity,
    J1, J2, K1, K2, K3, K4, L1, N1,
    Metro2Event, M2DataFile,
    UnparseableData
)


class MockRequest:
    pass

class Metro2EventAdminTestCase(TestCase):
    def setUp(self):
        self.request = MockRequest()
        self.ma = Metro2EventAdmin(Metro2Event, AdminSite())

    def test_add_permission_is_true(self):
        self.assertTrue(self.ma.has_add_permission(self.request))

    def test_view_permission_is_true(self):
        self.assertTrue(self.ma.has_view_permission(self.request))

    def test_change_permission_is_true(self):
        self.assertTrue(self.ma.has_change_permission(self.request))

    def test_delete_permission_is_true(self):
        self.assertTrue(self.ma.has_delete_permission(self.request))

class M2DataFileAdminTestCase(TestCase):
    def setUp(self):
        self.request = MockRequest()
        self.ma = M2DataFileAdmin(M2DataFile, AdminSite())

    def test_add_permission_is_false(self):
        self.assertFalse(self.ma.has_add_permission(self.request))

    def test_view_permission_is_true(self):
        self.assertTrue(self.ma.has_view_permission(self.request))

    def test_change_permission_is_false(self):
        self.assertFalse(self.ma.has_change_permission(self.request))

    def test_delete_permission_is_false(self):
        self.assertFalse(self.ma.has_delete_permission(self.request))

class UnparseableDataAdminTestCase(TestCase):
    def setUp(self):
        self.request = MockRequest()
        self.ma = UnparseableDataAdmin(UnparseableData, AdminSite())

    def test_add_permission_is_false(self):
        self.assertFalse(self.ma.has_add_permission(self.request))

    def test_view_permission_is_true(self):
        self.assertTrue(self.ma.has_view_permission(self.request))

    def test_change_permission_is_false(self):
        self.assertFalse(self.ma.has_change_permission(self.request))

    def test_delete_permission_is_false(self):
        self.assertFalse(self.ma.has_delete_permission(self.request))

class AccountHolderAdminTestCase(TestCase):
    def setUp(self):
        self.request = MockRequest()
        self.ma = AccountHolderAdmin(AccountHolder, AdminSite())

    def test_add_permission_is_false(self):
        self.assertFalse(self.ma.has_add_permission(self.request))

    def test_view_permission_is_true(self):
        self.assertTrue(self.ma.has_view_permission(self.request))

    def test_change_permission_is_false(self):
        self.assertFalse(self.ma.has_change_permission(self.request))

    def test_delete_permission_is_false(self):
        self.assertFalse(self.ma.has_delete_permission(self.request))

class AccountActivityAdminTestCase(TestCase):
    def setUp(self):
        self.request = MockRequest()
        self.ma = AccountActivityAdmin(AccountActivity, AdminSite())

    def test_add_permission_is_false(self):
        self.assertFalse(self.ma.has_add_permission(self.request))

    def test_view_permission_is_true(self):
        self.assertTrue(self.ma.has_view_permission(self.request))

    def test_change_permission_is_false(self):
        self.assertFalse(self.ma.has_change_permission(self.request))

    def test_delete_permission_is_false(self):
        self.assertFalse(self.ma.has_delete_permission(self.request))

class J1AdminTestCase(TestCase):
    def setUp(self):
        self.request = MockRequest()
        self.ma = J1Admin(J1, AdminSite())

    def test_add_permission_is_false(self):
        self.assertFalse(self.ma.has_add_permission(self.request))

    def test_view_permission_is_true(self):
        self.assertTrue(self.ma.has_view_permission(self.request))

    def test_change_permission_is_false(self):
        self.assertFalse(self.ma.has_change_permission(self.request))

    def test_delete_permission_is_false(self):
        self.assertFalse(self.ma.has_delete_permission(self.request))

class J2AdminTestCase(TestCase):
    def setUp(self):
        self.request = MockRequest()
        self.ma = J2Admin(J2, AdminSite())

    def test_add_permission_is_false(self):
        self.assertFalse(self.ma.has_add_permission(self.request))

    def test_view_permission_is_true(self):
        self.assertTrue(self.ma.has_view_permission(self.request))

    def test_change_permission_is_false(self):
        self.assertFalse(self.ma.has_change_permission(self.request))

    def test_delete_permission_is_false(self):
        self.assertFalse(self.ma.has_delete_permission(self.request))

class K1AdminTestCase(TestCase):
    def setUp(self):
        self.request = MockRequest()
        self.ma = K1Admin(K1, AdminSite())

    def test_add_permission_is_false(self):
        self.assertFalse(self.ma.has_add_permission(self.request))

    def test_view_permission_is_true(self):
        self.assertTrue(self.ma.has_view_permission(self.request))

    def test_change_permission_is_false(self):
        self.assertFalse(self.ma.has_change_permission(self.request))

    def test_delete_permission_is_false(self):
        self.assertFalse(self.ma.has_delete_permission(self.request))

class K2AdminTestCase(TestCase):
    def setUp(self):
        self.request = MockRequest()
        self.ma = K2Admin(K2, AdminSite())

    def test_add_permission_is_false(self):
        self.assertFalse(self.ma.has_add_permission(self.request))

    def test_view_permission_is_true(self):
        self.assertTrue(self.ma.has_view_permission(self.request))

    def test_change_permission_is_false(self):
        self.assertFalse(self.ma.has_change_permission(self.request))

    def test_delete_permission_is_false(self):
        self.assertFalse(self.ma.has_delete_permission(self.request))

class K3AdminTestCase(TestCase):
    def setUp(self):
        self.request = MockRequest()
        self.ma = K3Admin(K3, AdminSite())

    def test_add_permission_is_false(self):
        self.assertFalse(self.ma.has_add_permission(self.request))

    def test_view_permission_is_true(self):
        self.assertTrue(self.ma.has_view_permission(self.request))

    def test_change_permission_is_false(self):
        self.assertFalse(self.ma.has_change_permission(self.request))

    def test_delete_permission_is_false(self):
        self.assertFalse(self.ma.has_delete_permission(self.request))

class K4AdminTestCase(TestCase):
    def setUp(self):
        self.request = MockRequest()
        self.ma = K4Admin(K4, AdminSite())

    def test_add_permission_is_false(self):
        self.assertFalse(self.ma.has_add_permission(self.request))

    def test_view_permission_is_true(self):
        self.assertTrue(self.ma.has_view_permission(self.request))

    def test_change_permission_is_false(self):
        self.assertFalse(self.ma.has_change_permission(self.request))

    def test_delete_permission_is_false(self):
        self.assertFalse(self.ma.has_delete_permission(self.request))

class L1AdminTestCase(TestCase):
    def setUp(self):
        self.request = MockRequest()
        self.ma = L1Admin(L1, AdminSite())

    def test_add_permission_is_false(self):
        self.assertFalse(self.ma.has_add_permission(self.request))

    def test_view_permission_is_true(self):
        self.assertTrue(self.ma.has_view_permission(self.request))

    def test_change_permission_is_false(self):
        self.assertFalse(self.ma.has_change_permission(self.request))

    def test_delete_permission_is_false(self):
        self.assertFalse(self.ma.has_delete_permission(self.request))

class N1AdminTestCase(TestCase):
    def setUp(self):
        self.request = MockRequest()
        self.ma = N1Admin(N1, AdminSite())

    def test_add_permission_is_false(self):
        self.assertFalse(self.ma.has_add_permission(self.request))

    def test_view_permission_is_true(self):
        self.assertTrue(self.ma.has_view_permission(self.request))

    def test_change_permission_is_false(self):
        self.assertFalse(self.ma.has_change_permission(self.request))

    def test_delete_permission_is_false(self):
        self.assertFalse(self.ma.has_delete_permission(self.request))
