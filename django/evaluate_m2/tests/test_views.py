from django.test import TestCase

from evaluate_m2.evaluate import evaluator
from evaluate_m2.m2_evaluators.addl_dofd_evals import addl_dofd_1_func
from evaluate_m2.models import EvaluatorMetadata
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper

from parse_m2.models import M2DataFile, Metro2Event


class EvaluateViewsTestCase(TestCase, EvaluatorTestHelper):
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

    def create_activity_data(self):
                # Create the parent records for the AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()
        # Create the Account Holders
        self.create_bulk_account_holders(self.data_file, ('Z','Y'))
        # Create the Account Activities data
        activities = {
            'id':(32,33),
            'cons_acct_num':('0032','0033'),
            'account_holder':('Z','Y'),
            'acct_stat':('71','97'),
            'dofd':(None,None),
            'pmt_rating':('1','2')}
        self.create_bulk_activities(self.data_file, activities, 2)

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

    def test_download_evaluator_results(self):
        expected = {
            'hits': [
                {
                    'id': 32, 'activity_date': '2019-12-31', 'cons_acct_num': '0032',
                    'acct_stat': '71', 'dofd': None, 'amt_past_due': 0,
                    'compl_cond_cd': '0', 'current_bal': 0, 'date_closed': '2020-01-01',
                    'orig_chg_off_amt': 0, 'smpa': 0, 'spc_com_cd': 'X', 'terms_freq': '0'
                }, {
                    'id': 33, 'activity_date': '2019-12-31', 'cons_acct_num': '0033',
                    'acct_stat': '97', 'dofd': None, 'amt_past_due': 0,
                    'compl_cond_cd': '0', 'current_bal': 0, 'date_closed': '2020-01-01',
                    'orig_chg_off_amt': 0, 'smpa': 0, 'spc_com_cd': 'X',
                    'terms_freq': '0'
                }
            ]}
        self.create_activity_data()

        evaluator.evaluators = {
            "ADDL-DOFD-1": addl_dofd_1_func}
        evaluator.run_evaluators(self.event)
        response = self.client.get('/events/1/evaluator/ADDL-DOFD-1/')

        # the response should be a JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        # the response should a list of contain field_values from EvaluatorResult
        self.assertEqual(response.json(), expected)
