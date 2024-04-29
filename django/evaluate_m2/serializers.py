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


fields_used_format = """
Identifying information
DB record id
activity date
customer account number

Fields used for evaluator
used_fields

Helpful fields that are also displayed currently
display_fields
"""

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
        # First, get the default representation for the fields
        json = super().to_representation(instance)
        # Then override fields_used with our representation
        fields_string =  fields_used_format \
            .replace('used_fields', '\n'.join(instance.fields_used)) \
            .replace('display_fields', '\n'.join(instance.fields_display))
        json['fields_used'] = fields_string
        # Remove fields_display, since that isn't a separate column in the csv
        json.pop('fields_display')
        return json

    def to_internal_value(self, data):
        vals = super().to_internal_value(data)
        import pdb; pdb.set_trace()
        return vals

class EvaluatorResultsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluatorResult
        fields = ['field_values']

    def to_representation(self, obj):
        return obj.field_values
