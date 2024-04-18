from rest_framework import serializers

from .models import (
    EvaluatorMetadata,
    EvaluatorResult,
    EvaluatorResultSummary
)

class EventsViewSerializer(serializers.ModelSerializer):
    hits = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EvaluatorMetadata
        fields = ['hits','id','description','long_description',
                  'fields_used','fields_display',
                  'crrg_reference','potential_harm','rationale',
                  'alternate_explanation']

    def get_hits(self, obj):
        event = self.context.get("event")
        return EvaluatorResultSummary.objects.get(evaluator=obj, event=event).hits


class EvaluatorMetadataSerializer(serializers.ModelSerializer):
    fields_used = serializers.SerializerMethodField(read_only=True)
    fields_display = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = EvaluatorMetadata
        fields = ['id', 'description', 'long_description', 'fields_used',
            'fields_display', 'crrg_reference','potential_harm','rationale',
            'alternate_explanation']

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
