from django.test import TestCase


class TestBadRequestView(TestCase):

    def test_bad_request_view(self):
        response = self.client.get('/api/fake/')
        self.assertEqual(response.status_code, 400)

    def test_does_not_return_bad_request(self):
        response = self.client.get('/api/all-evaluator-metadata/')
        self.assertNotEqual(response.status_code, 400)
