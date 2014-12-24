__author__ = 'Anton Glukhov'

import unittest
from base import BaseTestCase
from sqlautocode_gen.model import *
from sqlautocode_gen.tbl_02_models import *
from tests.run import Session, server


def setUpModule():
    pass


def tearModuleDown():
    pass


class HelpBaseTestCase(BaseTestCase):

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

        cls.v1 = TrVehicle("v1", cls.u1.ID, car_model_id=111)
        cls.v2 = TrVehicle("v2", cls.u1.ID, car_model_id=222)
        v_list = [cls.v1, cls.v2]
        cls.v_count = len(v_list)
        session.add_all(v_list)
        session.commit()

        cls.m1 = TrHelp("Message1", "54.55,55.123", cls.v1.id)
        message_list = [cls.m1]
        cls.message_count = len(message_list)
        session.add_all(message_list)
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


    def test_relations_device_help(self):

        self.session.add_all([self.v1, self.v2])

        self.assertIsNotNone(self.v1.help)
        self.assertIsNone(self.v2.help)

    def test_cascade_delete_device_help(self):

        self.session.add(self.u1)
        self.session.add_all([self.v1, self.v2])

        v3 = TrVehicle("v3", self.u1.ID, car_model_id=333)
        self.session.add(v3)
        self.session.commit()

        m3 = TrHelp("Message_for_delete", "54.55,55.123", v3.id)
        self.session.add(m3)
        self.session.commit()

        self.assertIsNotNone(v3.help)

        message = v3.help.id

        self.session.delete(v3)
        self.session.commit()

        m = self.session.query(TrHelp).get(message)
        self.assertIsNone(m)


class HelpGetTestCase(BaseTestCase):

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

        cls.v1 = TrVehicle("v1", cls.u1.ID, car_model_id=111)
        cls.v2 = TrVehicle("v2", cls.u1.ID, car_model_id=222)
        v_list = [cls.v1, cls.v2]
        cls.v_count = len(v_list)
        session.add_all(v_list)
        session.commit()

        session.close()

        # cls.m1 = TrHelp("Message1", "54.55,55.123", "2013-12-12 12:12:12", cls.d1.device_ID)
        # cls.m2 = TrHelp("Message2", "51.123,33.566", "2014-01-01 02:10:10", cls.d1.device_ID)
        # message_list = [cls.m1, cls.m2]
        # cls.message_count = len(message_list)
        # cls.session.add_all(message_list)
        # cls.session.commit()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        for user in users:
            session.delete(user)
        session.commit()

        session.close()

    def test_get_helps(self):

        self.session.add(self.u1)
        self.session.add_all([self.v1, self.v2])

        data = server.getHelps(user_id=self.u1.ID, vehicle_id=self.v1.id, lat_log="54.123,55.123")

        self.assertJsonRpc(data)
        self.assertEquals(data['result'][0][u'message'], "Hey")

    def test_get_zero(self):

        self.session.add(self.u1)
        self.session.add_all([self.v1, self.v2])

        # TODO:: wrong location: too far away, etc.
        data = server.getHelps(user_id=self.u1.ID, vehicle_id=self.v1.id, lat_log="51.123,58.123")

        self.assertJsonRpc(data)
        self.assertEquals(data['result'][0][u'message'], "Hey")


class HelpAddTestCase(BaseTestCase):

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

        cls.v1 = TrVehicle("v1", cls.u1.ID, car_model_id=111)
        cls.v2 = TrVehicle("v2", cls.u1.ID, car_model_id=222)
        v_list = [cls.v1, cls.v2]
        cls.v_count = len(v_list)
        session.add_all(v_list)
        session.commit()

        session.close()

        # cls.m1 = TrHelp("Message1", "54.55,55.123", "2013-12-12 12:12:12", cls.d1.device_ID)
        # cls.m2 = TrHelp("Message2", "51.123,33.566", "2014-01-01 02:10:10", cls.d1.device_ID)
        # message_list = [cls.m1, cls.m2]
        # cls.message_count = len(message_list)
        # cls.session.add_all(message_list)
        # cls.session.commit()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        for user in users:
            session.delete(user)
        session.commit()

        session.close()


    def test_add_normal(self):

        self.session.add(self.u1)
        self.session.add_all([self.v1, self.v2])

        data = server.addHelp(user_id=self.u1.ID, vehicle_id=self.v2.id, message="Test1", lat_log="54.123,55.123", phone="+79266242473")

        self.assertJsonRpc(data)
        self.assertEquals(data['result'], True)

#     @unittest.skip("skip overwrite.")
#     def test_add_overwrite(self):
#
#         data = server.getHelps(user_id=self.u1.ID, device_id=self.d1.device_ID, lat_log="54.123,55.123")
#
#         self.assertJsonRpc(data)
#         self.assertEquals(data['result'][0][u'message'], "Hey")


def suite():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(HelpBaseTestCase))
    # suite.addTests(loader.loadTestsFromTestCase(HelpGetTestCase))
    # suite.addTests(loader.loadTestsFromTestCase(HelpAddTestCase))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')