# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

from flask.ext.login import login_required, current_user

import os

import simplejson as json
from decimal import Decimal

from TrackerRestApi import jsonrpc, app
from TrackerRestApi import Session

from flask_jsonrpc import ServerError
from sqlautocode_gen.model import *
from sqlautocode_gen.avto_dggr_model import TrAvtoDGGR


def fillVihecleResponse(v):

    ret = {
        "id": v.id,
        "name": v.name,
        "type": v.type,
        "year": v.year,
        "pic": app.config.get('VEHICLES_IMG_URL') + v.pic if v.pic is not None else v.pic,
        "logo": app.config.get('MAKERS_IMG_URL') + v.car_model.logo if v.car_model.logo is not None else v.car_model.logo,

        "maker": v.car_model.marka_name,
        "model": v.car_model.model,
        "generation": v.car_model.generation,
        "modification": v.car_model.modification,
        "year_start": v.car_model.year_start,
        "year_stop": v.car_model.year_start,

        "sts": v.car_sts,
        "number": v.car_number,
        "device": {"id": v.device.id, "sn": v.device.sn} if v.device is not None else None
    }

    return ret


def fillTechVehicle(v):

    ret = {
        "id": v.id,

        "kuzov": {
            "loading_height": v.car_model.loading_height,
            "perm_weight": v.car_model.perm_weight,
            "front_axle_load": v.car_model.front_axle_load,
            "rear_axle_load": v.car_model.rear_axle_load,
            "length_cargo_bay": v.car_model.length_cargo_bay,
            "width_cargo_bay": v.car_model.width_cargo_bay,
            "height_cargo_bay": v.car_model.height_cargo_bay,
            "volume_cargo_bay": v.car_model.volume_cargo_bay,
            "seats_number": v.car_model.seats_number,
            "max_trunk_volume": v.car_model.max_trunk_volume,
            "min_trunk_volume": v.car_model.min_trunk_volume,
            "track_front_wheels": v.car_model.track_front_wheels,
            "track_rear_wheels": v.car_model.track_rear_wheels,
            "wheelbase": v.car_model.wheelbase,
            "length": v.car_model.length,
            "width": v.car_model.width,
            "height": v.car_model.height,
            "payload": v.car_model.payload,
            "full_weight": v.car_model.full_weight,
            "curb_weight": v.car_model.curb_weight,
            "clearance": v.car_model.clearance
        },
        "dvigatel": {
            "cylinder_diameter": v.car_model.cylinder_diameter,
            "valves_number": v.car_model.valves_number,
            "cylinders_number": v.car_model.cylinders_number,
            "piston_stroke": v.car_model.piston_stroke,
            "maximum_torque": v.car_model.maximum_torque,
            "max_maximum_torque": v.car_model.max_maximum_torque,
            "min_maximum_torque": v.car_model.min_maximum_torque,
            "max_maximum_power": v.car_model.max_maximum_power,
            "min_maximum_power": v.car_model.min_maximum_power,
            "admission": v.car_model.admission,
            "engine_config": v.car_model.engine_config,
            "supercharging": v.car_model.supercharging,
            "intercooler_tmp": v.car_model.intercooler_tmp,
            "engine_power": v.car_model.engine_power,
            "engine_size": v.car_model.engine_size,
            "engine_type": v.car_model.engine_type
        },
        "transmissiya": {
            "stage_number": v.car_model.stage_number,
            "drive": v.car_model.drive,
            "transmission": v.car_model.transmission
        },
        "podveska_i_tormoza": {
            "rear_brakes": v.car_model.rear_brakes,
            "front_brakes": v.car_model.front_brakes,
            "rear_suspension": v.car_model.rear_suspension,
            "front_suspension": v.car_model.front_suspension
        },
        "eksplut_pokazately": {
            "fuel_capacity": v.car_model.fuel_capacity,
            "fuel_cons_highway": v.car_model.fuel_cons_highway,
            "fuel_cons_city": v.car_model.fuel_cons_city,
            "fuel_cons_mix": v.car_model.fuel_cons_mix,
            "eco_standard": v.car_model.eco_standard,
            "acceleration_to_100": v.car_model.acceleration_to_100,
            "max_speed": v.car_model.max_speed,
            "recommended_fuel": v.car_model.recommended_fuel
        },
        "rulevoe_upravlenie": {
            "turning_circle": v.car_model.turning_circle,
            "power_steering": v.car_model.power_steering
        },
        "diski": {
            "disk_rim_diameter_front": v.car_model.disk_rim_diameter_front,
            "disk_rim_diameter_rear": v.car_model.disk_rim_diameter_rear,
            "disk_rim_width_front": v.car_model.disk_rim_width_front,
            "disk_rim_width_rear": v.car_model.disk_rim_width_rear,
            "disk_mounting_holes_front": v.car_model.disk_mounting_holes_front,
            "disk_mounting_holes_rear": v.car_model.disk_mounting_holes_rear,
            "disk_diameter_holes_front": v.car_model.disk_diameter_holes_front,
            "disk_diameter_holes_rear": v.car_model.disk_diameter_holes_rear,
            "disk_offset_front": v.car_model.disk_offset_front,
            "disk_offset_rear": v.car_model.disk_offset_rear
        },
        "shini": {
            "tire_diameter_front": v.car_model.tire_diameter_front,
            "tire_diameter_rear": v.car_model.tire_diameter_rear,
            "tire_height_front": v.car_model.tire_height_front,
            "tire_height_rear": v.car_model.tire_height_rear,
            # "tire_width_front": v.car_model.tire_width_front,
            "tire_width_front": v.car_model.tire_width_rear,
            "tire_width_rear": v.car_model.tire_width_rear
        }
    }

    return ret


@jsonrpc.method('getVehicles(user_id=Number) -> Any', validate=True, authenticated=False)
@login_required
def getVehicles(user_id):

    session = Session()

    lst = []

    vehiles = session.query(TrVehicle).filter(TrVehicle.user_id == int(current_user.get_id())).all()

    for v in vehiles:
        lst.append(fillVihecleResponse(v))

    session.close()

    return lst


@jsonrpc.method('getVehicleTech(user_id=Number, id=Number) -> Object', validate=True, authenticated=False)
@login_required
def getVehicleTech(user_id, id):

    session = Session()

    v = session.query(TrVehicle).filter(TrVehicle.user_id == int(current_user.get_id())).filter(TrVehicle.id == id).first()

    if v is None:
        raise ServerError("Vehicle doesn't exist.")

    ret = fillTechVehicle(v)

    session.close()

    return ret


@jsonrpc.method('addVehicle(user_id=Number, name=String, type=String, maker=String, model=String, generation=String, modification=String, year=Number) -> Object', validate=True, authenticated=False)
@login_required
def addVehicle(user_id, name, type, maker, model, generation, modification, year):

    session = Session()

    car = session.query(TrAvtoDGGR).filter(TrAvtoDGGR.marka_name == maker).\
            filter(TrAvtoDGGR.model == model).filter(TrAvtoDGGR.generation == generation).\
            filter(TrAvtoDGGR.modification == modification).filter(TrAvtoDGGR.year_start <= year).\
            filter(or_(TrAvtoDGGR.year_stop >= year, TrAvtoDGGR.year_stop.is_(None))).first()

    if car is None:
        raise ServerError("Incorrect vehicle params.")

    if type != 'A' and type != 'M':
        raise ServerError("Incorrect vehicle type.")

    v = TrVehicle(user_id=int(current_user.get_id()), name=name, type=type, car_model_id=car.id, year=year)

    try:
        session.add(v)
        session.commit()
        session.flush()
        session.commit()
        session.refresh(v)
    except:
        session.rollback()
        raise ServerError("Can't add vehicle.")
    finally:
        session.close()

    return v.id


@jsonrpc.method('updateVehicle(user_id=Number, id=Number, name=String, maker=String, model=String, generation=String, modification=String, year=Number) -> Object', validate=True, authenticated=False)
@login_required
def updateVehicle(user_id, id, name, maker, model, generation, modification, year):

    session = Session()

    v = session.query(TrVehicle).filter(TrVehicle.user_id == int(current_user.get_id())).filter(TrVehicle.id == id).first()

    if v is None:
        session.close()
        raise ServerError("Vehicle doesn't exist.")

    if v.car_model.marka_name != maker or v.car_model.model != model or v.car_model.generation != generation or \
        v.car_model.modification != modification or v.car_model.year_start > year or v.car_model.year_stop < year:

        car = session.query(TrAvtoDGGR).filter(TrAvtoDGGR.marka_name == maker).\
            filter(TrAvtoDGGR.model == model).filter(TrAvtoDGGR.generation == generation).\
            filter(TrAvtoDGGR.modification == modification).filter(TrAvtoDGGR.year_start <= year).\
            filter(or_(TrAvtoDGGR.year_stop >= year, TrAvtoDGGR.year_stop.is_(None))).first()

        if car is None:
            session.close()
            raise ServerError("Incorrect vehicle params.")

        v.car_model_id = car.id
        v.year = year

    if v.name != name:
        v.name = name

    try:
        session.merge(v)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't add data.")
    finally:
        session.close()

    return True


@jsonrpc.method('addSTS(user_id=Number, id=Number, sts=String, number=String) -> Object', validate=True, authenticated=False)
@login_required
def addSTS(user_id, id, sts, number):
    """
        Cyrillic encoding supports by attaching header: \"Content-Type: text/html; charset=UTF-8\"
    """
    session = Session()

    # TODO: Add validation sts and number

    v = session.query(TrVehicle).filter(TrVehicle.user_id == int(current_user.get_id())).filter(TrVehicle.id == id).first()

    if v is None:
        session.close()
        raise ServerError("Vehicle doesn't exist.")

    v.car_sts = sts
    v.car_number = number

    try:
        session.merge(v)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't add data.")
    finally:
        session.close()

    return True


@jsonrpc.method('delSTS(user_id=Number, id=Number) -> Object', validate=True, authenticated=False)
@login_required
def delSTS(user_id, id):

    session = Session()

    v = session.query(TrVehicle).filter(TrVehicle.user_id == int(current_user.get_id())).filter(TrVehicle.id == id).first()

    if v is None:
        session.close()
        raise ServerError("Vehicle doesn't exist.")

    v.car_sts = None
    v.car_number = None

    try:
        session.merge(v)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't change data.")
    finally:
        session.close()

    return True


@jsonrpc.method('delVehicle(user_id=Number, id=Number) -> Object', validate=True, authenticated=False)
@login_required
def delVehicle(user_id, id):

    session = Session()

    v = session.query(TrVehicle).filter(TrVehicle.user_id == int(current_user.get_id())).filter(TrVehicle.id == id).first()

    if v is None:
        session.close()
        raise ServerError("Vehicle doesn't exist.")

    if v.device is not None:
        try:
            v.device.stat = False
            session.commit()
        except:
            session.rollback()

    try:
        app.logger.debug('Trying to delete old pic file.')
        os.remove(app.config.get('VEHICLES_IMG_PATH') + v.pic)
    except:
        pass

    try:
        print 'delete vehicle %d' % v.id
        session.delete(v)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't delete vehicle.")
    finally:
        session.close()

    return True


@jsonrpc.method('getMakers(user_id=Number, type=String) -> Object', validate=True, authenticated=False)
@login_required
def getMakers(user_id, type):

    session = Session()

    makers = session.query(TrAvtoDGGR.marka_name, TrAvtoDGGR.logo).distinct(TrAvtoDGGR.marka_name).order_by(TrAvtoDGGR.marka_name).all()

    lst = [{"maker": m.marka_name, "logo": m.logo} for m in makers]

    session.close()

    return lst


@jsonrpc.method('getModelsByMaker(user_id=Number, type=String, maker=String) -> Any', validate=True, authenticated=False)
@login_required
def getModelByMaker(user_id, type, maker):

    session = Session()

    models = session.query(TrAvtoDGGR.model).filter(TrAvtoDGGR.marka_name == maker).distinct(TrAvtoDGGR.model).\
        order_by(TrAvtoDGGR.model).all()

    lst = [m[0] for m in models]

    session.close()

    return lst


@jsonrpc.method('getGenByModelByMaker(user_id=Number, type=String, maker=String, model=String) -> Any', validate=True, authenticated=False)
@login_required
def getGenerationByModelByMaker(user_id, type, maker, model):

    session = Session()

    mods = session.query(TrAvtoDGGR.generation).filter(TrAvtoDGGR.marka_name == maker).\
        filter(TrAvtoDGGR.model == model).distinct(TrAvtoDGGR.generation).order_by(TrAvtoDGGR.generation).all()

    lst = [m[0] for m in mods]

    session.close()

    return lst


@jsonrpc.method('getModifByGenByModelByMaker(user_id=Number, type=String, maker=String, model=String, generation=String) -> Any', validate=True, authenticated=False)
@login_required
def getModificationByGenByModelByMaker(user_id, type, maker, model, generation):

    session = Session()

    mods = session.query(TrAvtoDGGR.modification).filter(TrAvtoDGGR.marka_name == maker).\
        filter(TrAvtoDGGR.model == model).filter(TrAvtoDGGR.generation == generation).distinct(TrAvtoDGGR.generation).order_by(TrAvtoDGGR.generation).all()

    lst = [m[0] for m in mods]

    session.close()

    return lst


@jsonrpc.method('getYearsByModifByGenByModelByMaker(user_id=Number, type=String, maker=String, model=String, generation=String, modification=String) -> Any', validate=True, authenticated=False)
@login_required
def getYearsByModifByGenByModelByMaker(user_id, type, maker, model, generation, modification):

    session = Session()

    cars = session.query(TrAvtoDGGR).filter(TrAvtoDGGR.marka_name == maker).\
        filter(TrAvtoDGGR.model == model).filter(TrAvtoDGGR.generation == generation).\
        filter(TrAvtoDGGR.modification == modification).all()

    lst = []

    now = datetime.datetime.now()

    for c in cars:
        if c.year_stop is None:
            c.year_stop = now.year
        lst.extend([c.year_start + x for x in xrange(c.year_stop - c.year_start + 1)])

    lst = list(set(lst))
    lst.sort()

    session.close()

    return lst


regions = {
    1:      u'Республика Адыгея',
    2:      u'Республика Башкортостан',
    102:    u'Республика Башкортостан',
    3:      u'Республика Бурятия',
    4:      u'Республика Алтай',
    5:      u'Республика Дагестан',
    6:      u'Республика Ингушетия',
    7:      u'Кабардино-Балкарская республика',
    8:      u'Республика Калмыкия',
    9:      u'Республика Карачаево-Черкесия',
    10:     u'Республика Карелия',
    11:     u'Республика Коми',
    12:     u'Республика Марий Эл',
    13:     u'Республика Мордовия',
    113:    u'Республика Мордовия',
    14:     u'Республика Саха (Якутия)',
    15:     u'Республика Северная Осетия — Алания',
    16:     u'Республика Татарстан',
    116:    u'Республика Татарстан',
    17:     u'Республика Тыва',
    18:     u'Удмуртская республика',
    19:     u'Республика Хакасия',
    21:     u'Чувашская республика',
    121:    u'Чувашская республика',

    82:     u'Республика Крым',
    777:    u'Республика Крым',

    95:     u'Чеченская республика',


    50:     u'Москва',
    150:    u'Московская область',
}

getRegionByNumber = lambda num: regions.get(int(num[6:]))


def doCalcTax(region, power, year):

    return 1800


@jsonrpc.method('getRoadTax(user_id=Number, vehicle_id=Number)', validate=True, authenticated=False)
@login_required
def getRoadTax(user_id, vehicle_id):

    session = Session()

    v = session.query(TrVehicle).filter(TrVehicle.user_id == int(current_user.get_id())).filter(TrVehicle.id == id).first()

    if v is None:
        session.close()
        raise ServerError("Vehicle doesn't exist.")

    if v.car_number is None:
        session.close()
        raise ServerError("Car number must be set.")

    tax = doCalcTax(int(v.car_number[6:]), v.car_model.engine_power, v.year)

    session.close()

    return {"vehicle_id": vehicle_id, "tax": tax, "region": getRegionByNumber(v.car_number)}
