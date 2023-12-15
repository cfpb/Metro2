from django.test import TestCase

from datetime import datetime
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper
from parse_m2.models import K2, Metro2Event, M2DataFile

class TestAddlDofdEvals(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()
        # Create the Account Holders
        self.account_holders = self.create_bulk_account_holders(self.data_file, ('Z','Y','X','W','V'))

    ############################
    # Tests for the category addl dofd evaluators
    def test_eval_addl_dofd_1(self):
    # Hits when all conditions met:
    # 1. acct_stat == '61', '62', '63', '64', '65', '71', '78', '80','82',
    #                 '83', '84', '88', '89', '94', '95', '96', '93', '97'
    # 2. dofd == None

        # Create the Account Activities data
        activities = { 'id':(32,33,34,35), 'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','X','W'),
            'acct_stat':('71','97','11','65'),
            'dofd':(None,None,None,datetime(2019, 12, 31))}
        # 1: HIT, 2: HIT, 3: NO-acct_stat=11, 4: NO-dofd=01012020
        self.account_activity = self.create_bulk_activities(self.data_file, activities, 4)

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': datetime(2019, 12, 31).date(),
            'cons_acct_num': '0032', 'acct_stat': '71', 'dofd': None,
            'amt_past_due': 0, 'compl_cond_cd':'0', 'current_bal': 0,
            'date_closed': datetime(2020, 1, 1).date(), 'orig_chg_off_amt': 0,
            'smpa': 0, 'spc_com_cd': 'X', 'terms_freq': '0'
        }, {
            'id': 33, 'activity_date': datetime(2019, 12, 31).date(),
            'cons_acct_num': '0033', 'acct_stat': '97', 'dofd': None,
            'amt_past_due': 0, 'compl_cond_cd':'0', 'current_bal': 0,
            'date_closed': datetime(2020, 1, 1).date(), 'orig_chg_off_amt': 0,
            'smpa': 0, 'spc_com_cd': 'X', 'terms_freq': '0'
        }]
        self.assert_evaluator_correct(self.event, 'ADDL-DOFD-1', expected)

    def test_eval_addl_dofd_2(self):
    # Hits when all conditions met:
    # 1. acct_stat == '13'
    # 2. pmt_rating == '1', '2', '3', '4', '5', '6', 'G', 'L'
    # 2. dofd == None

        # Create the Account Activities data
        activities = { 'id':(32,33,34,35,36),
            'cons_acct_num':('0032','0033','0034','0035', '0036'),
            'account_holder':('Z','Y','X','W','V'),
            'acct_stat':('13','13','11','13','13'),
            'dofd':(None,None,None,None,datetime(2019, 12, 31)),
            'pmt_rating':('1','2','3','0','L')}
        # 1: HIT, 2: HIT, 3: NO-acct_stat=11, 4: pmt_rating=0, 5: NO-dofd=01012020
        self.account_activity = self.create_bulk_activities(self.data_file, activities, 5)

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': datetime(2019, 12, 31).date(),
            'cons_acct_num': '0032', 'acct_stat': '13', 'dofd': None,
            'pmt_rating':'1', 'amt_past_due': 0, 'compl_cond_cd':'0',
            'current_bal': 0, 'date_closed': datetime(2020, 1, 1).date(),
            'orig_chg_off_amt': 0, 'smpa': 0, 'spc_com_cd': 'X',
            'terms_freq': '0'
        }, {
            'id': 33, 'activity_date': datetime(2019, 12, 31).date(),
            'cons_acct_num': '0033', 'acct_stat': '13', 'dofd': None,
            'pmt_rating':'2', 'amt_past_due': 0, 'compl_cond_cd':'0',
            'current_bal': 0, 'date_closed': datetime(2020, 1, 1).date(),
            'orig_chg_off_amt': 0, 'smpa': 0, 'spc_com_cd': 'X',
            'terms_freq': '0'
        }]
        self.assert_evaluator_correct(self.event, 'ADDL-DOFD-2', expected)

    def test_eval_addl_dofd_3(self):
    # Hits when all conditions met:
    # 1. acct_stat == '13'
    # 2. pmt_rating == '0'
    # 3. dofd != None

        # Create the Account Activities data
        activities = { 'id':(32,33,34,35,36),
            'cons_acct_num':('0032','0033','0034','0035', '0036'),
            'account_holder':('Z','Y','X','W','V'),
            'acct_stat':('13','13','11','13','13'),
            'dofd':(datetime(2019, 12, 31),datetime(2019, 12, 31),None,None,None),
            'pmt_rating':('0','0','0','3','0')}
        # 1: HIT, 2: HIT, 3: NO-acct_stat=11, 4: pmt_rating=3, 5: NO-dofd=01012020
        self.account_activity = self.create_bulk_activities(self.data_file, activities, 5)

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': datetime(2019, 12, 31).date(),
            'cons_acct_num': '0032', 'acct_stat': '13',
            'dofd': datetime(2019, 12, 31).date(), 'pmt_rating':'0',
            'amt_past_due': 0, 'compl_cond_cd':'0', 'current_bal': 0,
            'date_closed': datetime(2020, 1, 1).date(),
            'orig_chg_off_amt': 0, 'smpa': 0, 'spc_com_cd': 'X',
            'terms_freq': '0'
        }, {
            'id': 33, 'activity_date': datetime(2019, 12, 31).date(),
            'cons_acct_num': '0033', 'acct_stat': '13',
            'dofd': datetime(2019, 12, 31).date(), 'pmt_rating':'0',
            'amt_past_due': 0, 'compl_cond_cd':'0', 'current_bal': 0,
            'date_closed': datetime(2020, 1, 1).date(),
            'orig_chg_off_amt': 0, 'smpa': 0, 'spc_com_cd': 'X',
            'terms_freq': '0'
        }]
        self.assert_evaluator_correct(self.event, 'ADDL-DOFD-3', expected)
