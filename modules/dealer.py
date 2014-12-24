__author__ = 'Anton Glukhov'


from flask.ext.login import login_required, login_user

from TrackerRestApi import jsonrpc, app
from TrackerRestApi import Session

from flask_jsonrpc import ServerError
from sqlautocode_gen.model import *
from sqlautocode_gen.dealers_model import *
from sqlautocode_gen.tbl_02_models import *

from tools.pygeotools import GeoLocation


def fillDealerResponse(dl):

    ret = {
        "id": dl.id,
        "maker": dl.maker,
        "pic": app.config.get('MAKERS_IMG_URL') + dl.maker + '.png' if dl.maker is not None else dl.maker,
        "region": dl.region,
        "name": dl.name,
        "address": dl.address,
        "phone": dl.phone,
        "site": dl.site,
        "desc": dl.desc,
        "working_time": dl.working_time,
        "service": dl.service,
        "test_drive": dl.test_drive,
        "second_auto": dl.second_auto,
        "trade_in": dl.trade_in,
        "lat": dl.latitude,
        "lon": dl.longitude
    }

    return ret


@jsonrpc.method('getAllDealers(user_id=Number) -> Any', validate=True, authenticated=False)
def getAllDealers(user_id):

    session = Session()

    dls = session.query(TrDealer).all()

    if dls is None:
        session.close()
        raise ServerError("Dealers were not found.")

    ret = [fillDealerResponse(dl) for dl in dls]

    session.close()

    return ret


def f7(seq):
    """ Delete duplicates in a list """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


@jsonrpc.method('getDealers(user_id=Number, vehicle_id=Number, location=String, radius=Number) -> Object', validate=True, authenticated=False)
def getDealers(user_id, vehicle_id, location, radius):

    session = Session()

    v = session.query(TrVehicle).filter(TrVehicle.user_id == user_id).\
        filter(TrVehicle.id == vehicle_id).first()

    if v is None:
        session.close()
        raise ServerError("Vehicle doesn't exist.")

    lat_lon = location.split(',')
    base_point = GeoLocation.from_degrees(float(lat_lon[0]), float(lat_lon[1]))
    sw, ne = base_point.bounding_locations(radius)

    print sw.deg_lat
    print sw.deg_lon
    print ne.deg_lat
    print ne.deg_lon

    ds = session.query(TrDealer).filter(TrDealer.maker == v.car_model.marka_name).\
                                filter(TrDealer.latitude > sw.deg_lat).filter(TrDealer.longitude > sw.deg_lon).\
                                filter(TrDealer.latitude < ne.deg_lat).filter(TrDealer.longitude < ne.deg_lon).all()

    ret = [fillDealerResponse(d) for d in ds]

    session.close()

    return ret