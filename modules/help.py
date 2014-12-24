# -*- coding: utf8 -*-
__author__ = 'Anton Glukhov'

from flask.ext.login import login_required, login_user

from TrackerRestApi import jsonrpc, app
from TrackerRestApi import Session

from flask_jsonrpc import ServerError
from sqlautocode_gen.model import *


@jsonrpc.method('addHelp(user_id=Number,vehicle_id=Number,message=String,lat_log=String,phone=String) -> Object', validate=True, authenticated=False)
def addHelp(user_id,vehicle_id,message,lat_log, phone):

    session = Session()

    v = session.query(TrVehicle).filter(TrVehicle.id == vehicle_id).filter(TrVehicle.user_id == user_id).first()

    if v is None:
        session.close()
        raise ServerError("Vehicle doesn't exist.")

    if v.help is None:
        """Add new message"""
        message = TrHelp(vehicle_id=v.id, message=message, lat_log=lat_log)

        try:
            session.add(message)
            session.commit()
        except:
            session.rollback()
            raise ServerError("Can't add help message.")
        finally:
            session.close()

    else:
        """Update existing message"""
        help = session.query(TrHelp).filter(TrHelp.vehicle_id == v.id).first()

        setattr(help, 'message', message)
        setattr(help, 'lat_log', lat_log)
        setattr(help, 'creation_date', func.now())

        try:
            session.merge(help)
            session.commit()
        except:
            session.rollback()
            raise ServerError("Can't update")
        finally:
            session.close()

    return True


@jsonrpc.method('delHelp(user_id=Number,vehicle_id=Number) -> Object', validate=True, authenticated=False)
def delHelp(user_id,vehicle_id):

    session = Session()

    v = session.query(TrVehicle).filter(TrVehicle.id == vehicle_id).filter(TrVehicle.user_id == user_id).first()

    if v is None:
        session.close()
        raise ServerError("Device doesn't exist.")

    if v.help is not None:
        try:
            session.delete(v.help)
            session.commit()
        except:
            session.rollback()
            raise ServerError("Can't delete")
        finally:
            session.close()

    return True


@jsonrpc.method('getHelps(user_id=Number,vehicle_id=Number,lat_log=String) -> Object', validate=True, authenticated=False)
def getHelps(user_id, vehicle_id, lat_log):

    session = Session()

    #TODO:: sql request nearby helps

    helps = []

    help1 = {"message": "Hey guys, What's up!", "lat_log": "54.123,55.1231", "timestamp": 12345678}
    help2 = {"message": u'Тест', "lat_log": "55.123,34.345", "timestamp": 12345678}

    helps.append(help1)
    helps.append(help2)

    session.close()

    return helps


@jsonrpc.method('getGIBDD(user_id=Number,device_id=Number,lat_log=String) -> Object', validate=True, authenticated=False)
def getGIBDD(user_id, device_id, lat_log):

    session = Session()

    gs = []

    g1 = {"name": "ГИБДД", "desc": "ГИБДД Фрязино", "phone": "9266242473"}
    g2 = {"name": "GIBDD", "desc": "Moscow department", "phone": "02"}

    gs.append(g1)
    gs.append(g2)

    return gs


@jsonrpc.method('getEvs(user_id=Number,device_id=Number,lat_log=String) -> Object', validate=True, authenticated=False)
def getEvs(user_id, device_id, lat_log):

    session = Session()

    es = []

    e1 = {
            "name": "Москвовский эвакуатор",
            "logo": app.config.get('TOWS_IMG_URL') + "Angels.png",
            "desc": "Лучший Московский сервис!",
            "phone": "+79266242473",
            "tarif":
                {
                    "auto": 1600,
                    "moto": 1500,
                    "track": 1000,
                    "fail": 100
                }
        }

    e2 = {
            "name": "Авторейнджер",
            "logo": app.config.get('TOWS_IMG_URL') + "Autoranger.png",
            "desc": "The best!",
            "phone": "0402",
            "tarif":
                {
                    "auto": 1600,
                    "moto": 1500,
                    "track": 1000,
                    "fail": 100
                }
        }

    es.append(e1)
    es.append(e2)

    return es
