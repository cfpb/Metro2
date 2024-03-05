from django.test import TestCase
from datetime import date

from evaluate_m2.models import (
    EvaluatorMetadata,
    EvaluatorResult,
    EvaluatorResultSummary
)
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper
from parse_m2.models import M2DataFile, Metro2Event


class EvaluateViewsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self) -> None:
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
        self.eval2 = EvaluatorMetadata.create_from_dict({
            'id': 'ADDL-DOFD-2',
            'name': '',
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
        self.eval3 = EvaluatorMetadata.create_from_dict({
            'id': 'ADDL-DOFD-3',
            'name':'',
            'description': 'description for a third addl-dofd eval',
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
        self.expected_activity = [{
            'activity_date': '2019-12-31', 'port_type': 'X', 'acct_type': '00',
            'date_open': '2020-01-01', 'credit_limit': 0, 'hcola': 0, 'terms_dur': '0',
            'terms_freq': '0', 'smpa': 0, 'actual_pmt_amt': 0, 'acct_stat': '00',
            'pmt_rating': '0', 'php': '', 'spc_com_cd': 'X', 'compl_cond_cd': '0',
            'current_bal': 0, 'amt_past_due': 0, 'orig_chg_off_amt': 0,
            'doai': '2020-01-01', 'dofd': '2020-01-01', 'date_closed': '2020-01-01',
            'dolp': None, 'int_type_ind': ''}]

    def create_activity_data(self):
        # Create the parent records for the AccountActivity data
        event = Metro2Event(id=1, name='test_exam')
        event.save()
        data_file = M2DataFile(event=event, file_name='file.txt')
        data_file.save()
        # Create the Account Holders
        accounts = self.create_bulk_account_holders(data_file, ('Z','Y','X'))
        # Create the Account Activities data
        activities = {'id':(32,33), 'account_holder':('Z','Y'),
                      'cons_acct_num':('0032', '0033')}
        acct_actvities = self.create_bulk_activities(data_file, activities, 2)
        eval_rs = EvaluatorResultSummary(
            event=event, evaluator=self.eval1, hits=2)
        eval_rs.save()
        eval_rs2 = EvaluatorResultSummary(
            event=event, evaluator=self.eval3, hits=1)
        eval_rs2.save()
        eval_r1 = EvaluatorResult(
            result_summary=eval_rs, date=date(2021, 1, 1),
            field_values={'record': 1, 'acct_type':'y'},
            source_record= acct_actvities[0], acct_num='0032')
        eval_r1.save()
        eval_r2 = EvaluatorResult(
            result_summary=eval_rs, date=date(2021, 1, 1),
            field_values={'record': 2, 'acct_type': 'n'},
            source_record= acct_actvities[1], acct_num='0033')
        eval_r2.save()
        eval_r3 = EvaluatorResult(
            result_summary=eval_rs2, date=date(2021, 1, 1),
            field_values={'record': 3, 'acct_type': 'n'},
            source_record= acct_actvities[0], acct_num='0032')
        eval_r3.save()

    def test_download_eval_metadata(self):
        response = self.client.get('/all-evaluator-metadata')

        # the response should be a CSV
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/csv')
        self.assertIn('filename=evaluator-metadata',
            response.headers['Content-Disposition'])

        # the CSV should contain info about the evals
        csv_content = response.content.decode('utf-8')
        for item in self.eval1.serialize():
            self.assertIn(item, csv_content)
        for item in self.eval2.serialize():
            self.assertIn(item, csv_content)
        for item in self.eval3.serialize():
            self.assertIn(item, csv_content)

    def test_download_evaluator_results_csv(self):
        self.create_activity_data()

        response = self.client.get('/events/1/evaluator/ADDL-DOFD-1/csv')

        # the response should be a CSV
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/csv')
        self.assertIn(f'filename=test_exam_ADDL-DOFD-1_{date.today()}.csv',
            response.headers['Content-Disposition'])

        # the CSV should contain info about the evaluator_results
        csv_content = response.content.decode('utf-8')

        expected = "\r\n".join([
            "event_name,record,acct_type",
            "test_exam,1,y",
            "test_exam,2,n",
            "",
        ])
        self.assertEqual(csv_content, expected)

    def test_evaluator_results_view(self):
        expected = {'hits': [{'record': 1, 'acct_type':'y'},
                             {'record': 2, 'acct_type': 'n'}]}
        self.create_activity_data()

        response = self.client.get('/events/1/evaluator/ADDL-DOFD-1')
        # the response should be a JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        # the response should a hits field with a list of EvaluatorResult field_values
        self.assertEqual(response.json(), expected)

    def test_evaluator_results_view_with_error_no_evaluator_metadata(self):
        self.create_activity_data()
        response = self.client.get('/events/1/evaluator/NON_EXISTENT')

        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertContains(response, 'Evaluator: NON_EXISTENT does not exist.',
            status_code=404)

    def test_evaluator_results_view_with_error_no_event(self):
        response = self.client.get('/events/1/evaluator/ADDL-DOFD-1')

        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertContains(response, 'Event ID: 1 does not exist.', status_code=404)

    def test_evaluator_results_view_with_error_no_evaluator_results_summary(self):
        self.create_activity_data()
        response = self.client.get('/events/1/evaluator/ADDL-DOFD-2')
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertContains(response,
            'Evaluator result does not exist for event ID 1 or evaluator ID ADDL-DOFD-2.',
            status_code=404)

    def test_account_summary_view_single_results(self):
        self.create_activity_data()
        expected = {
            'const_acct_num': '0033',
            'inconsistencies': [
                {
                    'id': 'ADDL-DOFD-1',
                    'name': 'Additional evaluator for Date of First Delinquency'
                }
            ],
            'account_activity': self.expected_activity
        }

        response = self.client.get('/events/1/account/0033')
        # the response should be a JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        # the response should a hits field with a list of EvaluatorResult field_values
        self.assertEqual(response.json(), expected)

    def test_account_summary_view_multiple_results(self):
        self.create_activity_data()
        expected = {
            'const_acct_num': '0032',
            'inconsistencies': [
                { 'id': 'ADDL-DOFD-1',
                  'name': 'Additional evaluator for Date of First Delinquency' },
                { 'id': 'ADDL-DOFD-3', 'name': '' },
            ],
            'account_activity': self.expected_activity
        }

        response = self.client.get('/events/1/account/0032')
        # the response should be a JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        # the response should a hits field with a list of EvaluatorResult field_values
        self.assertEqual(response.json(), expected)