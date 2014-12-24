__author__ = 'Anton Glukhov'

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlautocode_gen import DeclarativeBase


class TrAvtoDGGR(DeclarativeBase):
    __tablename__ = 'tr_avto_dggr'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #column definitions
    id = Column(u'id', Integer, primary_key=True)
    marka = Column(u'marka', String(255), nullable=False)
    marka_name = Column(u'marka_name', String(255), nullable=False)
    model = Column(u'model', String(255), nullable=False)
    generation = Column(u'generation', String(255), nullable=False)
    modification = Column(u'modification', String(255), nullable=False)
    year = Column(u'year', String(255), nullable=False)
    year_start = Column(u'year_start', Integer, nullable=False)
    year_stop = Column(u'year_stop', Integer)
    logo = Column(u'logo', String(45))

    #kuzov
    loading_height = Column(u'loading_height', Integer)
    perm_weight = Column(u'perm_weight', Integer)
    front_axle_load = Column(u'front_axle_load', Integer)
    rear_axle_load = Column(u'rear_axle_load', Integer)
    length_cargo_bay = Column(u'length_cargo_bay', Integer)
    width_cargo_bay = Column(u'width_cargo_bay', Integer)
    height_cargo_bay = Column(u'height_cargo_bay', Integer)
    volume_cargo_bay = Column(u'volume_cargo_bay', Integer)
    seats_number = Column(u'seats_number', Integer)
    max_trunk_volume = Column(u'max_trunk_volume', Integer)
    min_trunk_volume = Column(u'min_trunk_volume', Integer)
    track_front_wheels = Column(u'track_front_wheels', Integer)
    track_rear_wheels = Column(u'track_rear_wheels', Integer)
    wheelbase = Column(u'wheelbase', Integer)
    length = Column(u'length', Integer)
    width = Column(u'width', Integer)
    height = Column(u'height', Integer)
    payload = Column(u'payload', Integer)
    full_weight = Column(u'full_weight', Integer)
    curb_weight = Column(u'curb_weight', Integer)
    clearance = Column(u'clearance', Integer)

    #dvigatel
    cylinder_diameter = Column(u'cylinder_diameter', Integer)
    valves_number = Column(u'valves_number', Integer)
    cylinders_number = Column(u'cylinders_number', Integer)
    piston_stroke = Column(u'piston_stroke', DECIMAL(precision=5, scale=2))
    maximum_torque = Column(u'maximum_torque', Integer)
    max_maximum_torque = Column(u'max_maximum_torque', Integer)
    min_maximum_torque = Column(u'min_maximum_torque', Integer)
    max_maximum_power = Column(u'max_maximum_power', Integer)
    min_maximum_power = Column(u'min_maximum_power', Integer)
    admission = Column(u'admission', String(255))
    engine_config = Column(u'engine_config', String(255))
    supercharging = Column(u'supercharging', String(255))
    intercooler_tmp = Column(u'intercooler_tmp', String(255))
    engine_power = Column(u'engine_power', Integer)
    engine_size = Column(u'engine_size', DECIMAL(precision=6, scale=2))
    engine_type = Column(u'engine_type', String(255))

    #transmissiya
    stage_number = Column(u'stage_number', Integer)
    drive = Column(u'drive', String(255))
    transmission = Column(u'transmission', String(255))

    #podveska_i_tormoza
    rear_brakes = Column(u'rear_brakes', String(255))
    front_brakes = Column(u'front_brakes', String(255))
    rear_suspension = Column(u'rear_suspension', String(255))
    front_suspension = Column(u'front_suspension', String(255))

    #eksplut_pokazately
    fuel_capacity = Column(u'fuel_capacity', Integer)
    fuel_cons_highway = Column(u'fuel_cons_highway', DECIMAL(precision=4, scale=2))
    fuel_cons_city = Column(u'fuel_cons_city', DECIMAL(precision=4, scale=2))
    fuel_cons_mix = Column(u'fuel_cons_mix', DECIMAL(precision=4, scale=2))
    eco_standard = Column(u'eco_standard', String(255))
    acceleration_to_100 = Column(u'acceleration_to_100', DECIMAL(precision=4, scale=2))
    max_speed = Column(u'max_speed', Integer)
    recommended_fuel = Column(u'recommended_fuel', String(255))

    #rulevoe_upravlenie
    turning_circle = Column(u'turning_circle', Integer)
    power_steering = Column(u'power_steering', String(255))

    #diski
    disk_rim_diameter_front = Column(u'disk_rim_diameter_front', Integer)
    disk_rim_diameter_rear = Column(u'disk_rim_diameter_rear', Integer)
    disk_rim_width_front = Column(u'disk_rim_width_front', DECIMAL(precision=3, scale=1))
    disk_rim_width_rear = Column(u'disk_rim_width_rear', DECIMAL(precision=3, scale=1))
    disk_mounting_holes_front = Column(u'disk_mounting_holes_front', Integer)
    disk_mounting_holes_rear = Column(u'disk_mounting_holes_rear', Integer)
    disk_diameter_holes_front = Column(u'disk_diameter_holes_front', Integer)
    disk_diameter_holes_rear = Column(u'disk_diameter_holes_rear', Integer)
    disk_offset_front = Column(u'disk_offset_front', Integer)
    disk_offset_rear = Column(u'disk_offset_rear', Integer)

    #shini
    tire_diameter_front = Column(u'tire_diameter_front', Integer)
    tire_diameter_rear = Column(u'tire_diameter_rear', Integer)
    tire_height_front = Column(u'tire_height_front', Integer)
    tire_height_rear = Column(u'tire_height_rear', Integer)
    tire_width_front = Column(u'tire_width_front', Integer)
    tire_width_rear = Column(u'tire_width_rear', Integer)

    vehicles = relationship("TrVehicle", backref="car_model")

    def __init__(self, marka, marka_name, model, generation, modification, year, logo,
                    loading_height=None,
                    perm_weight=None,
                    front_axle_load = None,
                    rear_axle_load=None,
                    length_cargo_bay=None,
                    width_cargo_bay=None,
                    height_cargo_bay=None,
                    volume_cargo_bay=None,
                    seats_number=None,
                    max_trunk_volume=None,
                    min_trunk_volume=None,
                    track_front_wheels=None,
                    track_rear_wheels=None,
                    wheelbase=None,
                    length=None,
                    width=None,
                    height=None,
                    payload=None,
                    full_weight=None,
                    curb_weight=None,
                    clearance=None,

                    cylinder_diameter=None,
                    valves_number=None,
                    cylinders_number=None,
                    piston_stroke=None,
                    maximum_torque=None,
                    max_maximum_torque=None,
                    min_maximum_torque=None,
                    max_maximum_power=None,
                    min_maximum_power=None,
                    admission=None,
                    engine_config=None,
                    supercharging=None,
                    intercooler_tmp=None,
                    engine_power=None,
                    engine_size=None,
                    engine_type=None,

                    stage_number = None,
                    drive = None,
                    transmission = None,

                    rear_brakes = None,
                    front_brakes = None,
                    rear_suspension = None,
                    front_suspension = None,

                    fuel_capacity = None,
                    fuel_cons_highway = None,
                    fuel_cons_city = None,
                    fuel_cons_mix = None,
                    eco_standard = None,
                    acceleration_to_100 = None,
                    max_speed = None,
                    recommended_fuel = None,

                    turning_circle = None,
                    power_steering = None,

                    disk_rim_diameter_front = None,
                    disk_rim_diameter_rear = None,
                    disk_rim_width_front = None,
                    disk_rim_width_rear = None,
                    disk_mounting_holes_front = None,
                    disk_mounting_holes_rear = None,
                    disk_diameter_holes_front = None,
                    disk_diameter_holes_rear = None,
                    disk_offset_front = None,
                    disk_offset_rear = None,

                    tire_diameter_front = None,
                    tire_diameter_rear = None,
                    tire_height_front = None,
                    tire_height_rear = None,
                    tire_width_front = None,
                    tire_width_rear = None
                    ):
        self.marka = marka
        self.marka_name = marka_name
        self.model = model
        self.generation = generation
        self.modification = modification
        self.year = year
        self.logo = logo

        self.loading_height = loading_height
        self.perm_weight = perm_weight
        self.front_axle_load = front_axle_load
        self.rear_axle_load = rear_axle_load
        self.length_cargo_bay = length_cargo_bay
        self.width_cargo_bay = width_cargo_bay
        self.height_cargo_bay = height_cargo_bay
        self.volume_cargo_bay = volume_cargo_bay
        self.seats_number = seats_number
        self.max_trunk_volume = max_trunk_volume
        self.min_trunk_volume = min_trunk_volume
        self.track_front_wheels = track_front_wheels
        self.track_rear_wheels = track_rear_wheels
        self.wheelbase = wheelbase
        self.length = length
        self.width = width
        self.height = height
        self.payload = payload
        self.full_weight = full_weight
        self.curb_weight = curb_weight
        self.clearance = clearance

        self.cylinder_diameter = cylinder_diameter
        self.valves_number = valves_number
        self.cylinders_number = cylinders_number
        self.piston_stroke = piston_stroke
        self.maximum_torque = maximum_torque
        self.max_maximum_torque = max_maximum_torque
        self.min_maximum_torque = min_maximum_torque
        self.max_maximum_power = max_maximum_power
        self.min_maximum_power = min_maximum_power
        self.admission = admission
        self.engine_config = engine_config
        self.supercharging = supercharging
        self.intercooler_tmp = intercooler_tmp
        self.engine_power = engine_power
        self.engine_size = engine_size
        self.engine_type = engine_type

        self.stage_number = stage_number
        self.drive = drive
        self.transmission = transmission

        self.rear_brakes = rear_brakes
        self.front_brakes = front_brakes
        self.rear_suspension = rear_suspension
        self.front_suspension = front_suspension

        self.fuel_capacity = fuel_capacity,
        self.fuel_cons_highway = fuel_cons_highway,
        self.fuel_cons_city = fuel_cons_city,
        self.fuel_cons_mix = fuel_cons_mix,
        self.eco_standard = eco_standard,
        self.acceleration_to_100 = acceleration_to_100,
        self.max_speed = max_speed,
        self.recommended_fuel = recommended_fuel,

        self.turning_circle = turning_circle,
        self.power_steering = power_steering,

        self.disk_rim_diameter_front = disk_rim_diameter_front,
        self.disk_rim_diameter_rear = disk_rim_diameter_rear,
        self.disk_rim_width_front = disk_rim_width_front,
        self.disk_rim_width_rear = disk_rim_width_rear,
        self.disk_mounting_holes_front = disk_mounting_holes_front,
        self.disk_mounting_holes_rear = disk_mounting_holes_rear,
        self.disk_diameter_holes_front = disk_diameter_holes_front,
        self.disk_diameter_holes_rear = disk_diameter_holes_rear,
        self.disk_offset_front = disk_offset_front,
        self.disk_offset_rear = disk_offset_rear,

        self.tire_diameter_front = tire_diameter_front,
        self.tire_diameter_rear = tire_diameter_rear,
        self.tire_height_front = tire_height_front,
        self.tire_height_rear = tire_height_rear,
        self.tire_width_front = tire_width_front,
        self.tire_width_rear = tire_width_rear