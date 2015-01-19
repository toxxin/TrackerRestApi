# -*- coding: utf-8 -*-
__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

import random
import string
from TrackerRestApi import jsonrpc, app
from TrackerRestApi import Session


CODE_LEN = 4


@jsonrpc.method('getCode(number=String) -> Any', validate=True, authenticated=False)
def getCode(number):

    login = ""
    password = ""

    phone_sms = ""
    msg_id = ""

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
    <text>3305</text>
    </message>
    <numbers>
    <number messageID=""></number>
    </numbers>
    </SMS>''' % (login, password)
    # ''.join(random.choice(string.digits) for _ in range(CODE_LEN))
    import urllib2, urllib
    senddata=[('XML',send_sms)]
    senddata=urllib.urlencode(senddata)
    path='http://atompark.com/members/sms/xml.php'
    req=urllib2.Request(path, senddata)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    result=urllib2.urlopen(req).read()
    print result

    return True

# @jsonrpc.method('getToken(number=Number, code=Code) -> Any', validate=True, authenticated=False)
# def getToken(number, code):
#     pass


@jsonrpc.method('getBalance(number=String) -> Any', validate=True, authenticated=False)
def getBalance(number):

    login = ""
    password = ""

    phone_sms = ""
    msg_id = ""

    get_balance = '''<?xml version="1.0" encoding="UTF-8"?>
    <SMS>
    <operations>
    <operation>BALANCE</operation>
    </operations>
    <authentification>
    <username>%s</username>
    <password>%s</password>
    </authentification>
    </SMS>''' % (login, password)

    import urllib2, urllib
    senddata=[('XML',get_balance)]
    senddata=urllib.urlencode(senddata)
    path='http://my.atompark.com/sms/xml.php'
    req=urllib2.Request(path, senddata)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    result=urllib2.urlopen(req).read()
    print result

    return True
