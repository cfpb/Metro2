from datetime import date
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from rest_framework.renderers import JSONRenderer

from evaluate_m2.models import EvaluatorMetadata
from evaluate_m2.serializers import EvaluatorMetadataSerializer

class EvaluatorMetadataSerializerTestCase(TestCase):
    def setUp(self) -> None:
        # Create an EvaluatorMetadata record
        self.eval1 = EvaluatorMetadata.create_from_dict({
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

        self.json_representation = {'id': 'ADDL-DOFD-1',
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
            'risk_level': 'High'}

    def test_evaluator_metadata_serializer(self):
        serializer = EvaluatorMetadataSerializer(self.eval1)
        self.assertEqual(serializer.data, self.json_representation)

    def test_group_serializer_many_true(self):
        eval_metadata = [self.eval1]
        serializer = EvaluatorMetadataSerializer(eval_metadata, many=True)
        json_output = JSONRenderer().render(serializer.data)
        expected = JSONRenderer().render([self.json_representation])
        self.assertEqual(json_output, expected)