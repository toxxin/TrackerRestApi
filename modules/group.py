# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

import calendar

from flask.ext.login import login_required, current_user

from TrackerRestApi import jsonrpc, app
from TrackerRestApi import Session

from flask_jsonrpc import ServerError, InvalidParamsError
from sqlautocode_gen.model import *
from sqlautocode_gen.group_model import TrGroup, association_table_user_group

from modules import group_mandatory_params, group_option_params


def fillGroupResponse(g, admin=False):

    ret = {
        "id": g.id,
        "title": g.title,
        "desc": g.desc,
        "pic": app.config.get('GROUP_IMG_URL') + g.pic if g.pic is not None else g.pic,
        "timestamp": calendar.timegm(g.creation_date.utctimetuple()),
        "admin": admin
    }

    return ret


@jsonrpc.method('getGroups(user_id=Number) -> Any', validate=True, authenticated=False)
@login_required
def getGroups(user_id):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    t = session.query(association_table_user_group).filter_by(user_id=uid).subquery('t')
    gs = session.query(TrGroup).filter(TrGroup.id == t.c.group_id).all()

    lst = [fillGroupResponse(g) for g in gs]

    gsa = session.query(TrGroup).filter(TrGroup.user_id == uid).all()

    lst_admin = [fillGroupResponse(ga, True) for ga in gsa]

    return lst + lst_admin


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


def isAllIncluded(S1, S2):
    """Return True if all values from list S1 are included in list S2"""
    return False if len(set(S1).intersection(S2)) != len(set(S1)) else True


@jsonrpc.method('updateGroup(user_id=Number, id=Number, title=String,desc=String,invitation=Boolean,meeting=Boolean,help=Boolean) -> Object', validate=False, authenticated=False)
@login_required
def updateGroup(user_id, id, **kwargs):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    t = session.query(association_table_user_group).filter(association_table_user_group.user_id == uid).\
                                                    filter(association_table_user_group.group_id == id).subquery('t')
    g = session.quiry(TrGroup).filter(TrGroup.id == t.c.group_id)

    if g is None:
        session.close()
        raise ServerError("Group doesn't exist.")

    if not isAllIncluded(kwargs.keys(), group_mandatory_params + group_option_params):
        session.close()
        raise InvalidParamsError("Incorrect parameters.")

    for k,v in kwargs.iteritems():
        setattr(g, k, v)

    try:
        session.merge(g)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't update group.")
    finally:
        session.close()

    return True


@jsonrpc.method('delGroup(user_id=Number,id=Number) -> Object', validate=True, authenticated=False)
@login_required
def delGroup(user_id, id):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    g = session.query(TrGroup).filter(TrGroup.id == id).filter(TrGroup.user_id == uid).first()

    if g is None:
        session.close()
        raise ServerError("Group doesn't exist.")

    try:
        session.delete(g)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't delete group.")
    finally:
        session.close()

    return True


@jsonrpc.method('getAccList(user_id=Number,list=String) -> Object', validate=True, authenticated=False)
@login_required
def getAccList(user_id, list):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    us = session.quiry(TrUser).filter(TrUser.login.in_(list.split(','))).all()

    lst = [u.login for u in us]

    session.close()

    return lst


def fillGroupMessageResponse(m):

    ret = {
        "id": m.id,
        "date": m.creation_date,
        "message": m.message,
        "user":
            {
                "id": u.id,
                "login": u.login,
                "pic": app.config.get('PROFILE_IMG_URL') + u.pic if u.pic is not None else u.pic
            }
    }

    return ret
    
@jsonrpc.method('getComments(user_id=Number,group_id=Number) -> Object', validate=True, authenticated=False)
@login_required
def getComments(user_id, group_id):

    session = Session()
    
    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    t = session.query(association_table_user_group).filter(association_table_user_group.user_id == uid).\
                                                    filter(association_table_user_group.group_id == group_id).subquery('t')
    ms = session.query(TrGroupComment).filter(TrGroupComment.user_group_id == t.c.id).all()

    lst = [fillGroupMessageResponse(m, current_user) for m in ms]
    
    session.close()
    
    return lst
    
    
@jsonrpc.method('addComment(user_id=Number,group_id=Number,message=String) -> Object', validate=True, authenticated=False)
@login_required
def addComment(user_id, group_id, message):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id
    
    t = session.quiry(association_table_user_group).filter(association_table_user_group.user_id == uid).\
                                                    filter(association_table_user_group.group_id == id).first()
    if t is None:
        session.close()
        raise ServerError("Group doesn't exist.")

    m = TrGroupComment(message=message, user_group_id=t.id)

    try:
        session.add(m)
        session.commit()
        session.refresh(m)
    except:
        session.rollback()
        raise ServerError("Can't add message.")
    finally:
        session.close()
        
    return m.id
    
    
@jsonrpc.method('delComment(user_id=Number,group_id=Number,id=Number) -> Object', validate=True, authenticated=False)
@login_required
def delComment(user_id, group_id, id):

    session = Session()
    
    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id
    
    t = session.query(association_table_user_group).filter(association_table_user_group.user_id == uid).\
                                                    filter(association_table_user_group.group_id == group_id).subquery('t')
    m = session.query(TrGroupComment).filter(TrGroupComment.user_group_id == t.c.id).\
                                        filter(TrGroupComment.id == id).first()

    if m is None:
        session.close()
        raise ServerError("Message doesn't exist.")

    try:
        session.delete(m)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't delete message.")
    finally:
        session.close()

    return True
