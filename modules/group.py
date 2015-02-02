# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

from flask.ext.login import login_required, current_user

from TrackerRestApi import jsonrpc, app
from TrackerRestApi import Session

from flask_jsonrpc import ServerError
from sqlautocode_gen.model import *
from sqlautocode_gen.group_model import TrGroup, association_table_user_group


def fillGroupResponse(g):

    ret = {
        "id": g.id,
        "title": g.title,
        "desc": g.desc,
        "pic": app.config.get('GROUP_IMG_URL') + g.pic if g.pic is not None else g.pic
    }

    return ret


@jsonrpc.method('getGroups(user_id=Number) -> Any', validate=True, authenticated=False)
@login_required
def getGroups(user_id):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    t = session.query(association_table_user_group).filter_by(user_id=uid).subquery('t')
    gs = session.query(TrGroup).filter(TrGroup.group_id == t.c.id).all()

    lst = [fillGroupResponse(g) for g in gs]

    return lst


@jsonrpc.method('addGroup(user_id=Number,title=String,desc=String,invitation=Boolean,meeting=Boolean,help=Boolean) -> Object', validate=True, authenticated=False)
@login_required
def addGroup(user_id, title, desc, invitation, meeting, help):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    g = TrGroup(title=title, desc=desc, invitation=invitation, meeting=meeting, help=help)

    try:
        session.add(g)
        session.commit()
        session.refresh(g)
    except:
        session.rollback()
        raise ServerError("Can't add group.")
    finally:
        session.close()

    return g.id
