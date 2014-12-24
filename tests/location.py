__author__ = 'Anton Glukhov'

import unittest
from base import BaseTestCase
from sqlautocode_gen.model import *
from tests.run import Session, server


def setUpModule():
    pass


def tearModuleDown():
    pass


class DLocationBaseTestCase(BaseTestCase):

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

        cls.l1 = TrDLocation("55.123,54.332", "2013-12-12 12:12:12", cls.d1.device_ID)
        cls.l2 = TrDLocation("33.123,33.332", "2013-12-12 11:11:11", cls.d2.device_ID)
        cls.l3 = TrDLocation("44.123,44.332", "2013-10-10 10:10:10", cls.d2.device_ID)
        location_list = [cls.l1, cls.l2, cls.l3]
        cls.location_count = len(location_list)
        session.add_all(device_list)
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

    @unittest.skip("Relations device location")
    def test_relations_device_location(self):

        self.assertEquals(len(self.d1.locations), 1)
        # self.assertEquals(self.d1.geos[0].name, "g1")

        self.assertEquals(len(self.d2.locations), 2)
        # self.assertEquals(self.d2.geos[0].name, "g2")
        # self.assertEquals(self.d2.geos[1].name, "g3")

        self.assertEquals(len(self.d3.locations), 0)


def suite():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(DLocationBaseTestCase))
    # suite.addTests(loader.loadTestsFromTestCase(DGeoGetTestCase))
    # suite.addTests(loader.loadTestsFromTestCase(DGeoAddTestCase))
    # suite.addTests(loader.loadTestsFromTestCase(DGeoDeleteTestCase))
    # suite.addTests(loader.loadTestsFromTestCase(DGeoUpdateTestcase))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')