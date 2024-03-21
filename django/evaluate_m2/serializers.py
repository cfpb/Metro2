from rest_framework import serializers

from .models import (
    EvaluatorMetadata,
    EvaluatorResult,EvaluatorResultSummary
)


class EvaluatorMetadataSerializer(serializers.ModelSerializer):
    fields_used = serializers.SerializerMethodField(read_only=True)
    fields_display = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = EvaluatorMetadata
        fields = ['id', 'name', 'description', 'long_description', 'fields_used',
            'fields_display', 'ipl', 'crrg_topics', 'crrg_page', 'pdf_page',
            'use_notes', 'alternative_explanation', 'risk_level']

    def get_fields_used(self, obj):
        if obj.fields_used:
            return ";".join(obj.fields_used)
        else:
            return ""

    def get_fields_display(self, obj):
        if obj.fields_display:
            return ";".join(obj.fields_display)
        else:
            return ""

class EvaluatorResultsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluatorResult
        fields = ['field_values']

    def to_representation(self, obj):
        return obj.field_values