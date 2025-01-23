from django.test import TestCase, override_settings
from datetime import date

from evaluate_m2.models import (
    EvaluatorMetadata,
    EvaluatorResult,
    EvaluatorResultSummary
)
from evaluate_m2.serializers import EvaluatorMetadataSerializer
from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.models import M2DataFile, Metro2Event


@override_settings(S3_ENABLED=False)
class EvaluateViewsTestCase(TestCase):

    ########################################
    # Methods for creating test data
    def setUp(self) -> None:
        self.stat_dofd_1 = EvaluatorMetadata.objects.create(
            id='Status-DOFD-1',
            category='DOFD',
            description='description of Status-DOFD-1',
            long_description='',
            fields_used=['placeholder', 'dofd'],
            fields_display=['amt_past_due', 'compl_cond_cd', 'smpa',],
        )
        self.stat_dofd_2 = EvaluatorMetadata.objects.create(
            id='Status-DOFD-2',
            description='description for the other status-dofd eval',
            long_description='',
            fields_used=['placeholder', 'dofd', 'php'],
            fields_display= ['orig_chg_off_amt'],
            crrg_reference='41',
            alternate_explanation='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
        )
        self.stat_dofd_4 = EvaluatorMetadata.objects.create(
            id='Status-DOFD-4',
            description= 'description for a third status-dofd eval',
            long_description='',
            fields_used= ['smpa'],
            fields_display= ['orig_chg_off_amt', 'terms_freq'],
            crrg_reference='410',
            alternate_explanation='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
        )
        self.stat_dofd_6 = EvaluatorMetadata.objects.create(
            id='Status-DOFD-6',
            category='account terms',
            description= 'description for a fourth status-dofd eval',
            long_description='',
            fields_used= ['smpa'],
            fields_display= ['orig_chg_off_amt', 'terms_freq'],
            crrg_reference='410',
            alternate_explanation='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
        )

    def get_account_activity(
        self, id: int, inconsistencies: list[str], cons_info_ind: str, ecoa: str, first_name: str, activity_date: str = '2023-12-31'):
        return { 'id': id, 'inconsistencies': inconsistencies,
                 'activity_date': activity_date, 'account_holder__surname': 'Doe',
                 'account_holder__first_name': first_name, 'port_type': 'A',
                 'acct_type': '', 'date_open': '2018-02-28', 'credit_limit': 0,
                 'hcola': 0, 'id_num': '', 'terms_dur': '00', 'terms_freq': '00',
                 'smpa': 0, 'actual_pmt_amt': 0, 'acct_stat': '00', 'pmt_rating': '0',
                 'php': '', 'spc_com_cd': '', 'compl_cond_cd': '', 'current_bal': 0,
                 'amt_past_due': 0, 'orig_chg_off_amt': 0, 'doai': '2022-05-01',
                 'dofd': None, 'date_closed': None, 'dolp': None,
                 'int_type_ind': '', 'account_holder__cons_info_ind': cons_info_ind,
                 'account_holder__ecoa': ecoa,
                 'account_holder__cons_info_ind_assoc': ['1A', 'B'],
                 'account_holder__ecoa_assoc': ['2', '1'],
                 'k2__purch_sold_ind': None, 'k2__purch_sold_name': None,
                 'k4__balloon_pmt_amt': None, 'l1__change_ind': None,
                 'l1__new_id_num': None, 'l1__new_acc_num': None}

    def create_activity_data(self, create_zero_hit:bool=False):
        # Create the parent records for the AccountActivity data
        self.event = Metro2Event.objects.create(
            id=1, name='test_exam', portfolio='credit cards',
            directory='Enforcement/Huyndai2025', eid_or_matter_num='123-456789',
            other_descriptor='',date_range_start='2023-11-30',
            date_range_end='2023-12-31')
        self.data_file = M2DataFile.objects.create(event=self.event, file_name='file.txt')

        # Create the Account Activities data
        acct_date=date(2023, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'00', 'pmt_rating':'0', 'amt_past_due': 0, 'surname':'Doe',
                'cons_info_ind': 'Z', 'first_name': 'Jane', 'ecoa_assoc': ['2', '1'],'cons_info_ind_assoc':['1A', 'B']
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'00', 'pmt_rating':'0', 'amt_past_due': 0, 'surname':'Doe',
                'cons_info_ind': 'Y', 'first_name': 'John', 'ecoa_assoc': ['2', '1'],'cons_info_ind_assoc':['1A', 'B']
            }]
        acct_actvities = []
        for item in activities:
            acct_actvities.append(acct_record(self.data_file, item))

        # Result records for Status-DOFD-1
        eval_rs = EvaluatorResultSummary.objects.create(
            event=self.event, evaluator=self.stat_dofd_1, hits=2, accounts_affected=1,
            inconsistency_start=acct_date, inconsistency_end=acct_date)
        EvaluatorResult.objects.create(result_summary=eval_rs, date=date(2021, 1, 1),
            source_record= acct_actvities[0], acct_num='0032', field_values={
                'record': 1, 'acct_type': 'y'
            })
        EvaluatorResult.objects.create(result_summary=eval_rs, date=date(2021, 1, 1),
            source_record= acct_actvities[1], acct_num='0033', field_values={
                'record': 2, 'acct_type': 'n'
            })

        # Result records for Status-DOFD-4
        eval_rs2 = EvaluatorResultSummary.objects.create(
            event=self.event, evaluator=self.stat_dofd_4, hits=1, accounts_affected=1,
            inconsistency_start=acct_date, inconsistency_end=acct_date)
        EvaluatorResult.objects.create(result_summary=eval_rs2, date=date(2021, 1, 1),
            source_record= acct_actvities[0], acct_num='0032', field_values={})

        # EvaluatorResultSummary for Status-DOFD-6
        self.eval_rs3 = EvaluatorResultSummary.objects.create(
            event=self.event, evaluator=self.stat_dofd_6, hits=25, accounts_affected=1,
            inconsistency_start=acct_date, inconsistency_end=acct_date)

        if create_zero_hit:
        # EvaluatorResultSummary for Status-DOFD-2
            self.eval_rs2 = EvaluatorResultSummary.objects.create(
                event=self.event, evaluator=self.stat_dofd_2, hits=0, accounts_affected=0,
                inconsistency_start=acct_date, inconsistency_end=acct_date)

    ########################################
    # Tests for Eval Metadata download
    def test_download_eval_metadata(self):
        response = self.client.get('/api/all-evaluator-metadata/')

        # the response should be a CSV
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/csv')
        self.assertIn('filename=evaluator-metadata',
            response.headers['Content-Disposition'])

        # the CSV should contain info about the evals
        csv_content = response.content.decode('utf-8')
        for item in EvaluatorMetadataSerializer(self.stat_dofd_1).data:
            self.assertIn(item, csv_content)
        for item in EvaluatorMetadataSerializer(self.stat_dofd_4).data:
            self.assertIn(item, csv_content)
        for item in EvaluatorMetadataSerializer(self.stat_dofd_6).data:
            self.assertIn(item, csv_content)

    ########################################
    # Tests for Eval Results CSV download
    def test_download_evaluator_results_csv(self):
        self.create_activity_data()

        response = self.client.get('/api/events/1/evaluator/Status-DOFD-1/csv/')

        # the response should be a CSV
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/csv')
        self.assertIn(f'filename=test_exam_Status-DOFD-1.csv',
            response.headers['Content-Disposition'])

        # the CSV should contain info about the evaluator_results
        csv_content = response.content.decode('utf-8')

        expected = '\r\n'.join([
            'event_name,id,activity_date,cons_acct_num,acct_stat,dofd,amt_past_due,compl_cond_cd,smpa',
            'test_exam,32,2023-12-31,0032,00,,0,,0',
            'test_exam,33,2023-12-31,0033,00,,0,,0',
            ''
        ])
        self.assertEqual(csv_content, expected)

    ########################################
    # Tests for Eval Results view API endpoint
    def test_evaluator_results_view(self):
        # Status-dofd-1 uses the following fields:
        #     acct_stat, dofd, amt_past_due, compl_cond_cd, smpa
        # along with the fields that are always returned:
        #     id, activity_date, cons_acct_num
        expected = [{
            'id': 32, 'activity_date': '2023-12-31', 'cons_acct_num': '0032',
            'acct_stat': '00', 'dofd': None, 'amt_past_due': 0,
            'compl_cond_cd': '', 'smpa': 0
        }, {
            'id': 33, 'activity_date': '2023-12-31', 'cons_acct_num': '0033',
            'acct_stat': '00', 'dofd': None, 'amt_past_due': 0,
            'compl_cond_cd': '', 'smpa': 0
        },]

        self.create_activity_data()
        response = self.client.get('/api/events/1/evaluator/Status-DOFD-1/')
        # the response should be a JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        # the response should return a hits field with a list of EvaluatorResult
        # field_values
        # There should be two hits. Each one should have a set of keys that matches
        # the fields in evaluator.result_summary_fields
        hits = response.json()['hits']
        self.assertEqual(hits, expected)

    def test_evaluator_results_view_max_20_results(self):
        self.create_activity_data()

        for index in range(25):
            activity = {'id': index, 'activity_date': date(2023, 12, 31),
                    'cons_acct_num': '0032'}
            record = acct_record(self.data_file, activity)
            EvaluatorResult.objects.create(
                result_summary=self.eval_rs3, date=date(2021, 1, 1),
                field_values={'record': index, 'acct_type':'y'},
                source_record=record, acct_num='0032')
        self.eval_rs3.sample_ids = [1,3,5,7,9]
        self.eval_rs3.save()

        response = self.client.get('/api/events/1/evaluator/Status-DOFD-6/')
        # the response should be a JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['hits']), 5)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

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

    ########################################
    # Tests for Account Summary view API endpoint
    def test_account_summary_view_single_results(self):
        self.create_activity_data()
        inconsistencies = ['Status-DOFD-1']
        expected = {
            'cons_acct_num': '0033',
            'inconsistencies': inconsistencies,
            'account_activity': [self.get_account_activity(33, inconsistencies, 'Y', '', 'John')]
        }
        response = self.client.get('/api/events/1/account/0033/')

        # the response should be a JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        self.assertEqual(response.json(), expected)

    def test_account_summary_view_multiple_results(self):
        self.create_activity_data()

        # Create the Previous Account Activities data
        prev_file = M2DataFile.objects.create(event=self.event, file_name='prev.txt')
        prev_date=date(2023, 11, 30)
        acct_record(prev_file, {
                'id': 22, 'activity_date': prev_date, 'cons_acct_num': '0032',
                'acct_stat':'00', 'pmt_rating':'0', 'amt_past_due': 0, 'surname':'Doe',
                'cons_info_ind': 'A', 'first_name': 'Jane', 'ecoa_assoc': ['2', '1'],'cons_info_ind_assoc':['1A', 'B']
        })
        inconsistencies = ['Status-DOFD-1', 'Status-DOFD-4']
        expected = {
            'cons_acct_num': '0032',
            'inconsistencies': inconsistencies,
            'account_activity': [
                self.get_account_activity(22, [], 'A', '', 'Jane', '2023-11-30'),
                self.get_account_activity(32, inconsistencies, 'Z', '', 'Jane')]
        }
        response = self.client.get('/api/events/1/account/0032/')

        # the response should be a JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        # the response should include an account_activity field as a list of
        # account activities sorted by the actvity_date
        self.assertEqual(response.json(), expected)

    def test_account_summary_view_no_accountactivity_for_event(self):
        self.create_activity_data()
        error='AccountActivity record(s) not found for account number 0039.'
        response = self.client.get('/api/events/1/account/0039/')

        # the response should be a JSON
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        self.assertEqual(response.json()['message'], error)

    ########################################
    # Tests for Account PII view API endpoint
    def test_account_pii_view(self):
        self.create_activity_data()

        response = self.client.get('/api/events/1/account/0033/account_holder/')
        # the response should be a JSON
        expected = {'id': response.json()['id'], 'surname': 'Doe', 'first_name': 'John',
                    'middle_name': '', 'gen_code': '', 'ssn': '', 'dob': '',
                    'phone_num': '', 'ecoa': '', 'cons_info_ind': 'Y',
                    'country_cd': '', 'addr_line_1': '', 'addr_line_2': '', 'city': '',
                    'state': '', 'zip': '', 'addr_ind': '', 'res_cd': '',
                    'cons_acct_num': '0033'}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        self.assertEqual(response.json(), expected)

    ########################################
    # Tests for Events view API endpoint (all evals with hits for an event)
    def test_events_view(self):
        self.create_activity_data(create_zero_hit=True)
        expected = {
            'id': 1,
            'name': 'test_exam',
            'portfolio': 'credit cards',
            'eid_or_matter_num': '123-456789',
            'other_descriptor': '',
            'directory': 'Enforcement/Huyndai2025',
            'date_range_start': '2023-11-30',
            'date_range_end': '2023-12-31',
            'evaluators': [{
                'hits': 2,
                'accounts_affected': 1,
                'inconsistency_start': '2023-12-31',
                'inconsistency_end': '2023-12-31',
                'id': 'Status-DOFD-1',
                'category': 'DOFD',
                'description': 'description of Status-DOFD-1', 'long_description': '',
                'fields_used': ['acct_stat', 'dofd'],
                'fields_display': ['amt_past_due', 'compl_cond_cd', 'smpa',],
                'crrg_reference': '', 'potential_harm': '',
                'rationale': '', 'alternate_explanation': '',
            }, {
                'hits': 1,
                'accounts_affected': 1,
                'inconsistency_start': '2023-12-31',
                'inconsistency_end': '2023-12-31',
                'id': 'Status-DOFD-4',
                'category': '',
                'description': 'description for a third status-dofd eval',
                'long_description': '',
                'fields_used': ['smpa'],
                'fields_display': ['orig_chg_off_amt', 'terms_freq'],
                'crrg_reference': '410', 'potential_harm': '',
                'rationale': '', 'alternate_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
            }, {
                'hits': 25,
                'accounts_affected': 1,
                'inconsistency_start': '2023-12-31',
                'inconsistency_end': '2023-12-31',
                'id': 'Status-DOFD-6',
                'category': 'account terms',
                'description': 'description for a fourth status-dofd eval', 'long_description': '',
                'fields_used': ['smpa'],
                'fields_display': ['orig_chg_off_amt', 'terms_freq'],
                'crrg_reference': '410',
                'potential_harm': '',
                'rationale': '',
                'alternate_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua'
        }]}

        response = self.client.get('/api/events/1/')
        # the response should be a JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        self.assertEqual(len(response.json()['evaluators']), 3)

        # the response should include the evaluator field as a list sorted by the id,
        # evaluators with a hits field greater than 0 will be returned
        self.assertEqual(response.json(), expected)


