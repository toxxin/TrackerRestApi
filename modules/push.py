# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"


from flask.ext.login import login_required, current_user

from TrackerRestApi import jsonrpc
from TrackerRestApi import Session

from flask_jsonrpc import ServerError
from sqlautocode_gen.model import *


@jsonrpc.method('addPushToken(user_id=Number,hardware_id=String,platform=String,token=String) -> Object', validate=True, authenticated=False)
@login_required
def addPushToken(user_id,hardware_id,platform,token):

    session = Session()

    push = session.query(TrPushToken).filter(TrPushToken.user_id == int(current_user.get_id())).filter(TrPushToken.hardware_id == hardware_id).first()

    if push is None:
        """Add new push token"""
        p = TrPushToken(hardware_id=hardware_id,
                        platform=platform,
                        token=token,
                        user_id=int(current_user.get_id()))

        try:
            session.add(p)
            session.commit()
        except:
            session.rollback()
            raise ServerError("Can't add push token.")
        finally:
            session.close()

    else:
        """Update existing token"""

        push.hardware_id=hardware_id
        push.platform=platform
        push.token=token

        try:
            session.merge(push)
            session.commit()
        except:
            session.rollback()
            raise ServerError("Can't update")
        finally:
            session.close()

    return True
