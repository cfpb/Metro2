from django.contrib import admin
from django.utils.html import format_html

from evaluate_m2.models import (
    EvaluatorMetadata,
    EvaluatorResult,
    EvaluatorResultMaterializedView,
    EvaluatorResultSummary,
)


# Register your models here.
class EvaluatorMetadataAdmin(admin.ModelAdmin):
    readonly_fields = [
        'id', 'category', 'fields_used', 'fields_display',
        'interpret_fields_last_modified',
        'additional_notes_last_modified',
    ]
    fields = [
        'category',
        'description', 'long_description',
        'crrg_reference', 'potential_harm',
        'rationale', 'alternate_explanation',
        'additional_notes',
        'fields_used', 'fields_display',
        'interpret_fields_last_modified',
        'additional_notes_last_modified',
    ]
    list_display = [
        'id', 'category', 'description', 'show_long_description',
    ]

    @admin.display(description='Long Description')
    def show_long_description(self, obj):
        return format_html(obj.long_description)

    def has_add_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return False


class EvaluatorResultSummaryAdmin(admin.ModelAdmin):
    list_display = ['event', 'evaluator', 'hits']

    def has_add_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


class EvaluatorResultAdmin(admin.ModelAdmin):
    list_display = ['result_summary', 'date', 'source_record', 'acct_num']

    def has_add_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


class EvaluatorResultMaterializedViewAdmin(admin.ModelAdmin):
    list_display = [
        'event_id',
        'evaluator_id',
        'source_record_id',
        'activity_date',
        'cons_acct_num',
        "acct_type",
        "acct_stat",
        "compl_cond_cd",
        "php",
        "php1",
        "pmt_rating",
        "spc_com_cd",
        "terms_freq",
        "cons_info_ind",
        "cons_info_ind_assoc",
        "change_ind",
        "dofd",
        "date_closed",
        "amt_past_due",
        "current_bal",
        "smpa",
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(EvaluatorMetadata, EvaluatorMetadataAdmin)
admin.site.register(EvaluatorResultSummary, EvaluatorResultSummaryAdmin)
admin.site.register(EvaluatorResult, EvaluatorResultAdmin)
admin.site.register(
    EvaluatorResultMaterializedView,
    EvaluatorResultMaterializedViewAdmin
)
