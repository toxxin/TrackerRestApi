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


class PlaceBaseTestCase(BaseTestCase):

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

        cls.p1 = TrPlace(title="Title1", latitude=54.123, longitude=35.123, type="Restaurant", user_id=cls.u1.ID)
        p_list = [cls.p1]
        cls.p_count = len(p_list)
        session.add_all(p_list)
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        places = session.query(TrPlace).all()
        map(session.delete, places)

        session.commit()

        session.close()


    def test_base_relation(self):

        self.session.add(self.u1)
        self.session.add(self.p1)

        self.assertEquals(len(self.u1.places), 1)
        self.assertEquals(self.u1.places[0].id, self.p1.id)


class PlaceGetTestCase(BaseTestCase):

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

        cls.p1 = TrPlace(title="Title1", latitude=54.123, longitude=35.123, type="Restaurant", user_id=cls.u1.ID)
        cls.p2 = TrPlace(title="Title2", latitude=54.123, longitude=35.123, type="Parking", user_id=cls.u2.ID)
        cls.p3 = TrPlace(title=u'Заголовок3', latitude=54.123, longitude=35.123, type="Caffe", user_id=cls.u2.ID)

        p_list = [cls.p1, cls.p2, cls.p3]
        cls.p_count = len(p_list)
        session.add_all(p_list)
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        places = session.query(TrPlace).all()
        map(session.delete, places)

        session.commit()

        session.close()


    def test_number_of_places_one(self):

        self.session.add(self.u1)

        data = server.getPlaces(self.u1.ID)

        self.assertIn(u'result', data)
        self.assertEquals(len(data['result']), 1)
        self.assertEquals(data['result'][0]['title'], 'Title1')

    def test_number_of_places_multiple(self):

        self.session.add(self.u2)

        data = server.getPlaces(self.u2.ID)

        self.assertIn(u'result', data)
        self.assertEquals(len(data['result']), 2)
        self.assertEquals(data['result'][0]['title'], u'Title2')
        self.assertEquals(data['result'][1]['title'], u'Заголовок3')

    def test_number_of_places_zero(self):

        self.session.add(self.u3)

        data = server.getPlaces(self.u3.ID)

        self.assertIn(u'result', data)
        self.assertEquals(len(data['result']), 0)


class PlaceAddTestCase(BaseTestCase):

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

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        places = session.query(TrPlace).all()
        map(session.delete, places)

        session.commit()

        session.close()


    def test_add_normal_place(self):

        self.session.add(self.u1)

        data = server.addPlace(self.u1.ID, "TestAddTitle", "77.7777", "11.1111", "cafe", "Description")

        self.assertIn(u'result', data)
        self.assertIs(isinstance(data['result']), False)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        ps = s.query(TrPlace).filter(TrPlace.user_id == self.u1.ID).all()
        self.assertEquals(len(ps), 1)
        self.assertEquals(ps[0].title, "TestAddTitle")
        s.close()

    def test_add_nonexistence_user(self):

        self.session.add(self.u1)

        data = server.addPlace(self.u1.ID + 1000, "TestAddTitle", "77.7777", "11.1111", "cafe", "Description")

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error'][u'message'], "ServerError: User doesn't exist.")

    def test_add_without_desc(self):

        self.session.add(self.u1)

        data = server.addPlace(self.u1.ID, "TestAddTitle", "77.7777", "11.1111", "cafe")

        self.assertIn(u'result', data)
        self.assertIs(data['result'], True)


class PlaceDeleteTestCase(BaseTestCase):

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

        cls.p1 = TrPlace(title="Title1", latitude=54.123, longitude=35.123, type="Restaurant", user_id=cls.u1.ID)
        cls.p2 = TrPlace(title="Title2", latitude=54.123, longitude=35.123, type="Parking", user_id=cls.u2.ID)
        cls.p3 = TrPlace(title=u'Заголовок3', latitude=54.123, longitude=35.123, type="Caffe", user_id=cls.u2.ID)

        p_list = [cls.p1, cls.p2, cls.p3]
        cls.p_count = len(p_list)
        session.add_all(p_list)
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        places = session.query(TrPlace).all()
        map(session.delete, places)

        session.commit()

        session.close()


    def test_delete_normal(self):

        self.session.add(self.u1)
        self.session.add(self.p1)

        data = server.delPlace(self.u1.ID, self.p1.id)

        self.assertJsonRpc(data)
        self.assertIs(data['result'], True)

    def test_delete_nonexistance_place(self):

        self.session.add(self.u2)
        self.session.add(self.p2)

        data = server.delPlace(self.u2.ID, self.p2.id + 1000)

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error'][u'message'], "ServerError: Place doesn't exist.")


class PlaceUpdateTestCase(BaseTestCase):

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

        cls.p1 = TrPlace(title="Title1", latitude=54.123, longitude=35.123, type="Restaurant", user_id=cls.u1.ID)
        cls.p2 = TrPlace(title="Title2", latitude=54.123, longitude=35.123, type="Parking", user_id=cls.u2.ID)
        cls.p3 = TrPlace(title=u'Заголовок3', latitude=54.123, longitude=35.123, type="Caffe", user_id=cls.u2.ID)

        p_list = [cls.p1, cls.p2, cls.p3]
        cls.p_count = len(p_list)
        session.add_all(p_list)
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        places = session.query(TrPlace).all()
        map(session.delete, places)

        session.commit()

        session.close()


    def test_update_place_title(self):

        self.session.add(self.u1)
        self.session.add(self.p1)

        data = server.updatePlace(self.u2.ID, self.p2.id + 1000)

        self.assertIn(u'result', data)
        self.assertIs(data['result'], True)

    # def test_update_place_latitude(self):
    # def test_update_place_longitude(self):
    # def test_update_place_type(self):


def suite():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(PlaceBaseTestCase))
    suite.addTests(loader.loadTestsFromTestCase(PlaceGetTestCase))
    suite.addTests(loader.loadTestsFromTestCase(PlaceAddTestCase))
    suite.addTests(loader.loadTestsFromTestCase(PlaceDeleteTestCase))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
