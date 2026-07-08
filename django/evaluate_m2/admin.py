from django.contrib import admin
from django.utils.html import format_html

from evaluate_m2.models import (
    EvaluatorMetadata,
    EvaluatorResult,
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
admin.site.register(EvaluatorMetadata, EvaluatorMetadataAdmin)
admin.site.register(EvaluatorResultSummary, EvaluatorResultSummaryAdmin)
admin.site.register(EvaluatorResult, EvaluatorResultAdmin)
