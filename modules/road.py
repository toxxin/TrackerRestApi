__author__ = 'Anton Glukhov'


import calendar

from flask.ext.login import login_required, login_user

from TrackerRestApi import jsonrpc, app
from TrackerRestApi import Session

from flask_jsonrpc import ServerError
from sqlautocode_gen.model import *


def fillNews(n):

    print n.creation_date
    ret = {
        "id": n.id,
        "title": n.title,
        "link": n.link,
        "pic": app.config.get('ROADS_IMG_URL') + n.pic if n.pic is not None else n.pic,
        "desc": n.desc,
        "ftext": n.fulltext,
        "tags": n.tag,
        "location": str(n.latitude) + ',' + str(n.longitude) if n.latitude is not None and n.longitude is not None else None,
        "timestamp": calendar.timegm(n.creation_date.utctimetuple())
    }

    return ret


@jsonrpc.method('getRoad(user_id=Number,since=Number) -> Object', validate=True, authenticated=False)
def getRoad(user_id, since):

    session = Session()

    news = session.query(TrRoadNews).filter(TrRoadNews.creation_date > datetime.datetime.fromtimestamp(since)).all()

    lst = [fillNews(n) for n in news]

    return lst