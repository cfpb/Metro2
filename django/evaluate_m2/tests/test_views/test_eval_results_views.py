from unittest.mock import patch

from django.test import override_settings

from evaluate_m2.models import (
    EvaluatorResultMaterializedView,
)
from evaluate_m2.tests.evaluator_test_helper import acct_record, evaluator_result_record
from evaluate_m2.tests.test_views.view_tests_helper import EvaluatorViewsTestHelper


class EvalResultsViewsTestCase(EvaluatorViewsTestHelper):
    def setUp(self):
        self.create_evaluator_metadata()
        self.create_eval_results_summaries()
        self.create_activity_and_eval_results()

    ########################################
    # Tests for Eval Results CSV download
    def test_download_evaluator_results_csv(self):
        response = self.client.get('/api/events/1/evaluator/Portfolio-Type-1/csv/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/csv')
        self.assertIn(
            'filename=Enforcement: ABC Bank_Portfolio-Type-1_filtered.csv',
            response.headers['Content-Disposition'])

        # iterate through the streaming response
        lines = []
        for line in response.streaming_content:
            lines.append(line.decode('utf-8'))

        # the CSV should have a row for each eval result as defined in
        # create_activity_data (plus the header)
        self.assertEqual(len(lines), 4)

    def test_download_evaluator_results_csv_filters_applied(self):
        response = self.client.get(
            '/api/events/1/evaluator/Portfolio-Type-1/csv/?acct_stat=1&show_counts=true')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/csv')
        self.assertIn(
            'filename=Enforcement: ABC Bank_Portfolio-Type-1_filtered.csv',
            response.headers['Content-Disposition'])

        # iterate through the streaming response
        lines = []
        for line in response.streaming_content:
            lines.append(line.decode('utf-8'))

        # filters returned 2 eval results (plus the header)
        self.assertEqual(len(lines), 3)

    @override_settings(S3_ENABLED=True)
    @patch('evaluate_m2.views.eval_results_views.EvaluatorResultsCSVView.fetch_csv_results_from_s3')  # noqa: E501
    def test_fetch_from_s3_when_enabled_and_no_filters_applied(self, s3_fetch_method):
        from django.http import HttpResponse
        s3_fetch_method.return_value = HttpResponse(content="content")
        self.client.get('/api/events/1/evaluator/Portfolio-Type-1/csv/')
        self.assertTrue(s3_fetch_method.called)

    @override_settings(S3_ENABLED=True)
    @patch('evaluate_m2.views.eval_results_views.EvaluatorResultsCSVView.fetch_csv_results_from_s3')  # noqa: E501
    def test_no_fetch_from_s3_when_filters_applied(self, s3_fetch_method):
        self.client.get(
            '/api/events/1/evaluator/Portfolio-Type-1/csv/?acct_stat=1&show_counts=true')
        self.assertFalse(s3_fetch_method.called)

    ########################################
    # Tests for Eval Results view API endpoint
    # The response should be a JSON with the following structure. Hits is a
    # list of evaluator results from the EvaluatorResultSerializer
    # {
    #     'count': 3,
    #     'hits': [ ... ]
    # }

    def test_evaluator_results_view_sample(self):
        response = self.client.get(
            '/api/events/1/evaluator/Portfolio-Type-1/?view=sample')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        self.assertEqual(response.json()['count'], 3)
        hits = response.json()['hits']
        self.assertEqual(len(hits), 3)
        for hit in hits:
            self.assertEqual(hit['cons_acct_num'], '908070')

    def test_evaluator_results_view_all(self):
        response = self.client.get('/api/events/1/evaluator/Portfolio-Type-1/?view=all')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        self.assertEqual(response.json()['count'], 3)
        hits = response.json()['hits']
        self.assertEqual(len(hits), 3)
        for hit in hits:
            self.assertEqual(hit['cons_acct_num'], '908070')

    def test_evaluator_results_view_zero_results(self):
        response = self.client.get('/api/events/1/evaluator/Portfolio-Type-3/?view=all')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        self.assertEqual(response.json()['count'], 0)
        hits = response.json()['hits']
        self.assertEqual(len(hits), 0)

    def test_evaluator_results_view_max_20_results(self):
        # create additional eval results, over 20
        for i in range(25):
            activity = {'id': i, 'cons_acct_num': '0032'}
            record = acct_record(self.m2_file, activity)
            evaluator_result_record(self.event, self.eval1.id, record)

        EvaluatorResultMaterializedView.create_or_refresh_materialized_view()

        response = self.client.get('/api/events/1/evaluator/Portfolio-Type-1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 20)
        self.assertEqual(len(response.json()['hits']), 20)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_evaluator_results_view_with_error_no_evaluator_metadata(self):
        response = self.client.get('/api/events/1/evaluator/NON_EXISTENT/')

        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertContains(response, 'record(s) not found', status_code=404)

    def test_evaluator_results_view_with_error_no_event(self):
        response = self.client.get('/api/events/2/evaluator/Portfolio-Type-1/')

        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertContains(response, 'Event ID: 2 does not exist.', status_code=404)
