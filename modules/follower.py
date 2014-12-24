__author__ = 'Anton Glukhov'

from flask.ext.jsonrpc import ServerError
from TrackerRestApi import Session, jsonrpc
from sqlautocode_gen.model import TrUser, TrFollower


def auth_type(user):
    if user.EXTERNAL_AUTH_ID == None:
        return "native"
    elif user.EXTERNAL_AUTH_ID == "socservices" and user.LOGIN[:3] == "FB_":
        return "fb"
    elif user.EXTERNAL_AUTH_ID == "socservices" and user.LOGIN[:6] == "VKuser":
        return "vk"
    else:
        return "tw"


@jsonrpc.method('getFollowers(user_id=Number) -> Any', validate=True, authenticated=False)
def getFollowers(user_id):
    '''Test user_id: 998'''

    session = Session()

    if session.query(TrUser).get(user_id) is None:
        raise ServerError("User does not exist")

    followers = []

# SELECT *
# FROM tr_follower AS f
#     LEFT JOIN b_user AS u ON u.ID = f.slave_id
# WHERE f.master_id = 998

    t = session.query(TrFollower.slave_id).filter(TrFollower.master_id == user_id).subquery('t')
    query = session.query(TrUser).filter(TrUser.ID == t.c.slave_id)

    for user in query:

        follower = next((x for x in user.masters if x.master_id == user_id), None)
        if follower is None:
            raise ServerError('Internal error')

        followers.append({
                            "id": follower.id,
                            "alias": follower.alias if follower.alias is not None else user.LOGIN,
                            "type": auth_type(user),
                            "login": user.LOGIN,
                            "first_name": "" if user.NAME is None else user.NAME,
                            "last_name": "" if user.LAST_NAME is None else user.LAST_NAME})

    session.close()

    return followers


@jsonrpc.method('delFollower(user_id=Number, follower_id=Number) -> Object', validate=True, authenticated=False)
def delFollower(user_id, follower_id):
    '''Delete follower by id'''

    session = Session()

    if session.query(TrUser).get(user_id) is None:
        raise ServerError("User does not exist")

    follower = session.query(TrFollower).filter_by(id=follower_id).first()

    try:
        session.delete(follower)
        session.commit()
    except:
        session.rollback()
        raise ServerError("Can't delete")
    finally:
        session.close()

    return True


@jsonrpc.method('udateFollower(follower_id=Number) -> Object', validate=True, authenticated=False)
def updateFollower(follower_id):
    '''Not implemented yet'''

    #TODO:: implement updateFollower
    pass