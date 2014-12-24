__author__ = 'Anton Glukhov'

import unittest
from base import BaseTestCase
from sqlautocode_gen.model import *
from tests.run import Session, server


def setUpModule():
    pass


def tearModuleDown():
    pass


class AuthBaseTestCase(unittest.TestCase):

    @unittest.skip("Base auth case.")
    def test_native_auth(self):
        pass

class NativeAuthTestCase(unittest.TestCase):

    @unittest.skip("Correct native auth.")
    def test_native_auth(self):
        pass

    @unittest.skip("Incorrect native auth: wrong login.")
    def test_native_auth_wrong_login(self):
        pass

    @unittest.skip("Incorrect native auth: wrong password.")
    def test_native_auth_wrong_password(self):
        pass

    @unittest.skip("Incorrect native auth: wrong params.")
    def test_native_auth_wrong_params(self):
        pass

class TwitterAuthTestCase(unittest.TestCase):

    @unittest.skip("Correct twitter auth.")
    def test_twitter_auth(self):
        pass

    @unittest.skip("Incorrect twitter auth: wrong token.")
    def test_twitter_auth_wrong_token(self):
        pass

    @unittest.skip("Incorrect twitter auth: wrong params.")
    def test_twitter_auth_wrong_params(self):
        pass


class FacebookAuthTestCase(unittest.TestCase):

    @unittest.skip("Correct fb auth.")
    def test_fb_auth(self):
        pass

    @unittest.skip("Incorrect fb auth: wrong token.")
    def test_fb_auth_wrong_token(self):
        pass

    @unittest.skip("Incorrect fb auth: wrong params.")
    def test_fb_auth_wrong_params(self):
        pass


class VkAuthTestCase(unittest.TestCase):

    @unittest.skip("Correct vk auth.")
    def test_vk_auth(self):
        pass

    @unittest.skip("Incorrect vk auth: wrong token.")
    def test_vk_auth_wrong_token(self):
        pass

    @unittest.skip("Incorrect vk auth: wrong params.")
    def test_vk_auth_wrong_params(self):
        pass


def suite():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(AuthBaseTestCase))
    suite.addTests(loader.loadTestsFromTestCase(NativeAuthTestCase))
    suite.addTests(loader.loadTestsFromTestCase(TwitterAuthTestCase))
    suite.addTests(loader.loadTestsFromTestCase(FacebookAuthTestCase))
    suite.addTests(loader.loadTestsFromTestCase(VkAuthTestCase))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')