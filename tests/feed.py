# -*- coding: utf-8 -*-
__author__ = 'Anton Glukhov'

import unittest
from base import BaseTestCase
from sqlautocode_gen.model import *
from tests.run import Session, server


def setUpModule():
    pass


def tearModuleDown():
    pass


class FeedBaseTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser("2013-12-12 12:12:12", "u1", "testtest")
        cls.u2 = TrUser("2013-12-12 12:12:12", "u2", "testtest")
        cls.u3 = TrUser("2013-12-12 12:12:12", "u3", "testtest")
        user_list = [cls.u1, cls.u2, cls.u3]
        cls.user_count = len(user_list)
        session.add_all(user_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.commit()

        cls.f1 = TrFeed("ttl1", "l1.com")
        cls.f2 = TrFeed("ttl2", "l2.com")
        f_list = [cls.f1, cls.f2]
        cls.v_count = len(f_list)
        session.add_all(f_list)
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        feeds = session.query(TrFeed).all()
        map(session.delete, feeds)

        session.commit()

        session.close()


    def test_base_relation(self):

        self.session.add(self.u1)
        self.session.add(self.f1)

        self.u1.feeds = [self.f1]
        self.session.commit()

        self.assertEquals(len(self.u1.feeds), 1)

    def test_autodelete_from_associated_table(self):

        self.session.add(self.u2)
        self.session.add(self.f2)

        self.u2.feeds = [self.f2]
        self.session.commit()

        self.session.delete(self.u2)
        self.session.commit()

        ufeeds = self.session.query(association_table_user_feed).filter_by(user_id = self.u2.ID).all()

        self.assertEquals(len(ufeeds), 0)


class FeedGetTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser("2013-12-12 12:12:12", "u1", "testtest")
        cls.u2 = TrUser("2013-12-12 12:12:12", "u2", "testtest")
        cls.u3 = TrUser("2013-12-12 12:12:12", "u3", "testtest")
        user_list = [cls.u1, cls.u2, cls.u3]
        cls.user_count = len(user_list)
        session.add_all(user_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.commit()

        cls.f1 = TrFeed("ttl1", "l1.com")
        cls.f2 = TrFeed("ttl2", "l2.com")
        f_list = [cls.f1, cls.f2]
        cls.v_count = len(f_list)
        session.add_all(f_list)
        session.commit()

        cls.u1.feeds = [cls.f1]
        cls.u2.feeds = [cls.f1, cls.f2]
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        feeds = session.query(TrFeed).all()
        map(session.delete, feeds)

        session.commit()

        session.close()


    def test_one_feed_for_user(self):

        self.session.add(self.u1)

        data = server.getFeeds(self.u1.ID)

        self.assertJsonRpc(data)
        self.assertIs(type(data['result']), list)
        self.assertEquals(len(data['result']), 1)
        self.assertEquals(data['result'][0]['title'], u'ttl1')


    def test_one_feed_for_user(self):

        self.session.add(self.u2)

        data = server.getFeeds(self.u2.ID)

        self.assertJsonRpc(data)
        self.assertIs(type(data['result']), list)
        self.assertEquals(len(data['result']), 2)
        self.assertEquals(data['result'][0]['title'], u'ttl1')
        self.assertEquals(data['result'][1]['title'], u'ttl2')


class FeedSubTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser("2013-12-12 12:12:12", "u1", "testtest")
        cls.u2 = TrUser("2013-12-12 12:12:12", "u2", "testtest")
        cls.u3 = TrUser("2013-12-12 12:12:12", "u3", "testtest")
        user_list = [cls.u1, cls.u2, cls.u3]
        cls.user_count = len(user_list)
        session.add_all(user_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.commit()

        cls.f1 = TrFeed("ttl1", "l1.com")
        cls.f2 = TrFeed("ttl2", "l2.com")
        f_list = [cls.f1, cls.f2]
        cls.v_count = len(f_list)
        session.add_all(f_list)
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        feeds = session.query(TrFeed).all()
        map(session.delete, feeds)

        session.commit()

        session.close()


    def test_add_normal_feed(self):

        self.session.add(self.u1)
        self.session.add(self.f1)

        data = server.subFeed(self.u1.ID, self.f1.id)

        self.assertJsonRpc(data)
        self.assertIs(data['result'], True)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        u = s.query(TrUser).get(self.u1.ID)
        self.assertIsNotNone(u)
        self.assertEquals(len(u.feeds), 1)
        s.close()

    def test_add_incorrect_user_id(self):

        self.session.add(self.u1)
        self.session.add(self.f1)

        data = server.subFeed(self.u1.ID + 1000, self.f1.id)

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error'][u'message'], "ServerError: User doesn't exist.")

    def test_incorrect_feed_id(self):

        self.session.add(self.u1)
        self.session.add(self.f1)

        data = server.subFeed(self.u1.ID, self.f1.id + 1000)

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error'][u'message'], "ServerError: Feed doesn't exist.")

    def test_subscribe_already_belongs(self):

        self.session.add(self.u2)
        self.session.add(self.f2)

        self.u2.feeds.append(self.f2)
        self.session.commit()

        data = server.subFeed(self.u2.ID, self.f2.id)

        self.assertJsonRpc(data)
        self.assertIs(data['result'], True)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        u = s.query(TrUser).get(self.u2.ID)
        self.assertIsNotNone(u)
        self.assertEquals(len(u.feeds), 1)
        s.close()


class FeedUnsubTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser("2013-12-12 12:12:12", "u1", "testtest")
        cls.u2 = TrUser("2013-12-12 12:12:12", "u2", "testtest")
        cls.u3 = TrUser("2013-12-12 12:12:12", "u3", "testtest")
        user_list = [cls.u1, cls.u2, cls.u3]
        cls.user_count = len(user_list)
        session.add_all(user_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.commit()

        cls.f1 = TrFeed("ttl1", "l1.com")
        cls.f2 = TrFeed("ttl2", "l2.com")
        f_list = [cls.f1, cls.f2]
        cls.v_count = len(f_list)
        session.add_all(f_list)
        session.commit()

        cls.u1.feeds = [cls.f1]
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        feeds = session.query(TrFeed).all()
        map(session.delete, feeds)

        session.commit()

        session.close()


    def test_unsubscribe_normal(self):

        self.session.add(self.u1)
        self.session.add(self.f1)

        data = server.unsubFeed(self.u1.ID, self.f1.id)

        self.assertJsonRpc(data)
        self.assertIs(data['result'], True)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        u = s.query(TrUser).get(self.u1.ID)
        self.assertIsNotNone(u)
        self.assertEquals(len(u.feeds), 0)
        s.close()


class FeedAddFavTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser("2013-12-12 12:12:12", "u1", "testtest")
        cls.u2 = TrUser("2013-12-12 12:12:12", "u2", "testtest")
        cls.u3 = TrUser("2013-12-12 12:12:12", "u3", "testtest")
        user_list = [cls.u1, cls.u2, cls.u3]
        cls.user_count = len(user_list)
        session.add_all(user_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.commit()

        cls.f1 = TrFeed("ttl1", "l1.com")
        cls.f2 = TrFeed("ttl2", "l2.com")
        f_list = [cls.f1, cls.f2]
        cls.v_count = len(f_list)
        session.add_all(f_list)
        session.commit()

        cls.u1.feeds = [cls.f1]
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        feeds = session.query(TrFeed).all()
        map(session.delete, feeds)

        session.commit()

        session.close()


    def test_add_fav_normal(self):

        self.session.add(self.u1)
        self.session.add(self.f1)

        data = server.addFavFeed(self.u1.ID, self.f1.id, "test_link")

        self.assertJsonRpc(data)
        self.assertIs(data['result'], True)


class FeedDelFavTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser("2013-12-12 12:12:12", "u1", "testtest")
        cls.u2 = TrUser("2013-12-12 12:12:12", "u2", "testtest")
        cls.u3 = TrUser("2013-12-12 12:12:12", "u3", "testtest")
        user_list = [cls.u1, cls.u2, cls.u3]
        cls.user_count = len(user_list)
        session.add_all(user_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.commit()

        cls.f1 = TrFeed("ttl1", "l1.com")
        cls.f2 = TrFeed("ttl2", "l2.com")
        f_list = [cls.f1, cls.f2]
        cls.v_count = len(f_list)
        session.add_all(f_list)
        session.commit()

        cls.u1.feeds = [cls.f1]
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        feeds = session.query(TrFeed).all()
        map(session.delete, feeds)

        session.commit()

        session.close()


    def test_del_fav_normal(self):

        self.session.add(self.u1)
        self.session.add(self.f1)

        data = server.addFavFeed(self.u1.ID, self.f1.id, "test_link")

        self.assertJsonRpc(data)
        self.assertIs(data['result'], True)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        u_f = s.query(association_table_user_feed).filter_by(user_id = self.u1.ID).filter_by(feed_id = self.f1.id).first()
        self.assertIsNotNone(u_f)
        self.assertEquals(u_f.user_id, self.u1.ID)
        self.assertEquals(u_f.feed_id, self.f1.id)
        s.close()

        data = server.delFavFeed(self.u1.ID, self.f1.id, "test_link")

        self.assertJsonRpc(data)
        self.assertIs(data['result'], True)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        u_f = s.query(association_table_user_feed).filter_by(user_id = self.u1.ID).filter_by(feed_id = self.f1.id).first()
        self.assertIsNotNone(u_f)
        self.assertEquals(u_f.user_id, self.u1.ID)
        self.assertEquals(u_f.feed_id, self.f1.id)
        s.close()


class FeedGetFavsTestCase(BaseTestCase):
    pass


def suite():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(FeedBaseTestCase))
    suite.addTests(loader.loadTestsFromTestCase(FeedGetTestCase))
    suite.addTests(loader.loadTestsFromTestCase(FeedSubTestCase))
    suite.addTests(loader.loadTestsFromTestCase(FeedUnsubTestCase))
    suite.addTests(loader.loadTestsFromTestCase(FeedAddFavTestCase))
    suite.addTests(loader.loadTestsFromTestCase(FeedDelFavTestCase))
    suite.addTests(loader.loadTestsFromTestCase(FeedGetFavsTestCase))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
