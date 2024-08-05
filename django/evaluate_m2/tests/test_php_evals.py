from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper, acct_record
from parse_m2.models import J1, J2, Metro2Event, M2DataFile

class PHPEvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()
        self.prev_file = M2DataFile(event=self.event, file_name="prev_file.txt")
        self.prev_file.save()
        self.d = date(2010, 11, 30)
        self.pd = date(2010, 10, 31)

    ############################
    # Tests for the category PHP evaluators

    # - - - - - - - - - - - - - - - - - - - - - -
    # Hits when all conditions are met:
    # 1. prev_cons_info_ind == ''
    # 2. prev_cons_info_ind_assoc == ''
    # 3. prev_acct_stat == '71' & first character of php != '1'
    # 4. prev_acct_stat == '78' & first character of php != '2'
    # 5. prev_acct_stat == '80' & first character of php != '3'
    # 6. prev_acct_stat == '82' & first character of php != '4'
    # 7. prev_acct_stat == '83' & first character of php != '5'
    # 8. prev_acct_stat == '84' & first character of php != '6'


    def test_eval_php_status_1(self):
        # Create previous Account Activities data
        prev_a1 = acct_record(self.prev_file, { "id":1, "activity_date": self.pd,
            "acct_stat":"71", "cons_acct_num": "001", "cons_info_ind":"",
            "cons_info_ind_assoc": [] })
        prev_a2 = acct_record(self.prev_file, {"id":2, "activity_date": self.pd,
            "acct_stat":"71",  "cons_acct_num": "002", "cons_info_ind":"",
            "cons_info_ind_assoc": [] })
        prev_a3 = acct_record(self.prev_file, {"id":3, "activity_date": self.pd,
            "acct_stat":"71",  "cons_acct_num": "003", "cons_info_ind":"",
            "cons_info_ind_assoc": ["X"] })
        J1.objects.create(account_activity=prev_a1, cons_info_ind="")
        J1.objects.create(account_activity=prev_a2, cons_info_ind="")
        J1.objects.create(account_activity=prev_a3, cons_info_ind="X")
        J2.objects.create(account_activity=prev_a1, cons_info_ind="")
        # Create current Account Activities data
        acct_record(self.data_file, {"id":11, "activity_date": self.d,
            "cons_acct_num": "001", "cons_info_ind":"", "php":"2L",
            "previous_values": prev_a1})
        acct_record(self.data_file, {"id":12, "activity_date": self.d,
            "cons_acct_num": "002", "cons_info_ind":"", "php":"1L",
            "previous_values": prev_a2})
        acct_record(self.data_file, {"id":13, "activity_date": self.d,
            "cons_acct_num": "003", "cons_info_ind":"", "php":"2L",
            "previous_values": prev_a3})

        # 11: HIT
        # 12: NO - previous_values__acct_stat == '71' & first character of php == '1'
        # 13: NO - previous_values__account_holder__cons_info_ind_assoc != ''

        # Create the segment data
        expected = [
            {'id': 11, 'activity_date': date(2010, 11, 30), 'cons_acct_num': '001'}
        ]
        self.assert_evaluator_correct(
            self.event, 'PHP-Status-1', expected)

    def test_eval_9_PHP_acct_stat_mismatch_missing_j_segments(self):
        prev_a = []
        # Create previous Account Activities data
        prev_a1 = acct_record(self.prev_file, {"id":1, "activity_date": self.pd,
            "acct_stat":"71", "cons_acct_num": "001", "cons_info_ind":""})
        prev_a2 = acct_record(self.prev_file, {"id":2, "activity_date": self.pd,
            "acct_stat":"71",  "cons_acct_num": "002", "cons_info_ind":""})
        prev_a3 = acct_record(self.prev_file, {"id":3, "activity_date": self.pd,
            "acct_stat":"71",  "cons_acct_num": "003", "cons_info_ind":"X"})

        # Create current Account Activities data

        acct_record(self.data_file, {"id":11, "activity_date": self.d,
            "cons_acct_num": "001", "cons_info_ind":"", "php":"2L",
            "previous_values": prev_a1})
        acct_record(self.data_file, {"id":12, "activity_date": self.d,
            "cons_acct_num": "002", "cons_info_ind":"", "php":"1L",
            "previous_values": prev_a2})
        acct_record(self.data_file, {"id":13, "activity_date": self.d,
            "cons_acct_num": "003", "cons_info_ind":"", "php":"2L",
            "previous_values": prev_a3})

        # 11: HIT
        # 12: NO - previous_values__acct_stat == '71' & first character of php == '1'
        # 13: NO - previous_values__account_holder__cons_info_ind == 'X'

        # Create the segment data
        expected = [
            {'id': 11, 'activity_date': date(2010, 11, 30), 'cons_acct_num': '001'}
        ]

        self.assert_evaluator_correct(
            self.event, 'PHP-Status-1', expected)