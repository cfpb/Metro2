from django.test import TestCase
from datetime import date

from evaluate_m2.models import (
    EvaluatorMetadata,
    EvaluatorResult,
    EvaluatorResultSummary
)
from evaluate_m2.serializers import EvaluatorMetadataSerializer
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper
from parse_m2.models import AccountHolder, M2DataFile, Metro2Event


class EvaluateViewsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self) -> None:
        self.eval1 = EvaluatorMetadata.objects.create(
            id='Status-DOFD-1',
            description='description of Status-DOFD-1',
            long_description='',
            fields_used=['placeholder', 'dofd'],
            fields_display=['amt_past_due', 'compl_cond_cd',
                'smpa', 'spc_com_cd', 'terms_freq'],
            crrg_reference='400',
            alternate_explanation='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
        )
        self.eval2 = EvaluatorMetadata.objects.create(
            id='Status-DOFD-2',
            description='description for the other status-dofd eval',
            long_description='',
            fields_used=['placeholder', 'dofd', 'php'],
            fields_display= ['orig_chg_off_amt'],
            crrg_reference='41',
            alternate_explanation='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
        )
        self.eval3 = EvaluatorMetadata.objects.create(
            id='Status-DOFD-4',
            description= 'description for a third status-dofd eval',
            long_description='',
            fields_used= ['smpa'],
            fields_display= ['orig_chg_off_amt', 'terms_freq'],
            crrg_reference='410',
            alternate_explanation='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
        )

    def get_account_activity(self, id: int, inconsistencies: list[str]):
        return [{ 'id': id, 'inconsistencies': inconsistencies,
                 'activity_date': '2019-12-31', 'port_type': 'X',
                 'acct_type': '00', 'date_open': '2020-01-01', 'credit_limit': 0,
                 'hcola': 0, 'id_num': '', 'terms_dur': '0', 'terms_freq': '0', 'smpa': 0,
                 'actual_pmt_amt': 0, 'acct_stat': '00', 'pmt_rating': '0', 'php': 'X',
                 'spc_com_cd': 'X', 'compl_cond_cd': '0', 'current_bal': 0,
                 'amt_past_due': 0, 'orig_chg_off_amt': 0, 'doai': '2020-01-01',
                 'dofd': '2020-01-01', 'date_closed': '2020-01-01', 'dolp': None,
                 'int_type_ind': ''}]

    def create_activity_data(self):
        # Create the parent records for the AccountActivity data
        event = Metro2Event(id=1, name='test_exam')
        event.save()
        data_file = M2DataFile(event=event, file_name='file.txt')
        data_file.save()
        # Create the Account Holders
        acct_holder = AccountHolder(id=1, data_file=data_file,
            activity_date=date(2023, 11, 30), surname='Doe', first_name='Jane',
            middle_name='A', gen_code='F', ssn='012345678', dob='01012000',
            phone_num='0123456789', ecoa='0', cons_info_ind='Z', cons_acct_num='012345')
        acct_holder.save()
        acct_holder2 = AccountHolder(id=2, data_file=data_file,
            activity_date=date(2023, 11, 30), cons_info_ind='Y', cons_acct_num='012345')
        acct_holder2.save()
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
        response = self.client.get('/api/all-evaluator-metadata/')

        # the response should be a CSV
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/csv')
        self.assertIn('filename=evaluator-metadata',
            response.headers['Content-Disposition'])

        # the CSV should contain info about the evals
        csv_content = response.content.decode('utf-8')
        for item in EvaluatorMetadataSerializer(self.eval1).data:
            self.assertIn(item, csv_content)
        for item in EvaluatorMetadataSerializer(self.eval2).data:
            self.assertIn(item, csv_content)
        for item in EvaluatorMetadataSerializer(self.eval3).data:
            self.assertIn(item, csv_content)

    def test_download_evaluator_results_csv(self):
        self.create_activity_data()

        response = self.client.get('/api/events/1/evaluator/Status-DOFD-1/csv/')

        # the response should be a CSV
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/csv')
        self.assertIn(f'filename=test_exam_Status-DOFD-1_{date.today()}.csv',
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

        response = self.client.get('/api/events/1/evaluator/Status-DOFD-1/')
        # the response should be a JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        # the response should a hits field with a list of EvaluatorResult field_values
        self.assertEqual(response.json(), expected)

    def test_evaluator_results_view_with_error_no_evaluator_metadata(self):
        self.create_activity_data()
        response = self.client.get('/api/events/1/evaluator/NON_EXISTENT/')

        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertContains(response, 'Evaluator: NON_EXISTENT does not exist.',
            status_code=404)

    def test_evaluator_results_view_with_error_no_event(self):
        response = self.client.get('/api/events/1/evaluator/Status-DOFD-1/')

        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertContains(response, 'Event ID: 1 does not exist.', status_code=404)

    def test_evaluator_results_view_with_error_no_evaluator_results_summary(self):
        self.create_activity_data()
        response = self.client.get('/api/events/1/evaluator/Status-DOFD-2/')
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertContains(response,
            'EvaluatorResultSummary record(s) not found for event ID 1.',
            status_code=404)

    def test_account_summary_view_single_results(self):
        self.create_activity_data()
        inconsistencies = ['Status-DOFD-1']
        expected = {
            'cons_acct_num': '0033',
            'inconsistencies': inconsistencies,
            'account_activity': self.get_account_activity(33, inconsistencies)
        }
        response = self.client.get('/api/events/1/account/0033/')

        # the response should be a JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        # the response should a hits field with a list of EvaluatorResult field_values
        self.assertEqual(response.json(), expected)

    def test_account_summary_view_multiple_results(self):
        self.create_activity_data()
        inconsistencies = ['Status-DOFD-1', 'Status-DOFD-4']
        expected = {
            'cons_acct_num': '0032',
            'inconsistencies': ['Status-DOFD-1', 'Status-DOFD-4'],
            'account_activity': self.get_account_activity(32, inconsistencies)
        }
        response = self.client.get('/api/events/1/account/0032/')

        # the response should be a JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        # the response should a hits field with a list of EvaluatorResult field_values
        self.assertEqual(response.json(), expected)

    def test_account_summary_view_no_accountactivity_for_event(self):
        self.create_activity_data()
        error='AccountActivity record(s) not found for account number 0039.'
        response = self.client.get('/api/events/1/account/0039/')

        # the response should be a JSON
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        self.assertEqual(response.json()['message'], error)

    def test_account_pii_view(self):
        self.create_activity_data()
        expected = {'id': 1, 'surname': 'Doe', 'first_name': 'Jane', 'middle_name': 'A',
                    'gen_code': 'F', 'ssn': '012345678', 'dob': '01012000',
                    'phone_num': '0123456789', 'ecoa': '0', 'cons_info_ind': 'Z',
                    'country_cd': '', 'addr_line_1': '', 'addr_line_2': '', 'city': '',
                    'state': '', 'zip': '', 'addr_ind': '', 'res_cd': '',
                    'cons_acct_num': '012345'}

        response = self.client.get('/api/events/1/account/012345/account_holder/')
        # the response should be a JSON

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        # the response should a hits field with a list of EvaluatorResult field_values
        self.assertEqual(response.json(), expected)

    def test_events_view(self):
        self.create_activity_data()
        expected = {
            'id': 1,
            'name': 'test_exam',
            'evaluators': [{
                'hits': 2, 'id': 'Status-DOFD-1',
                'description': 'description of Status-DOFD-1', 'long_description': '',
                'fields_used': ['acct_stat', 'dofd'],
                'fields_display': ['amt_past_due', 'compl_cond_cd', 'smpa', 'spc_com_cd', 'terms_freq'],
                'crrg_reference': '400', 'potential_harm': '',
                'rationale': '', 'alternate_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
            }, {
                'hits': 1, 'id': 'Status-DOFD-4', 'description':
                    'description for a third status-dofd eval', 'long_description': '',
                    'fields_used': ['smpa'],
                    'fields_display': ['orig_chg_off_amt', 'terms_freq'],
                'crrg_reference': '410', 'potential_harm': '',
                'rationale': '', 'alternate_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
            }]}


        response = self.client.get('/api/events/1/')
        # the response should be a JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        # the response should a hits field with a list of EvaluatorResult field_values
        self.assertEqual(len(response.json()['evaluators']), 2)
        self.assertEqual(response.json(), expected)
