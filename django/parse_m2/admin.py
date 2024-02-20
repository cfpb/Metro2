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
    form=Metro2EventForm
    fields = ['name','directory']

    def get_form(self, request, obj=None, **kwargs):
        """
        Overrides BaseModelAdmin get_form() to display fields based
        on an add/change view for Metro2Events
        """
        if obj: # obj is not None, so this is a change page
            self.readonly_fields = ['name']
            help_texts = {'name': ""}
            kwargs.update({'help_texts': help_texts})
        else: # obj is None, so this is an add page
            self.readonly_fields = []
        return super(Metro2EventAdmin, self).get_form(request, obj, **kwargs)

    def render_change_form(self, request, context, add=False, change=False, form_url="", obj=None):
        """
        Overrides BaseModelAdmin render_change_form() to update the flags to
        show/hide buttons on add or change view for Metro2Events
        """
        print('In render_change_form')
        if obj:
            context.update({"show_parse": False})
            context.update({"show_parse_eval": False})
            context.update({"show_eval": True})
        else:
            context.update({"show_parse": True})
            context.update({"show_parse_eval": True})
            context.update({"show_eval": False})
        context.update({"show_close": True})
        context.update({"show_save": False})
        context.update({"show_delete_link": False})
        context.update({"show_save_as_new": False})
        context.update({"show_save_and_add_another": False})
        context.update({"show_save_and_continue": False})

        return super(Metro2EventAdmin, self).render_change_form(request, context, add, change, form_url, obj)

    def response_change(self, request, obj):
        """
        Overrides ModelAdmin response_change() to call the evaluate mgmt command and add a message to django-admin that the command has completed.
        """
        logger = logging.getLogger('admin.response_change')
        if "_parse_eval" in request.POST or "_eval" in request.POST:
            try:
                obj.evaluate()
                messages.success(request, f"Finished running evaluators for event ID: {obj.id} and saving results.")
            except (ValueError, TypeError):
                pass
            return redirect(".")
        return  super(Metro2EventAdmin, self).response_change(request, obj)

    def message_user(self, request, message, level=messages.INFO, extra_tags='',
                    fail_silently=False):
        """
        Overrides ModelAdmin message_user() to only include the messages created and not the default messages
        """
        pass

    def save_model(self, request, obj, form, change):
        """
        Overrides ModelAdmin save_model() to update the message returned to the view
        """
        if obj.id:
            if not change: # This is a new
                messages.success(request, f'Created event ID: {obj.id}. Finished parsing data for event: {obj.name}')
                self.response_change(request, obj)
        else:
            messages.error(request, 'Event did not save successfully and did not parse data')
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request, obj=None):
        return True
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True

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

# This is to manually order the sites rather than the
# alphabetically ordered
def get_app_list(self, request, app_label=None):
    """Return the installed apps that have been registered in admin.py"""
    app_dict = self._build_app_dict(request, app_label)
    app_list = list(app_dict.values())
    return app_list

AdminSite.get_app_list = get_app_list
