from evaluate_m2.tests.test_views.view_tests_helper import EvaluatorViewsTestHelper


class AccountViewsTestCase(EvaluatorViewsTestHelper):
    def setUp(self):
        self.create_evaluator_metadata()
        self.create_eval_results_summaries()
        self.create_activity_and_eval_results()

    ########################################
    # Tests for Account list view API endpoint
    def test_account_list_view_no_acct_num(self):
        response = self.client.get("/api/events/1/account/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        # the response should be an empty list
        self.assertEqual(response.json(), [])

    def test_account_list_view(self):
        expected = [
            {
                "acct_type": "",
                "cons_acct_num": "908070",
                "total_records": 3,
                "port_type": "A",
                "total_hits": 4
            },
        ]
        # One of the accounts exists and is included in the response
        response = self.client.get("/api/events/1/account/?cons_acct_num=0033,908070")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.json(), expected)

    ########################################
    # Tests for Account Summary view API endpoint
    def test_account_summary_view_single_results(self):
        # Response follows this pattern, where account_activity is a list
        # of all accountactivity records for this consumer acct number
        # from the AccountActivitySerializer
        # expected = {
        #     'cons_acct_num': '908070',
        #     'inconsistencies': ['Portfolio-Type-1', 'Portfolio-Type-2'],
        #     'account_activity': [ ... ]
        # }

        response = self.client.get('/api/events/1/account/908070/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        resp = response.json()
        self.assertEqual(resp['cons_acct_num'], '908070')
        self.assertEqual(resp['inconsistencies'],
                         ['Portfolio-Type-1', 'Portfolio-Type-2'])
        self.assertEqual(len(resp['account_activity']), 3)

        first_acct_activity = resp['account_activity'][0]
        self.assertEqual(first_acct_activity['activity_date'], '2025-03-01')
        self.assertEqual(first_acct_activity['inconsistencies'], ['Portfolio-Type-1'])

    def test_account_summary_view_no_accountactivity_for_event(self):
        error='AccountActivity record(s) not found for account number 0039.'
        response = self.client.get('/api/events/1/account/0039/')

        # the response should be a JSON
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        self.assertEqual(response.json()['message'], error)

    ########################################
    # Tests for Account PII view API endpoint
    def test_account_pii_view(self):
        response = self.client.get('/api/events/1/account/908070/account_holder/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        expected = {
            'id': response.json()['id'], 'surname': 'Claus', 'first_name': 'Santa',
            'middle_name': '', 'gen_code': '', 'ssn': '', 'dob': '', 'phone_num': '',
            'ecoa': '', 'cons_info_ind': '', 'country_cd': '', 'addr_line_1': '',
            'addr_line_2': '', 'city': '', 'state': '', 'zip': '', 'addr_ind': '',
            'res_cd': '', 'cons_acct_num': '908070'
        }
        self.assertEqual(response.json(), expected)
