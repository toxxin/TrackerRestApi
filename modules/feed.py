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

    TODO::Incorrect SQL statement!
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


def s_fillFeedResponse(f, fav):

    ret = {
        "id": f.id,
        "feed_id": f.feed_id,
        "title": f.title,
        "link": f.link,
        "pic": f.pic if f.pic is not None else None,
        "desc": f.desc,
        "fulltext": f.fulltext,
        "published": calendar.timegm(f.published.utctimetuple()),
        "fav": fav
    }

    return ret

@jsonrpc.method('s_getFeedNews(user_id=Number, since=Number) -> Object', validate=True, authenticated=False)
@login_required
def s_getFeedNews(user_id, since):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    t = session.query(association_table_user_feed).filter_by(user_id=uid).subquery('t')
    fs = session.query(TrFeedNews, TrUserFeedFav.id).outerjoin(TrUserFeedFav).filter(TrFeedNews.feed_id == t.c.feed_id).\
                        filter(TrFeedNews.published > datetime.datetime.fromtimestamp(since)).all()

    lst = [s_fillFeedResponse(f[0], f[1] is not None) for f in fs]

    lst = [s_fillFeedResponse(f) for f in fs]

    session.close()

    return lst

@jsonrpc.method('s_addFavFeed(user_id=Number, feed_id=Number, id=Number) -> Object', validate=True, authenticated=False)
def s_addFavFeed(user_id, feed_id, id):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    u_f = session.query(association_table_user_feed).filter_by(user_id=uid).filter_by(feed_id=feed_id).first()
    if u_f is None:
        session.close()
        raise ServerError("User or feed doesn't exist.")

    uf_fav = session.query(TrUserFeedFav).filter_by(uf_id=u_f.id).filter_by(feed_news_id=id).first()

    if uf_fav is None:
        new_fav = TrUserFeedFav(uf_id=u_f.id, feed_news_id=id)

        try:
            session.add(new_fav)
            session.commit()
        except:
            session.rollback()
            raise ServerError("Can't add item to favorites.")
        finally:
            session.close()
    else:
        session.close()

    return True


@jsonrpc.method('s_delFavFeed(user_id=Number, feed_id=Number, id=Number) -> Object', validate=True, authenticated=False)
def s_delFavFeed(user_id, feed_id, id):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    u_f = session.query(association_table_user_feed).filter_by(user_id=uid).filter_by(feed_id=feed_id).first()
    if u_f is None:
        session.close()
        raise ServerError("User or feed doesn't exist.")

    uf_fav = session.query(TrUserFeedFav).filter_by(uf_id=u_f.id).filter_by(feed_news_id=id).first()

    if uf_fav is not None:

        try:
            session.delete(uf_fav)
            session.commit()
        except:
            session.rollback()
            raise ServerError("Can't delete item from favorites.")
        finally:
            session.close()
    else:
        session.close()

    return True


@jsonrpc.method('s_getFavsFeed(user_id=Number, feed_id=Number) -> Object', validate=True, authenticated=False)
def s_getFavsFeed(user_id, feed_id):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    u_f = session.query(association_table_user_feed).filter_by(user_id=uid).filter_by(feed_id=feed_id).first()
    if u_f is None:
        session.close()
        raise ServerError("User or feed doesn't exist.")

    favs = session.query(TrUserFeedFav).filter_by(uf_id=u_f.id).all()

    ret = [f.feed_news_id for f in favs]

    session.close()

    return ret
