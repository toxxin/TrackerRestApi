# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"


from flask.ext.login import login_required, current_user

from TrackerRestApi import jsonrpc, app
from TrackerRestApi import Session

from flask_jsonrpc import ServerError, InvalidParamsError
from sqlautocode_gen.model import *
from sqlautocode_gen.group_model import TrGroup, TrGroupComment, association_table_user_group


def __doCalcTax(region, power, year):

    session = Session()

    regs = session.query(TrRegion).all()
    for r in regs:
        if region in r.region_ids.split(","):
            reg = r.title
            r_id = r.id
            break

    tx = session.query(TrVehicleTax).filter(TrVehicleTax.region_id == r_id).first()

    if tx is None:
        return None

    session.close()

    return 1800, reg


@jsonrpc.method('getRoadTax(user_id=Number, vehicle_id=Number)', validate=True, authenticated=False)
@login_required
def getRoadTax(user_id, vehicle_id):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    v = session.query(TrVehicle).filter(TrVehicle.user_id == uid).filter(TrVehicle.id == id).first()

    if v is None:
        session.close()
        raise ServerError("Vehicle doesn't exist.")

    if v.car_number is None:
        session.close()
        raise ServerError("Car number must be set.")

    tax, reg = __doCalcTax(int(v.car_number[6:]), v.car_model.engine_power, v.year)

    session.close()

    return {"vehicle_id": vehicle_id, "tax": tax, "region": reg}
