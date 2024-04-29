from datetime import date
from django.test import TestCase
from rest_framework.renderers import JSONRenderer

from evaluate_m2.models import EvaluatorMetadata, EvaluatorResult, EvaluatorResultSummary
from evaluate_m2.serializers import (
    ImportEvaluatorMetadataSerializer,
    EvaluatorResultsViewSerializer,
    EventsViewSerializer
)
from parse_m2.models import AccountActivity, AccountHolder, M2DataFile, Metro2Event


e1_expected_fields_used = """
Identifying information
DB record id
activity date
customer account number

Fields used for evaluator
consumer information indicator
date of last payment

Helpful fields that are also displayed currently
special comment code
date of first delinquency
"""

e2_expected_fields_used = """
Identifying information
DB record id
activity date
customer account number

Fields used for evaluator
wrong
misspelled

Helpful fields that are also displayed currently
other
"""

class ImportEvalSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.multi_line_text="""Here is some text.
        It is split over two lines."""

        self.e1 = EvaluatorMetadata(
            id="Betsy-1",
            description="desc 1",
            long_description=self.multi_line_text,
            fields_used=["cons_info_ind", "dolp"],
            fields_display=["spc_com_cd", "dofd"],
            crrg_reference="PDF page 3",
        )

        self.e1_json = {
            'id': 'Betsy-1',
            'description': 'desc 1',
            'long_description': self.multi_line_text,
            'fields_used': e1_expected_fields_used,
            'crrg_reference': 'PDF page 3',
            'potential_harm': '',
            'rationale': '',
            'alternate_explanation': '',
        }

    def test_to_json(self):
        to_json = ImportEvaluatorMetadataSerializer(self.e1)
        self.assertEqual(to_json.data, self.e1_json)

    def test_default_value_if_field_name_nonexistent(self):
        e2 = EvaluatorMetadata(
            id="TEST-11",
            fields_used=["wrong", "misspelled"],
            fields_display=["other"],
        )
        e2_json = {
            'id': 'TEST-11',
            'description': '',
            'long_description': '',
            'fields_used': e2_expected_fields_used,
            'crrg_reference': '',
            'potential_harm': '',
            'rationale': '',
            'alternate_explanation': '',
        }

        to_json = ImportEvaluatorMetadataSerializer(e2)
        self.assertEqual(to_json.data, e2_json)

    def test_from_json(self):
        json = self.e1_json.copy()
        json['id'] = "BETSY-NEW"
        from_json = ImportEvaluatorMetadataSerializer(data=json)
        self.assertTrue(from_json.is_valid())
        record = from_json.save()
        self.assertEqual(record.id, "BETSY-NEW")
        self.assertEqual(record.description, self.e1_json['description'])
        self.assertEqual(record.fields_used, ['cons_info_ind', 'dolp'])
        self.assertEqual(record.fields_display, ['spc_com_cd', 'dofd'])

    def test_many_to_json(self):
        eval_metadata = [self.e1]
        serializer = ImportEvaluatorMetadataSerializer(eval_metadata, many=True)
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render([self.e1_json])
        self.assertEqual(json_output, expected)


class EvaluatorResultsViewSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.eval1 = EvaluatorMetadata.objects.create(
            id='Status-DOFD-1',
            description='description of Status-DOFD-1',
            long_description='',
            fields_used='account status;date of first delinquency',
            fields_display='amount past due;compliance condition code;current balance;date closed;original charge-off amount;scheduled monthly payment amount;special comment code;terms frequency',
            crrg_reference='400',
            alternate_explanation='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
        )
        # Create an EvaluatorResults record
        event = Metro2Event(name="tst")
        event.save()
        file = M2DataFile(event=event, file_name="tst.txt")
        file.save()
        acct_holder = AccountHolder(
            data_file=file,activity_date=date(2023, 11, 30), cons_acct_num="98765")
        acct_holder.save()

        self.acct_activity = AccountActivity(
            account_holder=acct_holder,
            activity_date=date(2023,11,20),
            cons_acct_num="98765",
            port_type="port_type",
            acct_type="acct_type",
            date_open=date(2020,3,17),
            credit_limit=9000,
            hcola=90210,
            terms_dur="terms_dur",
            terms_freq="terms_freq",
            smpa=5,
            actual_pmt_amt=201,
            acct_stat="acct_stat",
            pmt_rating="pmt_rating",
            php="php",
            spc_com_cd="spc_com_cd",
            compl_cond_cd="compl_cond_cd",
            current_bal=12345,
            amt_past_due=111,
            orig_chg_off_amt=0,
            doai=date(2023,11,3),
            dofd=None,
            date_closed=None,
            dolp=date(2023,1,1),
            int_type_ind="int_type_ind",
        )
        self.acct_activity.save()
        self.ers = EvaluatorResultSummary(event=event, evaluator=self.eval1, hits=1)
        self.ers.save()
        self.eval_result = EvaluatorResult(
            result_summary=self.ers, date=date(2021, 1, 1),
            field_values={'record': 1, 'acct_type':'y'},
            source_record= self.acct_activity, acct_num='0032')
        self.eval_result.save()
        self.json_representation = {'record': 1, 'acct_type':'y'}

    def test_evaluator_results_serializer(self):
        serializer = EvaluatorResultsViewSerializer(self.eval_result)
        self.assertEqual(serializer.data, self.json_representation)


class EventsViewSerializerTestCase(TestCase):
    def setUp(self) -> None:
        # Create an EvaluatorMetadata record
        self.eval = EvaluatorMetadata.objects.create(
            id='Status-DOFD-1',
            description='description of Status-DOFD-1',
            long_description='',
            fields_used=['placeholder', 'date of first delinquency'],
            fields_display=['amount past due', 'compliance condition code',
                    'current balance', 'date closed', 'original charge-off amount', 'scheduled monthly payment amount', 'special comment code',
                    'terms frequency'],
            crrg_reference='400',
            alternate_explanation='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
        )

        # Create the parent records for the AccountActivity data
        self.event = Metro2Event(id=1, name='test_exam')
        self.event.save()

        self.eval_rs = EvaluatorResultSummary(
            event=self.event, evaluator=self.eval, hits=2)
        self.eval_rs.save()

        self.json_representation = {
                'hits': 2, 'id': 'Status-DOFD-1',
                'description': 'description of Status-DOFD-1', 'long_description': '',
                'fields_used': ['account status', 'date of first delinquency'],
                'fields_display': ['amount past due', 'compliance condition code',
                    'current balance', 'date closed', 'original charge-off amount', 'scheduled monthly payment amount', 'special comment code',
                    'terms frequency'],
                'crrg_reference': '400', 'potential_harm': '',
                'rationale': '', 'alternate_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
            }

    def test_evaluator_metadata_serializer(self):
        serializer = EventsViewSerializer(self.eval, many=False, context={'event': self.event})
        self.assertEqual(serializer.data, self.json_representation)

    def test_group_serializer_many_true(self):
        evals = [self.eval]
        serializer = EventsViewSerializer(evals, many=True, context={'event': self.event})
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render([self.json_representation])
        self.assertEqual(json_output, expected)
