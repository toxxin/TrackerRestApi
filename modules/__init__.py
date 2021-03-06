__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

device_params = ["time_interval", "accel_stat"]

device_test_mandatory_params = []
device_test_option_params = ["time_interval", "accel_stat"]

geo_mandatory_params = ["name", "shape", "center", "radius"]
geo_option_params = ["color", "state", ]
geo_params_must_for_circus_or_square = ["center", "radius"]
geo_params_must_for_rand = ["vertices"]

place_mandatory_params = ["title", "longitude", "latitude", "type"]
place_option_params = ["desc"]

group_mandatory_params = ["title"]
group_option_params = ["desc", "invitation", "meeting", "help"]

GEO_SHAPE_CIRCUS = 0
GEO_SHAPE_SQUARE = 1
GEO_SHAPE_RANDOM = 2

PUSH_GROUP_SOS = 0
PUSH_TARGET_NEWS = 1
PUSH_GROUP_INVITE = 2
PUSH_GROUP_MESSAGE = 3
PUSH_SYS = 4
PUSH_ROAD_ASSIST = 5
PUSH_PARKING = 6
PUSH_FINE = 7
PUSH_TIRE = 8
