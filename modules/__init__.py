__author__ = 'Anton Glukhov'

device_params = ["time_interval", "accel_stat"]

device_test_mandatory_params = []
device_test_option_params = ["time_interval", "accel_stat"]

geo_mandatory_params = ["name", "shape", "center", "radius"]
geo_option_params = ["color", "state", ]
geo_params_must_for_circus_or_square = ["center", "radius"]
geo_params_must_for_rand = ["vertices"]

GEO_SHAPE_CIRCUS = 0
GEO_SHAPE_SQUARE = 1
GEO_SHAPE_RANDOM = 2
