from django.test import TestCase
from evaluate_m2.models import EvaluatorMetadata

class EvaluateViewsTestCase(TestCase):
    def setUp(self) -> None:
        self.eval1 = EvaluatorMetadata.create_from_dict({
            'name': 'ADDL-DOFD-1',
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
        self.eval2 = EvaluatorMetadata.create_from_dict({
            'name': 'ADDL-DOFD-2',
            'description': 'description for the other addl-dofd eval',
            'long_description': '',
            'fields_used': 'account status;dofd;php',
            'fields_display': 'original charge-off amount;scheduled monthly payment amount;special comment code;terms frequency',
            'ipl': '',
            'crrg_topics': '',
            'crrg_page': '41',
            'pdf_page': '',
            'use_notes': '',
            'alternative_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
            'risk_level': 'High'
        })
        return super().setUp()

    def test_download_eval_metadata(self):
        response = self.client.get('/all-evaluator-metadata/')

        # the response should be a CSV
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/csv')
        self.assertIn('filename=evaluator-metadata', response.headers['Content-Disposition'])

        # the CSV should contain info about the evals
        csv_content = response.content.decode('utf-8')
        for item in self.eval1.serialize():
            self.assertIn(item, csv_content)
        for item in self.eval2.serialize():
            self.assertIn(item, csv_content)
