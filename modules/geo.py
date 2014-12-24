__author__ = 'Anton Glukhov'

from TrackerRestApi import jsonrpc
from TrackerRestApi import Session

from flask_jsonrpc import ServerError, InvalidParamsError

from sqlautocode_gen.model import *


from modules import *


@jsonrpc.method('getDGeos(user_id=Number, device_id=Number) -> Object', validate=True, authenticated=False)
def getDGeos(user_id, device_id):

    session = Session()

    dev = session.query(TrDevice).filter(TrDevice.device_userID == user_id).all()

    if dev is None:
        raise ServerError("Device doesn't exist.")

    t = session.query(TrDevice.device_ID).filter(TrDevice.device_ID == device_id).\
                                            filter(TrDevice.device_userID == user_id).subquery('t')
    geos = session.query(TrDGeozone).filter(TrDGeozone.device_id == t.c.device_ID)

    lst = []

    for geo in geos:
        ret = {
            "id":       geo.id,
            "name":     geo.name,
            "shape":     geo.shape,
            "radius":   geo.radius,
            "center":   geo.center,
            "color":    geo.color,
            "state":     bool(geo.state)}
        lst.append(ret)

    session.close()

    return lst


@jsonrpc.method('updateDGeo(user_id=Number, id=Number, name=String, center=String, color=String, radius=Number, state=Boolean) -> Any',
                        validate=False, authenticated=False)
def updateDGeo(user_id=null, id=null, **kwargs):

    session = Session()

    t = session.query(TrDevice.device_ID).filter(TrDevice.device_userID == user_id).subquery('t')
    geo = session.query(TrDGeozone).filter(TrDGeozone.device_id == t.c.device_ID).filter(TrDGeozone.id == id).first()

    if geo is None:
        session.close()
        raise ServerError("Geozone doesn't exist.")

    """check all params"""
    if not isAllIncluded(kwargs.keys(), geo_mandatory_params + geo_option_params):
        session.close()
        raise InvalidParamsError("Incorrect parameters.")

    # for k,v in kwargs.iteritems():
    #     if k not in geo_params:
    #         session.close()
    #         raise ServerError("Incorrect arg: %s" % k)

    for k,v in kwargs.iteritems():
        setattr(geo, k, v)

    try:
        session.merge(geo)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't update")
    finally:
        session.close()

    return True


@jsonrpc.method('delDGeo(user_id=Number, id=Number) -> Object', validate=True, authenticated=False)
def delDGeo(user_id, id):

    session = Session()

    t = session.query(TrDevice.device_ID).filter(TrDevice.device_userID == user_id).subquery('t')
    geo = session.query(TrDGeozone).filter(TrDGeozone.device_id == t.c.device_ID).filter(TrDGeozone.id == id).first()

    if geo is None:
        session.close()
        raise ServerError("Geozone doesn't exist.")

    try:
        print 'delete geo %s' % geo.id
        session.delete(geo)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't delete")
    finally:
        session.close()

    return True


def isAllIncluded(S1, S2):
    """Return True if all values from list S1 are included in list S2"""
    return False if len(set(S1).intersection(S2)) != len(set(S1)) else True

# isAllIncluded = lambda s1, s2: len(set(s1)) == len(set(s1).intersection(set(s2)))


@jsonrpc.method('addDGeo(name=String, shape=Number, center=String, color=String, radius=Number, state=Boolean, device_id=Number) -> Any', validate=False, authenticated=False)
def addDGeo(user_id=null, device_id=null, **kwargs):

    # 1. check that user_id has device_id
    # 2. check that all params from list
    # 3. check mandatory params

    session = Session()

    if user_id == null or device_id == null:
        session.close()
        raise InvalidParamsError("user_id or device_id is not specified.")

    """check if user exist and has such device"""
    dev = session.query(TrDevice).filter(TrDevice.device_ID == device_id) \
                                    .filter(TrDevice.device_userID == user_id).first()
    if dev is None:
        session.close()
        raise ServerError("Incorrect user or device.")

    """check all params"""
    if not isAllIncluded(kwargs.keys(), geo_mandatory_params + geo_option_params):
        session.close()
        raise InvalidParamsError("Incorrect parameters.")

    """check mandatory params"""
    if not isAllIncluded(geo_mandatory_params, kwargs.keys()):
        session.close()
        raise InvalidParamsError("Incorrect mandatory parameters.")

    # check special params
    if kwargs['shape'] == GEO_SHAPE_RANDOM:
        pass
        # # if checkParams(kwargs.keys(), geo_test_params_must_for_rand) == True:
        # S1 = set(geo_test_params_must_for_rand)
        # S2 = set(kwargs.keys())
        #
        # if len(S1.intersection(S2)) != len(S1):
        #     session.close()
        #     raise ServerError("Incorrect parameters")
        # else:
        #     # add geozone!

    elif kwargs['shape'] == GEO_SHAPE_CIRCUS or kwargs['shape'] == GEO_SHAPE_SQUARE:

        geo = TrDGeozone(device_id=device_id,
                         name=kwargs['name'],
                         shape=kwargs['shape'],
                         center=kwargs['center'],
                         radius=kwargs['radius'],
                         color=kwargs['color'] if 'color' in kwargs else "#ff00ff",
                         state=kwargs['state'] if 'state' in kwargs else True)

        try:
            session.add(geo)
            session.commit()
        except:
            session.rollback()
            raise ServerError("Can't add geo.")
        finally:
            session.close()

        return True

    else:
        session.close()
        raise ServerError("Incorrect value for shape")


@jsonrpc.method('getFGeos(user_id=Number, follower_id=Number) -> Any', validate=True, authenticated=False)
def getFGeos(user_id, follower_id):

    session = Session()

    if session.query(TrUser).get(user_id) is None:
        raise ServerError("User does not exist")

    follower = session.query(TrFollower).filter(TrFollower.id == follower_id).first()

    if follower is None:
        raise ServerError('Follower does not exist')

    lst = []

    for geo in follower.geos:
        lst.append({
            "id": geo.id,
            "name": geo.name,
            "state": geo.state,
            "shape": geo.shape,
            "center": geo.center,
            "radius": geo.radius,
            "color": geo.color
        })

    session.close()

    return lst
