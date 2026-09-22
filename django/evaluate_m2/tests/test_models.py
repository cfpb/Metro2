from datetime import date

from django.test import TestCase

from evaluate_m2.models import (
    EvaluatorMetadata,
    EvaluatorResult,
    EvaluatorResultSummary,
    EvaluatorResultMaterializedView,
)
from evaluate_m2.serializers import EvaluatorMetadataSerializer
from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.models import M2DataFile, Metro2Event


class EvaluatorResultSummaryTestCase(TestCase):
    def setUp(self):
        event = Metro2Event.objects.create(name="MyeVent")
        eval = EvaluatorMetadata.objects.create(
            id="my-eval-3",
            fields_used=["amt_past_due"],
            fields_display=["doai"]
        )
        f = M2DataFile.objects.create(event=event)
        r1 = acct_record(f, {"id": 31})
        r2 = acct_record(f, {"id": 32})
        r3 = acct_record(f, {"id": 33})
        r4 = acct_record(f, {"id": 34})
        self.ers = EvaluatorResultSummary.objects.create(
            event=event,
            evaluator=eval,
            hits=4
        )
        res1 = EvaluatorResult.objects.create(
            date=r1.activity_date,
            result_summary=self.ers,
            source_record=r1
        )
        res2 = EvaluatorResult.objects.create(
            date=r2.activity_date,
            result_summary=self.ers,
            source_record=r2
        )
        res3 = EvaluatorResult.objects.create(
            date=r3.activity_date,
            result_summary=self.ers,
            source_record=r3
        )
        res4 = EvaluatorResult.objects.create(
            date=r4.activity_date,
            result_summary=self.ers,
            source_record=r4
        )
        self.eval_results = [res1, res2, res3, res4]

    def test_sample_randomize(self):
        self.ers._save_sample_of_results(sample_size=2)
        result = self.ers.sample_results()

        # There should be two items in the list
        self.assertEqual(len(result), 2)

        # each item should be an EvaluatorResult object
        for x in result:
            self.assertTrue(x in self.eval_results)

        # IDs in the list should not be repeated
        self.assertNotEqual(result[0], result[1])


class EvaluatorMetadataTestCase(TestCase):
    def test_save_new_from_csv_imports_last_modified_dates(self):
        info = {
            "id": "Test-Type-A",
            "category": "testing",
            "description": "",
            "long_description": "",
            "fields_used": "",
            "fields_display": "",
            "crrg_reference": "",
            "potential_harm": "",
            "rationale": "",
            "alternate_explanation": "",
            "interpret_fields_last_modified": "2023-02-28",
            "additional_notes": "",
            "additional_notes_last_modified": "",
        }
        from_json = EvaluatorMetadataSerializer(data=info)
        self.assertTrue(from_json.is_valid())
        record = from_json.save()
        self.assertEqual(
            record.interpret_fields_last_modified,
            date(2023,2,28)
        )
        self.assertEqual(
            record.additional_notes_last_modified,
            EvaluatorMetadata._last_modified_never
        )

    def test_save_existing_from_csv_uses_imported_dates(self):
        ev = EvaluatorMetadata(
            id="Sample-1",
            interpret_fields_last_modified=date(2025,9,30),
            additional_notes_last_modified=EvaluatorMetadata._last_modified_never,
        )
        ev.save()

        update_info = {
            "id": "Sample-1",
            "category": "testing",
            "description": "",
            "long_description": "",
            "fields_used": "",
            "fields_display": "",
            "crrg_reference": "",
            "potential_harm": "",
            "rationale": "",
            "alternate_explanation": "",
            "interpret_fields_last_modified": "2023-02-28",
            "additional_notes": "",
            "additional_notes_last_modified": "",
        }
        from_json = EvaluatorMetadataSerializer(ev, data=update_info)
        self.assertTrue(from_json.is_valid())
        record = from_json.save()

        self.assertEqual(
            record.interpret_fields_last_modified,
            date(2023,2,28)
        )
        self.assertEqual(
            record.additional_notes_last_modified,
            EvaluatorMetadata._last_modified_never
        )


    def test_manual_edit_updates_last_modified_date(self):
        ev = EvaluatorMetadata(
            id = "Test-Mod-1",
            rationale = "An initial rationale.",
        )
        ev.save()
        self.assertEqual(
            ev.interpret_fields_last_modified,
            EvaluatorMetadata._last_modified_never)
        self.assertEqual(
            ev.additional_notes_last_modified,
            EvaluatorMetadata._last_modified_never)

        eval_load = EvaluatorMetadata.objects.get(id="Test-Mod-1")
        eval_load.rationale = "Modified rationale"
        eval_load.additional_notes = "Modified notes"
        eval_load.save()

        eval_load_2 = EvaluatorMetadata.objects.get(id="Test-Mod-1")
        self.assertEqual(
            eval_load_2.interpret_fields_last_modified,
            date.today()
        )
        self.assertEqual(
            eval_load_2.additional_notes_last_modified,
            date.today()
        )


class EvaluatorResultMaterializedViewTestCase(TestCase):
    def test_csv_fields(self):
        self.assertEqual(
            EvaluatorResultMaterializedView.csv_fields(),
            [
                'activity_date',
                'cons_acct_num',
                'port_type',
                'acct_type',
                'date_open',
                'credit_limit',
                'hcola',
                'id_num',
                'terms_dur',
                'terms_freq',
                'smpa',
                'actual_pmt_amt',
                'acct_stat',
                'pmt_rating',
                'php',
                'php1',
                'spc_com_cd',
                'compl_cond_cd',
                'current_bal',
                'amt_past_due',
                'orig_chg_off_amt',
                'doai',
                'dofd',
                'date_closed',
                'dolp',
                'int_type_ind',
                'ecoa',
                'ecoa_assoc',
                'cons_info_ind',
                'cons_info_ind_assoc',
                'purch_sold_ind',
                'purch_sold_name',
                'spc_pmt_ind',
                'deferred_pmt_st_dt',
                'balloon_pmt_due_dt',
                'balloon_pmt_amt',
                'change_ind',
                'new_acc_num',
                'new_id_num',
                'prior_activity_date',
                'prior_port_type',
                'prior_acct_type',
                'prior_date_open',
                'prior_id_num',
                'prior_acct_stat',
                'prior_pmt_rating',
                'prior_current_bal',
                'prior_orig_chg_off_amt',
                'prior_dofd',
                'prior_date_closed',
                'prior_ecoa',
                'prior_ecoa_assoc',
                'prior_cons_info_ind',
                'prior_cons_info_ind_assoc',
                'prior_change_ind',
                'prior_new_acc_num',
                'prior_new_id_num',
            ]
        )