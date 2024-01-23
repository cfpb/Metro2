from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper
from parse_m2.models import Metro2Event, M2DataFile

class Cat9_EvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the previous AccountActivity data
        self.prev_event = Metro2Event(name='test_exam')
        self.prev_event.save()
        self.prev_data_file = M2DataFile(event=self.prev_event, file_name='old_file.txt')
        self.prev_data_file.save()
        # Create the Account Holders
        self.prev_accounts = self.create_bulk_account_holders(self.prev_data_file, ('','','','A','','','',''))
        # Create the parent records for the AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()
        # Create the Account Holders
        self.accounts = self.create_bulk_account_holders(self.data_file, ('A','B','C','D','E','F','G','H'))

    ############################
    # Tests for the category 9 evaluators
    def test_eval_9_3A_acct_stat_current_PHP_not_current(self):
    # Hits when conditions met:
    # 1. prior_cons_info_ind=''
    # 2. any (prior_j1.cons_info_ind == '')
    # 3. any (prior_j2.cons_info_ind == '')
    # 4. prior_acct_stat == '11'
    # 5. prior_current_bal > 0
    # 6. port_type  == 'C', 'O', 'R'
    # 7. php != 'O'

        # Create previous Account Activities data
        prev_activities = { 'id':(32,33,34,35,36,37,38,39),
            'activity_date':(date(2019, 11, 30), date(2019, 11, 30), date(2019, 11, 30),
                             date(2019, 11, 30), date(2019, 11, 30), date(2019, 11, 30),
                             date(2019, 11, 30), date(2019, 11, 30)),
            'cons_acct_num':('0032','0033','0034','0035','0036','0037','0038','0039'),
            'acct_stat':('11','11','11','11','11','11','10','11'),
            'account_holder_id':self.prev_accounts,
            'current_bal':(5, 10, 15, 20, 25, 0, 35, 40)}
        self.create_bulk_activities(self.prev_data_file, prev_activities, 8)

        prev_j1_data = {
              'account_activity':(32,33,34,35,36,37,38,39),
              'cons_info_ind':('','','','','M','','','')}
        self.create_bulk_JSegments('j1', prev_j1_data, 8)

        prev_j2_data = {
              'account_activity':(32,33,34,35,36,37,38,39),
              'cons_info_ind':('','','','','','','','')}
        self.create_bulk_JSegments('j2', prev_j2_data, 8)

        # Create the Account Activities data
        activities = { 'id':(42,43,44,45,46,47,48,49),
            'cons_acct_num':('0032','0033','0034','0035','0036','0037','0038','0039'),
            'account_holder_id':self.accounts,
            'port_type':('C','O','A','C','O','R','C','O'),
            'php':('LLL','LLL','LLL','LLL','LLL','LLL','LLL','OLL')}
        self.create_bulk_activities(self.data_file, activities, 8)

        j1_data = {
              'account_activity':(42,43,44,45,46,47,48,49),
              'cons_info_ind':('A','B','C','D','E','F','G','H')}
        self.create_bulk_JSegments('j1', j1_data, 8)

        j2_data = {
              'account_activity':(42,43,44,45,46,47,48,49),
              'cons_info_ind':('A','B','C','D','E','F','G','H')}
        self.create_bulk_JSegments('j2', j2_data, 8)
        # 1: HIT, 2: HIT, 3: NO-port_type='A', 4: NO-prev_cons_info_ind='A',
        # 5: NO-prev_j1__cons_info_ind='M', 6: NO-prev_current_bal=0,
        # 7: NO-prev_acct_stat=10, 8: NO-php=O

        # Create the segment data
        expected = [{
            'id': 42, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'php':'LLL', 'port_type':'C',
            'prev_acct_stat':'11', 'prev_cons_info_ind': '',
            'prev_j1__cons_info_ind': '', 'prev_j2__cons_info_ind': '',
            'prev_current_bal': 5
        }, {
            'id': 43, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'php':'LLL', 'port_type':'O',
            'prev_acct_stat':'11', 'prev_cons_info_ind': '',
            'prev_j1__cons_info_ind': '', 'prev_j2__cons_info_ind': '',
            'prev_current_bal': 10
        }]
        self.assert_evaluator_correct(self.event, '9-3A Account Status current but PHP not current', expected)
