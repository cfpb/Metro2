from rest_framework import serializers

from evaluate_m2.metadata_utils import (
    code_to_plain_field_map,
    format_fields_for_csv,
    parse_fields_from_csv,
    plain_to_code_field_map,
)
from evaluate_m2.models import (
    EvaluatorMetadata,
    EvaluatorResultMaterializedView,
    EvaluatorResultSummary,
)


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
    interpret_fields_last_modified = serializers.SerializerMethodField(read_only=True)
    additional_notes = serializers.SerializerMethodField(read_only=True)
    additional_notes_last_modified = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EvaluatorResultSummary
        fields = ['hits', 'accounts_affected', 'inconsistency_start',
                  'inconsistency_end', 'id', 'category',
                  'description', 'long_description',
                  'fields_used', 'fields_display', 'crrg_reference',
                  'potential_harm','rationale', 'alternate_explanation',
                  'interpret_fields_last_modified',
                  'additional_notes', 'additional_notes_last_modified',
        ]

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
    def get_interpret_fields_last_modified(self, obj: EvaluatorResultSummary):
        value = obj.evaluator.interpret_fields_last_modified
        if value == EvaluatorMetadata._last_modified_never:
            return None
        else:
            return value
    def get_additional_notes(self, obj: EvaluatorResultSummary):
        return obj.evaluator.additional_notes
    def get_additional_notes_last_modified(self, obj: EvaluatorResultSummary):
        value = obj.evaluator.additional_notes_last_modified
        if value == EvaluatorMetadata._last_modified_never:
            return None
        else:
            return value


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
            'alternate_explanation', 'interpret_fields_last_modified',
            'additional_notes', 'additional_notes_last_modified',
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
    interpret_fields_last_modified = serializers.DateField()
    additional_notes = serializers.CharField(required=False, allow_blank=True)
    additional_notes_last_modified = serializers.DateField()

    def create(self, validated_data):
        return EvaluatorMetadata.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # don't update instance.id
        instance.category = validated_data.get('category', instance.description)
        instance.description = validated_data.get(
            'description',
            instance.description
        )
        instance.long_description = validated_data.get(
            'long_description',
            instance.long_description
        )
        instance.fields_used = validated_data.get(
            'fields_used',
            instance.fields_used
        )
        instance.fields_display = validated_data.get(
            'fields_display',
            instance.fields_display
        )
        instance.crrg_reference = validated_data.get(
            'crrg_reference',
            instance.crrg_reference
        )
        instance.potential_harm = validated_data.get(
            'potential_harm',
            instance.potential_harm
        )
        instance.rationale = validated_data.get('rationale', instance.rationale)
        instance.alternate_explanation = validated_data.get(
            'alternate_explanation',
            instance.alternate_explanation
        )
        instance.interpret_fields_last_modified = validated_data.get(
            'interpret_fields_last_modified',
            instance.interpret_fields_last_modified
        )
        instance.additional_notes = validated_data.get(
            'additional_notes',
            instance.additional_notes
        )
        instance.additional_notes_last_modified = validated_data.get(
            'additional_notes_last_modified',
            instance.additional_notes_last_modified
        )
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
        fields_display = [
            code_to_plain_field_map.get(k, k) for k in json['fields_display']
        ]

        # Then override fields_used with the newline-delimited string version
        json['fields_used'] = format_fields_for_csv(fields_used)
        json['fields_display'] = format_fields_for_csv(fields_display)

        # Also translate default date values to blank
        default_date = str(EvaluatorMetadata._last_modified_never)
        if json['additional_notes_last_modified'] == default_date:
            json['additional_notes_last_modified'] = ''
        if json['interpret_fields_last_modified'] == default_date:
            json['interpret_fields_last_modified'] = ''

        return json

    def to_internal_value(self, data: dict):
        """
        Convert a JSON object (as it comes from the evaluator CSV) to
        an instance of EvaluatorMetadata
        """
        # First, catch blank date values and set them to the default date
        default_value = EvaluatorMetadata._last_modified_never
        key1 = 'additional_notes_last_modified'
        if not (key1 in data and data[key1]):
            data[key1] = default_value
        key2 = 'interpret_fields_last_modified'
        if not (key2 in data and data[key2]):
            data[key2] = default_value

        # Then, get the default values
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

        # signal to the model that this instance is coming from a metadata
        # import, rather than the Admin interface
        vals['from_bulk_import'] = True

        return vals

    def validate(self, data):
        """
        Check that the values from the fields_used column in the evaluator CSV
        are all valid fields. If not, is_valid() returns False.
        """
        invalid_fields = []
        for f in data['fields_used'] + data['fields_display']:
            if f not in code_to_plain_field_map:
                invalid_fields.append(f)
        if invalid_fields:
            raise serializers.ValidationError(f"Invalid field names: {invalid_fields}")
        return data


class EvaluatorResultSerializer(serializers.ModelSerializer):
    # Outside of the materialized view, the API serializes related objects
    # using Django's __ notation. These fields preserve those fieldnames.
    k2__purch_sold_ind = serializers.CharField(source="purch_sold_ind")
    k2__purch_sold_name = serializers.CharField(source="purch_sold_name")
    k4__spc_pmt_ind = serializers.CharField(source="spc_pmt_ind")
    k4__deferred_pmt_st_dt = serializers.CharField(source="deferred_pmt_st_dt")
    k4__balloon_pmt_due_dt = serializers.CharField(source="balloon_pmt_due_dt")
    k4__balloon_pmt_amt = serializers.CharField(source="balloon_pmt_amt")
    l1__change_ind = serializers.CharField(source="change_ind")
    l1__new_acc_num = serializers.CharField(source="new_acc_num")
    l1__new_id_num = serializers.CharField(source="new_id_num")
    previous_value__activity_date = serializers.CharField(source="prior_activity_date")
    previous_value__port_type = serializers.CharField(source="prior_port_type")
    previous_value__acct_type = serializers.CharField(source="prior_acct_type")
    previous_value__date_open = serializers.CharField(source="prior_date_open")
    previous_value__id_num = serializers.CharField(source="prior_id_num")
    previous_value__acct_stat = serializers.CharField(source="prior_acct_stat")
    previous_value__pmt_rating = serializers.CharField(source="prior_pmt_rating")
    previous_value__current_bal = serializers.CharField(source="prior_current_bal")
    previous_value__orig_chg_off_amt = serializers.CharField(
        source="prior_orig_chg_off_amt")
    previous_value__dofd = serializers.CharField(source="prior_dofd")
    previous_value__date_closed = serializers.CharField(source="prior_date_closed")
    previous_value__surname = serializers.CharField(source="prior_surname")
    previous_value__first_name = serializers.CharField(source="prior_first_name")
    previous_value__ecoa = serializers.CharField(source="prior_ecoa")
    previous_value__ecoa_assoc = serializers.CharField(source="prior_ecoa_assoc")
    previous_value__cons_info_ind = serializers.CharField(source="prior_cons_info_ind")
    previous_value__cons_info_ind_assoc = serializers.CharField(
        source="prior_cons_info_ind_assoc")
    previous_value__l1__change_ind = serializers.CharField(source="prior_change_ind")
    previous_value__l1__new_acc_num = serializers.CharField(source="prior_new_acc_num")
    previous_value__l1__new_id_num = serializers.CharField(source="prior_new_id_num")

    class Meta:
        model = EvaluatorResultMaterializedView
        fields = '__all__'
