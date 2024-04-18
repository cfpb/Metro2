from datetime import date
from django.test import TestCase
from rest_framework.renderers import JSONRenderer

from evaluate_m2.models import EvaluatorMetadata, EvaluatorResult, EvaluatorResultSummary
from evaluate_m2.serializers import (
    EvaluatorMetadataSerializer,
    EvaluatorResultsViewSerializer,
    EventsViewSerializer
)
from parse_m2.models import AccountActivity, AccountHolder, M2DataFile, Metro2Event


class EvaluatorMetadataSerializerTestCase(TestCase):
    def setUp(self) -> None:
        # Create an EvaluatorMetadata record
        self.eval1 = EvaluatorMetadata.create_from_dict({
            'id': 'Status-DOFD-1',
            'description': 'description of Status-DOFD-1',
            'long_description': '',
            'fields_used': 'account status;date of first delinquency',
            'fields_display': 'amount past due;compliance condition code;current balance;date closed;original charge-off amount;scheduled monthly payment amount;special comment code;terms frequency',
            'crrg_topics': '',
            'crrg_page': '400',
            'pdf_page': '',
            'use_notes': '',
            'alternative_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
        })

        self.json_representation = {'id': 'Status-DOFD-1',
            'description': 'description of Status-DOFD-1',
            'long_description': '',
            'fields_used': 'account status;date of first delinquency',
            'fields_display': 'amount past due;compliance condition code;current balance;date closed;original charge-off amount;scheduled monthly payment amount;special comment code;terms frequency',
            'crrg_topics': '',
            'crrg_page': '400',
            'pdf_page': '',
            'use_notes': '',
            'alternative_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
        }

    def test_evaluator_metadata_serializer(self):
        serializer = EvaluatorMetadataSerializer(self.eval1)
        self.assertEqual(serializer.data, self.json_representation)

    def test_group_serializer_many_true(self):
        eval_metadata = [self.eval1]
        serializer = EvaluatorMetadataSerializer(eval_metadata, many=True)
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render([self.json_representation])
        self.assertEqual(json_output, expected)

class EvaluatorResultsViewSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.eval1 = EvaluatorMetadata.create_from_dict({
            'id': 'Status-DOFD-1',
            'description': 'description of Status-DOFD-1',
            'long_description': '',
            'fields_used': 'account status;date of first delinquency',
            'fields_display': 'amount past due;compliance condition code;current balance;date closed;original charge-off amount;scheduled monthly payment amount;special comment code;terms frequency',
            'crrg_topics': '',
            'crrg_page': '400',
            'pdf_page': '',
            'use_notes': '',
            'alternative_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
        })
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
        self.eval = EvaluatorMetadata.create_from_dict({
            'id': 'Status-DOFD-1',
            'description': 'description of Status-DOFD-1',
            'long_description': '',
            'fields_used': 'account status;date of first delinquency',
            'fields_display': 'amount past due;compliance condition code;current balance;date closed;original charge-off amount;scheduled monthly payment amount;special comment code;terms frequency',
            'crrg_topics': '',
            'crrg_page': '400',
            'pdf_page': '',
            'use_notes': '',
            'alternative_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
        })

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
                'crrg_topics': '', 'crrg_page': '400', 'pdf_page': '',
                'use_notes': '', 'alternative_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
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
