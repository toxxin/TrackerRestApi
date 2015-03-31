# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

import calendar

from flask.ext.login import login_required, current_user

from TrackerRestApi import jsonrpc, app
from TrackerRestApi import Session

from flask_jsonrpc import ServerError
from sqlautocode_gen.model import *
from sqlautocode_gen.feed_model import TrFeed, TrFeedNews, TrFavFeed, TrFavFeedTest


def fillFeedResponse(feed, sub):

    ret = {
        "id": feed.id,
        "title": feed.title,
        "link": feed.link,
        "pic": app.config.get('FEEDS_IMG_URL') + feed.pic if feed.pic is not None else feed.pic,
        "sub": sub
    }

    return ret


@jsonrpc.method('s_getFeeds(user_id=Number) -> Any', validate=True, authenticated=False)
@login_required
def s_getFeeds(user_id):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    u = session.query(TrUser).filter(TrUser.id == uid).first()
    if u is None:
        session.close()
        raise ServerError("User doesn't exist.")

    feeds = session.query(TrFeed, association_table_user_feed).outerjoin(association_table_user_feed).all()

    lst = [fillFeedResponse(f[0], f[1] is not None) for f in feeds]

    session.close()

    return lst


@jsonrpc.method('s_subFeed(user_id=Number, feed_id=Number) -> Object', validate=True, authenticated=False)
@login_required
def s_subFeed(user_id, feed_id):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    u = session.query(TrUser).filter(TrUser.id == uid).first()
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


@jsonrpc.method('s_unsubFeed(user_id=Number, feed_id=Number) -> Object', validate=True, authenticated=False)
@login_required
def s_unsubFeed(user_id, feed_id):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    u = session.query(TrUser).filter(TrUser.id == user_id).first()
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

@jsonrpc.method('s_getFeedNews(user_id=Number, since=Number) -> Object', validate=True, authenticated=False)
@login_required
def s_getFeedNews(user_id, since):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    t = session.query(association_table_user_feed).filter_by(user_id=uid).subquery('t')
    fs = session.query(TrFeedNews).filter(TrFeedNews.feed_id == t.c.feed_id).\
                                    filter(TrFeedNews.pub_date > datetime.datetime.fromtimestamp(since)).all()

    lst = [s_fillFeedResponse(f) for f in fs]

    session.close()

    return lst
