from django.conf import settings
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.views.generic.detail import DetailView
from django.urls import path, reverse
from django.utils.html import format_html

from parse_m2.models import (
    AccountHolder, AccountActivity,
    J1, J2, K1, K2, K3, K4, L1, N1,
    Metro2Event, M2DataFile,
    UnparseableData
)


class EventParseEvalView(DetailView):
    template_name = 'admin/parse_m2/event_parse_eval.html'
    model = Metro2Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context | admin.site.each_context(self.request)
        context["opts"] = self.model._meta
        return context


class Metro2EventAdmin(admin.ModelAdmin):
    fields = ['name', 'portfolio', 'eid_or_matter_num', 'other_descriptor', 'directory', 'members']
    list_display = ['name', 'portfolio', 'eid_or_matter_num', 'import_data']
    filter_horizontal = ['members']

    def get_urls(self):
        return [
            path("<pk>/parse_evaluate", self.admin_site.admin_view(EventParseEvalView.as_view()), name="parse_evaluate_event"),
            *super().get_urls(),
        ]

    # Create a column called "Import data" in the list view for the Event admin page
    # The column contains a link to the data import detail page (EventParseEvalView)
    def import_data(self, obj: Metro2Event) -> str:
        url = reverse("admin:parse_evaluate_event", args=[obj.pk])
        return format_html(f"<a href='{url}'>Data import info</a>")

    def get_form(self, request, obj: Metro2Event = None, change: bool = False, **kwargs):
        form =  super().get_form(request, obj, change, **kwargs)
        name_field = form.base_fields['name']
        name_field.label = "Institution name"
        eid_field = form.base_fields['eid_or_matter_num']
        eid_field.label = "EID or matter number"
        other_field = form.base_fields['other_descriptor']
        other_field.label = "Other descriptor (optional)"
        directory_field = form.base_fields['directory']
        if settings.SSO_ENABLED:
            help_msg = "The location of the raw data files in the data directory. Starts with Enforcement/ or Supervision/ ."
        else:
            help_msg = f"The location of the raw data files in the local filesystem (SSO not enabled). If in doubt, use: {settings.LOCAL_EVENT_DATA}."
        directory_field.help_text = help_msg
        return form

    def has_add_permission(self, request, obj=None):
        return True
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True

class M2DataFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'file_name', 'parsing_status',
                    'parsed_lines', 'unparseable_lines', 'timestamp',
                    'error_message']

    def parsed_lines(self, obj):
        return obj.accountholder_set.count()

    def unparseable_lines(self, obj):
        return obj.unparseabledata_set.count()

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
                    'addr_ind', 'res_cd', 'cons_info_ind_assoc',
                    'ecoa_assoc']
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
    list_display = ['account_activity', 'surname',
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
    list_display = ['account_activity', 'surname',
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

# This is to manually order the sites rather than the
# alphabetically ordered
def get_app_list(self, request, app_label=None):
    """Return the installed apps that have been registered in admin.py"""
    app_dict = self._build_app_dict(request, app_label)
    app_list = list(app_dict.values())
    return app_list

AdminSite.get_app_list = get_app_list
