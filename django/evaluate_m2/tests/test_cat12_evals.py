from django.test import TransactionTestCase

from datetime import datetime
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper
from parse_m2.models import AccountActivity, AccountHolder, K2, M2DataFile


class TestCat12Evals(TransactionTestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the M2 Data File
        self.data_file = M2DataFile(id=1, exam_identifier='test_exam', file_name='file.txt')
        self.data_file.save()
        # Create the Account Holders
        self.account_holders = self.create_bulk_account_holders(self.data_file, ('Z','Y','X','W','V','U','T'))

    ############################
    # Tests for the category 12 evaluators
    def test_eval_12_installment_no_HCOLA(self):
        # Hits when conditions are met:
        # 1. port_type == 'I'
        # 2. acct_type == '00', '3A', '10', '91', '6A', '7B', '05',
        #                 '0A', '0F', '47', '9A', '17', '01', '02',
        #                 '03', '11', '13', '04', '20', '6D', '06'
        # 3. terms_freq != 'D'
        # 4. hcola < 0
        # hcola cannot be an empty string or NULL by constraints

        # Create the Account Activities data
        activities = {'id':(32,33,34,35,36,37,38),
                      'account_holder':('Z','Y','X','W','V','U','T'),
                      'acct_type':('00','3A','12','91','00','3A','20'),
                      'cons_acct_num':('0032','0033','0034','0035','0036','0037','0038'), 'credit_limit':(10,20,30,40,50,60,70), 'hcola':(-1,-1,-5,-5,0,5,-5), 'port_type':('I','M','I','I','I','I','I'), 'terms_dur':('5','10','15','20','25','30','35'), 'terms_freq':('P','W','P','D','P','P','W')}
        # 1: HIT, 2: NO-port_type=M, 3: NO-acct_type=12, 4: NO-terms_freq=D,
        # 5: NO-hcola=0, 6: NO-hcola=5, 7: HIT
        self.account_activity = self.create_bulk_activities(activities, 7)

        expected = [{
            'id': 32, 'activity_date': datetime(2019, 12, 31).date(), 'cons_acct_num': '0032', 'acct_type': '00', 'port_type': 'I', 'hcola': -1,
            'terms_freq': 'P', 'credit_limit': 10, 'terms_dur': '5'
        }, {
            'id': 38, 'activity_date': datetime(2019, 12, 31).date(), 'cons_acct_num': '0038', 'acct_type': '20', 'port_type': 'I', 'hcola': -5,
            'terms_freq': 'W', 'credit_limit': 70, 'terms_dur': '35'
        }]
        self.assert_evaluator_correct('12-Installment no HCOLA', expected)

    def test_eval_12_mortgage_no_HCOLA(self):
        # Hits when conditions are met:
        # 1. port_type == 'M'
        # 2. acct_type == '08', '19', '25', '26', '2C', '5A', '5B', '6B'
        # 3. terms_freq != 'D'
        # 4. hcola < 0 OR hcola=''
        # hcola cannot be an empty string or NULL by constraints

        # Create the Account Activities data
        activities = {'id':(32,33,34,35,36,37,38),
                      'account_holder':('Z','Y','X','W','V','U','T'),
                      'acct_type':('08','19','11','25','01','26','2C'),
                      'cons_acct_num':('0032','0033','0034','0035','0036','0037','0038'), 'credit_limit':(10,20,30,40,50,60,70), 'hcola':(-1,-1,-5,-5,0,5,-5), 'port_type':('M','I','M','M','M','M','M'), 'terms_dur':('5','10','15','20','25','30','35'), 'terms_freq':('P','W','P','D','P','P','W')}
        # 1: HIT, 2: NO-port_type=I, 3: NO-acct_type=11, 4: NO-terms_freq=D,
        # 5: NO-hcola=0, 6: NO-hcola=5, 7: HIT
        self.account_activity = self.create_bulk_activities(activities, 7)

        expected = [{
            'id': 32, 'activity_date': datetime(2019, 12, 31).date(), 'cons_acct_num': '0032', 'acct_type': '08', 'port_type': 'M', 'hcola': -1,
            'terms_freq': 'P', 'credit_limit': 10, 'terms_dur': '5'
        }, {
            'id': 38, 'activity_date': datetime(2019, 12, 31).date(), 'cons_acct_num': '0038', 'acct_type': '2C', 'port_type': 'M', 'hcola': -5,
            'terms_freq': 'W', 'credit_limit': 70, 'terms_dur': '35'
        }]
        self.assert_evaluator_correct('12-Mortgage no HCOLA', expected)

    def test_eval_12_open_no_HCOLA(self):
        # Hits when conditions are met:
        # 1. port_type == 'O'
        # 2. acct_type == '0C', '48', '77'
        # 3. terms_freq != 'D'
        # 4. hcola < 0 OR hcola=''
        # hcola cannot be an empty string or NULL by constraints

        # Create the Account Activities data
        activities = {'id':(32,33,34,35,36,37,38),
                      'account_holder':('Z','Y','X','W','V','U','T'),
                      'acct_type':('0C','48','11','77','0C','48','77'),
                      'cons_acct_num':('0032','0033','0034','0035','0036','0037','0038'), 'credit_limit':(10,20,30,40,50,60,70), 'hcola':(-1,-1,-5,-5,0,5,-5), 'port_type':('O','I','O','O','O','O','O'), 'terms_dur':('5','10','15','20','25','30','35'), 'terms_freq':('P','W','P','D','P','P','W')}
        # 1: HIT, 2: NO-port_type=I, 3: NO-acct_type=11, 4: NO-terms_freq=D,
        # 5: NO-hcola=0, 6: NO-hcola=5, 7: HIT
        self.account_activity = self.create_bulk_activities(activities, 7)

        expected = [{
            'id': 32, 'activity_date': datetime(2019, 12, 31).date(), 'cons_acct_num': '0032', 'acct_type': '0C', 'port_type': 'O', 'hcola': -1,
            'terms_freq': 'P', 'credit_limit': 10, 'terms_dur': '5'
        }, {
            'id': 38, 'activity_date': datetime(2019, 12, 31).date(), 'cons_acct_num': '0038', 'acct_type': '77', 'port_type': 'O', 'hcola': -5,
            'terms_freq': 'W', 'credit_limit': 70, 'terms_dur': '35'
        }]
        self.assert_evaluator_correct("12-Open no HCOLA", expected)
