from collections import Counter
from functools import reduce
from rest_framework import serializers
from rest_framework.utils import model_meta

from .models import (
    EvaluatorMetadata,
    EvaluatorResult,
    EvaluatorResultSummary
)
from evaluate_m2.metadata_utils import (
    code_to_plain_field_map,
    plain_to_code_field_map,
    format_fields_for_csv,
    parse_fields_from_csv
)
from parse_m2.models import AccountActivity


class EventsViewSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
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
                  'inconsistency_end', 'id', 'category',
                  'description', 'long_description',
                  'fields_used', 'fields_display', 'crrg_reference',
                  'potential_harm','rationale', 'alternate_explanation']

    def get_id(self, obj: EvaluatorResultSummary):
        return obj.evaluator.id
    def get_description(self, obj: EvaluatorResultSummary):
        return obj.evaluator.description
    def get_long_description(self, obj: EvaluatorResultSummary):
        return obj.evaluator.long_description
    def get_category(self, obj: EvaluatorResultSummary):
        return obj.evaluator.category
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
        json['fields_used'] = format_fields_for_csv(fields_used)
        json['fields_display'] = format_fields_for_csv(fields_display)

        return json

    def to_internal_value(self, data):
        """
        Convert a JSON object (as it comes from the evaluator CSV) to
        an instance of EvaluatorMetadata
        """
        # First, get the default values
        vals = super().to_internal_value(data)

        # get the fields_used and fields_display values from the
        # newline-delimited string columns of the SSoTS
        vals['fields_used'] = parse_fields_from_csv(vals['fields_used'])
        vals['fields_display'] = parse_fields_from_csv(vals['fields_display'])

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


# TODO: See if we can reuse AccountActivitySerializer? It doesn't serialize
# all fields though.
class EvaluatorResultAccountActivitySerializer(serializers.ModelSerializer):
    """Serialize evaluator summary fields on an AccountActivity object.

    Given an `evaluator` object, serialize an AccountActivity record with
    just the evaluator's `result_summary_fields()`. This is used when
    paginating all results from an evaluator.
    """

    class Meta:
        model = AccountActivity
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # We'll use the evaluator's result_summary_fields() to populate the
        # fields list dynamically.
        self.evaluator = kwargs.pop("evaluator")
        assert self.evaluator is not None, "`evaluator` is required."

        super().__init__(*args, **kwargs)

        # Drop any fields that are not in the evaluator's summary fields.
        self.filter_evaluator_fields()

    def get_fields(self):
        # Get fields we might want to include from related models
        fields = self.get_flat_related_fields()

        # Get the default fields from our superclass and override any of the
        # previous fields with these.
        fields.update(super().get_fields())
        return fields

    def get_flat_related_fields(self):
        # Because we include related model fields as Django double-undescores,
        # we have to add them manually to the fields list as
        # SerializerMethodFields.
        fields = {}

        # Use a DRF model field utility to get all this model's reverse
        # relations
        related_fields = model_meta.get_field_info(
            self.Meta.model
        ).reverse_relations

        # Limit the fields we include from related models to this list of
        # models
        # TODO: This won't really work for related models that aren't
        # one-to-one. That means J1 and J2 don't get included
        models_to_include = ["AccountHolder", "K1", "K3", "K4", "L1", "N1", ]
        for related_name, related_field in related_fields.items():
            related_model = related_field.related_model
            if related_model.__name__ not in models_to_include:
                continue

            # Get this model's concrete field info using the DRF model field
            # utility
            related_model_fields = model_meta.get_field_info(
                related_field.related_model
            )

            # For each concrete field on the related model, add a
            # SerializerMethodField for a {related_name}__{field_name}
            # field on this serializer.
            for field_name, field in related_model_fields.fields.items():
                # Set the field name to the getter function
                self.add_related_field_method(related_name, field_name)
                fields[f"{related_name}__{field_name}"] = serializers.SerializerMethodField()

        return fields

    def add_related_field_method(self, related_name, field_name):
        def field_getter(obj):
            if hasattr(obj, related_name):
                related_instance = getattr(obj, related_name)
                return getattr(related_instance, field_name)
        setattr(self, f"get_{related_name}__{field_name}", field_getter)

    def filter_evaluator_fields(self):
        # Based on the DRF example here: https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
        evaluator_fields = set(self.evaluator.result_summary_fields())
        all_fields = set(self.fields)

        for field_name in all_fields - evaluator_fields:
            self.fields.pop(field_name)
