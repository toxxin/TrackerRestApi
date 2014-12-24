# -*- coding: utf8 -*-
__author__ = 'Anton Glukhov'


from flask.ext.login import login_required, login_user

from TrackerRestApi import jsonrpc
from TrackerRestApi import Session

from flask_jsonrpc import ServerError
from sqlautocode_gen.model import *


@jsonrpc.method('addPushToken(user_id=Number,hardware_id=String,platform=String,token=String) -> Object', validate=True, authenticated=False)
def addPushToken(user_id,hardware_id,platform,token):

    session = Session()

    push = session.query(TrPushToken).filter(TrPushToken.user_id == user_id).filter(TrPushToken.hardware_id == hardware_id).first()

    if push is None:
        """Add new push token"""
        p = TrPushToken(hardware_id=hardware_id,
                        platform=platform,
                        token=token,
                        user_id=user_id)

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