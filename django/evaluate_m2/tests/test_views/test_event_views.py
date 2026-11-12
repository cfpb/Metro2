from evaluate_m2.tests.test_views.view_tests_helper import EvaluatorViewsTestHelper


class EventViewsTestCase(EvaluatorViewsTestHelper):
    def setUp(self):
        self.create_evaluator_metadata()
        self.create_eval_results_summaries()

    # Test for Events view API endpoint (all evals with hits for an event).
    # The evaluator field of the response is a list of evaluators with >0 hits
    # for this event, sorted by ID.
    def test_events_view(self):
        event_id=self.event.id
        expected = {
            'id': 1,
            'name': 'Enforcement: ABC Bank',
            'portfolio': 'Debt collection',
            'eid_or_matter_num': '123-456789',
            'other_descriptor': '',
            'directory': 'Enforcement/ABC',
            'date_range_start': '2024-09-28',
            'date_range_end': '2026-01-30',
            'total_tradelines': 65432,
            'total_accounts': 3456,
            'evaluators': [{
                'hits': 3398,
                'accounts_affected': 121,
                'inconsistency_start': '2025-03-30',
                'inconsistency_end': '2025-03-30',
                'id': 'Portfolio-Type-1',
                'category': 'DOFD',
                'description': 'description of Portfolio-Type-1',
                'long_description': '',
                'fields_used': ['hcola', 'smpa', 'dofd'],
                'fields_display': ['amt_past_due', 'compl_cond_cd', 'smpa'],
                'crrg_reference': '',
                'potential_harm': '',
                'rationale': '',
                'alternate_explanation': '',
                'interpret_fields_last_modified': None,
                'additional_notes': '',
                'additional_notes_last_modified': '2026-03-31'
            }, {
                'hits': 52,
                'accounts_affected': 23,
                'inconsistency_start': '2025-01-30',
                'inconsistency_end': '2025-07-30',
                'id': 'Portfolio-Type-2',
                'category': '',
                'description': 'description for the other Portfolio-Type eval',
                'long_description': '',
                'fields_used': ['placeholder', 'dofd', 'php'],
                'fields_display': ['orig_chg_off_amt'],
                'crrg_reference': '41',
                'potential_harm': '',
                'rationale': '',
                'alternate_explanation': 'addl expl',
                'interpret_fields_last_modified': None,
                'additional_notes': '',
                'additional_notes_last_modified': None
            }]
        }

        response = self.client.get(f'/api/events/{event_id}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(len(response.json()['evaluators']), 2)

        self.assertEqual(response.json(), expected)
