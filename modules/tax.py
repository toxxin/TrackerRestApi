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


def __getTaxByPower(region_id, power, year):

    session = Session()

    tx = session.query(TrVehicleTax).filter(TrVehicleTax.id == region_id).first()

    if tx is None:
        return None

    #TODO: add tax parse and calcucation

    session.close()

    return


@jsonrpc.method('getTax(user_id=Number,vehicle_id=Number) -> Any', validate=True, authenticated=False)
@login_required
def getTax(user_id, vehicle_id):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    #TODO: add tax logic

    session.close()

    return
