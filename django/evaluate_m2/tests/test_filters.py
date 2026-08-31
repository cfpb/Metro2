from datetime import date
from unittest import mock

from django.db.models import Q
from django.test import SimpleTestCase, TestCase, override_settings

from evaluate_m2.filters import (
    AnyCharFilter,
    EvaluatorResultFilterSet,
    JSONArrayContainsFilter,
)
from evaluate_m2.models import (
    EvaluatorMetadata,
    EvaluatorResult,
    EvaluatorResultMaterializedView,
    EvaluatorResultSummary,
)
from evaluate_m2.tests.evaluator_test_helper import acct_record, l1_record
from parse_m2.models import M2DataFile, Metro2Event


class AnyCharFilterTestCase(SimpleTestCase):
    def test_filtering_empty_string(self):
        qs = mock.Mock(spec=["filter"])
        f = AnyCharFilter("test_field")

        expected_q = (
            Q(test_field__isnull=True) |
            Q(test_field="") |
            Q(test_field__in=["value", "other"])
        )

        result = f.filter(qs, ["value", "blank", "other"])
        qs.filter.assert_called_once_with(expected_q)
        self.assertNotEqual(qs, result)


class JSONArrayContainsFilterTestCase(SimpleTestCase):
    def test_filtering_empty_string(self):
        qs = mock.Mock(spec=["filter"])
        f = JSONArrayContainsFilter("test_field")

        expected_q = (
            Q(test_field__isnull=True) |
            Q(test_field__contains=["value", ]) |
            Q(test_field__contains=["other", ])
        )

        result = f.filter(qs, ["value", "blank", "other"])
        qs.filter.assert_called_once_with(expected_q)
        self.assertNotEqual(qs, result)


@override_settings(S3_ENABLED=False)
class BaseFilterSetTestCase(TestCase):
    acct_date = date(2023, 12, 31)

    def setUp(self):
        self.evaluator = EvaluatorMetadata.objects.create(
            id="Filter-Test-1",
            category="filters",
            description="evaluator used for filter tests",
            long_description="",
            fields_used=["acct_stat", "dofd", "amt_past_due"],
            fields_display=[],
        )
        self.event = Metro2Event.objects.create(
            id=1,
            name="test_exam",
            portfolio="credit cards",
            directory="Enforcement/FilterTest",
            eid_or_matter_num="123-456789",
            other_descriptor="",
            date_range_start="2023-11-30",
            date_range_end="2023-12-31"
        )
        self.data_file = M2DataFile.objects.create(
            event=self.event,
            file_name="file.txt"
        )
        self.summary = EvaluatorResultSummary.objects.create(
            event=self.event,
            evaluator=self.evaluator,
            hits=0,
            accounts_affected=0,
            inconsistency_start=self.acct_date,
            inconsistency_end=self.acct_date
        )

        self.create_activity_rows()

        EvaluatorResultMaterializedView.create_or_refresh_materialized_view()

    def create_activity_rows(self):
        raise NotImplementedError

    def create_result(self, l1_fields=None, **fields):
        """Create a set of AccountActivity and EvaluatorResult objects"""
        fields.setdefault("activity_date", self.acct_date)
        fields.setdefault("cons_acct_num", f"{fields["id"]:04d}")

        activity = acct_record(self.data_file, fields)

        EvaluatorResult.objects.create(
            result_summary=self.summary,
            date=date(2021, 1, 1),
            source_record=activity,
            acct_num=activity.cons_acct_num
        )

        if l1_fields is not None:
            l1_fields.setdefault("id", activity.id)
            l1_record(l1_fields)

        return activity

    def filter(self, **params):
        """Return the source_record_ids that result from the filter params"""
        filter_set = EvaluatorResultFilterSet(
            data=params,
            queryset=EvaluatorResultMaterializedView.objects.all(),
        )
        # Assert that it"s valid first
        self.assertTrue(filter_set.is_valid(), filter_set.errors)
        # Return a set of the filtered source_record_ids
        return set(filter_set.qs.values_list("source_record_id", flat=True))


class EvaluatorResultAnyCharFiltersTestCase(BaseFilterSetTestCase):

    def create_activity_rows(self):
        self.result_1 = self.create_result(
            id=32,
            acct_type="07",
            acct_stat="11",
            compl_cond_cd="XB",
            php="0",
            php1="0",
            pmt_rating="0",
            spc_com_cd="AH",
            terms_freq="M",
            cons_info_ind="Z",
            l1_fields={"change_ind": "1"},
        )
        self.result_2 = self.create_result(
            id=33,
            acct_type="15",
            acct_stat="13",
            compl_cond_cd="XH",
            php="1",
            php1="1",
            pmt_rating="1",
            spc_com_cd="AI",
            terms_freq="W",
            cons_info_ind="Y",
            l1_fields={"change_ind": "2"},
        )
        # Empty string values, no L1 segment
        self.result_3 = self.create_result(
            id=34,
            acct_type="",
            acct_stat="",
            compl_cond_cd="",
            php="",
            php1="",
            pmt_rating="",
            spc_com_cd="",
            terms_freq="",
            cons_info_ind="",
        )


    def test_acct_stat_single_value(self):
        results = self.filter(acct_stat="11")
        self.assertEqual(
            results,
            {
                self.result_1.id,
            }
        )

    def test_acct_stat_list(self):
        results = self.filter(acct_stat="11,13")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_2.id,
            }
        )

    def test_acct_stat_list_blank(self):
        results = self.filter(acct_stat="11,blank")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_3.id,
            }
        )

    def test_acct_stat_no_match(self):
        results = self.filter(acct_stat="99")
        self.assertEqual(results, set())

    def test_acct_type_single_value(self):
        results = self.filter(acct_type="07")
        self.assertEqual(results, {self.result_1.id})

    def test_acct_type_list(self):
        # FAILING: acct_type is a plain CharFilter, so this matches the
        # literal string "07,15" and returns nothing. Should be AnyCharFilter.
        results = self.filter(acct_type="07,15")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_2.id,
            }
        )

    def test_acct_type_blank(self):
        # FAILING for the same reason: a plain CharFilter has no blank
        # sentinel, so this matches the literal string "blank".
        results = self.filter(acct_type="blank")
        self.assertEqual(
            results,
            {
                self.result_3.id,
            }
        )

    def test_compl_cond_cd_list(self):
        results = self.filter(compl_cond_cd="XB,XH")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_2.id,
            }
        )

    def test_compl_cond_cd_list_blank(self):
        results = self.filter(compl_cond_cd="XB,blank")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_3.id,
            }
        )

    def test_php_list(self):
        results = self.filter(php="0,1")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_2.id,
            }
        )

    def test_php_list_blank(self):
        results = self.filter(php="0,blank")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_3.id,
            }
        )

    def test_php1_list(self):
        results = self.filter(php1="0,1")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_2.id,
            }
        )

    def test_php1_list_blank(self):
        results = self.filter(php1="0,blank")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_3.id,
            }
        )

    def test_pmt_rating_list(self):
        results = self.filter(pmt_rating="0,1")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_2.id,
            }
        )

    def test_pmt_rating_list_blank(self):
        results = self.filter(pmt_rating="0,blank")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_3.id,
            }
        )

    def test_spc_com_cd_list(self):
        results = self.filter(spc_com_cd="AH,AI")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_2.id,
            }
        )

    def test_spc_com_cd_list_blank(self):
        results = self.filter(spc_com_cd="AH,blank")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_3.id,
            }
        )

    def test_terms_freq_list(self):
        results = self.filter(terms_freq="M,W")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_2.id,
            }
        )

    def test_terms_freq_list_blank(self):
        results = self.filter(terms_freq="M,blank")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_3.id,
            }
        )

    def test_cons_info_ind_list(self):
        results = self.filter(cons_info_ind="Y,Z")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_2.id,
            }
        )

    def test_cons_info_ind_list_blank(self):
        results = self.filter(cons_info_ind="Z,blank")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_3.id,
            }
        )

    def test_no_filter_returns_all_rows(self):
        results = self.filter()
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_2.id,
                self.result_3.id,
            }
        )

    def test_change_ind_list(self):
        results = self.filter(l1__change_ind="1,2")
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_2.id,
            }
        )

    def test_change_ind_list_blank(self):
        results = self.filter(l1__change_ind="blank,2")
        self.assertEqual(
            results,
            {
                self.result_2.id,
                self.result_3.id,
            }
        )

    def test_multiple_filters_are_combined(self):
        results = self.filter(acct_stat="11", php="0")
        self.assertEqual(
            results,
            {
                self.result_1.id,
            }
        )

    def test_multiple_filters_across_different_rows(self):
        # acct_stat matches result_1, php matches result_2, so the
        # intersection is empty
        results = self.filter(acct_stat="11", php="1")
        self.assertEqual(results, set())

    def test_multiple_filters_with_lists(self):
        # acct_stat matches result_1 and result_2, terms_freq matches
        # result_2 only
        results = self.filter(acct_stat="11,13", terms_freq="W")
        self.assertEqual(
            results,
            {
                self.result_2.id,
            }
        )


class EvaluatorResultBoolFiltersTestCase(BaseFilterSetTestCase):

    def create_activity_rows(self):
        self.result_1 = self.create_result(
            id=32,
            dofd=date(2019, 1, 31),
            date_closed=date(2019, 2, 28)
        )
        self.result_2 = self.create_result(
            id=33,
            dofd=None,
            date_closed=None
        )

    def test_dofd_true(self):
        results = self.filter(dofd="true")
        self.assertEqual(results, {self.result_1.id, })

    def test_dofd_false(self):
        results = self.filter(dofd="false")
        self.assertEqual(results, {self.result_2.id, })

    def test_date_closed_true(self):
        results = self.filter(date_closed="true")
        self.assertEqual(results, {self.result_1.id, })

    def test_date_closed_false(self):
        results = self.filter(date_closed="false")
        self.assertEqual(results, {self.result_2.id, })


class EvaluatorResultRangeFiltersTestCase(BaseFilterSetTestCase):

    def create_activity_rows(self):
        self.result_1 = self.create_result(
            id=32,
            amt_past_due=0,
            current_bal=0,
            smpa=0
        )
        self.result_2 = self.create_result(
            id=33,
            amt_past_due=400,
            current_bal=400,
            smpa=400
        )
        self.result_3 = self.create_result(
            id=34,
            amt_past_due=500,
            current_bal=500,
            smpa=500
        )
        self.result_4 = self.create_result(
            id=35,
            amt_past_due=900,
            current_bal=900,
            smpa=900
        )

    def test_amt_past_due_range(self):
        results = self.filter(amt_past_due_min='400', amt_past_due_max='500')
        self.assertEqual(
            results,
            {
                self.result_2.id,
                self.result_3.id,
            }
        )

    def test_amt_past_due_min_only(self):
        results = self.filter(amt_past_due_min='500')
        self.assertEqual(
            results,
            {
                self.result_3.id,
                self.result_4.id,
            }
        )

    def test_amt_past_due_max_only(self):
        results = self.filter(amt_past_due_max='400')
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_2.id,
            }
        )

    def test_current_bal_range(self):
        results = self.filter(current_bal_min='400', current_bal_max='500')
        self.assertEqual(
            results,
            {
                self.result_2.id,
                self.result_3.id,
            }
        )

    def test_smpa_range(self):
        results = self.filter(smpa_min='0', smpa_max='400')
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_2.id,
            }
        )


class EvaluatorResultJSONFiltersTestCase(BaseFilterSetTestCase):

    def create_activity_rows(self):
        self.result_1 = self.create_result(
            id=32,
            cons_info_ind_assoc=['1A', 'B'],
        )
        self.result_2 = self.create_result(
            id=33,
            cons_info_ind_assoc=['B', 'C'],
        )
        self.result_3 = self.create_result(
            id=34,
            cons_info_ind_assoc=['Z'],
        )
        self.result_4 = self.create_result(
            id=35,
            cons_info_ind_assoc=[],
        )

    def test_cons_info_ind_assoc_single_value(self):
        results = self.filter(cons_info_ind_assoc='B')
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_2.id,
            }
        )

    def test_cons_info_ind_assoc_list(self):
        results = self.filter(cons_info_ind_assoc='1A,C')
        self.assertEqual(
            results,
            {
                self.result_1.id,
                self.result_2.id,
            }
        )

    def test_cons_info_ind_assoc_blank(self):
        results = self.filter(cons_info_ind_assoc='blank')
        self.assertEqual(results, set())
