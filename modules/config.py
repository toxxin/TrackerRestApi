__author__ = 'Anton Glukhov'

from TrackerRestApi import jsonrpc, Session
from sqlautocode_gen.model import TrFollower
from flask.ext.jsonrpc import ServerError


@jsonrpc.method('getConfig(user_id=Number) -> Any', validate=True, authenticated=False)
def getConfig(user_id):

    conf = {
                "updates_on":               True,
                "accuracy":                 200,
                "server_update_sec":        300,
                "location_update_sec":      60
    }

    return conf


@jsonrpc.method('getConfigTest(hw_id=String) -> Any', validate=True, authenticated=False)
def getConfigTest(hw_id):

    session = Session()

    followers = session.query(TrFollower).filter(TrFollower.master_id == 998).\
                                filter(TrFollower.slave_id > 963).\
                                filter(TrFollower.slave_id < 975).all()

    x = [int(f.slave_id) for f in followers if f.hw_id == hw_id]
    if len(x) == 1:
        user_id = x[0]
    elif len(x) == 0:
        folls = [f for f in followers if f.hw_id is None]
        if len(folls) == 0:
            # no available slots for testers
            raise ServerError("Can't add new tester. No available slots.")
        else:
            foll = folls[0]
            setattr(foll, 'hw_id', hw_id)
            try:
                session.merge(foll)
                session.commit()
                user_id = foll.slave_id
            except:
                session.rollback()
                raise ServerError("Can't update. Server is unavailable.")
            finally:
                session.close()
    else:
        raise ServerError("Double hw_id.")


    conf = {
                "user_id":                  user_id,
                "accuracy":                 200,
                "updates_on":               True,
                "server_update_sec":        300,
                "location_update_sec":      60
    }

    return conf