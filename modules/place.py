# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

from flask.ext.login import login_required, current_user

from TrackerRestApi import jsonrpc
from TrackerRestApi import Session

from flask_jsonrpc import ServerError, InvalidParamsError
from sqlautocode_gen.model import *

from modules import *


def fillPlaceResponse(place):

    ret = {
        "id": place.id,
        "title": place.title,
        "desc": place.desc if place.desc is not None else None,
        "longitude": place.longitude,
        "latitude": place.latitude,
        "type": place.type
    }

    return ret


place_types = ["hotel", "restaurant", "cafe"]


@jsonrpc.method('getPlaces(user_id=Number) -> Any', validate=True, authenticated=False)
@login_required
def getPlaces(user_id):

    session = Session()

    pls = session.query(TrPlace).filter(TrPlace.user_id == int(current_user.get_id())).all()

    lst = [fillPlaceResponse(p) for p in pls]

    session.close()

    return lst


@jsonrpc.method('addPlace(user_id=Number, title=String, longitude=String, latitude=String, type=String, desc=String) -> Object', validate=True, authenticated=False)
@login_required
def addPlace(user_id, title, longitude, latitude, type, desc):

    session = Session()

    p = TrPlace(user_id=int(current_user.get_id()), title=title, longitude=float(longitude), latitude=float(latitude), type=type, desc=desc)

    try:
        session.add(p)
        session.commit()
        session.refresh(p)
    except:
        session.rollback()
        raise ServerError("Can't add place.")
    finally:
        session.close()

    return p.id


@jsonrpc.method('delPlace(user_id=Number, place_id=Number) -> Object', validate=True, authenticated=False)
@login_required
def delPlace(user_id, place_id):

    session = Session()

    p = session.query(TrPlace).filter(TrPlace.user_id == int(current_user.get_id())).filter(TrPlace.id == place_id).first()

    if p is None:
        session.close()
        raise ServerError("Place doesn't exist.")

    try:
        session.delete(p)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't delete place.")
    finally:
        session.close()

    session.close()

    return True


def isAllIncluded(S1, S2):
    """Return True if all values from list S1 are included in list S2"""
    return False if len(set(S1).intersection(S2)) != len(set(S1)) else True

@jsonrpc.method('updatePlace(user_id=Number, place_id=Number, title=String, longitude=String, latitude=String, type=String, desc=String) -> Object', validate=False, authenticated=False)
@login_required
def updatePlace(user_id, place_id, **kwargs):

    session = Session()

    p = session.query(TrPlace).filter(TrPlace.user_id == int(current_user.get_id())).filter(TrPlace.id == place_id).first()

    if p is None:
        session.close()
        raise ServerError("Place doesn't exist.")

    """check all params"""
    if not isAllIncluded(kwargs.keys(), place_mandatory_params + place_option_params):
        session.close()
        raise InvalidParamsError("Incorrect parameters.")

    for k,v in kwargs.iteritems():
        setattr(p, k, v)

    try:
        session.merge(p)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't update place.")
    finally:
        session.close()

    return True
