from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper
from parse_m2.models import Metro2Event, M2DataFile

class Cat9_EvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the previous AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.prev_files=[]
        # Create the parent records for
        # the AccountActivity data
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()
        # Create the Account Holders
        self.accounts = self.create_bulk_account_holders(self.data_file, ('A','B','C','D','E','F','G','H'))
        self.prev_j1 = []

    def create_all_records(self, acct_stats:tuple, phps:tuple, size: int,
                           create_all_j1_segments:bool, addl_fields=list()):

        # Create previous Account Activities data
        ids=[(22,23,24,25,26,27,28,29),(32,33,34,35,36,37,38,39)]
        activity_dates=[date(2019, 10, 31), date(2019, 11, 30)]

        prev_port_type=[
            ('A','A','A','A','A','A','A','A'),
            ('B','B','R','B','B','B','B','R')
        ]
        prev_phps=[
            ('LLL','LLL','LLL','LLL','LLL','LLL','LLL','0LL'),
            ('0LL','0LL','0LL','0LL','0LL','0LL','LLL','LLL')
        ]
        file_names=('oct_file.txt','nov_file.txt')
        for i in range(0, len(file_names)):
            # Create previous files
            file = M2DataFile(event=self.event, file_name=file_names[i])
            file.save()
            self.prev_files.append(file)

        for i in range(0, len(ids)):
        # Create the Account Holders
            prev_accounts = self.create_bulk_account_holders(self.prev_files[i], ('','','','A','','','',''))

            prev_activities = { 'id':ids[i],
                'activity_date':activity_dates[i],
                'cons_acct_num':('0032','0033','0034','0035','0036','0037','0038','0039'),
                'current_bal': (5, 10, 15, 20, 25, 0, 35, 40),
                'acct_stat':acct_stats[i],
                'port_type':prev_port_type[i],
                'php':prev_phps[i],
                'account_holder_id':prev_accounts}
            self.create_bulk_activities(file, prev_activities, size)

            if create_all_j1_segments:
                j1_data = {
                    'account_activity':ids[i],
                    'cons_info_ind':('','','','','M','','','')}
                self.nov_j1 = self.create_bulk_JSegments('j1', j1_data, size)
            else:
                missing_ids=list(ids[i])
                missing_ids.pop(1)
                j1_data = {
                    'account_activity':missing_ids,
                    'cons_info_ind':('','','','M','','','')}
                self.nov_j1 = self.create_bulk_JSegments('j1', j1_data, size - 1)

            j2_data = {
                'account_activity':ids[i],
                'cons_info_ind':('','','','','','','','')}
            self.create_bulk_JSegments('j2', j2_data, size)

        # Create the Account Activities data
        current_activities = { 'id':(42,43,44,45,46,47,48,49),
            'cons_acct_num':('0032','0033','0034','0035','0036','0037','0038','0039'),
            'account_holder_id':self.accounts,
            'port_type':('C','O','A','C','O','R','C','O'),
            'php':phps}

        if 'port_type' in addl_fields:
            current_activities['port_type']=('C','O','A','C','O','R','C','O')
        self.create_bulk_activities(self.data_file, current_activities, size)

    ############################
    # Tests for the category 9 evaluators

    # - - - - - - - - - - - - - - - - - - - - - -

    # Hits when conditions met:
    # 1. prior_cons_info_ind=''
    # 2. any (prior_j1.cons_info_ind == '')
    # 3. any (prior_j2.cons_info_ind == '')
    # 4. prior_acct_stat == '11'
    # 5. prior_current_bal > 0
    # 6. port_type  == 'C', 'O', 'R'
    # 7. php != 'O'

    def test_eval_9_3A_acct_stat_current_PHP_not_current(self):
        # Create previous Account Activities data
        addl_fields=['current_bal', 'port_type']
        acct_stats=[('10','10','11','10','10','10','10','11'),
                         ('11','11','11','11','11','11','10','11')]
        phps=('LLL','LLL','LLL','LLL','LLL','LLL','LLL','0LL')
        self.create_all_records(acct_stats, phps, 8, True, addl_fields)
        # 22, 23, 24, 25, 26, 27, 28, 29 - No
        # 32-37: No-php==0, 38: port_type == 'B', 39: HIT
        # 42-43: HIT, 44: NO-port_type='A', 45: NO-prev_cons_info_ind='A', 46: NO-prev_j1__cons_info_ind='M'
        # 47: NO-prev_current_bal=0, 48: NO-prev_acct_stat=10, 49: NO-php=O

        # Create the segment data
        expected = [{
            'id': 39, 'activity_date': date(2019, 11, 30),
            'cons_acct_num': '0039', 'php':'LLL', 'port_type':'R',
            'prev_acct_stat':'11', 'prev_cons_info_ind': '',
            'prev_j1__cons_info_ind': '', 'prev_j2__cons_info_ind': '',
            'prev_current_bal': 40
        },{
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


    def test_eval_9_3A_acct_stat_current_PHP_missing_j1_segment(self):
        # Create previous Account Activities data
        addl_fields=['current_bal', 'port_type']
        acct_stats=[('10','10','11','10','10','10','10','11'),
                         ('11','11','11','11','11','11','10','11')]
        phps=('LLL','LLL','LLL','LLL','LLL','LLL','LLL','0LL')
        self.create_all_records(acct_stats, phps, 8, False, addl_fields)
        # 22, 23, 24, 25, 26, 27, 28, 29 - No
        # 32-37: No-php==0, 38: No-port_type == 'B', 39: HIT
        # 42: HIT, 43: No-missing J1 segment, 44: NO-port_type='A',
        # 45: NO-prev_cons_info_ind='A', 46: NO-prev_j1__cons_info_ind='M',
        # 47: NO-prev_current_bal=0, 48: NO-prev_acct_stat=10, 49: NO-php=O

        # Create the segment data
        expected = [{
            'id': 39, 'activity_date': date(2019, 11, 30),
            'cons_acct_num': '0039', 'php':'LLL', 'port_type':'R',
            'prev_acct_stat':'11', 'prev_cons_info_ind': '',
            'prev_j1__cons_info_ind': '', 'prev_j2__cons_info_ind': '',
            'prev_current_bal': 40
        },{
            'id': 42, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'php':'LLL', 'port_type':'C',
            'prev_acct_stat':'11', 'prev_cons_info_ind': '',
            'prev_j1__cons_info_ind': '', 'prev_j2__cons_info_ind': '',
            'prev_current_bal': 5
        }]
        self.assert_evaluator_correct(self.event, '9-3A Account Status current but PHP not current', expected)

    def test_eval_9_3A_acct_stat_current_PHP_many_j1_segments(self):
        # Create previous Account Activities data
        addl_fields=['current_bal', 'port_type']
        acct_stats=[('10','10','11','10','10','10','10','11'),
                         ('11','11','11','11','11','11','10','11')]
        phps=('LLL','LLL','LLL','LLL','LLL','LLL','LLL','0LL')
        self.create_all_records(acct_stats, phps, 8, True, addl_fields)
        # 22, 23, 24, 25, 26, 27, 28, 29 - No
        # 32-37: No-php==0, 38: No-port_type == 'B', 39: HIT
        # 42: HIT-multiple J1 Segments('','') only one record returned,
        # 43: HIT, 44: NO-port_type='A', 45: NO-prev_cons_info_ind='A',
        # 46: HIT-multiple J1 Segments prev_j1__cons_info_ind=['M',''],
        # 47: NO-prev_current_bal=0, 48: NO-prev_acct_stat=10, 49: NO-php=O

        # Create additional J1 segments for previous record
        addl_j1_data = {
            'account_activity':(32,36),
            'cons_info_ind':('','')
        }
        self.prev_j1.append(self.create_bulk_JSegments('j1', addl_j1_data, 2))

        # Create the segment data
        expected = [{
            'id': 39, 'activity_date': date(2019, 11, 30),
            'cons_acct_num': '0039', 'php':'LLL', 'port_type':'R',
            'prev_acct_stat':'11', 'prev_cons_info_ind': '',
            'prev_j1__cons_info_ind': '', 'prev_j2__cons_info_ind': '',
            'prev_current_bal': 40
        },{
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
        }, {
            'id': 46, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0036', 'php':'LLL', 'port_type':'O',
            'prev_acct_stat':'11', 'prev_cons_info_ind': '',
            'prev_j1__cons_info_ind': '', 'prev_j2__cons_info_ind': '',
            'prev_current_bal': 25
        }]
        self.assert_evaluator_correct(self.event, '9-3A Account Status current but PHP not current', expected)
