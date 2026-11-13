from datetime import date

from django.test import TestCase

from evaluate_m2.models import (
    EvaluatorMetadata,
    EvaluatorResultMaterializedView,
    EvaluatorResultSummary,
)
from evaluate_m2.tests.evaluator_test_helper import acct_record, evaluator_result_record
from parse_m2.models import M2DataFile, Metro2Event


class EvaluatorViewsTestHelper(TestCase):
    def create_evaluator_metadata(self):
        self.eval1 = EvaluatorMetadata.objects.create(
            id='Portfolio-Type-1',
            category='DOFD',
            description='description of Portfolio-Type-1',
            long_description='',
            fields_used=['hcola', 'smpa', 'dofd'],
            fields_display=['amt_past_due', 'compl_cond_cd', 'smpa',],
            additional_notes_last_modified=date(2026,3,31),
        )
        self.eval2 = EvaluatorMetadata.objects.create(
            id='Portfolio-Type-2',
            description='description for the other Portfolio-Type eval',
            long_description='',
            fields_used=['placeholder', 'dofd', 'php'],
            fields_display= ['orig_chg_off_amt'],
            crrg_reference='41',
            alternate_explanation='addl expl',
        )
        self.eval3 = EvaluatorMetadata.objects.create(
            id='Portfolio-Type-3',
            fields_used=[],
            fields_display= [],
        )

    def create_eval_results_summaries(self):
        self.event = Metro2Event.objects.create(
            id=1,
            name='Enforcement: ABC Bank',
            portfolio='Debt collection',
            eid_or_matter_num='123-456789',
            directory='Enforcement/ABC',
            date_range_start='2024-09-28',
            date_range_end='2026-01-30',
            total_tradelines=65432,
            total_accounts=3456,
        )
        self.results1 = EvaluatorResultSummary.objects.create(
            event=self.event,
            evaluator_id='Portfolio-Type-1',
            hits=3398,
            accounts_affected=121,
            inconsistency_start='2025-03-30',
            inconsistency_end='2025-03-30',
        )
        self.results2 = EvaluatorResultSummary.objects.create(
            event=self.event,
            evaluator_id='Portfolio-Type-2',
            hits=52,
            accounts_affected=23,
            inconsistency_start='2025-01-30',
            inconsistency_end='2025-07-30',
        )
        EvaluatorResultSummary.objects.create(
            event=self.event,
            evaluator_id='Portfolio-Type-3',
            hits=0,
        )

    def create_activity_and_eval_results(self):
        self.m2_file = M2DataFile.objects.create(event=self.event)
        consumer_info = {'cons_acct_num': '908070', 'surname': 'Claus',
                         'first_name': 'Santa'}
        a1 = acct_record(
            self.m2_file,
            {'id': 1, 'activity_date': date(2025,3,1), 'acct_stat': 1} | consumer_info)
        a2 = acct_record(
            self.m2_file,
            {'id': 2, 'activity_date': date(2025,4,1), 'acct_stat': 1} | consumer_info)
        a3 = acct_record(
            self.m2_file,
            {'id': 3, 'activity_date': date(2025,5,1), 'acct_stat': 2} | consumer_info)

        # all three records hit on eval 1
        evaluator_result_record(self.event, self.eval1.id, a1)
        evaluator_result_record(self.event, self.eval1.id, a2)
        evaluator_result_record(self.event, self.eval1.id, a3)
        # one record hit on eval 2
        evaluator_result_record(self.event, self.eval2.id, a2)

        # Finally, create the materialized view
        EvaluatorResultMaterializedView.create_or_refresh_materialized_view()
