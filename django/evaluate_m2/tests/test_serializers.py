from datetime import date
from django.test import TestCase
from rest_framework.renderers import JSONRenderer

from evaluate_m2.models import EvaluatorMetadata, EvaluatorResult, EvaluatorResultSummary
from evaluate_m2.serializers import (
    EvaluatorMetadataSerializer,
    EventsViewSerializer,
    EvaluatorResultAccountActivitySerializer
)
from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.models import M2DataFile, Metro2Event


e1_fields_used = """
consumer information indicator
date of last payment
ID number
"""

e1_fields_display = """
special comment code
date of first delinquency
L1 change indicator
"""

e2_fields_used = """
wrong
misspelled
"""

e2_fields_display = """
other
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
            'fields_used': e1_fields_used.strip(),
            'fields_display': e1_fields_display.strip(),
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
            'fields_used': e2_fields_used.strip(),
            'fields_display': e2_fields_display.strip(),
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
        fields_used = "\r\n".join([
            "cONsumer information indicator",
            "date of last payment",
            "id number",
        ])

        fields_display = "\r\n".join([
            "special comment CODE",
            "date of FIRST delinquency",
            "L1 change indicator",
            "ECoa",
        ])

        eval_json = {
            'id': 'Test-19',
            'description': 'desc 1',
            'long_description': self.multi_line_text,
            'fields_used': fields_used,
            'fields_display': fields_display,
            'crrg_reference': 'PDF page 3',
            'potential_harm': '',
            'rationale': '',
            'alternate_explanation': '',
        }

        from_json = EvaluatorMetadataSerializer(data=eval_json)
        self.assertTrue(from_json.is_valid())
        record = from_json.save()
        self.assertEqual(record.id, "Test-19")
        self.assertEqual(record.description, self.e1_json['description'])
        self.assertEqual(record.fields_used, ['account_holder__cons_info_ind', 'dolp', 'id_num'])
        self.assertEqual(record.fields_display, ['spc_com_cd', 'dofd', 'l1__change_ind',
                                                 'account_holder__ecoa'])

    def test_import_fails_when_field_names_incorrect(self):
        fields = "\r\n".join([
            "date of last payment",
            "bogus name",
            "K2 purchased - sold indicator",
            "something misspelled",
        ])
        e4_json = {
            'id': 'TEST-99',
            'description': '',
            'long_description': '',
            'fields_used': fields,
            'fields_display': '',
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
            category='closed/not closed',
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
            'category': 'closed/not closed',
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


class EvaluatorResultAccountActivitySerializerTestCase(TestCase):
    def setUp(self):
        self.evaluator = EvaluatorMetadata.objects.create(
            id="my-eval-3",
            fields_used=["amt_past_due", "account_holder__ecoa"],
            fields_display=["doai"],
        )

        # Create the results and records
        event = Metro2Event.objects.create(name="AnEvent")
        data_file = M2DataFile.objects.create(event=event)

        self.record1 = acct_record(data_file, {"id": 1, "cons_acct_num": "41", "ecoa": "AB"})
        self.record2 = acct_record(data_file, {"id": 2, "cons_acct_num": "42", "ecoa": "AC"})
        self.record3 = acct_record(data_file, {"id": 3, "cons_acct_num": "43", "ecoa": ""})
        self.record4 = acct_record(data_file, {"id": 4, "cons_acct_num": "44", "ecoa": "AE"})

        results_summary = EvaluatorResultSummary.objects.create(
            event=event,
            evaluator=self.evaluator,
            hits=4
        )
        EvaluatorResult.objects.create(
            date=self.record1.activity_date,
            result_summary=results_summary,
            source_record=self.record1,
        )
        EvaluatorResult.objects.create(
            date=self.record2.activity_date,
            result_summary=results_summary,
            source_record=self.record2
        )
        EvaluatorResult.objects.create(
            date=self.record3.activity_date,
            result_summary=results_summary,
            source_record=self.record3
        )
        EvaluatorResult.objects.create(
            date=self.record4.activity_date,
            result_summary=results_summary,
            source_record=self.record4
        )

    def test_get_flat_related_fields(self):
        serializer = EvaluatorResultAccountActivitySerializer(
            self.record1,
            evaluator=self.evaluator,
        )

        related_fields = serializer.get_flat_related_fields()

        # Make sure we have fields from AccountHolder
        self.assertTrue(
            any(key.startswith("account_holder") for key in related_fields)
        )

        # Make sure that models we *don't* want aren't included,
        # like EvaluatorResult
        self.assertFalse(
            any(key.startswith("evaluatorresult") for key in related_fields)
        )

    def test_serialize_single(self):
        serializer = EvaluatorResultAccountActivitySerializer(
            self.record1,
            evaluator=self.evaluator,
        )
        result_data = serializer.data
        # The record only has the number of fields in the
        # evaluator.result_summary_fields()
        self.assertEqual(
            len(result_data),
            len(self.evaluator.result_summary_fields())
        )

    def test_serialize_multiple(self):
        serializer = EvaluatorResultAccountActivitySerializer(
            [self.record1, self.record2, self.record3, self.record4],
            evaluator=self.evaluator,
            many=True,
        )
        result_data = serializer.data
        # There are four serialized records
        self.assertEqual(len(result_data), 4)

        first_result = result_data[0]
        # The records only have the number of fields in the
        # evaluator.result_summary_fields()
        self.assertEqual(
            len(first_result),
            len(self.evaluator.result_summary_fields())
        )
