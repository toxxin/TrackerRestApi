from tools.pygeotools import GeoLocation

__author__ = 'Anton Glukhov'

import sys
sys.path.append('..')

import unittest
import datetime
# from modules import location

@unittest.skip("Fix location first")
class TestDistanceBetweenPoints(unittest.TestCase):
    def setUp(self):
        self.a = {'x': 55.895546, 'y': 37.45308, 't': datetime.datetime.fromtimestamp(1)}
        self.b = {'x': 55.97889, 'y': 37.164284, 't': datetime.datetime.fromtimestamp(1)}

    def tearDown(self):
        pass

    def test_normal_case(self):
        self.assertEqual(location.distance(self.a, self.b), 20256)

    def test_same_coords(self):
        self.assertEquals(location.distance(self.a, self.a), 0)

    def test_same_coords_with_round_fix(self):
        self.x1 = {'y': 37.38777, 'x': 55.80714, 't': datetime.datetime(2014, 6, 1, 6, 53, 14)}
        self.x2 = {'y': 37.38777, 'x': 55.80714, 't': datetime.datetime(2014, 6, 1, 6, 52, 15)}

        self.assertEquals(location.distance(self.x1, self.x2), 0)

    def test_one_arg(self):
        # self.assertEqual(location.distance(self.a, {}), 240.86943513223758)
        pass
@unittest.skip("Fix location first")
class TestDurationPoints(unittest.TestCase):

    def test_sorted_cl(self):
        self.cl = [
            {'x': 35.32, 'y': 55.123, 't': datetime.datetime.fromtimestamp(1401648830)},
            {'x': 36.11, 'y': 55.321, 't': datetime.datetime.fromtimestamp(1401648832)},
            {'x': 36.11, 'y': 55.321, 't': datetime.datetime.fromtimestamp(1401648835)},
            {'x': 36.11, 'y': 55.321, 't': datetime.datetime.fromtimestamp(1401648836)}
        ]

        print location.duration(self.cl)
        self.assertEqual(location.duration(self.cl), datetime.timedelta(seconds=6))

    def test_random_cl(self):
        self.cl = [
            {'x': 35.32, 'y': 55.123, 't': datetime.datetime.fromtimestamp(1401648835)},
            {'x': 36.11, 'y': 55.321, 't': datetime.datetime.fromtimestamp(1401648832)},
            {'x': 36.11, 'y': 55.321, 't': datetime.datetime.fromtimestamp(1401648830)},
            {'x': 36.11, 'y': 55.321, 't': datetime.datetime.fromtimestamp(1401648836)}
        ]

        self.assertEquals(location.duration(self.cl), datetime.timedelta(seconds=6))

    def test_one_element_in_cl(self):
        self.cl = [
            {'x': 35.32, 'y': 55.123, 't': datetime.datetime.fromtimestamp(1401648835)}
        ]

        self.assertEquals(location.duration(self.cl), datetime.timedelta(seconds=0))

    def test_empty_cl(self):
        self.cl = []

        self.assertEquals(location.duration(self.cl), datetime.timedelta(seconds=0))


class TestBoundingLocations(unittest.TestCase):

    # 55.7512701,37.618324 - Russia, Moscow, Kremlin

    def test_bounding_locations(self):

        loc1 = GeoLocation.from_degrees(55.7512701,37.618324)
        tmp = loc1.bounding_locations(2)

        print tmp

        print "SW - %f" % tmp[0].deg_lat
        print "SW - %f" % tmp[0].deg_lon

        print "NE - %f" % tmp[1].deg_lat
        print "NE - %f" % tmp[1].deg_lon


def suite():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestDistanceBetweenPoints))
    suite.addTests(loader.loadTestsFromTestCase(TestDurationPoints))
    suite.addTests(loader.loadTestsFromTestCase(TestDurationPoints))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
