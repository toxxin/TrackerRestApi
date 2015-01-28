# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

from flask.ext.login import login_required, current_user

from TrackerRestApi import jsonrpc
from TrackerRestApi import Session

from flask_jsonrpc import ServerError
from sqlautocode_gen.model import *


def fillDeviceResponse(dev):

    ret = {
        "id": dev.id,
        "type": dev.type,
        "time_interval": dev.time_interval,
        "accel_stat": dev.accel_stat,
        "sn": dev.sn
    }

    return ret


@jsonrpc.method('getDevice(user_id=Number,device_id=Number) -> Any', validate=True, authenticated=False)
@login_required
def getDevice(user_id, device_id):

    session = Session()

    t = session.query(TrVehicle.id).filter(TrVehicle.user_id == int(current_user.get_id())).subquery('t')
    dev = session.query(TrDevice).filter(TrDevice.id == device_id).filter(TrDevice.vehicle_id == t.c.id).first()

    if dev is None:
        session.close()
        raise ServerError("Device doesn't exist.")

    session.close()

    return fillDeviceResponse(dev)


@jsonrpc.method('getDevices(user_id=Number) -> Any', validate=True, authenticated=False)
@login_required
def getDevices(user_id):

    session = Session()

    t = session.query(TrVehicle.id).filter(TrVehicle.user_id == int(current_user.get_id())).subquery('t')
    devs = session.query(TrDevice).filter(TrDevice.vehicle_id == t.c.id).all()

    lst = [fillDeviceResponse(dev) for dev in devs]

    session.close()

    return lst


@jsonrpc.method('delDevice(user_id=Number,device_id=Number) -> Object', validate=True, authenticated=False)
@login_required
def delDevice(user_id, device_id):

    session = Session()

    t = session.query(TrVehicle.id).filter(TrVehicle.user_id == int(current_user.get_id())).subquery('t')
    dev = session.query(TrDevice).filter(TrDevice.vehicle_id == t.c.id).filter(TrDevice.id == device_id).first()

    if dev is None:
        session.close()
        raise ServerError("Device doesn't exist.")

    try:
        session.delete(dev)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Cannot delete device.")
    finally:
        session.close()

    return True


# @jsonrpc.method('updateDevice(user_id=Number, device_id=Number, alias=String, color=String, icon=String, time_interval=Number, accel_stat=Boolean) -> Object',
#                         validate=False, authenticated=False)
# # @login_required
# def updateDevice(user_id, device_id, **kwargs):
#
#     session = Session()
#
#     dev = session.query(TrDevice).filter(TrDevice.device_userID == int(current_user.get_id())).\
#                                     filter(TrDevice.device_ID == device_id).first()
#
#     if dev is None:
#         session.close()
#         raise ServerError("Device doesn't exist.")
#
#     for k,v in kwargs.iteritems():
#         if k not in device_params:
#             session.close()
#             raise ServerError("Incorrect arg: %s" % k)
#
#     for k,v in kwargs.iteritems():
#         setattr(dev, "device_"+k, v)
#
#     try:
#         session.merge(dev)
#         session.commit()
#     except:
#         session.rollback()
#         raise ServerError("Can't update")
#     finally:
#         session.close()
#
#     return True


@jsonrpc.method('regDevice(user_id=Number,vehicle_id=Number,sn=String,secret_code=String) -> Object', validate=True, authenticated=False)
@login_required
def regDevice(user_id, vehicle_id, sn, secret_code):

    session = Session()

    v = session.query(TrVehicle).filter(TrVehicle.user_id == int(current_user.get_id())).\
                                    filter(TrVehicle.id == vehicle_id).first()

    if v is None:
        session.close()
        raise ServerError("Vehicle doesn't exist.")

    dev = session.query(TrDevice).filter(TrDevice.sn == sn).\
                                    filter(TrDevice.secret_code == secret_code).first()

    if dev is None:
        session.close()
        raise ServerError("Device doesn't exist.")

    if dev.stat is True:
        session.close()
        raise ServerError("Device is already in use.")

    if v.device is not None:
        session.close()
        raise ServerError("Vehicle already has device.")

    try:
        dev.stat = True
        v.device = dev
        session.commit()
        ret_id = dev.id
    except:
        session.rollback()
        raise ServerError("Can't register device.")
    finally:
        session.close()

    return ret_id


@jsonrpc.method('unregDevice(user_id=Number,vehicle_id=Number,device_id=Number) -> Object', validate=True, authenticated=False)
@login_required
def unregDevice(user_id, vehicle_id, device_id):

    session = Session()

    v = session.query(TrVehicle).filter(TrVehicle.user_id == int(current_user.get_id())).\
                                filter(TrVehicle.id == vehicle_id).first()

    if v is None:
        session.close()
        raise ServerError("Vehicle doesn't exist.")

    if v.device is None or v.device.id != device_id:
        session.close()
        raise ServerError("Incorrect device or doesn't exist.")

    try:
        v.device.stat = False
        v.device = None
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't unregister device.")
    finally:
        session.close()

    return True
