from datetime import date

from django.test import TestCase

from rest_framework.renderers import JSONRenderer

from evaluate_m2.models import (
    EvaluatorMetadata,
    EvaluatorResult,
    EvaluatorResultMaterializedView,
    EvaluatorResultSummary,
)
from evaluate_m2.serializers import (
    EvaluatorMetadataSerializer,
    EvaluatorResultSerializer,
    EventsViewSerializer,
)
from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.models import M2DataFile, Metro2Event


class EvalSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.multi_line_text="""Here is some text.
        It is split over two lines."""

        self.e1 = EvaluatorMetadata(
            id="Betsy-1",
            category="paid/not paid",
            description="desc 1",
            long_description=self.multi_line_text,
            fields_used=["cons_info_ind", "dolp", "id_num"],
            fields_display=["spc_com_cd", "dofd", "l1__change_ind"],
            crrg_reference="PDF page 3",
            interpret_fields_last_modified=date(2025,9,30),
        )

        self.e1_json = {
            'id': 'Betsy-1',
            'category': 'paid/not paid',
            'description': 'desc 1',
            'long_description': self.multi_line_text,
            'fields_used': "cons_info_ind;dolp;id_num",
            'fields_display': "spc_com_cd;dofd;l1__change_ind",
            'crrg_reference': 'PDF page 3',
            'potential_harm': '',
            'rationale': '',
            'alternate_explanation': '',
            'interpret_fields_last_modified': '2025-09-30',
            'additional_notes': '',
            'additional_notes_last_modified': '',
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
            'fields_used': "wrong;misspelled",
            'fields_display': "other",
            'crrg_reference': '',
            'potential_harm': '',
            'rationale': '',
            'alternate_explanation': '',
            'interpret_fields_last_modified': '',
            'additional_notes': '',
            'additional_notes_last_modified': '',
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
        self.assertEqual(record.fields_used, ['cons_info_ind', 'dolp', 'id_num'])
        self.assertEqual(
            record.fields_display,
            ['spc_com_cd', 'dofd', 'l1__change_ind']
        )
        self.assertEqual(record.interpret_fields_last_modified, date(2025,9,30))
        self.assertEqual(record.additional_notes_last_modified,
                         EvaluatorMetadata._last_modified_never)

    def test_import_fails_when_field_names_incorrect(self):
        fields = "dolp;bogus;k2__purc_sold_ind;wrong"
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
            id='Sample-Eval-1',
            category='paid/not paid',
            description='description of Sample-Eval-1',
            long_description='',
            fields_used=['hcola', 'smpa', 'date of first delinquency'],
            fields_display=['amount past due', 'compliance condition code',
                    'current balance', 'date closed', 'original charge-off amount',
                    'terms frequency'],
            crrg_reference='400',
            alternate_explanation='Lorem ipsum dolor sit amet',
            interpret_fields_last_modified=date(2025,10,31),
        )

        # Create the parent records for the AccountActivity data
        self.event = Metro2Event.objects.create(id=1, name='test_exam')
        file = M2DataFile.objects.create(event=self.event, file_name="tst.txt")
        activity = { 'id': 32, 'activity_date': date(2023,11,20),
                    'cons_acct_num': '0032','current_bal':0, 'amt_past_due': 5 }
        acct_record(file, activity)

        self.eval_rs = EvaluatorResultSummary.objects.create(
            event=self.event,
            evaluator=self.eval,
            hits=2,
            accounts_affected=1,
            inconsistency_start=date(2021, 1, 1),
            inconsistency_end=date(2021, 2, 1)
        )

        self.json_representation = {
            'hits': 2,
            'accounts_affected': 1,
            'inconsistency_start':date(2021, 1, 1),
            'inconsistency_end': date(2021, 2, 1),
            'id': 'Sample-Eval-1',
            'category': 'paid/not paid',
            'description': 'description of Sample-Eval-1',
            'long_description': '',
            'fields_used': ['hcola', 'smpa', 'date of first delinquency'],
            'fields_display': [
                'amount past due',
                'compliance condition code',
                'current balance',
                'date closed',
                'original charge-off amount',
                'terms frequency'
            ],
            'crrg_reference': '400',
            'potential_harm': '',
            'rationale': '',
            'alternate_explanation': 'Lorem ipsum dolor sit amet',
            'interpret_fields_last_modified': date(2025,10,31),
            'additional_notes': '',
            'additional_notes_last_modified': None,
        }

    def test_evaluator_metadata_serializer(self):
        serializer = EventsViewSerializer(
            self.eval_rs,
            many=False,
            context={'event': self.event}
        )
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render(self.json_representation)
        self.assertEqual(json_output, expected)

    def test_group_serializer_many_true(self):
        evals = [self.eval_rs]
        serializer = EventsViewSerializer(
            evals,
            many=True,
            context={'event': self.event}
        )
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render([self.json_representation])
        self.assertEqual(json_output, expected)


class EvaluatorResultSerializerTestCase(TestCase):
    acct_date = date(2023, 12, 31)

    def setUp(self):
        self.evaluator = EvaluatorMetadata.objects.create(id="Filter-Test-1")
        self.event = Metro2Event.objects.create(name="test_exam")
        data_file = M2DataFile.objects.create(
            event=self.event,
            file_name="file.txt"
        )
        summary = EvaluatorResultSummary.objects.create(
            event=self.event,
            evaluator=self.evaluator,
        )
        acct_activity = acct_record(data_file, {
            'id': 32,
            'cons_acct_num': 'ABC123',
            'acct_stat': '11',
            'compl_cond_cd': 'XB',
            'php': '000000000000010',
            'php1': '0',
            'pmt_rating': '0',
            'spc_com_cd': 'AH',
            'terms_freq': 'M',
            'cons_info_ind': 'Z',
        })

        EvaluatorResult.objects.create(
            result_summary=summary,
            source_record=acct_activity,
            date=self.acct_date,
        )

        EvaluatorResultMaterializedView.create_or_refresh_materialized_view()

        self.result = EvaluatorResultMaterializedView.objects.first()

    def test_export_to_json(self):
        # The serializer uses all columns of the
        # EvaluatorResultMaterializedView and translates the column names
        # to match those on the AccountActivity model (using double
        # underscores for related models).
        to_json = EvaluatorResultSerializer(self.result)
        expected_keys = [
            'k2__purch_sold_ind',
            'k2__purch_sold_name',
            'k4__spc_pmt_ind',
            'k4__deferred_pmt_st_dt',
            'k4__balloon_pmt_due_dt',
            'k4__balloon_pmt_amt',
            'l1__change_ind',
            'l1__new_acc_num',
            'l1__new_id_num',
            'previous_values__activity_date',
            'previous_values__port_type',
            'previous_values__acct_type',
            'previous_values__date_open',
            'previous_values__id_num',
            'previous_values__acct_stat',
            'previous_values__pmt_rating',
            'previous_values__current_bal',
            'previous_values__orig_chg_off_amt',
            'previous_values__dofd',
            'previous_values__date_closed',
            'previous_values__surname',
            'previous_values__first_name',
            'previous_values__ecoa',
            'previous_values__ecoa_assoc',
            'previous_values__cons_info_ind',
            'previous_values__cons_info_ind_assoc',
            'previous_values__l1__change_ind',
            'previous_values__l1__new_acc_num',
            'previous_values__l1__new_id_num',
            'activity_date',
            'cons_acct_num',
            'port_type',
            'acct_type',
            'date_open',
            'credit_limit',
            'hcola',
            'id_num',
            'terms_dur',
            'terms_freq',
            'smpa',
            'actual_pmt_amt',
            'acct_stat',
            'pmt_rating',
            'php',
            'php1',
            'spc_com_cd',
            'compl_cond_cd',
            'current_bal',
            'amt_past_due',
            'orig_chg_off_amt',
            'doai',
            'dofd',
            'date_closed',
            'dolp',
            'int_type_ind',
            'surname',
            'first_name',
            'middle_name',
            'gen_code',
            'ssn',
            'dob',
            'phone_num',
            'ecoa',
            'ecoa_assoc',
            'cons_info_ind',
            'cons_info_ind_assoc',
            'addr_line_1',
            'addr_line_2',
            'city',
            'state',
            'zip',
            'addr_ind',
            'res_cd',
        ]
        actual_keys = to_json.data.keys()
        [self.assertIn(k, actual_keys) for k in expected_keys]
        self.assertEqual(len(actual_keys), len(expected_keys))
