from evaluate_m2.serializers import EvaluatorMetadataSerializer
from evaluate_m2.tests.test_views.view_tests_helper import EvaluatorViewsTestHelper


class EvalMetadataViewsTestCase(EvaluatorViewsTestHelper):
    def setUp(self):
        self.create_evaluator_metadata()

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
        for item in EvaluatorMetadataSerializer(self.eval1).data:
            self.assertIn(item, csv_content)
        for item in EvaluatorMetadataSerializer(self.eval2).data:
            self.assertIn(item, csv_content)
        for item in EvaluatorMetadataSerializer(self.eval3).data:
            self.assertIn(item, csv_content)
