__author__ = 'Anton Glukhov'

import calendar

from flask.ext.login import login_required, login_user

from TrackerRestApi import jsonrpc, app
from TrackerRestApi import Session

from flask_jsonrpc import ServerError
from sqlautocode_gen.model import *
from sqlautocode_gen.feed_model import TrFeed, TrFeedNews, TrFavFeed, TrFavFeedTest


def fillFeedResponse(feed):

    ret = {
        "id": feed.id,
        "title": feed.title,
        "link": feed.link,
        "pic": app.config.get('FEEDS_IMG_URL') + feed.pic if feed.pic is not None else feed.pic
    }

    return ret

@jsonrpc.method('getFeeds(user_id=Number) -> Any', validate=True, authenticated=False)
def getFeeds(user_id):

    session = Session()

    u = session.query(TrUser).filter(TrUser.ID == user_id).first()

    if u is None:
        session.close()
        raise ServerError("User doesn't exist.")

    lst = [fillFeedResponse(f) for f in u.feeds]

    session.close()

    return lst


@jsonrpc.method('getAllFeeds(user_id=Number, type=String) -> Object', validate=False, authenticated=False)
def getAllFeeds(user_id, type=None):

    session = Session()

    if type is None:
        feeds = session.query(TrFeed).all()
    else:
        feeds = session.query(TrFeed).filter(TrFeed.type == type).all()

    lst = [fillFeedResponse(f) for f in feeds]

    session.close()

    return lst


@jsonrpc.method('subFeed(user_id=Number, feed_id=Number) -> Object', validate=True, authenticated=False)
def subFeed(user_id, feed_id):

    session = Session()

    u = session.query(TrUser).filter(TrUser.ID == user_id).first()

    if u is None:
        session.close()
        raise ServerError("User doesn't exist.")

    f = session.query(TrFeed).filter(TrFeed.id == feed_id).first()

    if f is None:
        session.close()
        raise ServerError("Feed doesn't exist.")

    u.feeds.append(f)
    session.commit()

    session.close()

    return True


@jsonrpc.method('unsubFeed(user_id=Number, feed_id=Number) -> Object', validate=True, authenticated=False)
def unsubFeed(user_id, feed_id):

    session = Session()

    u = session.query(TrUser).filter(TrUser.ID == user_id).first()

    if u is None:
        session.close()
        raise ServerError("User doesn't exist.")

    for f in u.feeds:

        if f.id == feed_id:
            u.feeds.remove(f)
            session.commit()
            break

    session.close()

    return True


@jsonrpc.method('addFavFeed(user_id=Number, feed_id=Number, link=String) -> Object', validate=True, authenticated=False)
def addFavFeed(user_id, feed_id, link):

    session = Session()

    u_f = session.query(association_table_user_feed).filter_by(user_id = user_id).filter_by(feed_id = feed_id).first()

    if u_f is None:
        session.close()
        raise ServerError("User or feed doesn't exist.")

    fav = TrFavFeed(link=link, user_feed_id=u_f.id)

    try:
        session.add(fav)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't add item to favorites.")
    finally:
        session.close()

    return True


@jsonrpc.method('s_addFavFeed(user_id=Number, feed_id=Number, id=Number) -> Object', validate=True, authenticated=False)
def s_addFavFeed(user_id, feed_id, id):

    session = Session()

    u_f = session.query(association_table_user_feed).filter_by(user_id = user_id).filter_by(feed_id = feed_id).first()

    if u_f is None:
        session.close()
        raise ServerError("User or feed doesn't exist.")

    fav = TrFavFeedTest(u_f.user_id, u_f.feed_id, id)

    try:
        session.add(fav)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't add item to favorites.")
    finally:
        session.close()


@jsonrpc.method('delFavFeed(user_id=Number, feed_id=Number, link=String) -> Object', validate=True, authenticated=False)
def delFavFeed(user_id, feed_id, link):

    session = Session()

    t = session.query(association_table_user_feed).filter_by(user_id = user_id).filter_by(feed_id = feed_id).subquery('t')
    fav = session.query(TrFavFeed).filter(TrFavFeed.user_feed_id == t.c.id).filter(TrFavFeed.link == link).first()

    if fav is None:
        session.close()
        raise ServerError("Fav item doesn't exist.")

    try:
        session.delete(fav)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't delete item from favorites.")
    finally:
        session.close()

    return True


@jsonrpc.method('s_delFavFeed(user_id=Number, feed_id=Number, id=Number) -> Object', validate=True, authenticated=False)
def s_delFavFeed(user_id, feed_id, id):

    session = Session()

    fav = session.query(TrFavFeedTest).filter(TrFavFeedTest.u_id == user_id).\
                                        filter(TrFavFeedTest.f_id == feed_id).\
                                        filter(TrFavFeedTest.p_id == id).first()

    if fav is None:
        session.close()
        raise ServerError("Fav item doesn't exist.")

    try:
        session.delete(fav)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't delete item from favorites.")
    finally:
        session.close()

    return True


@jsonrpc.method('getFavsFeed(user_id=Number, feed_id=Number) -> Object', validate=True, authenticated=False)
def getFavsFeed(user_id, feed_id):

    session = Session()

    t = session.query(association_table_user_feed).filter_by(user_id = user_id).filter_by(feed_id = feed_id).subquery('t')
    favs = session.query(TrFavFeed).filter(TrFavFeed.user_feed_id == t.c.id).all()

    ret = [f.link for f in favs]

    session.close()

    return ret


@jsonrpc.method('s_getFavsFeed(user_id=Number, feed_id=Number) -> Object', validate=True, authenticated=False)
def s_getFavsFeed(user_id, feed_id):

    session = Session()

    favs = session.query(TrFavFeedTest).filter(TrFavFeedTest.u_id == user_id).\
                                        filter(TrFavFeedTest.f_id == feed_id).all()

    ret = [f.p_id for f in favs]

    session.close()

    return ret


def s_fillFeedResponse(f):

    ret = {
        "id": f.id,
        "feed_id": f.feed_id,
        "title": f.title,
        "link": f.link,
        "pic": f.pic if f.pic is not None else None,
        "desc": f.desc,
        "fulltext": f.fulltext,
        "pub_date": calendar.timegm(f.pub_date.utctimetuple())
    }

    return ret


@jsonrpc.method('s_getFeeds(user_id=Number, since=Number) -> Any', validate=True, authenticated=False)
def s_getFeeds(user_id, since):

    session = Session()

    t = session.query(association_table_user_feed).filter_by(user_id=user_id).subquery('t')
    fs = session.query(TrFeedNews).filter(TrFeedNews.feed_id == t.c.feed_id).\
                                    filter(TrFeedNews.pub_date > datetime.datetime.fromtimestamp(since)).all()

    lst = [s_fillFeedResponse(f) for f in fs]

    session.close()

    return lst