# -*- coding: utf-8 -*-
__author__ = 'Anton Glukhov'

import unittest
from base import BaseTestCase
from sqlautocode_gen.model import *
from sqlautocode_gen.avto_dggr_model import *
from tests.run import Session, server


def setUpModule():
    pass


def tearModuleDown():
    pass


class VehicleBaseTestCase(BaseTestCase):

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

        cls.v1 = TrVehicle("v1", cls.u1.ID, car_model_id=111, year=2000)
        cls.v2 = TrVehicle("v2", cls.u2.ID, car_model_id=222, year=2000)
        cls.v3 = TrVehicle("v3", cls.u2.ID, car_model_id=333, year=2000)
        v_list = [cls.v1, cls.v2, cls.v3]
        cls.v_count = len(v_list)
        session.add_all(v_list)
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


    def test_number_of_vehicles_zero(self):

        self.session.add_all([self.u1, self.u2, self.u3])

        data = server.getVehicles(self.u3.ID)

        self.assertIn(u'result', data)
        self.assertEquals(len(data['result']), 0)

    def test_number_of_vehicles_one(self):

        self.session.add_all([self.u1, self.u2, self.u3])

        data = server.getVehicles(self.u1.ID)

        self.assertIn(u'result', data)
        self.assertEquals(len(data['result']), 1)

    def test_number_of_vehicles_multi(self):

        self.session.add_all([self.u1, self.u2, self.u3])

        data = server.getVehicles(self.u2.ID)

        self.assertIn(u'result', data)
        self.assertEquals(len(data['result']), 2)

    def test_check_properties(self):

        self.session.add_all([self.u1, self.u2, self.u3])

        data = server.getVehicles(self.u1.ID)

        self.assertIn(u'jsonrpc', data)
        self.assertIn(u'result', data)

        self.assertEquals(len(data['result']), 1)

        self.assertEqual(data['result'][0][u'name'], u'v1')


class VehicleAddTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser("2013-12-12 12:12:12", "user_del", "testtest")
        session.add(cls.u1)
        session.flush()
        session.refresh(cls.u1)
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


    def test_add_new_vehicle(self):

        self.session.add(self.u1)

        data = server.addVehicle(self.u1.ID, "Test", "A", "BMW", u'3 серия', u'E30 [рестайлинг] Touring универсал', "316i AT", 1992)

        self.assertJsonRpc(data)
        self.assertIs(type(data['result']), int)
        id = data['result']

        s = Session()
        v = s.query(TrVehicle).get(id)
        self.assertEquals(v.name, u'Test')
        self.assertEquals(v.year, 1992)
        s.close()

    def test_add_new_vehicle_cyrillic_name(self):

        self.session.add(self.u1)

        data = server.addVehicle(self.u1.ID, "Машина", "A", "BMW", u'3 серия', u'E30 [рестайлинг] Touring универсал', "316i AT", 1992)

        self.assertJsonRpc(data)
        self.assertIs(type(data['result']), int)
        id = data['result']

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        v = s.query(TrVehicle).get(id)
        self.assertEquals(v.name, u'Машина')
        s.close()


class VehicleAddSTSTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser("2013-12-12 12:12:12", "user1", "testtest")
        session.add(cls.u1)
        session.flush()
        session.refresh(cls.u1)
        session.commit()

        cls.v1 = TrVehicle("v1", cls.u1.ID, car_model_id=111, year=2000)
        v_list = [cls.v1]
        cls.v_count = len(v_list)
        session.add_all(v_list)
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


    def test_add_sts_to_vehicle(self):

        self.session.add(self.u1)
        self.session.add(self.v1)

        self.assertIsNone(self.v1.car_sts)
        self.assertIsNone(self.v1.car_number)

        data = server.addSTS(self.u1.ID, self.v1.id, "321232", "А123СТ")

        self.assertJsonRpc(data)
        self.assertIs(data['result'], True)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        v = s.query(TrVehicle).get(self.v1.id)
        self.assertIsNotNone(v)
        self.assertEquals(v.id, self.v1.id)
        self.assertEquals(v.car_sts, u'321232')
        self.assertEquals(v.car_number, u'А123СТ')
        s.close()


    def test_add_sts_nonexistence_vehicle(self):
        pass


class VehicleDeleteSTSTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser("2013-12-12 12:12:12", "user1", "testtest")
        session.add(cls.u1)
        session.flush()
        session.refresh(cls.u1)
        session.commit()

        cls.v1 = TrVehicle("v1", cls.u1.ID, car_model_id=111, year=2000)
        v_list = [cls.v1]
        cls.v_count = len(v_list)
        session.add_all(v_list)
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


    def test_del_sts_from_vehicle(self):

        self.session.add(self.u1)
        self.session.add(self.v1)

        data = server.addSTS(self.u1.ID, self.v1.id, "111222", "Ф666МИ")

        self.assertJsonRpc(data)
        self.assertIs(data['result'], True)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        v = s.query(TrVehicle).get(self.v1.id)
        self.assertIsNotNone(v)
        self.assertEquals(v.id, self.v1.id)
        self.assertEquals(v.car_sts, u'111222')
        self.assertEquals(v.car_number, u'Ф666МИ')
        s.close()

        data = server.delSTS(self.u1.ID, self.v1.id)

        self.assertJsonRpc(data)
        self.assertIs(data['result'], True)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        v = s.query(TrVehicle).get(self.v1.id)
        self.assertIsNotNone(v)
        self.assertEquals(v.id, self.v1.id)
        self.assertIsNone(v.car_sts)
        self.assertIsNone(v.car_number)
        s.close()


class VehicleDeleteTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser("2013-12-12 12:12:12", "user_del", "testtest")
        session.add(cls.u1)
        session.flush()
        session.refresh(cls.u1)
        session.commit()

        cls.v1 = TrVehicle("v1", cls.u1.ID, car_model_id=111, year=2000)
        cls.v2 = TrVehicle("v2", cls.u1.ID, car_model_id=111, year=2000)
        v_list_del = [cls.v1, cls.v2]
        session.add_all(v_list_del)
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


    def test_delete_vehicle(self):

        self.session.add(self.u1)

        data = server.getVehicles(self.u1.ID)

        self.assertIn(u'result', data)
        self.assertEquals(len(data['result']), 2)

        data = server.delVehicle(self.u1.ID, self.u1.vehicles[0].id)

        self.assertJsonRpc(data)
        self.assertIs(data['result'], True)

        data = server.getVehicles(self.u1.ID)

        self.assertJsonRpc(data)
        self.assertEquals(len(data['result']), 1)

    def test_delete_nonexistent_vehicle(self):

        self.session.add(self.u1)

        data = server.delVehicle(self.u1.ID, self.u1.vehicles[0].id + 1000)

        self.assertIn(u'error', data)
        self.assertEquals(data['error'][u'message'], "ServerError: Vehicle doesn't exist.")


class VehicleUpdateTestCase(BaseTestCase):

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

        cls.v1 = TrVehicle("v1", cls.u1.ID, car_model_id=111, year=1989)
        cls.v2 = TrVehicle("v2", cls.u1.ID, car_model_id=222, year=1980)
        cls.v3 = TrVehicle("v3", cls.u1.ID, car_model_id=333, year=1980)
        v_list = [cls.v1, cls.v2, cls.v3]
        cls.v_count = len(v_list)
        session.add_all(v_list)
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


    def test_update_vehicle_name(self):

        self.session.add(self.u1)
        self.session.add(self.v1)

        data = server.updateVehicle(user_id=self.u1.ID, id=self.v1.id, name="new_name",
                                    maker="Alfa Romeo", model="164", generation="1 поколение седан",
                                    modification="2.0 MT", year=1989) # car_model_id = 111

        self.assertJsonRpc(data)
        self.assertIs(data['result'], True)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        v = s.query(TrVehicle).get(self.v1.id)
        self.assertIsNotNone(v)
        self.assertEquals(v.name, u'new_name')
        self.assertEquals(v.year, 1989)
        self.assertEquals(v.car_model_id, 111)
        s.close()


    def test_update_vehicle_name_and_model(self):

        self.session.add(self.u1)
        self.session.add(self.v2)

        data = server.updateVehicle(user_id=self.u1.ID, id=self.v2.id, name="new_name",
                                    maker="AC", model="Cobra", generation="1 поколение родстер",
                                    modification="4.9 MT", year=2000) # car_model_id = 8

        self.assertJsonRpc(data)
        self.assertIs(data['result'], True)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        v = s.query(TrVehicle).get(self.v2.id)
        self.assertIsNotNone(v)
        self.assertEquals(v.name, u'new_name')
        self.assertEquals(v.year, 2000)
        self.assertEquals(v.car_model_id, 4)
        s.close()


    def test_update_vehicle_name_with_incorrect_model_year(self):

        self.session.add(self.u1)
        self.session.add(self.v3)

        data = server.updateVehicle(user_id=self.u1.ID, id=self.v3.id, name="new_name",
                                    maker="AC", model="Cobra", generation="1 поколение родстер",
                                    modification="4.9 MT", year=1985)

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error'][u'message'], "ServerError: Incorrect vehicle params.")

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        v = s.query(TrVehicle).get(self.v3.id)
        self.assertIsNotNone(v)
        self.assertEquals(v.name, u'v3')
        self.assertEquals(v.car_model_id, 333)
        s.close()


def suite():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(VehicleBaseTestCase))
    suite.addTests(loader.loadTestsFromTestCase(VehicleAddTestCase))
    suite.addTests(loader.loadTestsFromTestCase(VehicleDeleteTestCase))
    suite.addTests(loader.loadTestsFromTestCase(VehicleUpdateTestCase))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')