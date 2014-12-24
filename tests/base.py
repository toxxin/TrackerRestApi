__author__ = 'Anton Glukhov'

import unittest
from tests.run import Session


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


    def setUp(self):
        self.session = Session()

    def tearDown(self):
        self.session.expunge_all()
        self.session.close()


    def assertJsonRpc(self, data):
        self.assertIn(u'result', data)

    def assertJsonRpcErr(self, data):
        self.assertIn(u'error', data)