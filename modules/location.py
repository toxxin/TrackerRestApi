__author__ = 'Anton Glukhov'

import time
from copy import deepcopy

from flask_jsonrpc import ServerError

from tools.pygeotools import GeoLocation
from TrackerRestApi import jsonrpc
from TrackerRestApi import Session
from sqlautocode_gen.model import *


@jsonrpc.method('addLocation(user_id=Number, points=Any) -> Object', validate=True, authenticated=False)
def addLocation(user_id, points):

    session = Session()

    if session.query(TrUser).get(user_id) is None:
        raise ServerError("User does not exist")

    if len(points) <= 0:
        raise ServerError("Points is empty.")

    location = []

    for point in points:
        location.append(TrULocation(lat_log=point['location'], accuracy=point['accuracy'],
                creation_time=datetime.datetime.fromtimestamp(int(point['timestamp'])).strftime('%Y-%m-%d %H:%M:%S'),
                battery=point['properties'].get('battery'),
                speed=point['properties'].get('speed'),
                user_id=user_id))

    try:
        session.add_all(location)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't add new locations")
    finally:
        session.close()

    return True


@jsonrpc.method('getFLocation(user_id=Number, follower_id=Number, since=Number) -> Object', validate=True, authenticated=False)
def getFLocation(user_id, follower_id, since):

    session = Session()

    if session.query(TrUser).get(user_id) is None:
        raise ServerError("User does not exist")

    lst = []

    t = session.query(TrFollower.slave_id).filter(TrFollower.id == follower_id).\
                                            filter(TrFollower.master_id == user_id).subquery('t')
    locs = session.query(TrULocation).filter(TrULocation.user_id == t.c.slave_id).\
                                        filter(TrULocation.creation_time > datetime.datetime.fromtimestamp(since)).all()

    for loc in locs:
        lst.append({
                    "lat_log": loc.lat_log,
                    "creation_date": int(loc.creation_time.strftime("%s")),
                    # "timestamp": loc.creation_time.strptime("%Y-%m-%d %H:%M:%S"),
                    "sensors": {"battery": loc.battery}})

    session.close()

    return lst


@jsonrpc.method('getDLocation(user_id=Number, device_id=Number, since=Number) -> Object', validate=True, authenticated=False)
def getDLocation(user_id, device_id, since):

    session = Session()

    if session.query(TrUser).get(user_id) is None:
        raise ServerError("User does not exist")

    lst = []

    locs = session.query(TrDLocation).join(TrDevice, TrDLocation.device_id == TrDevice.device_ID).\
                            filter(TrDLocation.device_id == device_id).\
                            filter(TrDLocation.creation_time > datetime.datetime.fromtimestamp(since)).\
                            filter(TrDevice.device_userID == user_id).all()

    for loc in locs:
        lst.append({
                    "lat_log": loc.lat_log,
                    "creation_date": int(loc.creation_time.strftime("%s")),
                    "speed": loc.speed,
                    "sensors": {
                        "battery": 10,
                        "accel": True,
                        "temp": -19}
        })

    session.close()

    return lst


def duration(cl):
    if len(cl) > 1:
        c = sorted(cl, key=lambda k: k['t'])
        return c[-1]['t'] - c[0]['t']
    else:
        return datetime.timedelta(0)


def get_mean(cl):

    if len(cl) > 1:
        xs = [loc['x'] for loc in cl]
        ys = [loc['y'] for loc in cl]

        xmean = round(reduce(lambda x, y: x+y, xs)/len(cl), 6)
        ymean = round(reduce(lambda x, y: x+y, ys)/len(cl), 6)

        return {'x': xmean, 'y': ymean, 't': cl[0]['t']}

    elif len(cl) == 1:
        return {'x': cl[0]['x'], 'y': cl[0]['y'], 't': cl[0]['t']}

    else:
        pass # TODO:: add exception!


def distance(a, b):

    loc1 = GeoLocation.from_degrees(a['x'], a['y'])
    loc2 = GeoLocation.from_degrees(b['x'], b['y'])

    return round(loc1.distance_to(loc2)*1000)


@jsonrpc.method('getPoints(user_id=Number, follower_id=Number) -> Object', validate=True, authenticated=False)
def getPoints(user_id, follower_id):

    session = Session()

    if session.query(TrUser).get(user_id) is None:
        raise ServerError("User does not exist")

    t = session.query(TrFollower.slave_id).filter(TrFollower.id == follower_id).\
                                            filter(TrFollower.master_id == user_id).subquery('t')
    locs = session.query(TrULocation).filter(TrULocation.user_id == t.c.slave_id).\
                                        filter(TrULocation.creation_time > datetime.datetime.fromtimestamp(round(time.time() - 86400))).all()

    r = [{"x": float(loc.lat_log.split(',')[0]), "y": float(loc.lat_log.split(',')[1]), "t": loc.creation_time} for loc in locs]

    if len(r) <= 3:
        return []

    # cl - cluster
    # plocs - pending locations
    # places - significant places

    # d - max distance cl to new point
    # t - threshold duration

    cl = []
    plocs = []
    places = []

    d = 200     # 200m
    t = 60*15   # 15min

    cl.append(r[0])

    r = r[1:]
    print len(r)

    for loc in r:
        if distance(get_mean(cl), loc) < d:
            cl.append(loc)
        else:
            if len(plocs) > 1:
                if duration(cl) > datetime.timedelta(seconds=t):
                    places.append(deepcopy(cl))
                del cl[:]
                cl.append(plocs[-1])
                del plocs[:]
                if distance(get_mean(cl), loc) < d:
                    cl.append(loc)
                    del plocs[:]
                else:
                    plocs.append(loc)
            else:
                plocs.append(loc)

    if duration(cl) > datetime.timedelta(seconds=t):
        places.append(deepcopy(cl))

    result = []

    for cl in places:
        mean = get_mean(cl)
        loc = str(mean['x']) + ',' + str(mean['y'])
        result.append({"geoname": "test",
                                 "address": None,
                                 "timein": int(cl[0]['t'].strftime("%s")),
                                 "timeout": int(cl[-1]['t'].strftime("%s")),
                                 "location": loc})

    session.close()

    return result
