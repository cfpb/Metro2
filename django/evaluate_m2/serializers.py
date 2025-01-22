from collections import Counter
from functools import reduce
from rest_framework import serializers

from .models import (
    EvaluatorMetadata,
    EvaluatorResult,
    EvaluatorResultSummary
)
from evaluate_m2.metadata_utils import (
    code_to_plain_field_map,
    plain_to_code_field_map,
    format_fields_used_for_csv,
    parse_fields_display_from_csv,
    parse_fields_used_from_csv
)

class EventsViewSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    long_description = serializers.SerializerMethodField(read_only=True)
    fields_used = serializers.SerializerMethodField(read_only=True)
    fields_display = serializers.SerializerMethodField(read_only=True)
    crrg_reference = serializers.SerializerMethodField(read_only=True)
    potential_harm = serializers.SerializerMethodField(read_only=True)
    rationale = serializers.SerializerMethodField(read_only=True)
    alternate_explanation = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EvaluatorResultSummary
        fields = ['hits', 'accounts_affected', 'inconsistency_start',
                  'inconsistency_end', 'id', 'description', 'long_description',
                  'fields_used', 'fields_display', 'crrg_reference',
                  'potential_harm','rationale', 'alternate_explanation']

    def get_id(self, obj: EvaluatorResultSummary):
        return obj.evaluator.id
    def get_description(self, obj: EvaluatorResultSummary):
        return obj.evaluator.description
    def get_long_description(self, obj: EvaluatorResultSummary):
        return obj.evaluator.long_description
    def get_fields_used(self, obj: EvaluatorResultSummary):
        return obj.evaluator.fields_used
    def get_fields_display(self, obj: EvaluatorResultSummary):
        return obj.evaluator.fields_display
    def get_crrg_reference(self, obj: EvaluatorResultSummary):
        return obj.evaluator.crrg_reference
    def get_potential_harm(self, obj: EvaluatorResultSummary):
        return obj.evaluator.potential_harm
    def get_rationale(self, obj: EvaluatorResultSummary):
        return obj.evaluator.rationale
    def get_alternate_explanation(self, obj: EvaluatorResultSummary):
        return obj.evaluator.alternate_explanation


class EvaluatorMetadataSerializer(serializers.Serializer):
    """
    This serializer is used when importing the evaluator metadata CSV
    (using the import_evaluator_metadata management command), and when
    exporting metadata with the /api/all-evaluator-metadata/ endpoint.
    It uses the format in our evaluator source of truth spreadsheet.
    """
    class Meta:
        fields = [
            'id', 'category', 'description', 'long_description', 'fields_used',
            'fields_display', 'crrg_reference','potential_harm','rationale',
            'alternate_explanation'
        ]

    id = serializers.CharField()
    category = serializers.CharField(required=False, allow_blank=True)
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
        instance.category = validated_data.get('category', instance.description)
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
        """
        Convert an instance of the EvaluatorMetadata class to JSON,
        so it can be written to CSV.
        """
        # First, get the default representation
        json = super().to_representation(instance)

        # Then translate the fields from code to plain language
        fields_used = [code_to_plain_field_map.get(k, k) for k in json['fields_used']]
        fields_display = [code_to_plain_field_map.get(k, k) for k in json['fields_display']]

        # Then override fields_used with the newline-delimited string version
        json['fields_used'] = format_fields_used_for_csv(fields_used, fields_display)

        # Remove fields_display, since that isn't a separate column in the csv
        json.pop('fields_display')
        return json

    def to_internal_value(self, data):
        """
        Convert a JSON object (as it comes from the evaluator CSV) to
        an instance of EvaluatorMetadata
        """
        # First, get the default values
        vals = super().to_internal_value(data)

        # from the `fields_used` column in the spreadsheet, get the
        # fields_used and fields_display values from the newline-delimited string
        source_fields_used = vals['fields_used']
        vals['fields_used'] = parse_fields_used_from_csv(source_fields_used)
        vals['fields_display'] = parse_fields_display_from_csv(source_fields_used)

        # Then translate the fields from plain language to code
        vals['fields_used'] = [plain_to_code_field_map.get(k, k) \
            for k in vals['fields_used']]
        vals['fields_display'] = [plain_to_code_field_map.get(k, k) \
            for k in vals['fields_display']]

        return vals

    def validate(self, data):
        """
        Check that the values from the fields_used column in the evaluator CSV
        are all valid fields. If not, is_valid() returns False.
        """
        invalid_fields = []
        for f in data['fields_used'] + data['fields_display']:
            if f not in code_to_plain_field_map.keys():
                invalid_fields.append(f)
        if invalid_fields:
            raise serializers.ValidationError(f"Invalid field names: {invalid_fields}")
        return data
