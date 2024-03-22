from django.test import TestCase
from rest_framework.renderers import JSONRenderer

from evaluate_m2.models import EvaluatorMetadata, EvaluatorResultSummary
from evaluate_m2.serializers import EventsViewSerializer
from parse_m2.models import Metro2Event


class EventsViewSerializerTestCase(TestCase):
    def setUp(self) -> None:
        # Create an EvaluatorMetadata record
        self.eval = EvaluatorMetadata.create_from_dict({
            'id': 'ADDL-DOFD-1',
            'name': 'Additional evaluator for Date of First Delinquency',
            'description': 'description of addl-dofd-1',
            'long_description': '',
            'fields_used': 'account status;date of first delinquency',
            'fields_display': 'amount past due;compliance condition code;current balance;date closed;original charge-off amount;scheduled monthly payment amount;special comment code;terms frequency',
            'ipl': '',
            'crrg_topics': '',
            'crrg_page': '400',
            'pdf_page': '',
            'use_notes': '',
            'alternative_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
            'risk_level': 'High'
        })

        # Create the parent records for the AccountActivity data
        self.event = Metro2Event(id=1, name='test_exam')
        self.event.save()

        self.eval_rs = EvaluatorResultSummary(
            event=self.event, evaluator=self.eval, hits=2)
        self.eval_rs.save()

        self.json_representation = {
                'hits': 2, 'id': 'ADDL-DOFD-1',
                'name': 'Additional evaluator for Date of First Delinquency',
                'description': 'description of addl-dofd-1', 'long_description': '',
                'fields_used': ['account status', 'date of first delinquency'],
                'fields_display': ['amount past due', 'compliance condition code',
                    'current balance', 'date closed', 'original charge-off amount', 'scheduled monthly payment amount', 'special comment code',
                    'terms frequency'],
                'ipl': '', 'crrg_topics': '', 'crrg_page': '400', 'pdf_page': '',
                'use_notes': '', 'alternative_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua', 'risk_level': 'High'
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
