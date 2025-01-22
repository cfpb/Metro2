from datetime import date
from django.test import TestCase
from rest_framework.renderers import JSONRenderer

from evaluate_m2.models import EvaluatorMetadata, EvaluatorResult, EvaluatorResultSummary
from evaluate_m2.serializers import (
    EvaluatorMetadataSerializer,
    EventsViewSerializer
)
from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.models import M2DataFile, Metro2Event


shared_initial_values = """
Identifying information
DB record id
activity date
consumer account number
"""

e1_expected_fields_used = shared_initial_values + """
Fields used for evaluator
consumer information indicator
date of last payment
ID number

Helpful fields that are also displayed currently
special comment code
date of first delinquency
L1 change indicator
"""

e2_expected_fields = shared_initial_values + """
Fields used for evaluator
wrong
misspelled

Helpful fields that are also displayed currently
other
"""

# Import should be case insensitive
e3_case_insensitive = shared_initial_values + """
Fields USED for EvAlUaToR
consumer information indicator
date of last payment
id number

Helpful FIELDS that ARE ALSO DISPLAYED CURRENTLY
special comment CODE
date of FIRST delinquency
L1 change indicator
ECOA
"""

e4_invalid_input = shared_initial_values + """
Fields used for evaluator
date of last payment
bogus name

Helpful fields that are also displayed currently
K2 purchased - sold indicator
something misspelled
"""

class EvalSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.multi_line_text="""Here is some text.
        It is split over two lines."""

        self.e1 = EvaluatorMetadata(
            id="Betsy-1",
            category="paid/not paid",
            description="desc 1",
            long_description=self.multi_line_text,
            fields_used=["account_holder__cons_info_ind", "dolp", "id_num"],
            fields_display=["spc_com_cd", "dofd", "l1__change_ind"],
            crrg_reference="PDF page 3",
        )

        self.e1_json = {
            'id': 'Betsy-1',
            'category': 'paid/not paid',
            'description': 'desc 1',
            'long_description': self.multi_line_text,
            'fields_used': e1_expected_fields_used,
            'crrg_reference': 'PDF page 3',
            'potential_harm': '',
            'rationale': '',
            'alternate_explanation': '',
        }

        self.e3_json = {
            'id': 'Test-19',
            'description': 'desc 1',
            'long_description': self.multi_line_text,
            'fields_used': e3_case_insensitive,
            'crrg_reference': 'PDF page 3',
            'potential_harm': '',
            'rationale': '',
            'alternate_explanation': '',
        }

    #### Tests for exporting EvaluatorMetadata records
    def test_export_to_json(self):
        to_json = EvaluatorMetadataSerializer(self.e1)
        self.assertEqual(to_json.data, self.e1_json)

    def test_export_if_field_name_nonexistent(self):
        e2 = EvaluatorMetadata(
            id="TEST-11",
            fields_used=["wrong", "misspelled"],
            fields_display=["other"],
        )
        e2_json = {
            'id': 'TEST-11',
            'category': '',
            'description': '',
            'long_description': '',
            'fields_used': e2_expected_fields,
            'crrg_reference': '',
            'potential_harm': '',
            'rationale': '',
            'alternate_explanation': '',
        }

        to_json = EvaluatorMetadataSerializer(e2)
        self.assertEqual(to_json.data, e2_json)

    #### Tests for importing EvaluatorMetadata records
    def test_import_from_json(self):
        json = self.e1_json.copy()
        json['id'] = "BETSY-NEW"
        from_json = EvaluatorMetadataSerializer(data=json)
        self.assertTrue(from_json.is_valid())
        record = from_json.save()
        self.assertEqual(record.id, "BETSY-NEW")
        self.assertEqual(record.category, 'paid/not paid')
        self.assertEqual(record.description, self.e1_json['description'])
        self.assertEqual(record.fields_used, ['account_holder__cons_info_ind', 'dolp', 'id_num'])
        self.assertEqual(record.fields_display, ['spc_com_cd', 'dofd', 'l1__change_ind'])

    def test_import_from_json_case_insensitive(self):
        from_json = EvaluatorMetadataSerializer(data=self.e3_json)
        self.assertTrue(from_json.is_valid())
        record = from_json.save()
        self.assertEqual(record.id, "Test-19")
        self.assertEqual(record.description, self.e1_json['description'])
        self.assertEqual(record.fields_used, ['account_holder__cons_info_ind', 'dolp', 'id_num'])
        self.assertEqual(record.fields_display, ['spc_com_cd', 'dofd', 'l1__change_ind',
                                                 'account_holder__ecoa'])

    def test_import_fails_when_field_names_incorrect(self):
        e4_json = {
            'id': 'TEST-99',
            'description': '',
            'long_description': '',
            'fields_used': e4_invalid_input,
        }
        result = EvaluatorMetadataSerializer(data=e4_json)
        self.assertFalse(result.is_valid())

    def test_many_to_json(self):
        eval_metadata = [self.e1]
        serializer = EvaluatorMetadataSerializer(eval_metadata, many=True)
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render([self.e1_json])
        self.assertEqual(json_output, expected)


class EventsViewSerializerTestCase(TestCase):
    def setUp(self) -> None:
        # Create an EvaluatorMetadata record
        self.eval = EvaluatorMetadata.objects.create(
            id='Status-DOFD-1',
            description='description of Status-DOFD-1',
            long_description='',
            fields_used=['placeholder', 'date of first delinquency'],
            fields_display=['amount past due', 'compliance condition code',
                    'current balance', 'date closed', 'original charge-off amount',
                    'terms frequency'],
            crrg_reference='400',
            alternate_explanation='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
        )

        # Create the parent records for the AccountActivity data
        self.event = Metro2Event(id=1, name='test_exam')
        self.event.save()
        file = M2DataFile(event=self.event, file_name="tst.txt")
        file.save()
        activity = { 'id': 32, 'activity_date': date(2023,11,20),
                    'cons_acct_num': '0032','current_bal':0, 'amt_past_due': 5 }
        acct_activity = acct_record(file, activity)

        self.eval_rs = EvaluatorResultSummary(
            event=self.event, evaluator=self.eval, hits=2, accounts_affected=1,
            inconsistency_start=date(2021, 1, 1), inconsistency_end=date(2021, 2, 1))
        self.eval_rs.save()

        self.json_representation = {
            'hits': 2, 'accounts_affected': 1, 'inconsistency_start':date(2021, 1, 1),
            'inconsistency_end': date(2021, 2, 1), 'id': 'Status-DOFD-1',
            'description': 'description of Status-DOFD-1', 'long_description': '',
            'fields_used': ['account status', 'date of first delinquency'],
            'fields_display': ['amount past due', 'compliance condition code',
                'current balance', 'date closed', 'original charge-off amount',
                'terms frequency'],
            'crrg_reference': '400', 'potential_harm': '',
            'rationale': '', 'alternate_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
            }

    def test_evaluator_metadata_serializer(self):
        serializer = EventsViewSerializer(self.eval_rs, many=False, context={'event': self.event})
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render(self.json_representation)
        self.assertEqual(json_output, expected)

    def test_group_serializer_many_true(self):
        evals = [self.eval_rs]
        serializer = EventsViewSerializer(evals, many=True, context={'event': self.event})
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render([self.json_representation])
        self.assertEqual(json_output, expected)
