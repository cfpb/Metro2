from django.test import TestCase

from datetime import datetime
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper
from parse_m2.models import Metro2Event, M2DataFile


class TestCat12Evals(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()
        # Create the Account Holders
        self.account_holders = self.create_bulk_account_holders(self.data_file, ('Z','Y','X','W','V','U','T'))

    ############################
    # Tests for the category 12 evaluators
    def test_eval_12_installment_no_HCOLA(self):
        # Hits when all conditions are met:
        # 1. port_type == 'I'
        # 2. acct_type == '00', '3A', '10', '91', '6A', '7B', '05',
        #                 '0A', '0F', '47', '9A', '17', '01', '02',
        #                 '03', '11', '13', '04', '20', '6D', '06'
        # 3. terms_freq != 'D'
        # 4. hcola <= 0

        # Create the Account Activities data
        activities = {'id':(32,33,34,35,36,37),
                      'account_holder':('Z','Y','X','W','V','U'),
                      'acct_type':('00','3A','12','91','00','3A'),
                      'cons_acct_num':('0032','0033','0034','0035','0036','0037'), 'credit_limit':(10,20,30,40,50,60),
                      'hcola':(-1,-1,-5,-5,0,5),
                      'port_type':('I','M','I','I','I','I'),
                      'terms_dur':('5','10','15','20','25','30'),
                      'terms_freq':('P','W','P','D','W','P')}
        # 1: HIT, 2: NO-port_type=M, 3: NO-acct_type=12, 4: NO-terms_freq=D,
        # 5: HIT, 6: NO-hcola=5
        self.account_activity = self.create_bulk_activities(self.data_file, activities, 6)

        expected = [{
            'id': 32, 'activity_date': datetime(2019, 12, 31).date(), 'cons_acct_num': '0032', 'acct_type': '00', 'port_type': 'I', 'hcola': -1,
            'terms_freq': 'P', 'credit_limit': 10, 'terms_dur': '5'
        }, {
            'id': 36, 'activity_date': datetime(2019, 12, 31).date(), 'cons_acct_num': '0036', 'acct_type': '00', 'port_type': 'I', 'hcola': 0,
            'terms_freq': 'W', 'credit_limit': 50, 'terms_dur': '25'
        }]
        self.assert_evaluator_correct(self.event, '12-Installment loan no HCOLA', expected)

    def test_eval_12_mortgage_no_HCOLA(self):
        # Hits when all conditions are met:
        # 1. port_type == 'M'
        # 2. acct_type == '08', '19', '25', '26', '2C', '5A', '5B', '6B'
        # 3. terms_freq != 'D'
        # 4. hcola <= 0

        # Create the Account Activities data
        activities = {'id':(32,33,34,35,36,37),
                      'account_holder':('Z','Y','X','W','V','U'),
                      'acct_type':('08','19','11','25','2C','26'),
                      'cons_acct_num':('0032','0033','0034','0035','0036','0037'), 'credit_limit':(10,20,30,40,50,60),
                      'hcola':(-1,-1,-5,-5,0,5),
                      'port_type':('M','I','M','M','M','M'),
                      'terms_dur':('5','10','15','20','25','30'),
                      'terms_freq':('P','W','P','D','W','P')}
        # 1: HIT, 2: NO-port_type=I, 3: NO-acct_type=11, 4: NO-terms_freq=D,
        # 5: HIT, 6: NO-hcola=5
        self.account_activity = self.create_bulk_activities(self.data_file, activities, 6)

        expected = [{
            'id': 32, 'activity_date': datetime(2019, 12, 31).date(), 'cons_acct_num': '0032', 'acct_type': '08', 'port_type': 'M', 'hcola': -1,
            'terms_freq': 'P', 'credit_limit': 10, 'terms_dur': '5'
        }, {
            'id': 36, 'activity_date': datetime(2019, 12, 31).date(), 'cons_acct_num': '0036', 'acct_type': '2C', 'port_type': 'M', 'hcola': 0,
            'terms_freq': 'W', 'credit_limit': 50, 'terms_dur': '25'
        }]
        self.assert_evaluator_correct(self.event, '12-Mortgage no HCOLA', expected)

    def test_eval_12_open_no_HCOLA(self):
        # Hits when all conditions are met:
        # 1. port_type == 'O'
        # 2. acct_type == '0C', '48', '77'
        # 3. terms_freq != 'D'
        # 4. hcola <= 0
        # hcola cannot be an empty string or NULL by constraints

        # Create the Account Activities data
        activities = {'id':(32,33,34,35,36,37),
                      'account_holder':('Z','Y','X','W','V','U'),
                      'acct_type':('0C','48','11','77','0C','48'),
                      'cons_acct_num':('0032','0033','0034','0035','0036','0037'), 'credit_limit':(10,20,30,40,50,60),
                      'hcola':(-1,-1,-5,-5,0,5),
                      'port_type':('O','I','O','O','O','O'),
                      'terms_dur':('5','10','15','20','25','30'),
                      'terms_freq':('P','W','P','D','W','P')}
        # 1: HIT, 2: NO-port_type=I, 3: NO-acct_type=11, 4: NO-terms_freq=D,
        # 5: HIT, 6: NO-hcola=5
        self.account_activity = self.create_bulk_activities(self.data_file, activities, 6)

        expected = [{
            'id': 32, 'activity_date': datetime(2019, 12, 31).date(), 'cons_acct_num': '0032', 'acct_type': '0C', 'port_type': 'O', 'hcola': -1,
            'terms_freq': 'P', 'credit_limit': 10, 'terms_dur': '5'
        }, {
            'id': 36, 'activity_date': datetime(2019, 12, 31).date(), 'cons_acct_num': '0036', 'acct_type': '0C', 'port_type': 'O', 'hcola': 0,
            'terms_freq': 'W', 'credit_limit': 50, 'terms_dur': '25'
        }]
        self.assert_evaluator_correct(self.event, "12-Open no HCOLA", expected)
