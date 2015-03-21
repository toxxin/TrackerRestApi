# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

import random
import string
import urllib2, urllib
import datetime
import xml.etree.ElementTree as ET

import facebook
import twitter

from flask.ext.jsonrpc import ServerError
from flask.ext.login import login_user, login_required, logout_user, current_user
from sqlautocode_gen.model import TrUser, TrPushToken

from TrackerRestApi import jsonrpc, app
from TrackerRestApi import Session


@jsonrpc.method('getCode(number=String) -> Any', validate=True, authenticated=False)
def getCode(number):

    session = Session()

    sms = SmsEpochta()
    code = ''.join(random.choice(string.digits) for _ in range(app.config.get('SMS_CODE_LEN')))

    u = session.query(TrUser).filter(TrUser.login == number).first()

    if u is None:
        u = TrUser(login=number, auth_code=code, active='N')
        session.add(u)
    else:
        setattr(u, 'auth_code', code)
        setattr(u, 'active', 'N')
        session.merge(u)

    try:
        session.commit()
        session.refresh(u)
    except:
        session.rollback()
        raise ServerError("Can't generate new code.")
    finally:
        session.close()

    sms.send(number, code)

    return u.id


@jsonrpc.method('login(id=Number, code=String, platform=String, hw_id=String, reg_id=String) -> Object', validate=True, authenticated=False)
def login(id, code, platform, hw_id, reg_id):

    if platform not in ["A", "a", "I", "i"]:
        raise ServerError("Incorrect platform.")

    s = Session()

    u = s.query(TrUser).filter(TrUser.id == id).first()

    if u is None:
        s.close()
        raise ServerError("User doesn't exist.")

    #TODO:: expired date of code
    exp = int((datetime.datetime.now() - u.last_modified).total_seconds())
    print exp
    if exp > app.config['SMS_CODE_LIFETIME']:
        s.close()
        raise ServerError("Invalid code.")

    if u.auth_code == code:
        u.authenticated = True
        s.merge(u)
        s.commit()
        login_user(u)

    """Save token for push notification"""
    pt = s.query(TrPushToken).filter(TrPushToken.platform == platform.upper()).\
                                filter(TrPushToken.hardware_id == hw_id).first()
    if pt is None:
        pt = TrPushToken(hw_id, platform.upper(), reg_id, id)
        s.add(pt)
        s.commit()
    else:
        setattr(pt, 'hardware_id', hw_id)
        setattr(pt, 'token', reg_id)
        setattr(pt, 'user_id', id)
        s.merge(pt)
        s.commit()

    s.close()

    return True


def __authUser(s, login, type, platform, hw_id, reg_id):

    print "Auth user"
    u = s.query(TrUser).filter(TrUser.login == login).filter(TrUser.type == type).first()
    if u is None:
        """ Create new user """
        print "Add new user"
        u = TrUser(login=login, type=type, auth_code="9999", authenticated=True)
        try:
            s.add(u)
            s.flush()
            s.refresh(u)
            pt = s.query(TrPushToken).filter(TrPushToken.hardware_id == hw_id).filter(TrPushToken.platform == platform.upper()).first()
            if pt is None:
                pt = TrPushToken(hardware_id=hw_id, platform=platform, token=reg_id, user_id=u.id)
                s.add(pt)
            else:
                setattr(pt, 'token', reg_id)
                setattr(pt, 'user_id', u.id)
                s.merge(pt)
            s.commit()
        except:
            s.rollback()
            raise Exception("Can't add new user.")
    else:
        """ Update existed user """
        print "user exists"
        pt = s.query(TrPushToken).filter(TrPushToken.hardware_id == hw_id).filter(TrPushToken.platform == platform.upper()).first()
        try:
            if pt is None:
                pt = TrPushToken(hardware_id=hw_id, platform=platform, token=reg_id, user_id=u.id)
                s.add(pt)
            else:
                setattr(pt, 'token', reg_id)
                setattr(pt, 'user_id', u.id)
                s.merge(pt)
            s.commit()
        except:
            s.rollback()
            raise Exception("Can't update user data.")

    login_user(u)
    return u.id


@jsonrpc.method('login_soc(type=String, tkn=String, tkn_secret=String, platform=String, hw_id=String, reg_id=String) -> Object', validate=True, authenticated=False)
def login_soc(type, tkn, tkn_secret, platform, hw_id, reg_id):

    if platform not in ["A", "a", "I", "i"]:
        raise ServerError("Incorrect platform.")

    s = Session()

    if type.lower() == "fb":
        graph = facebook.GraphAPI(tkn)
        try:
            profile = graph.get_object("me")
            print profile
            login = "fb_" + profile['id']
        except:
            s.close()
            raise ServerError("Incorrect credentials.")
    elif type.lower() == "tw":
        try:
            tw = twitter.Api(consumer_key=app.config.get('TWITTER_CONSUMER_KEY'),
                          consumer_secret=app.config.get('TWITTER_CONSUMER_SECRET'),
                          access_token_key=tkn,
                          access_token_secret=tkn_secret)
            prof = tw.VerifyCredentials()
            login = "tw_" + str(prof.id)
        except:
            s.close()
            raise ServerError("Incorrect credentials.")
    elif type.lower() == "vk":
        pass
    else:
        s.close()
        raise ServerError("Incorrect type.")

    try:
        return __authUser(s=s, login=login, type=type, platform=platform, hw_id=hw_id, reg_id=reg_id)
    except:
        raise ServerError("Can't auth user.")
    finally:
        s.close()


@jsonrpc.method('logout() -> Any', validate=True, authenticated=False)
@login_required
def logout():
    s = Session()
    u = current_user
    u.authenticated = False
    s.merge(u)
    s.commit()
    s.close()
    logout_user()
    return True


class SmsProvider(object):

    login = ""
    password = ""

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def send(self, number, message):
        raise NotImplementedError('Method send() is pure virtual')

    def status(self, mes_id):
        raise NotImplementedError('Method status() is pure virtual')

    def balance(self):
        raise NotImplementedError('Method balance() is pure virtual')


class SmsEpochta(SmsProvider):

    def __init__(self, login=app.config.get('SMS_LOGIN'), password=app.config.get('SMS_PASS')):
        super(SmsEpochta, self).__init__(login, password)

    def send(self, number, message):

        mes_id = "123456"

        send_sms = '''<?xml version="1.0" encoding="UTF-8"?>
        <SMS>
        <operations>
        <operation>SEND</operation>
        </operations>
        <authentification>
        <username>%s</username>
        <password>%s</password>
        </authentification>
        <message>
        <sender>SMS</sender>
        <text>%s</text>
        </message>
        <numbers>
        <number messageID="%s">%s</number>
        </numbers>
        </SMS>''' % (self.login, self.password, message, mes_id, number)

        senddata=[('XML',send_sms)]
        senddata=urllib.urlencode(senddata)
        path='http://atompark.com/members/sms/xml.php'
        req=urllib2.Request(path, senddata)
        req.add_header("Content-type", "application/x-www-form-urlencoded")
        result=urllib2.urlopen(req).read()

        root = ET.fromstring(result)
        r = {c.tag: c.text for c in root}

        app.logger.debug('sms: send: %s' % r)

    def get_status(self, mes_id):

        get_sms_status = '''<?xml version="1.0" encoding="UTF-8"?>
        <SMS>
        <operations>
        <operation>GETSTATUS</operation>
        </operations>
        <authentification>
        <username>%s</username>
        <password>%s</password>
        </authentification>
        <statistics>
        <messageid>%s</messageid>
        </statistics>
        </SMS>''' % (self.login, self.password, mes_id)

        senddata=[('XML',get_sms_status)]
        senddata=urllib.urlencode(senddata)
        path='http://my.atompark.com/sms/xml.php'
        req=urllib2.Request(path, senddata)
        req.add_header("Content-type", "application/x-www-form-urlencoded")
        result=urllib2.urlopen(req).read()

        root = ET.fromstring(result)
        r = {c.tag: c.text for c in root}

        app.logger.debug('sms: status: %s' % r)

    def balance(self):

        get_balance = '''<?xml version="1.0" encoding="UTF-8"?>
        <SMS>
        <operations>
        <operation>BALANCE</operation>
        </operations>
        <authentification>
        <username>%s</username>
        <password>%s</password>
        </authentification>
        </SMS>''' % (self.login, self.password)

        senddata=[('XML',get_balance)]
        senddata=urllib.urlencode(senddata)
        path='http://my.atompark.com/sms/xml.php'
        req=urllib2.Request(path, senddata)
        req.add_header("Content-type", "application/x-www-form-urlencoded")
        result=urllib2.urlopen(req).read()

        root = ET.fromstring(result)
        r = {c.tag: c.text for c in root}

        app.logger.debug('sms: balance: %s' % r)

    # def get_price(self):
    #
    #     get_send_price = '''<?xml version="1.0" encoding="UTF-8"?>
    #     <SMS>
    #     <operations>
    #     <operation>GETPRICE</operation>
    #     </operations>
    #     <authentification>
    #     <username>%s</username>
    #     <password>%s</password>
    #     </authentification>
    #     <message>
    #     <sender>SMS</sender>
    #     <text>Test message [UTF-8]</text>
    #     </message>
    #     <numbers>
    #     <number messageID="%s">%s</number>
    #     </numbers>
    #     </SMS>''' % (self.login, self.password, phone_sms, msg_id)
    #
    #     senddata=[('XML',get_send_price)]
    #     senddata=urllib.urlencode(senddata)
    #     path='http://my.atompark.com/sms/xml.php'
    #     req=urllib2.Request(path, senddata)
    #     req.add_header("Content-type", "application/x-www-form-urlencoded")
    #     result=urllib2.urlopen(req).read()
    #     print result


@jsonrpc.method('getProfile(user_id=Number) -> Any', validate=True, authenticated=False)
@login_required
def getProfile(user_id):

    session = Session()

    uid = int(current_user.get_id()) if app.config.get('LOGIN_DISABLED') is False else user_id

    u = session.query(TrUser).get(uid)

    if u is None:
        session.close()
        raise ServerError("User doesn't exist.")

    ret = {
        "login": u.login,
        "pic": app.config.get('PROFILE_IMG_URL') + u.pic if u.pic is not None else u.pic
    }

    session.close()

    return ret


@app.route('/test', methods=['POST', 'GET'])
@login_required
def test():
    return 'Test'


@jsonrpc.method('testSession(id=Number) -> Any', validate=True, authenticated=False)
@login_required
def testSession(id):
    return True
