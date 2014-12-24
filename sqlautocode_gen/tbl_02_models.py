__author__ = 'Anton Glukhov'

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlautocode_gen.model import DeclarativeBase


class Tbl02Model(DeclarativeBase):
    __tablename__ = 'tbl_02_models'

    #column definitions
    model_0_to_100_kph = Column(u'model_0_to_100_kph', DECIMAL(precision=4, scale=1))
    model_body = Column(u'model_body', VARCHAR(length=64))
    model_co2 = Column(u'model_co2', INTEGER())
    model_doors = Column(u'model_doors', INTEGER())
    model_drive = Column(u'model_drive', VARCHAR(length=16))
    model_engine_bore_mm = Column(u'model_engine_bore_mm', DECIMAL(precision=6, scale=1))
    model_engine_cc = Column(u'model_engine_cc', INTEGER())
    model_engine_compression = Column(u'model_engine_compression', VARCHAR(length=8))
    model_engine_cyl = Column(u'model_engine_cyl', INTEGER())
    model_engine_fuel = Column(u'model_engine_fuel', VARCHAR(length=32))
    model_engine_position = Column(u'model_engine_position', VARCHAR(length=8))
    model_engine_power_ps = Column(u'model_engine_power_ps', INTEGER())
    model_engine_power_rpm = Column(u'model_engine_power_rpm', INTEGER())
    model_engine_stroke_mm = Column(u'model_engine_stroke_mm', DECIMAL(precision=6, scale=1))
    model_engine_torque_nm = Column(u'model_engine_torque_nm', INTEGER())
    model_engine_torque_rpm = Column(u'model_engine_torque_rpm', INTEGER())
    model_engine_type = Column(u'model_engine_type', VARCHAR(length=32))
    model_engine_valves_per_cyl = Column(u'model_engine_valves_per_cyl', INTEGER())
    model_fuel_cap_l = Column(u'model_fuel_cap_l', INTEGER())
    model_height_mm = Column(u'model_height_mm', INTEGER())
    model_id = Column(u'model_id', INTEGER(), primary_key=True, nullable=False)
    model_length_mm = Column(u'model_length_mm', INTEGER())
    model_lkm_city = Column(u'model_lkm_city', DECIMAL(precision=4, scale=1))
    model_lkm_hwy = Column(u'model_lkm_hwy', DECIMAL(precision=4, scale=1))
    model_lkm_mixed = Column(u'model_lkm_mixed', DECIMAL(precision=4, scale=1))
    model_make_display = Column(u'model_make_display', VARCHAR(length=32))
    model_make_id = Column(u'model_make_id', VARCHAR(length=32), nullable=False)
    model_name = Column(u'model_name', VARCHAR(length=64), nullable=False)
    model_seats = Column(u'model_seats', INTEGER())
    model_sold_in_us = Column(u'model_sold_in_us', INTEGER())
    model_top_speed_kph = Column(u'model_top_speed_kph', INTEGER())
    model_transmission_type = Column(u'model_transmission_type', VARCHAR(length=32))
    model_trim = Column(u'model_trim', VARCHAR(length=64), nullable=False)
    model_weight_kg = Column(u'model_weight_kg', INTEGER())
    model_wheelbase_mm = Column(u'model_wheelbase_mm', INTEGER())
    model_width_mm = Column(u'model_width_mm', INTEGER())
    model_year = Column(u'model_year', INTEGER(), nullable=False)

    #relation definitions
    # vehicles = relationship("TrVehicle", backref="car_model")