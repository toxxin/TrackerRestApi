__author__ = 'Anton Glukhov'

import unittest
from base import BaseTestCase
from sqlautocode_gen.model import *
from tests.run import Session, server


def setUpModule():
    pass


def tearModuleDown():
    pass


class DGeoBaseTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser("2013-12-12 12:12:12", "u1", "testtest")
        user_list = [cls.u1]
        cls.user_count = len(user_list)
        session.add_all(user_list)
        session.flush()
        session.refresh(cls.u1)
        session.commit()

        cls.d1 = TrDevice("d1", cls.u1.ID)
        cls.d2 = TrDevice("d2", cls.u1.ID)
        cls.d3 = TrDevice("d3", cls.u1.ID)
        device_list = [cls.d1, cls.d2, cls.d3]
        cls.device_count = len(device_list)
        session.add_all(device_list)
        session.commit()

        cls.g1 = TrDGeozone("g1", cls.d1.device_ID)
        cls.g2 = TrDGeozone("g2", cls.d2.device_ID)
        cls.g3 = TrDGeozone("g3", cls.d2.device_ID)
        geo_list = [cls.g1, cls.g2, cls.g3]
        cls.device_count = len(geo_list)
        session.add_all(geo_list)
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        for user in users:
            session.delete(user)
        session.commit()

        session.close()


    def test_relations_device_geo(self):

        self.session.add_all([self.d1, self.d2, self.d3])
        self.session.add_all([self.g1, self.g2, self.g3])

        self.assertEquals(len(self.d1.geos), 1)
        self.assertEquals(self.d1.geos[0].name, "g1")

        self.assertEquals(len(self.d2.geos), 2)
        self.assertEquals(self.d2.geos[0].name, "g2")
        self.assertEquals(self.d2.geos[1].name, "g3")

        self.assertEquals(len(self.d3.geos), 0)

    def test_cascade_delete_device_geo(self):

        self.session.add(self.u1)

        d4 = TrDevice("d4", self.u1.ID)
        self.session.add(d4)
        self.session.commit()
        g4 = TrDGeozone("g4", d4.device_ID)
        self.session.add(g4)
        self.session.commit()

        self.assertEquals(len(d4.geos), 1)

        geo_id = d4.geos[0].id

        self.session.delete(d4)
        self.session.commit()

        geo = self.session.query(TrDGeozone).get(geo_id)
        self.assertIsNone(geo)


class DGeoGetTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser("2013-12-12 12:12:12", "u1", "testtest")
        user_list = [cls.u1]
        cls.user_count = len(user_list)
        session.add_all(user_list)
        session.flush()
        session.refresh(cls.u1)
        session.commit()

        cls.d1 = TrDevice("d1", cls.u1.ID)
        cls.d2 = TrDevice("d2", cls.u1.ID)
        cls.d3 = TrDevice("d3", cls.u1.ID)
        device_list = [cls.d1, cls.d2, cls.d3]
        cls.device_count = len(device_list)
        session.add_all(device_list)
        session.commit()

        cls.g1 = TrDGeozone("g1", cls.d1.device_ID)
        cls.g2 = TrDGeozone("g2", cls.d2.device_ID)
        cls.g3 = TrDGeozone("g3", cls.d2.device_ID)
        geo_list = [cls.g1, cls.g2, cls.g3]
        cls.device_count = len(geo_list)
        session.add_all(geo_list)
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        for user in users:
            session.delete(user)
        session.commit()

        session.close()


    def test_get_geos_zero(self):

        self.session.add(self.u1)
        self.session.add_all([self.d1, self.d2, self.d3])
        self.session.add_all([self.g1, self.g2, self.g3])

        data = server.getDGeos(user_id=self.u1.ID, device_id=self.d3.device_ID)

        self.assertJsonRpc(data)
        self.assertEqual(len(data['result']), 0)

    def test_get_geos_one(self):

        self.session.add(self.u1)
        self.session.add_all([self.d1, self.d2, self.d3])
        self.session.add_all([self.g1, self.g2, self.g3])

        data = server.getDGeos(user_id=self.u1.ID, device_id=self.d1.device_ID)

        self.assertJsonRpc(data)
        self.assertEqual(len(data['result']), 1)
        self.assertEqual(data['result'][0][u'name'], u'g1')

    def test_get_geos_multi(self):

        self.session.add(self.u1)
        self.session.add_all([self.d1, self.d2, self.d3])
        self.session.add_all([self.g1, self.g2, self.g3])

        data = server.getDGeos(user_id=self.u1.ID, device_id=self.d2.device_ID)

        self.assertJsonRpc(data)
        self.assertEqual(len(data['result']), 2)
        self.assertEqual(data['result'][0][u'name'], u'g2')
        self.assertEqual(data['result'][1][u'name'], u'g3')


class DGeoAddTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser("2013-12-12 12:12:12", "u1", "testtest")
        user_list = [cls.u1]
        cls.user_count = len(user_list)
        session.add_all(user_list)
        session.flush()
        session.refresh(cls.u1)
        session.commit()

        cls.d1 = TrDevice("d1", cls.u1.ID)
        device_list = [cls.d1]
        device_count = len(device_list)
        session.add_all(device_list)
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        session = Session()
        users = session.query(TrUser).all()
        for user in users:
            session.delete(user)
        session.commit()

        session.close()


    def test_add_new_geo(self):

        self.session.add(self.u1)
        self.session.add(self.d1)

        data = server.addDGeo(user_id=self.u1.ID, device_id=self.d1.device_ID,
                              name="New test geo", shape=0, center="54.123,55.123", radius=100)

        self.assertJsonRpc(data)
        self.assertIs(data['result'], True)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        d = s.query(TrDevice).get(self.d1.device_ID)

        self.assertEquals(len(d.geos), 1)
        self.assertEquals(d.geos[0].name, u'New test geo')
        self.assertEquals(d.geos[0].shape, 0)
        self.assertEquals(d.geos[0].center, u'54.123,55.123')
        self.assertEquals(d.geos[0].radius, 100)
        self.assertEquals(d.geos[0].state, True)

        s.close()

    def test_add_not_enough_params_user_id(self):

        self.session.add(self.d1)

        data = server.addDGeo(device_id=self.d1.device_ID, alias="New device")
        self.assertJsonRpcErr(data)
        self.assertEquals(data['error']['message'], u'InvalidParamsError: user_id or device_id is not specified.')

    def test_add_not_enough_params_device_id(self):

        data = server.addDGeo(user_id=self.u1.ID, alias="New device")
        self.assertJsonRpcErr(data)
        self.assertEquals(data['error']['message'], u'InvalidParamsError: user_id or device_id is not specified.')

    def test_add_not_mandatory_params(self):

        data = server.addDGeo(user_id=self.u1.ID, device_id=self.d1.device_ID, color="#FF00FF")
        self.assertJsonRpcErr(data)
        self.assertEquals(data['error']['message'], u'InvalidParamsError: Incorrect mandatory parameters.')

    def test_add_wrong_params(self):

        data = server.addDGeo(user_id=self.u1.ID, device_id=self.d1.device_ID, abc="#FF00FF")
        self.assertJsonRpcErr(data)
        self.assertEquals(data['error']['message'], u'InvalidParamsError: Incorrect parameters.')

    def test_add_user_does_not_exist(self):

        data = server.addDGeo(user_id=self.u1.ID + 1000, device_id=self.d1.device_ID, abc="#FF00FF")
        self.assertJsonRpcErr(data)
        self.assertEquals(data['error']['message'], u'ServerError: Incorrect user or device.')

    def test_add_device_does_not_exist(self):

        self.session.add(self.u1)
        self.session.add(self.d1)

        data = server.addDGeo(user_id=self.u1.ID, device_id=self.d1.device_ID + 1000, abc="#FF00FF")
        self.assertJsonRpcErr(data)
        self.assertEquals(data['error']['message'], u'ServerError: Incorrect user or device.')


class DGeoDeleteTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        cls.session = Session()

        cls.u1 = TrUser("2013-12-12 12:12:12", "u1", "testtest")
        cls.u2 = TrUser("2013-12-12 12:12:12", "u2", "testtest1")
        user_list = [cls.u1, cls.u2]
        cls.user_count = len(user_list)
        cls.session.add_all(user_list)
        cls.session.flush()
        cls.session.refresh(cls.u1)
        cls.session.refresh(cls.u2)
        cls.session.commit()

        cls.d1 = TrDevice("d1", cls.u1.ID)
        cls.d2 = TrDevice("d2", cls.u2.ID)
        device_list = [cls.d1, cls.d2]
        cls.device_count = len(device_list)
        cls.session.add_all(device_list)
        cls.session.commit()

        cls.g1 = TrDGeozone("g1", cls.d1.device_ID)
        cls.g2 = TrDGeozone("g2", cls.d2.device_ID)
        geo_list = [cls.g1, cls.g2]
        cls.geo_count = len(geo_list)
        cls.session.add_all(geo_list)
        cls.session.commit()

    @classmethod
    def tearDownClass(cls):

        users = cls.session.query(TrUser).all()
        for user in users:
            cls.session.delete(user)
        cls.session.commit()

        cls.session.close()

    def test_delete_geo(self):

        data = server.delDGeo(user_id=self.u1.ID, id=self.d1.geos[0].id)
        gid = self.d1.geos[0].id
        self.assertJsonRpc(data)
        self.assertEquals(data['result'], True)

        s = Session()
        d = s.query(TrDevice).get(self.d1.device_ID)
        self.assertEqual(len(d.geos), 0)

    def test_delete_inexistent_geo(self):

        data = server.delDGeo(user_id=self.u1.ID, id=self.d1.geos[0].id + 1000)

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error']['message'], u'ServerError: Geozone doesn\'t exist.')

    def test_delete_doesnt_belong_geo(self):

        data = server.delDGeo(user_id=self.u1.ID, id=self.d2.geos[0].id)

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error']['message'], u'ServerError: Geozone doesn\'t exist.')


class DGeoUpdateTestcase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser("2013-12-12 12:12:12", "u1", "testtest")
        cls.u2 = TrUser("2013-12-12 12:12:12", "u2", "testtest1")
        user_list = [cls.u1, cls.u2]
        cls.user_count = len(user_list)
        session.add_all(user_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.commit()

        cls.d1 = TrDevice("d1", cls.u1.ID)
        cls.d2 = TrDevice("d2", cls.u2.ID)
        device_list = [cls.d1, cls.d2]
        cls.device_count = len(device_list)
        session.add_all(device_list)
        session.commit()

        cls.g1 = TrDGeozone("g1", cls.d1.device_ID)
        cls.g2 = TrDGeozone("g2", cls.d2.device_ID)
        geo_list = [cls.g1, cls.g2]
        cls.geo_count = len(geo_list)
        session.add_all(geo_list)
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        for user in users:
            session.delete(user)
        session.commit()

        session.close()


    def test_update_geo_name(self):

        self.session.add_all([self.u1, self.u2])
        self.session.add_all([self.d1, self.d2])

        data = server.updateDGeo(user_id=self.u1.ID, id=self.d1.geos[0].id, name="Updated name.")

        self.assertJsonRpc(data)
        self.assertEquals(data['result'], True)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        g = s.query(TrDGeozone).get(self.d1.geos[0].id)
        self.assertEquals(g.name, u'Updated name.')
        s.close()

    def test_update_geo_radius(self):

        self.session.add_all([self.u1, self.u2])
        self.session.add_all([self.d1, self.d2])

        data = server.updateDGeo(user_id=self.u1.ID, id=self.d1.geos[0].id, radius=11)

        self.assertJsonRpc(data)
        self.assertEquals(data['result'], True)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        g = s.query(TrDGeozone).get(self.d1.geos[0].id)
        self.assertEquals(g.radius, 11)
        s.close()

    def test_update_geo_state(self):

        self.session.add_all([self.u1, self.u2])
        self.session.add_all([self.d1, self.d2])

        data = server.updateDGeo(user_id=self.u1.ID, id=self.d1.geos[0].id, state=False)

        self.assertJsonRpc(data)
        self.assertEquals(data['result'], True)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        g = s.query(TrDGeozone).get(self.d1.geos[0].id)
        self.assertEquals(g.state, False)
        s.close()

    def test_inexistent_geo(self):

        self.session.add_all([self.u1, self.u2])
        self.session.add_all([self.d1, self.d2])

        data = server.updateDGeo(user_id=self.u1.ID, id=self.d1.geos[0].id + 1000, name="Test")

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error']['message'], u'ServerError: Geozone doesn\'t exist.')

    def test_delete_doesnt_belong_geo(self):

        self.session.add_all([self.u1, self.u2])
        self.session.add_all([self.d1, self.d2])

        data = server.updateDGeo(user_id=self.u1.ID, id=self.d2.geos[0].id, name="Test")

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error']['message'], u'ServerError: Geozone doesn\'t exist.')

    @unittest.skip("Update geo empty value.")
    def test_update_geo_empty_value(self):
        pass

    @unittest.skip("Update geo incorrect value.")
    def test_update_geo_incorrect_value(self):
        pass


def suite():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(DGeoBaseTestCase))
    suite.addTests(loader.loadTestsFromTestCase(DGeoGetTestCase))
    suite.addTests(loader.loadTestsFromTestCase(DGeoAddTestCase))
    suite.addTests(loader.loadTestsFromTestCase(DGeoDeleteTestCase))
    suite.addTests(loader.loadTestsFromTestCase(DGeoUpdateTestcase))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')