from django.test import TestCase

from datetime import date
from parse_m2.initiate_post_parsing import associate_previous_records
from evaluate_m2.tests.evaluator_test_helper import (
    EvaluatorTestHelper,
    acct_record
)
from parse_m2.models import Metro2Event, M2DataFile

class ProgEvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the previous AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()

        self.prev_data_file = M2DataFile(event=self.event, file_name='old_file.txt')
        self.prev_data_file.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()

    ############################
    # Tests for the category addl dofd evaluators

    def test_eval_prog_dofd_1(self):
    # Hits when all conditions met:
    # 1. previous_values__acct_stat == '61', '62', '63', '64', '65', '71',
    #                 '78', '80' '82', '83', '84', '88', '89', '94', '95',
    #                 '96', '93', '97'
    # 2. acct_stat == '61', '62', '63', '64', '65', '71', '78', '80','82',
    #                 '83', '84', '88', '89', '94', '95', '96', '93', '97'
    # 3. previous_values__dofd != dofd

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'acct_stat':'61', 'dofd': None
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'acct_stat':'62', 'dofd': date(2019, 11, 1)
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'acct_stat':'66', 'dofd': None
            }, {
                'id': 35, 'activity_date': prev_acct_date, 'cons_acct_num': '0035',
                'acct_stat':'71', 'dofd': date(2019, 10, 31)
            }, {
                'id': 36, 'activity_date': prev_acct_date, 'cons_acct_num': '0036',
                'acct_stat':'78', 'dofd': None
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)


        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'61', 'dofd': date(2019, 12, 1)
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'62', 'dofd': date(2019, 12, 10)
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'63', 'dofd': date(2019, 10, 31)
            }, {
                'id': 45, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'77', 'dofd': None
            }, {
                'id': 46, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'78', 'dofd': None
            }]
        for i in range(0, len(activities)):
            acct_record(self.data_file, activities[i])
        associate_previous_records(self.event)
        # 42: HIT, 43: HIT, 44: NO-previous_values__acct_stat=66,
        # 45: NO-acct_stat=77, 46: No-previous_values__dofd == dofd

        expected = [{
            'id': 42, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
        }, {
            'id': 43, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
        }]
        self.assert_evaluator_correct(self.event, 'PROG-DOFD-1', expected)

    def test_eval_prog_status_1(self):
    # Hits when the following one conditions are met...
    #   a. previous_values__acct_stat == '71' & acct_stat == '80', '82', '83', '84'
    #   b. previous_values__acct_stat == '78' & acct_stat == '82', '83', '84'
    #   c. previous_values__acct_stat == '80' & acct_stat == '83', '84'
    #   d. previous_values__acct_stat == '82' & acct_stat == '84'

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'acct_stat':'71'
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'acct_stat':'78'
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'acct_stat':'79'
            }, {
                'id': 35, 'activity_date': prev_acct_date, 'cons_acct_num': '0035',
                'acct_stat':'80'
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'80'
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'84'
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'83'
            }, {
                'id': 45, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'82'
            }]
        for r in activities:
            acct_record(self.data_file, r)
        associate_previous_records(self.event)
        # 42: HIT, 43: HIT, 44: NO-previous_values__acct_stat=79,
        # 45: NO-acct_stat=82

        expected = [
            {'id': 42, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 43, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'}]

        self.assert_evaluator_correct(self.event, 'PROG-Status-1', expected)

    def test_eval_prog_status_2(self):
    # Hits when both conditions met:
    # 1. previous_values__acct_stat == '89', '94'
    # 2. acct_stat == '97'

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'acct_stat':'89'
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'acct_stat':'71'
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'acct_stat':'97'
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'97'
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'97'
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'77'
            }]
        for r in activities:
            acct_record(self.data_file, r)
        associate_previous_records(self.event)
        # 42: HIT, 43: NO-previous_values__acct_stat=71,
        # 44: NO-acct_stat=77

        expected = [
            {'id': 42, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'}]
        self.assert_evaluator_correct(self.event, 'PROG-Status-2', expected)

    def test_eval_prog_status_3(self):
    # Hits when both conditions met:
    # 1. previous_values__acct_stat == '13', '62'
    # 2. acct_stat != '13', '62'
    # 3. port_type == 'I', 'M'

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'acct_stat':'13', 'port_type': 'I'
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'acct_stat':'71', 'port_type': 'M'
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'acct_stat':'13', 'port_type': 'I'
            }, {
                'id': 35, 'activity_date': prev_acct_date, 'cons_acct_num': '0035',
                'acct_stat':'62', 'port_type': 'M'
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'97', 'port_type': 'I'
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'97', 'port_type': 'M'
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'62', 'port_type': 'I'
            }, {
                'id': 45, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'77', 'port_type': 'A'
            }]
        for r in activities:
            acct_record(self.data_file, r)
        associate_previous_records(self.event)
        # 42: HIT, 43: NO-previous_values__acct_stat=71,
        # 44: NO-acct_stat=62, 45: NO-port_type='A'

        expected = [
            {'id': 42, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'}]
        self.assert_evaluator_correct(self.event, 'PROG-Status-3', expected)