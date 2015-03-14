# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

import unittest
from base import BaseTestCase
from sqlautocode_gen.model import TrUser, TrVehicle, TrDevice
from sqlautocode_gen.place_model import TrPlace
from sqlautocode_gen.avto_dggr_model import TrAvtoDGGR
from tests.run import Session, server


def setUpModule():
    pass


def tearModuleDown():
    pass


class DeviceBaseTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser(login="11111", auth_code="1111", authenticated=True)
        cls.u2 = TrUser(login="22222", auth_code="2222", authenticated=True)
        cls.u3 = TrUser(login="33333", auth_code="3333", authenticated=True)
        u_list = [cls.u1, cls.u2, cls.u3]
        cls.user_count = len(u_list)
        session.add_all(u_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.commit()

        cls.v1 = TrVehicle("v1", cls.u1.id, car_model_id=111, year=1991)
        cls.v2 = TrVehicle("v2", cls.u2.id, car_model_id=111, year=1991)
        cls.v3 = TrVehicle("v3", cls.u2.id, car_model_id=111, year=1991)
        v_list = [cls.v1, cls.v2, cls.v3]
        cls.v_count = len(v_list)
        session.add_all(v_list)
        session.commit()

        cls.d1 = TrDevice(sn='EW-14100001-UT', imei_number='1234', accel_stat=True, time_interval=1, phone1="+79260000001", vehicle_id=cls.v1.id)
        cls.d2 = TrDevice(sn='EW-14100002-UT', imei_number='5678', accel_stat=True, time_interval=2, phone1="+79260000002", vehicle_id=cls.v2.id)
        cls.d3 = TrDevice(sn='EW-14100003-UT', imei_number='9012', accel_stat=True, time_interval=3, phone1="+79260000003", vehicle_id=None)
        cls.d4 = TrDevice(sn='EW-14100004-UT', imei_number='3456', accel_stat=True, time_interval=4, phone1="+79260000003", vehicle_id=None)
        d_list = [cls.d1, cls.d2, cls.d3, cls.d4]
        cls.device_count = len(d_list)
        session.add_all(d_list)
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        for user in users:
            session.delete(user)
        session.commit()

        devices = session.query(TrDevice).all()
        for d in devices:
            session.delete(d)
        session.commit()

        session.close()

    def test_relations_vehicle_device(self):

        self.session.add(self.u1)
        self.session.add(self.d1)

        self.assertEquals(len(self.u1.vehicles), 1)
        self.assertEquals(self.u1.vehicles[0].device.id, self.d1.id)

    def test_number_of_devices_zero(self):

        self.session.add(self.u3)

        self.assertEquals(len(self.u3.vehicles), 0)

        # data = server.getDevices(self.u3.id)
        #
        # self.assertIn(u'result', data)
        # self.assertEquals(len(data['result']), 0)

    def test_number_of_devices_one(self):

        self.session.add(self.u1)
        self.session.add(self.d1)

        self.assertEquals(len(self.u1.vehicles), 1)
        self.assertEquals(self.u1.vehicles[0].device.id, self.d1.id)

    def test_number_of_devices_multi(self):
        """add test as adding second device for v2 and catch exception."""
        pass

    def test_check_properties(self):

        self.session.add(self.u1)

        data = server.getDevices(self.u1.id)

        self.assertIn(u'jsonrpc', data)
        self.assertIn(u'result', data)

        self.assertEquals(len(data['result']), 1)

        self.assertEqual(data['result'][0][u'time_interval'], 1)
        self.assertEqual(data['result'][0][u'accel_stat'], True)
        self.assertEqual(data['result'][0][u'sn'], "EW-14100001-UT")


class DeviceGetTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser(login="11111", auth_code="1111", authenticated=True)
        cls.u2 = TrUser(login="22222", auth_code="2222", authenticated=True)
        cls.u3 = TrUser(login="33333", auth_code="3333", authenticated=True)
        u_list = [cls.u1, cls.u2, cls.u3]
        cls.user_count = len(u_list)
        session.add_all(u_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.commit()

        cls.v1 = TrVehicle("v1", cls.u1.id, car_model_id=111, year=2000)
        cls.v2 = TrVehicle("v2", cls.u2.id, car_model_id=111, year=2000)
        cls.v3 = TrVehicle("v3", cls.u2.id, car_model_id=111, year=2000)
        v_list = [cls.v1, cls.v2, cls.v3]
        cls.v_count = len(v_list)
        session.add_all(v_list)
        session.commit()

        cls.d1 = TrDevice(sn='EW-14100001-UT', imei_number='1111', accel_stat=True, time_interval=1, phone1="+79260000001", vehicle_id=cls.v1.id)
        cls.d2 = TrDevice(sn='EW-14100002-UT', imei_number='2222', accel_stat=True, time_interval=2, phone1="+79260000002", vehicle_id=cls.v2.id)
        cls.d3 = TrDevice(sn='EW-14100003-UT', imei_number='3333', accel_stat=True, time_interval=3, phone1="+79260000003", vehicle_id=None)
        cls.d4 = TrDevice(sn='EW-14100004-UT', imei_number='4444', accel_stat=True, time_interval=4, phone1="+79260000003", vehicle_id=None)
        d_list = [cls.d1, cls.d2, cls.d3, cls.d4]
        cls.device_count = len(d_list)
        session.add_all(d_list)
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        for user in users:
            session.delete(user)
        session.commit()

        devices = session.query(TrDevice).all()
        for d in devices:
            session.delete(d)
        session.commit()

        session.close()


    def test_number_of_devices_one(self):

        self.session.add(self.u1)

        data = server.getDevices(self.u1.id)

        self.assertIn(u'result', data)
        self.assertEquals(len(data['result']), 1)
        self.assertEquals(data['result'][0]['sn'], 'EW-14100001-UT')

    def test_number_of_devices_zero(self):

        self.session.add(self.u3)

        data = server.getDevices(self.u3.id)

        self.assertIn(u'result', data)
        self.assertEquals(len(data['result']), 0)


class DeviceDeleteTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser(login="11111", auth_code="1111", authenticated=True)
        cls.u2 = TrUser(login="22222", auth_code="2222", authenticated=True)
        cls.u3 = TrUser(login="33333", auth_code="3333", authenticated=True)
        u_list = [cls.u1, cls.u2, cls.u3]
        cls.user_count = len(u_list)
        session.add_all(u_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.commit()

        cls.v1 = TrVehicle("v1", cls.u1.id, car_model_id=111, year=2000)
        cls.v2 = TrVehicle("v2", cls.u2.id, car_model_id=111, year=2000)
        cls.v3 = TrVehicle("v3", cls.u2.id, car_model_id=111, year=2000)
        v_list = [cls.v1, cls.v2, cls.v3]
        cls.v_count = len(v_list)
        session.add_all(v_list)
        session.commit()

        cls.d1 = TrDevice(sn='EW-14100001-UT', imei_number='1111', accel_stat=True, time_interval=1, phone1="+79260000001", vehicle_id=cls.v1.id)
        cls.d2 = TrDevice(sn='EW-14100002-UT', stat=True, imei_number='2222', accel_stat=True, time_interval=2, phone1="+79260000002", vehicle_id=cls.v2.id)
        cls.d3 = TrDevice(sn='EW-14100003-UT', imei_number='3333', accel_stat=True, time_interval=3, phone1="+79260000003", vehicle_id=None)
        cls.d4 = TrDevice(sn='EW-14100004-UT', imei_number='4444', accel_stat=True, time_interval=4, phone1="+79260000003", vehicle_id=None)
        d_list = [cls.d1, cls.d2, cls.d3, cls.d4]
        cls.device_count = len(d_list)
        session.add_all(d_list)
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        for user in users:
            session.delete(user)
        session.commit()

        devices = session.query(TrDevice).all()
        for d in devices:
            session.delete(d)
        session.commit()

        session.close()


    def test_delete_normal(self):

        self.session.add(self.u1)
        self.session.add(self.v1)
        self.session.add(self.d1)

        data = server.delDevice(self.u1.id, self.d1.id)

        self.assertJsonRpc(data)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        v = s.query(TrVehicle).get(self.v1.id)
        self.assertIsNotNone(v)
        self.assertIsNone(v.device)
        s.close()

    def test_delete_nonexistent_device(self):

        self.session.add(self.u1)
        self.session.add(self.d1)

        data = server.delDevice(self.u1.id, self.d1.id + 1000)

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error'][u'message'], "ServerError: Device doesn't exist.")

    def test_delete_vehicle(self):

        self.session.add(self.u2)
        self.session.add(self.v2)
        self.session.add(self.d2)

        data = server.delVehicle(self.u2.id, self.v2.id)

        self.assertJsonRpc(data)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        d = s.query(TrDevice).get(self.d2.id)
        self.assertIsNotNone(d)
        self.assertEquals(d.id, self.d2.id)
        self.assertEquals(d.sn, 'EW-14100002-UT')
        self.assertEquals(d.stat, False)
        s.close()

class DeviceAddTestCase(BaseTestCase):

    @unittest.skip("Add new device.")
    def test_add_new_device(self):
        pass


class DeviceRegistrationTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        """
        x - x - d1
        u1 - v1 - x
            "Ok"

        x - x - d3
        u2 - v2 - d2
            "Vehicle already has device"

        u3 - v3 - d2
            "Device already in use"
        """

        session = Session()

        cls.u1 = TrUser(login="11111", auth_code="1111", authenticated=True)
        cls.u2 = TrUser(login="22222", auth_code="2222", authenticated=True)
        cls.u3 = TrUser(login="33333", auth_code="3333", authenticated=True)
        u_list = [cls.u1, cls.u2, cls.u3]
        cls.user_count = len(u_list)
        session.add_all(u_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.refresh(cls.u3)
        session.commit()

        cls.v1 = TrVehicle("v1", cls.u1.id, car_model_id=111, year=2000)
        cls.v2 = TrVehicle("v2", cls.u2.id, car_model_id=111, year=2000)
        cls.v3 = TrVehicle("v3", cls.u3.id, car_model_id=111, year=2000)
        v_list = [cls.v1, cls.v2, cls.v3]
        cls.v_count = len(v_list)
        session.add_all(v_list)
        session.commit()

        cls.d1 = TrDevice(sn='EW-14100001-UT', secter_code='sec1', imei_number='1111', accel_stat=True, time_interval=1, phone1="+79260000001", vehicle_id=None)
        cls.d2 = TrDevice(sn='EW-14100002-UT', secter_code='sec2', stat=True, imei_number='2222', accel_stat=True, time_interval=2, phone1="+79260000002", vehicle_id=cls.v2.id)
        cls.d3 = TrDevice(sn='EW-14100003-UT', secter_code='sec3', imei_number='3333', accel_stat=True, time_interval=3, phone1="+79260000003", vehicle_id=None)
        d_list = [cls.d1, cls.d2, cls.d3]
        cls.device_count = len(d_list)
        session.add_all(d_list)
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        for user in users:
            session.delete(user)
        session.commit()

        devices = session.query(TrDevice).all()
        for d in devices:
            session.delete(d)
        session.commit()

        session.close()


    def test_reg_normal_device(self):

        self.session.add(self.u1)
        self.session.add(self.v1)
        self.session.add(self.d1)

        data = server.regDevice(user_id=self.u1.id, vehicle_id=self.v1.id, sn='EW-14100001-UT', secret_code='sec1')

        self.assertJsonRpc(data)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        v = s.query(TrVehicle).get(self.v1.id)
        self.assertIsNotNone(v)
        self.assertEquals(v.id, self.v1.id)
        self.assertIsNotNone(v.device)
        self.assertEquals(v.device.id, self.d1.id)
        self.assertEquals(v.device.sn, 'EW-14100001-UT')
        self.assertEquals(v.device.stat, True)
        s.close()

    def test_reg_one_more_device_to_vehicle(self):

        self.session.add(self.u2)
        self.session.add(self.v2)
        self.session.add(self.d2)
        self.session.add(self.d3)

        data = server.regDevice(user_id=self.u2.id, vehicle_id=self.v2.id, sn='EW-14100003-UT', secret_code='sec3')

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error'][u'message'], "ServerError: Vehicle already has device.")

    def test_reg_device_which_already_in_use(self):

        self.session.add(self.u3)
        self.session.add(self.v3)
        self.session.add(self.d2)

        data = server.regDevice(user_id=self.u3.id, vehicle_id=self.v3.id, sn='EW-14100002-UT', secret_code='sec2')

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error'][u'message'], "ServerError: Device is already in use.")

    def test_reg_same_device(self):

        self.session.add(self.u2)
        self.session.add(self.v2)
        self.session.add(self.d2)

        data = server.regDevice(user_id=self.u2.id, vehicle_id=self.v2.id, sn='EW-14100002-UT', secret_code='sec2')

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error'][u'message'], "ServerError: Device is already in use.")


class DeviceUnRegistrationTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        """
        u1 - v1 - d1
            "Ok"

        u2 - v2 - d2 (try to unreg d3)
            "Incorrect device or doesn't exist."
        """

        session = Session()

        cls.u1 = TrUser(login="11111", auth_code="1111", authenticated=True)
        cls.u2 = TrUser(login="22222", auth_code="2222", authenticated=True)
        cls.u3 = TrUser(login="33333", auth_code="3333", authenticated=True)
        u_list = [cls.u1, cls.u2, cls.u3]
        cls.user_count = len(u_list)
        session.add_all(u_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.refresh(cls.u3)
        session.commit()

        cls.v1 = TrVehicle("v1", cls.u1.id, car_model_id=111, year=2000)
        cls.v2 = TrVehicle("v2", cls.u2.id, car_model_id=111, year=2000)
        cls.v3 = TrVehicle("v3", cls.u3.id, car_model_id=111, year=2000)
        v_list = [cls.v1, cls.v2, cls.v3]
        cls.v_count = len(v_list)
        session.add_all(v_list)
        session.commit()

        cls.d1 = TrDevice(sn='EW-14100001-UT', secter_code='sec1', stat=True, imei_number='1111', accel_stat=True, time_interval=1, phone1="+79260000001", vehicle_id=cls.v1.id)
        cls.d2 = TrDevice(sn='EW-14100002-UT', secter_code='sec2', stat=True, imei_number='2222', accel_stat=True, time_interval=2, phone1="+79260000002", vehicle_id=cls.v2.id)
        cls.d3 = TrDevice(sn='EW-14100003-UT', secter_code='sec3', imei_number='3333', accel_stat=True, time_interval=3, phone1="+79260000003", vehicle_id=None)
        d_list = [cls.d1, cls.d2, cls.d3]
        cls.device_count = len(d_list)
        session.add_all(d_list)
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        for user in users:
            session.delete(user)
        session.commit()

        devices = session.query(TrDevice).all()
        for d in devices:
            session.delete(d)
        session.commit()

        session.close()


    def test_unreg_normal(self):

        self.session.add(self.u1)
        self.session.add(self.v1)
        self.session.add(self.d1)

        data = server.unregDevice(user_id=self.u1.id, vehicle_id=self.v1.id, device_id=self.d1.id)

        self.assertJsonRpc(data)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        v = s.query(TrVehicle).get(self.v1.id)
        self.assertIsNotNone(v)
        self.assertEquals(v.id, self.v1.id)
        self.assertIsNone(v.device)

        d = s.query(TrDevice).get(self.d1.id)
        self.assertIsNotNone(d)
        self.assertEquals(d.id, self.d1.id)
        self.assertEquals(d.stat, False)
        s.close()

    def test_unreg_nonexistance_device(self):

        self.session.add(self.u3)
        self.session.add(self.v3)
        self.session.add(self.d1)

        data = server.unregDevice(user_id=self.u3.id, vehicle_id=self.v3.id, device_id=self.d1.id + 1000)

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error'][u'message'], "ServerError: Incorrect device or doesn't exist.")

    def test_unreg_device_which_doesnt_belong_to_vehicle(self):

        self.session.add(self.u2)
        self.session.add(self.v2)
        self.session.add(self.d3)

        data = server.unregDevice(user_id=self.u2.id, vehicle_id=self.v2.id, device_id=self.d3.id)

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error'][u'message'], "ServerError: Incorrect device or doesn't exist.")


# class DeviceUpdateTestCase(BaseTestCase):
#
#     @classmethod
#     def setUpClass(cls):
#
#         session = Session()
#
#         cls.u1 = TrUser("2013-12-12 12:12:12", "u1", "testtest")
#         user_list = [cls.u1]
#         cls.user_count = len(user_list)
#         session.add_all(user_list)
#         session.flush()
#         session.refresh(cls.u1)
#         session.commit()
#
#         cls.d1 = TrDevice("d1", cls.u1.id)
#         device_list = [cls.d1]
#         cls.device_count = len(device_list)
#         session.add_all(device_list)
#         session.commit()
#
#         session.close()
#
#     @classmethod
#     def tearDownClass(cls):
#
#         session = Session()
#
#         users = session.query(TrUser).all()
#         for user in users:
#             session.delete(user)
#         session.commit()
#
#         session.close()
#
#     @unittest.skip("Reconfig structure.")
#     def test_update_device_name(self):
#
#         data = server.updateDevice(user_id=self.u1.id, device_id=self.d1.device_ID, alias="new_name")
#
#         self.assertJsonRpc(data)
#         self.assertIs(data['result'], True)
#
#         data = server.getDevices(self.u1.id)
#
#         self.assertJsonRpc(data)
#         self.assertEquals(data['result'][0][u'name'], u'new_name')
#     @unittest.skip("Reconfig structure.")
#     def test_update_time_interval(self):
#
#         data = server.updateDevice(user_id=self.u1.id, device_id=self.d1.device_ID, time_interval=12)
#
#         self.assertJsonRpc(data)
#         self.assertIs(data['result'], True)
#
#         data = server.getDevices(self.u1.id)
#
#         self.assertJsonRpc(data)
#         self.assertEquals(data['result'][0][u'time_interval'], 12)
#     @unittest.skip("Reconfig structure.")
#     def test_update_accel_stat(self):
#
#         data = server.updateDevice(user_id=self.u1.id, device_id=self.d1.device_ID, accel_stat=True)
#
#         self.assertJsonRpc(data)
#         self.assertIs(data['result'], True)
#
#         data = server.getDevices(self.u1.id)
#
#         self.assertJsonRpc(data)
#         self.assertEquals(data['result'][0][u'accel_stat'], True)
#
#     @unittest.skip("Update device empty value.")
#     def test_update_device_empty_value(self):
#         pass
#     @unittest.skip("Reconfig structure.")
#     def test_update_device_incorrect_param(self):
#
#         data = server.updateDevice(user_id=self.u1.id, device_id=self.d1.device_ID, wrong_param="test")
#
#         self.assertJsonRpcErr(data)
#         self.assertEquals(data['error']['message'], u'ServerError: Incorrect arg: wrong_param')
#
#     @unittest.skip("Update device incorrect value.")
#     def test_update_device_incorrect_value(self):
#
#         """Auto cast to unicode. Ex.: Boolean: True -> u'1'; Number: 12 - > u'12'"""
#         data = server.updateDevice(user_id=self.u1.id, device_id=self.d1.device_ID, alias=True)
#
#         self.assertJsonRpc(data)
#
#         data = server.getDevices(self.u1.id)
#         print data
#         self.assertJsonRpc(data)


def suite():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(DeviceBaseTestCase))
    suite.addTests(loader.loadTestsFromTestCase(DeviceGetTestCase))
    suite.addTests(loader.loadTestsFromTestCase(DeviceAddTestCase))
    suite.addTests(loader.loadTestsFromTestCase(DeviceDeleteTestCase))
    suite.addTests(loader.loadTestsFromTestCase(DeviceRegistrationTestCase))
    suite.addTests(loader.loadTestsFromTestCase(DeviceUnRegistrationTestCase))
    # suite.addTests(loader.loadTestsFromTestCase(DeviceUpdateTestCase))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
