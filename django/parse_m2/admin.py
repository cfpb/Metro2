import logging

from django.contrib import admin, messages
from django.contrib.admin import AdminSite
from django.core.management import call_command
from django.shortcuts import redirect

from parse_m2.forms import  Metro2EventForm
from parse_m2.models import (
    AccountHolder, AccountActivity,
    J1, J2, K1, K2, K3, K4, L1, N1,
    Metro2Event, M2DataFile,
    UnparseableData
)


# Register your models here.
class Metro2EventAdmin(admin.ModelAdmin):
    list_display = ['name']

    def has_add_permission(self, request, obj=None):
        return True
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return False

class M2DataFileAdmin(admin.ModelAdmin):
    list_display = ['event', 'file_name', 'timestamp']

    def has_add_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class UnparseableDataAdmin(admin.ModelAdmin):
    list_display = ['data_file', 'unparseable_line', 'error_description']

    def has_add_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class AccountHolderAdmin(admin.ModelAdmin):
    list_display = ['data_file', 'activity_date', 'cons_acct_num', 'surname',
                    'first_name', 'middle_name', 'gen_code','ssn', 'dob',
                    'phone_num', 'ecoa', 'cons_info_ind', 'country_cd',
                    'addr_line_1', 'addr_line_2', 'city', 'state', 'zip',
                    'addr_ind', 'res_cd']
    def has_add_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class AccountActivityAdmin(admin.ModelAdmin):
    list_display = ['account_holder', 'activity_date', 'cons_acct_num', 'port_type',
                    'acct_type', 'date_open', 'credit_limit','hcola', 'terms_dur',
                    'terms_freq', 'smpa', 'actual_pmt_amt', 'acct_stat', 'pmt_rating',
                    'php', 'spc_com_cd', 'compl_cond_cd', 'current_bal', 'amt_past_due',
                    'orig_chg_off_amt', 'doai', 'dofd', 'date_closed', 'dolp',
                    'int_type_ind']

    def has_add_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class J1Admin(admin.ModelAdmin):
    list_display = ['account_activity', 'surname', 'surname',
                    'first_name', 'middle_name', 'gen_code','ssn',
                    'dob', 'phone_num', 'ecoa', 'cons_info_ind']

    def has_add_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class J2Admin(admin.ModelAdmin):
    list_display = ['account_activity', 'surname', 'surname',
                    'first_name', 'middle_name', 'gen_code','ssn',
                    'dob', 'phone_num', 'ecoa', 'cons_info_ind',
                    'country_cd', 'addr_line_1', 'addr_line_2',
                    'city', 'state', 'zip', 'addr_ind', 'res_cd']

    def has_add_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class K1Admin(admin.ModelAdmin):
    list_display = ['account_activity', 'orig_creditor_name',
                    'creditor_classification']

    def has_add_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class K2Admin(admin.ModelAdmin):
    list_display = ['account_activity', 'purch_sold_ind',
                    'purch_sold_name']

    def has_add_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class K3Admin(admin.ModelAdmin):
    list_display = ['account_activity', 'agency_id',
                    'agency_acct_num', 'min']

    def has_add_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class K4Admin(admin.ModelAdmin):
    list_display = ['account_activity', 'spc_pmt_ind',
                    'deferred_pmt_st_dt', 'balloon_pmt_due_dt',
                    'balloon_pmt_amt']

    def has_add_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class L1Admin(admin.ModelAdmin):
    list_display = ['account_activity', 'change_ind', 'new_acc_num',
                    'new_id_num']

    def has_add_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class N1Admin(admin.ModelAdmin):
    list_display = ['account_activity', 'employer_name', 'employer_addr1',
                    'employer_addr2', 'employer_city', 'employer_state',
                    'employer_zip', 'occupation']

    def has_add_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Metro2Event, Metro2EventAdmin)
admin.site.register(M2DataFile, M2DataFileAdmin)
admin.site.register(UnparseableData, UnparseableDataAdmin)
admin.site.register(AccountHolder, AccountHolderAdmin)
admin.site.register(AccountActivity, AccountActivityAdmin)
admin.site.register(J1, J1Admin)
admin.site.register(J2, J2Admin)
admin.site.register(K1, K1Admin)
admin.site.register(K2, K2Admin)
admin.site.register(K3, K3Admin)
admin.site.register(K4, K4Admin)
admin.site.register(L1, L1Admin)
admin.site.register(N1, N1Admin)

def get_app_list(self, request, app_label=None):
    """Return the installed apps that have been registered in admin.py"""
    app_dict = self._build_app_dict(request, app_label)
    app_list = list(app_dict.values())
    return app_list


AdminSite.get_app_list = get_app_list
