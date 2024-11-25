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
        self.prev_file = M2DataFile(event=self.event, file_name='prev_file.txt')
        self.prev_file.save()
        self.d = date(2010, 11, 30)
        self.pd = date(2010, 10, 31)
        self.expected = [
            {'id': 11, 'activity_date': date(2010, 11, 30), 'cons_acct_num': '001'}]

    ############################
    # Tests for the category PHP evaluators

    # - - - - - - - - - - - - - - - - - - - - - -
    # Hits when the following two conditions are met...
    # 1. previous_values__account_holder__cons_info_ind == ''
    # 2. previous_values__account_holder__cons_info_ind_assoc == ''

    # ... AND at least one of the following sets of conditions
    # a. previous_values__acct_stat == '71' & first character of php != '1'
    # b. previous_values__acct_stat == '78' & first character of php != '2'
    # c. previous_values__acct_stat == '80' & first character of php != '3'
    # d. previous_values__acct_stat == '82' & first character of php != '4'
    # e. previous_values__acct_stat == '83' & first character of php != '5'
    # f. previous_values__acct_stat == '84' & first character of php != '6'
    def test_eval_php_status_1(self):
        # Create previous Account Activities data
        prev_a1 = acct_record(self.prev_file, { 'id':1, 'activity_date': self.pd,
            'acct_stat':'71', 'cons_acct_num': '001', 'cons_info_ind':'',
            'cons_info_ind_assoc': [] })
        prev_a2 = acct_record(self.prev_file, {'id':2, 'activity_date': self.pd,
            'acct_stat':'71',  'cons_acct_num': '002', 'cons_info_ind':'',
            'cons_info_ind_assoc': [] })
        prev_a3 = acct_record(self.prev_file, {'id':3, 'activity_date': self.pd,
            'acct_stat':'71',  'cons_acct_num': '003', 'cons_info_ind':'',
            'cons_info_ind_assoc': ['X'] })

        # Create current Account Activities data
        acct_record(self.data_file, {'id':11, 'activity_date': self.d,
            'cons_acct_num': '001', 'cons_info_ind':'', 'php':'2L',
            'previous_values': prev_a1})
        acct_record(self.data_file, {'id':12, 'activity_date': self.d,
            'cons_acct_num': '002', 'cons_info_ind':'', 'php':'1L',
            'previous_values': prev_a2})
        acct_record(self.data_file, {'id':13, 'activity_date': self.d,
            'cons_acct_num': '003', 'cons_info_ind':'', 'php':'2L',
            'previous_values': prev_a3})
        # 11: HIT
        # 12: NO - previous_values__acct_stat == '71' & first character of php == '1'
        # 13: NO - previous_values__account_holder__cons_info_ind_assoc != ''

        self.assert_evaluator_correct(
            self.event, 'PHP-Status-1', self.expected)

    def test_eval_php_status_2(self):
    # Hits when conditions met:
    # 1. previous_values__account_holder__cons_info_ind=''
    # 2. previous_values__account_holder__cons_info_ind_assoc == ''
    # 3. previous_values__acct_stat == '11'
    # 4. previous_values__current_bal > 0
    # 5. port_type  == 'C', 'O', 'R'
    # 6. first character of php != '0'

        # Create previous Account Activities data
        prev1 = acct_record(self.prev_file, {'id': 1, 'activity_date': self.pd,
            'cons_acct_num': '001','acct_stat':'11', 'cons_info_ind':'',
            'cons_info_ind_assoc': [], 'port_type':'C', 'current_bal': 10})
        prev2 = acct_record(self.prev_file, {'id': 2, 'activity_date': self.pd,
            'cons_acct_num': '002', 'acct_stat':'11', 'cons_info_ind':'',
            'cons_info_ind_assoc': [], 'port_type':'O', 'current_bal': 10})
        prev3 = acct_record(self.prev_file, {'id': 3, 'activity_date': self.pd,
            'cons_acct_num': '003', 'acct_stat':'11', 'cons_info_ind':'X',
            'cons_info_ind_assoc': [], 'port_type':'R', 'current_bal': 10})
        prev4 = acct_record(self.prev_file, {'id': 4, 'activity_date': self.pd,
            'cons_acct_num': '004', 'acct_stat':'62',  'cons_info_ind':'',
            'cons_info_ind_assoc': [], 'port_type':'C', 'current_bal': 10})
        prev5 = acct_record(self.prev_file, {'id': 5, 'activity_date': self.pd,
            'cons_acct_num': '005', 'acct_stat':'11',  'cons_info_ind':'',
            'cons_info_ind_assoc': ['X'], 'port_type':'O', 'current_bal': 10})
        prev6 = acct_record(self.prev_file, {'id': 6, 'activity_date': self.pd,
            'cons_acct_num': '006', 'acct_stat':'11',  'cons_info_ind':'',
            'cons_info_ind_assoc': [], 'port_type':'R', 'current_bal': 0})
        prev7 = acct_record(self.prev_file, {'id': 7, 'activity_date': self.pd,
            'cons_acct_num': '007', 'acct_stat':'11',  'cons_info_ind':'',
            'cons_info_ind_assoc': [], 'port_type':'A', 'current_bal': 10})

        # Create current Account Activities data
        acct_record(self.data_file, {'id':11, 'activity_date': self.d,
            'cons_acct_num': '001', 'cons_info_ind':'', 'php':'2L',
            'previous_values': prev1, 'port_type':'C'})
        acct_record(self.data_file, {'id':12, 'activity_date': self.d,
            'cons_acct_num': '002', 'cons_info_ind':'', 'php':'0L',
            'previous_values': prev2, 'port_type':'O'})
        acct_record(self.data_file, {'id':13, 'activity_date': self.d,
            'cons_acct_num': '003', 'cons_info_ind':'', 'php':'2L',
            'previous_values': prev3, 'port_type':'R'})
        acct_record(self.data_file, {'id':14, 'activity_date': self.d,
            'cons_acct_num': '004', 'cons_info_ind':'', 'php':'2L',
            'previous_values': prev4, 'port_type':'C'})
        acct_record(self.data_file, {'id':15, 'activity_date': self.d,
            'cons_acct_num': '005', 'cons_info_ind':'', 'php':'2L',
            'previous_values': prev5, 'port_type':'O'})
        acct_record(self.data_file, {'id':16, 'activity_date': self.d,
            'cons_acct_num': '006', 'cons_info_ind':'', 'php':'2L',
            'previous_values': prev6, 'port_type':'R'})
        acct_record(self.data_file, {'id':17, 'activity_date': self.d,
            'cons_acct_num': '007', 'cons_info_ind':'', 'php':'2L',
            'previous_values': prev7, 'port_type':'A'})
        # 11: HIT
        # 12: NO - first character of php == '0'
        # 13: NO - previous_values__account_holder__cons_info_ind == 'X'
        # 14: NO - previous_values__acct_stat == '62'
        # 15: NO - previous_values__account_holder__cons_info_ind_assoc == 'X'
        # 16: NO - previous_values__current_bal == 0
        # 17: NO - port_type == 'A'

        self.assert_evaluator_correct(self.event, 'PHP-Status-2', self.expected)

    def test_eval_php_status_3(self):
    #     Hits when the following two conditions are met...
    #     1. previous_values__account_holder__cons_info_ind == ''
    #     2. previous_values__account_holder__cons_info_ind_assoc == ''

    # ... AND at least one of the following sets of conditions
    #     a. previous_values__acct_stat == '62', '93' & first character of php != 'G'
    #     b. previous_values__acct_stat == '65', '94' & first character of php != 'H'
    #     c. previous_values__acct_stat == '61', '95' & first character of php != 'J'
    #     d. previous_values__acct_stat == '63', '96' & first character of php != 'K'
    #     e. previous_values__acct_stat == '64', '97' & first character of php != 'L'

        # Create previous Account Activities data
        prev1 = acct_record(self.prev_file, {'id': 1, 'activity_date': self.pd,
            'cons_acct_num': '001','acct_stat':'62', 'cons_info_ind':'',
            'cons_info_ind_assoc': [] })
        prev2 = acct_record(self.prev_file, {'id': 2, 'activity_date': self.pd,
            'cons_acct_num': '002', 'acct_stat':'93', 'cons_info_ind':'',
            'cons_info_ind_assoc': [] })
        prev3 = acct_record(self.prev_file, {'id': 3, 'activity_date': self.pd,
            'cons_acct_num': '003', 'acct_stat':'62', 'cons_info_ind':'X',
            'cons_info_ind_assoc': [] })
        prev4 = acct_record(self.prev_file, {'id': 4, 'activity_date': self.pd,
            'cons_acct_num': '004', 'acct_stat':'61',  'cons_info_ind':'',
            'cons_info_ind_assoc': [] })
        prev5 = acct_record(self.prev_file, {'id': 5, 'activity_date': self.pd,
            'cons_acct_num': '005', 'acct_stat':'93',  'cons_info_ind':'',
            'cons_info_ind_assoc': ['X'] })
        prev6 = acct_record(self.prev_file, {'id': 6, 'activity_date': self.pd,
            'cons_acct_num': '006','acct_stat':'61', 'cons_info_ind':'',
            'cons_info_ind_assoc': [] })
        prev7 = acct_record(self.prev_file, {'id': 7, 'activity_date': self.pd,
            'cons_acct_num': '007', 'acct_stat':'97', 'cons_info_ind':'',
            'cons_info_ind_assoc': [] })

        # Create current Account Activities data
        acct_record(self.data_file, {'id':11, 'activity_date': self.d,
            'cons_acct_num': '001', 'cons_info_ind':'', 'php':'2L',
            'previous_values': prev1})
        acct_record(self.data_file, {'id':12, 'activity_date': self.d,
            'cons_acct_num': '006', 'cons_info_ind':'', 'php':'HK',
            'previous_values': prev6})
        acct_record(self.data_file, {'id':13, 'activity_date': self.d,
            'cons_acct_num': '002', 'cons_info_ind':'', 'php':'GL',
            'previous_values': prev2})
        acct_record(self.data_file, {'id':14, 'activity_date': self.d,
            'cons_acct_num': '007', 'cons_info_ind':'', 'php':'LG',
            'previous_values': prev7})
        acct_record(self.data_file, {'id':15, 'activity_date': self.d,
            'cons_acct_num': '003', 'cons_info_ind':'', 'php':'2L',
            'previous_values': prev3})
        acct_record(self.data_file, {'id':16, 'activity_date': self.d,
            'cons_acct_num': '004', 'cons_info_ind':'', 'php':'JL',
            'previous_values': prev4})
        acct_record(self.data_file, {'id':17, 'activity_date': self.d,
            'cons_acct_num': '005', 'cons_info_ind':'', 'php':'2L',
            'previous_values': prev5})
        # 11: HIT
        # 12: HIT
        # 13: NO - previous_values__acct_stat == 93 & first character of php == 'G'
        # 14: NO - previous_values__acct_stat == 97 & first character of php == 'L'
        # 15: NO - previous_values__account_holder__cons_info_ind == 'X'
        # 16: NO - previous_values__acct_stat == '61'
        # 17: NO - previous_values__account_holder__cons_info_ind_assoc == 'X'

        expected = [
            {'id': 11, 'activity_date': date(2010, 11, 30), 'cons_acct_num': '001'},
            {'id': 12, 'activity_date': date(2010, 11, 30), 'cons_acct_num': '006'}]

        self.assert_evaluator_correct(self.event, 'PHP-Status-3', expected)
