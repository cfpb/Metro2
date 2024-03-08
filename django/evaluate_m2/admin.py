from django.contrib import admin
from evaluate_m2.models import EvaluatorMetadata, EvaluatorResultSummary, EvaluatorResult

# Register your models here.
class EvaluatorMetadataAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    fields = [
            'name', 'description', 'long_description',
            'fields_used', 'fields_display', 'ipl',
            'crrg_topics', 'crrg_page', 'pdf_page',
            'use_notes', 'alternative_explanation',
            'risk_level']
    list_display = [
        'id', 'name', 'description', 'long_description',
        'fields_used', 'fields_display', 'ipl',
        'crrg_topics', 'crrg_page', 'pdf_page',
        'use_notes', 'alternative_explanation',
        'risk_level']

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
    list_display = ['result_summary', 'date', 'field_values',
                    'source_record', 'acct_num']

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
