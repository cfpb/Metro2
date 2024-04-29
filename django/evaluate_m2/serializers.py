from rest_framework import serializers

from .models import (
    EvaluatorMetadata,
    EvaluatorResult,
    EvaluatorResultSummary
)
from evaluate_m2.metadata_utils import (
    format_fields_used_for_csv,
    parse_fields_display_from_csv,
    parse_fields_used_from_csv
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


class ImportEvaluatorMetadataSerializer(serializers.Serializer):
    class Meta:
        fields = [
            'id', 'description', 'long_description', 'fields_used',
            'fields_display', 'crrg_reference','potential_harm','rationale',
            'alternate_explanation'
        ]

    id = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    long_description = serializers.CharField(required=False, allow_blank=True)
    fields_used = serializers.JSONField(required=False)
    fields_display = serializers.JSONField(required=False)
    crrg_reference = serializers.CharField(required=False, allow_blank=True)
    potential_harm = serializers.CharField(required=False, allow_blank=True)
    rationale = serializers.CharField(required=False, allow_blank=True)
    alternate_explanation = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        return EvaluatorMetadata.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # don't update instance.id
        instance.description = validated_data.get('description', instance.description)
        instance.long_description = validated_data.get('long_description', instance.long_description)
        instance.fields_used = validated_data.get('fields_used', instance.fields_used)
        instance.fields_display = validated_data.get('fields_display', instance.fields_display)
        instance.crrg_reference = validated_data.get('crrg_reference', instance.crrg_reference)
        instance.potential_harm = validated_data.get('potential_harm', instance.potential_harm)
        instance.rationale = validated_data.get('rationale', instance.rationale)
        instance.alternate_explanation = validated_data.get('alternate_explanation', instance.alternate_explanation)
        instance.save()
        return instance

    def to_representation(self, instance):
        # First, get the default representation
        json = super().to_representation(instance)
        # Then override fields_used with our representation
        json['fields_used'] = format_fields_used_for_csv(instance)
        # Remove fields_display, since that isn't a separate column in the csv
        json.pop('fields_display')
        return json

    def to_internal_value(self, data):
        vals = super().to_internal_value(data)
        # from the `fields_used` column in the spreadsheet, get the
        # fields_used and fields_display values
        source_fields_used = vals['fields_used']
        vals['fields_used'] = parse_fields_used_from_csv(source_fields_used)
        vals['fields_display'] = parse_fields_display_from_csv(source_fields_used)
        return vals

class EvaluatorResultsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluatorResult
        fields = ['field_values']

    def to_representation(self, obj):
        return obj.field_values
