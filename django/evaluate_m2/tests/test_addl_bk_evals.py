from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper
from parse_m2.models import Metro2Event, M2DataFile

class Addl_Bk_EvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()
        # Create the Account Holders
        self.create_bulk_account_holders(self.data_file, ('A','J','K','B','M'))

    def create_bulk_records(self, create_j1: bool):
        activities = { 'id':(32,33,34,35,36),
            'cons_acct_num':('0032','0033','0034','0035','0036'),
            'account_holder':('A','J','K','B','M'),
            'dofd':(None,None,None,date(2019, 12, 31),None)}
        self.create_bulk_activities(self.data_file, activities, 5)

        if create_j1:
            print('J1-data created')
            j1_data = {
                'account_activity':(32,33,34,35,36),
                'cons_info_ind':('I','C','K','L','M')}
            self.create_bulk_JSegments('j1', j1_data, 5)
        else:
            print('No J1-data created')

        j2_data = {
              'account_activity':(32,33,34,35,36),
              'cons_info_ind':('I','J','D','K','L')}
        self.create_bulk_JSegments('j2', j2_data, 5)

    ############################
    # Tests for the category addl bk evaluators

    # Hits when all conditions met:
    # dofd == None
    # (cons_info_ind == 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'Z', 'V', '1A' ||
    #  any (J1.cons_info_ind == 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'Z', 'V', '1A') ||
    #  any (J2.cons_info_ind == 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'Z', 'V', '1A'))
    def test_eval_addl_bk_1(self):
        create_j1_data=True
        self.create_bulk_records(create_j1_data)
        # 1: HIT, 2: HIT, 3: HIT, 4: NO-dofd=01012020, 5: NO-all cons_info_ind not valid

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'account_holder__cons_info_ind': 'A',
            'j1__cons_info_ind': 'I', 'j2__cons_info_ind': 'I',
            'dofd': None
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'account_holder__cons_info_ind': 'J',
            'j1__cons_info_ind': 'C', 'j2__cons_info_ind': 'J',
            'dofd': None
        }, {
            'id': 34, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0034', 'account_holder__cons_info_ind': 'K',
            'j1__cons_info_ind': 'K', 'j2__cons_info_ind': 'D',
            'dofd': None
        }]
        self.assert_evaluator_correct(self.event, 'ADDL-BK-1', expected)

    def test_eval_addl_bk_1_no_j1_segment(self):
        create_j1_data=False
        self.create_bulk_records(create_j1_data)
        # 1: HIT, 2: HIT, 3: HIT, 4: NO-dofd=01012020, 5: NO-all cons_info_ind not valid

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'account_holder__cons_info_ind': 'A',
            'j1__cons_info_ind': None, 'j2__cons_info_ind': 'I',
            'dofd': None
        }, {
            'id': 34, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0034', 'account_holder__cons_info_ind': 'K',
            'j1__cons_info_ind': None, 'j2__cons_info_ind': 'D',
            'dofd': None
        }]
        self.assert_evaluator_correct(self.event, 'ADDL-BK-1', expected)

    def test_eval_addl_bk_1_two_j1_segments(self):
        create_j1_data=True
        self.create_bulk_records(create_j1_data)
        j1_data = {
            'account_activity':(33,36),
            'cons_info_ind':('E','O')}
        self.create_bulk_JSegments('j1', j1_data, 2)
        # 1: HIT, 2: HIT, 3: HIT, 4: NO-dofd=01012020, 5: NO-all cons_info_ind not valid

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'account_holder__cons_info_ind': 'A',
            'j1__cons_info_ind': 'I', 'j2__cons_info_ind': 'I',
            'dofd': None
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'account_holder__cons_info_ind': 'J',
            'j1__cons_info_ind': 'C', 'j2__cons_info_ind': 'J',
            'dofd': None
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'account_holder__cons_info_ind': 'J',
            'j1__cons_info_ind': 'E', 'j2__cons_info_ind': 'J',
            'dofd': None
        }, {
            'id': 34, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0034', 'account_holder__cons_info_ind': 'K',
            'j1__cons_info_ind': 'K', 'j2__cons_info_ind': 'D',
            'dofd': None
        }]
        self.assert_evaluator_correct(self.event, 'ADDL-BK-1', expected)

    def test_eval_addl_bk_1_two_entry_for_one_j2_segment(self):
        create_j1_data=True
        self.create_bulk_records(create_j1_data)
        j1_data = {
            'account_activity':(34,36),
            'cons_info_ind':('O','O')}
        self.create_bulk_JSegments('j1', j1_data, 2)
        # 1: HIT, 2: HIT, 3: HIT, 4: NO-dofd=01012020, 5: NO-all cons_info_ind not valid

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'account_holder__cons_info_ind': 'A',
            'j1__cons_info_ind': 'I', 'j2__cons_info_ind': 'I',
            'dofd': None
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'account_holder__cons_info_ind': 'J',
            'j1__cons_info_ind': 'C', 'j2__cons_info_ind': 'J',
            'dofd': None
        }, {
            'id': 34, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0034', 'account_holder__cons_info_ind': 'K',
            'j1__cons_info_ind': 'K', 'j2__cons_info_ind': 'D',
            'dofd': None
        }, {
            'id': 34, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0034', 'account_holder__cons_info_ind': 'K',
            'j1__cons_info_ind': 'O', 'j2__cons_info_ind': 'D',
            'dofd': None
        }]
        self.assert_evaluator_correct(self.event, 'ADDL-BK-1', expected)
