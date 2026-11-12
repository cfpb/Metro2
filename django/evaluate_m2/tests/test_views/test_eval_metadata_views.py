from evaluate_m2.tests.test_views.view_tests_helper import EvaluatorViewsTestHelper


class EvalMetadataViewsTestCase(EvaluatorViewsTestHelper):
    def setUp(self):
        self.create_evaluator_metadata()

    ########################################
    # Tests for Eval Metadata download
    def test_download_eval_metadata(self):
        response = self.client.get('/api/all-evaluator-metadata/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/csv')
        self.assertIn('filename=evaluator-metadata',
            response.headers['Content-Disposition'])

        # The CSV should contain info about the test evals
        csv_content = response.content.decode('utf-8')

        self.assertIn('Portfolio-Type-1', csv_content)
        self.assertIn('description of Portfolio-Type-1', csv_content)
        self.assertIn('hcola;smpa;dofd', csv_content)
        self.assertIn('Portfolio-Type-2', csv_content)
        self.assertIn('description for the other Portfolio-Type eval',
                      csv_content)
        self.assertIn('Portfolio-Type-3', csv_content)
