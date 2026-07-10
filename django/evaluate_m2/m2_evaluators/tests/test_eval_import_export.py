from django.core.management import call_command
from django.test import TestCase

from evaluate_m2.models import EvaluatorMetadata


class EvalMetadataImportExportTestCase(TestCase):
    #### Test with the actual eval metadata that we import from eval_metadata.csv
    def test_actual_eval_metadata(self):
        # Test that the actual eval_metadata gets imported without exceptions
        call_command(
            'import_evaluator_metadata',
            '--file_path=evaluate_m2/m2_evaluators/eval_metadata.csv'
        )
        count = EvaluatorMetadata.objects.count()
        self.assertEqual(count, 1)

        # Test that actual eval metadata exports successfully from the exporting
        # evaluator metadata API endpoint
        response = self.client.get('/api/all-evaluator-metadata/')

        # the response should be a CSV
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/csv')
        self.assertIn('filename=evaluator-metadata',
            response.headers['Content-Disposition'])

        # the CSV should contain info about the evals
        csv_content = response.content.decode('utf-8')
        csv_content_lines = csv_content.splitlines()
        expected_header = \
            "id,category,description,long_description,fields_used," + \
            "fields_display,crrg_reference,potential_harm,rationale," + \
            "alternate_explanation,interpret_fields_last_modified," + \
            "additional_notes,additional_notes_last_modified"
        self.assertEqual(csv_content_lines[0], expected_header)
        self.assertIn('Portfolio-Type-1', csv_content)
