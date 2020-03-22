from unittest import TestCase

from caller import Caller


class IntegrationTest(TestCase):

    def setUp(self):
        self.caller = Caller('http://localhost:8000')

    def test_make_request(self):
        response = self.caller.make_request()
        self.assertEqual(response, 'Hello, World!', 'wrong response')
