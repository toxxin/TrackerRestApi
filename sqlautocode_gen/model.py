__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

import datetime
from flask.ext.login import make_secure_token
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlautocode_gen import DeclarativeBase
from sqlautocode_gen.feed_model import association_table_user_feed


class TrUser(DeclarativeBase):
    __tablename__ = 'b_user'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #column definitions
    ACTIVE = Column(u'ACTIVE', CHAR(length=1, collation=u'utf8_unicode_ci'), nullable=False)
    ADMIN_NOTES = Column(u'ADMIN_NOTES', TEXT(collation=u'utf8_unicode_ci'))
    AUTO_TIME_ZONE = Column(u'AUTO_TIME_ZONE', CHAR(length=1, collation=u'utf8_unicode_ci'))
    CHECKWORD = Column(u'CHECKWORD', VARCHAR(length=50, collation=u'utf8_unicode_ci'))
    CHECKWORD_TIME = Column(u'CHECKWORD_TIME', DATETIME())
    CONFIRM_CODE = Column(u'CONFIRM_CODE', VARCHAR(length=8, collation=u'utf8_unicode_ci'))
    DATE_REGISTER = Column(u'DATE_REGISTER', DATETIME(), nullable=False)
    EMAIL = Column(u'EMAIL', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    EXTERNAL_AUTH_ID = Column(u'EXTERNAL_AUTH_ID', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    ID = Column(u'ID', INTEGER(), primary_key=True, nullable=False)
    LAST_ACTIVITY_DATE = Column(u'LAST_ACTIVITY_DATE', DATETIME())
    LAST_LOGIN = Column(u'LAST_LOGIN', DATETIME())
    LAST_NAME = Column(u'LAST_NAME', VARCHAR(length=50, collation=u'utf8_unicode_ci'))
    LID = Column(u'LID', CHAR(length=2, collation=u'utf8_unicode_ci'))
    LOGIN = Column(u'LOGIN', VARCHAR(length=50, collation=u'utf8_unicode_ci'), nullable=False)
    LOGIN_ATTEMPTS = Column(u'LOGIN_ATTEMPTS', INTEGER())
    NAME = Column(u'NAME', VARCHAR(length=50, collation=u'utf8_unicode_ci'))
    PASSWORD = Column(u'PASSWORD', VARCHAR(length=50, collation=u'utf8_unicode_ci'), nullable=False)
    PERSONAL_BIRTHDATE = Column(u'PERSONAL_BIRTHDATE', VARCHAR(length=50, collation=u'utf8_unicode_ci'))
    PERSONAL_BIRTHDAY = Column(u'PERSONAL_BIRTHDAY', DATE())
    PERSONAL_CITY = Column(u'PERSONAL_CITY', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    PERSONAL_COUNTRY = Column(u'PERSONAL_COUNTRY', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    PERSONAL_FAX = Column(u'PERSONAL_FAX', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    PERSONAL_GENDER = Column(u'PERSONAL_GENDER', CHAR(length=1, collation=u'utf8_unicode_ci'))
    PERSONAL_ICQ = Column(u'PERSONAL_ICQ', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    PERSONAL_MAILBOX = Column(u'PERSONAL_MAILBOX', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    PERSONAL_MOBILE = Column(u'PERSONAL_MOBILE', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    PERSONAL_NOTES = Column(u'PERSONAL_NOTES', TEXT(collation=u'utf8_unicode_ci'))
    PERSONAL_PAGER = Column(u'PERSONAL_PAGER', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    PERSONAL_PHONE = Column(u'PERSONAL_PHONE', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    PERSONAL_PHOTO = Column(u'PERSONAL_PHOTO', INTEGER())
    PERSONAL_PROFESSION = Column(u'PERSONAL_PROFESSION', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    PERSONAL_STATE = Column(u'PERSONAL_STATE', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    PERSONAL_STREET = Column(u'PERSONAL_STREET', TEXT(collation=u'utf8_unicode_ci'))
    PERSONAL_WWW = Column(u'PERSONAL_WWW', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    PERSONAL_ZIP = Column(u'PERSONAL_ZIP', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    SECOND_NAME = Column(u'SECOND_NAME', VARCHAR(length=50, collation=u'utf8_unicode_ci'))
    STORED_HASH = Column(u'STORED_HASH', VARCHAR(length=32, collation=u'utf8_unicode_ci'))
    TIMESTAMP_X = Column(u'TIMESTAMP_X', TIMESTAMP(), nullable=False)
    TIME_ZONE = Column(u'TIME_ZONE', VARCHAR(length=50, collation=u'utf8_unicode_ci'))
    TIME_ZONE_OFFSET = Column(u'TIME_ZONE_OFFSET', INTEGER())
    WORK_CITY = Column(u'WORK_CITY', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    WORK_COMPANY = Column(u'WORK_COMPANY', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    WORK_COUNTRY = Column(u'WORK_COUNTRY', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    WORK_DEPARTMENT = Column(u'WORK_DEPARTMENT', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    WORK_FAX = Column(u'WORK_FAX', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    WORK_LOGO = Column(u'WORK_LOGO', INTEGER())
    WORK_MAILBOX = Column(u'WORK_MAILBOX', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    WORK_NOTES = Column(u'WORK_NOTES', TEXT(collation=u'utf8_unicode_ci'))
    WORK_PAGER = Column(u'WORK_PAGER', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    WORK_PHONE = Column(u'WORK_PHONE', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    WORK_POSITION = Column(u'WORK_POSITION', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    WORK_PROFILE = Column(u'WORK_PROFILE', TEXT(collation=u'utf8_unicode_ci'))
    WORK_STATE = Column(u'WORK_STATE', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    WORK_STREET = Column(u'WORK_STREET', TEXT(collation=u'utf8_unicode_ci'))
    WORK_WWW = Column(u'WORK_WWW', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    WORK_ZIP = Column(u'WORK_ZIP', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    XML_ID = Column(u'XML_ID', VARCHAR(length=255, collation=u'utf8_unicode_ci'))

    #relation definitions
    # slaves = relationship("TrFollower", foreign_keys="TrFollower.master_id", cascade="all,delete")
    # masters = relationship("TrFollower", foreign_keys="TrFollower.slave_id", cascade="all,delete")

    # locations = relationship("TrULocation", foreign_keys="TrULocation.user_id", cascade="all,delete")

    vehicles = relationship("TrVehicle", foreign_keys="TrVehicle.user_id", cascade="all,delete")

    tokens = relationship("TrPushToken", foreign_keys="TrPushToken.user_id", cascade="all,delete")

    feeds = relationship("TrFeed", secondary=association_table_user_feed)

    places = relationship("TrPlace", foreign_keys="TrPlace.user_id", cascade="all,delete")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.ID)

    def __init__(self, date, login, password, active='Y'):
        self.DATE_REGISTER = date
        self.ACTIVE = active
        self.LOGIN = login
        self.PASSWORD = password


class TrUserTest(DeclarativeBase):
    __tablename__ = 'tr_user'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False)
    active = Column(u'active', CHAR(length=1, collation=u'utf8_unicode_ci'), nullable=False)
    authenticated = Column(u'authenticated', Boolean, nullable=False)
    login = Column(u'login', VARCHAR(length=50, collation=u'utf8_unicode_ci'), nullable=False)
    auth_code = Column(u'auth_code', CHAR(length=4), nullable=False)
    last_modified = Column(u'last_modified', TIMESTAMP(), nullable=False, onupdate=func.now())
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())
    token = Column(u'token', VARCHAR(length=255, collation=u'utf8_unicode_ci'))
    session = Column(u'session', VARCHAR(length=255, collation=u'utf8_unicode_ci'))

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True if self.active == 'Y' else False

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def get_auth_token(self):
        return make_secure_token("123456")

    def __init__(self, login, auth_code, active='Y', authenticated=False, token=None, session=None):
        self.login = login
        self.auth_code = auth_code
        self.active = active
        self.token = token
        self.session = session


class TrVehicle(DeclarativeBase):
    __tablename__ = 'tr_vehicle'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #column definitions
    id = Column(u'id', Integer, primary_key=True)
    name = Column(u'name', String(20), nullable=False)
    pic = Column(u'pic', String(20), nullable=True)
    type = Column(u'type', CHAR(1), nullable=False)
    year = Column(u'year', Integer, nullable=False)
    car_model_id = Column(u'car_model_id', Integer, ForeignKey('tr_avto_dggr.id'), nullable=False)
    #moto_model_id = Column(u'moto_model_id', Integer, ForeignKey(''), nullable=False)
    car_sts = Column(u'car_sts', String(20), nullable=True)
    car_number = Column(u'car_number', String(10), nullable=True)
    last_modified = Column(u'last_modified', TIMESTAMP(), nullable=False, onupdate=func.now())
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())
    user_id = Column(u'user_id', Integer, ForeignKey('b_user.ID'), nullable=False)

    #relation definitions
    device = relationship("TrDevice", foreign_keys="TrDevice.vehicle_id", uselist=False)
    help = relationship("TrHelp", foreign_keys="TrHelp.vehicle_id", uselist=False, cascade="all,delete")

    def __init__(self, name, user_id, car_model_id, year, type='A', pic=None):
        self.name = name
        self.pic = pic
        self.year = year
        self.type = type
        self.car_model_id = car_model_id
        self.user_id = user_id


class TrDevice(DeclarativeBase):
    __tablename__ = 'tr_device'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #column definitions
    id = Column(u'id', Integer, primary_key=True, nullable=False)
    accel_stat = Column(u'accel_stat', Boolean, nullable=False, default=False)
    hash = Column(u'hash', String(50), nullable=False)
    hw_version = Column(u'hw_version', SmallInteger, nullable=False)
    sw_version = Column(u'sw_version', SMALLINT(), nullable=False)
    imei_number = Column(u'imei_number', String(64), unique=True, nullable=False)
    phone1 = Column(u'phone1', String(12))
    phone2 = Column(u'phone2', String(12))
    server1 = Column(u'server1', String(64))
    server2 = Column(u'server2', String(64))
    simcardid = Column(u'simcardid', Integer, nullable=True)
    sms_pass = Column(u'sms_pass', String(4), nullable=False, default="1234")
    sn = Column(u'sn', String(20), unique=True, nullable=False)
    secret_code = Column(u'secret_code', String(20), nullable=False)
    stat = Column(u'stat', Boolean, nullable=False, default=False)
    time_interval = Column(u'time_interval', SmallInteger, nullable=False, default=15)
    type = Column(u'type', SmallInteger)
    last_modified = Column(u'last_modified', TIMESTAMP(), nullable=False, onupdate=func.now())
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())
    vehicle_id = Column(u'vehicle_id', Integer, ForeignKey('tr_vehicle.id', ondelete='SET NULL'), unique=True, nullable=True)

    #relation definitions
    locations = relationship("TrDLocation", foreign_keys="TrDLocation.device_id", cascade="all,delete")
    geos = relationship("TrDGeozone", foreign_keys="TrDGeozone.device_id", cascade="all,delete")

    def __init__(self, sn, imei_number, secter_code='password', hash='123', hw_version=1, sw_version=1, simcardid='3322', sms_pass='1234',
                 stat=False, time_interval=15, type=1, accel_stat=None, server1=None, server2=None,
                 phone1=None, phone2=None, vehicle_id=None):
        self.accel_stat = accel_stat
        self.hash = hash
        self.hw_version = hw_version
        self.sw_version = sw_version
        self.imei_number = imei_number
        self.server1 = server1
        self.server2 = server2
        self.phone1 = phone1
        self.phone2 = phone2
        self.simcardid = simcardid
        self.sms_pass = sms_pass
        self.sn = sn
        self.secret_code = secter_code
        self.stat = stat
        self.time_interval = time_interval
        self.type = type
        self.vehicle_id = vehicle_id


# class TrEvent(DeclarativeBase):
#     __tablename__ = 'tr_event'
#
#     __table_args__ = {'mysql_engine': 'InnoDB'}
#
#     #column definitions
#     event_ID = Column(u'event_ID', INTEGER(), primary_key=True)
#     event_deviceID = Column(u'event_deviceID', INTEGER(), nullable=False)
#     #FIXME:: boolean type
#     event_stat = Column(u'event_stat', Integer(), nullable=False)
#
#     #relation definitions
#     tr_geozone = relationship("TrGeozone", uselist=False, backref="tr_event", cascade="delete")
#
# class TrGeozone(DeclarativeBase):
#     __tablename__ = 'tr_geozone'
#
#     __table_args__ = {'mysql_engine': 'InnoDB'}
#
#     #column definitions
#     geozone_ID = Column(u'geozone_ID', INTEGER(), primary_key=True, nullable=False)
#     geozone_center = Column(u'geozone_center', VARCHAR(length=20), nullable=False)
#     geozone_color = Column(u'geozone_color', VARCHAR(length=12), nullable=False)
#     geozone_eventID = Column(u'geozone_eventID', INTEGER(), ForeignKey('tr_event.event_ID'))
#     geozone_name = Column(u'geozone_name', VARCHAR(length=20), nullable=False)
#     geozone_radius = Column(u'geozone_radius', INTEGER(), nullable=False)
#
#     def __init__(self, id):
#         self.geozone_ID = id
#
#     def __repr__(self):
#         return "<User(id='%d', name='%s', radius='%d', center='%s')>" % \
#                                     (self.geozone_ID, self.geozone_name, self.geozone_radius, self.geozone_center)


'''Shape params:    0: circle, 1: square, 2: random'''
class TrDGeozone(DeclarativeBase):
    __tablename__ = 'tr_dgeozone'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #column definitions
    id = Column(u'id', Integer, primary_key=True)
    name = Column(u'name', String(20), nullable=False)
    state = Column(u'state', Boolean, nullable=False)
    shape = Column(u'shape', SmallInteger, nullable=False)
    center = Column(u'center', String(20), nullable=False)
    radius = Column(u'radius', Integer, nullable=False)
    color = Column(u'color', String(7), nullable=False)
    last_modified = Column(u'last_modified', TIMESTAMP(), nullable=False, onupdate=func.now())
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())
    device_id = Column(u'device_id', Integer, ForeignKey('tr_device.id'), nullable=False)

    def __init__(self, name, device_id, state=True, shape=0, center="55.7500,37.6167", radius=100, color="#00ff00"):
        self.name = name
        self.state = state
        self.shape = shape
        self.center = center
        self.radius = radius
        self.color = color
        self.device_id = device_id

    def __repr__(self):
        return "<FGeo(id='%d', name='%s', shape='%d', center='%s', radius='%d', color='%s')>" % \
                                        (self.id, self.name, self.shape, self.center, self.radius, self.color)



# '''Shape params:    0: circle, 1: square, 2: random'''
# class TrFGeozone(DeclarativeBase):
#     __tablename__ = 'tr_fgeozone'
#
#     __table_args__ = {'mysql_engine': 'InnoDB'}
#
#     #column definitions
#     id = Column(u'id', Integer, primary_key=True)
#     name = Column(u'name', String(20), nullable=False)
#     state = Column(u'state', Boolean, nullable=False)
#     shape = Column(u'shape', SmallInteger, nullable=False)
#     center = Column(u'center', String(20), nullable=False)
#     radius = Column(u'radius', Integer, nullable=False);
#     color = Column(u'color', String(7), nullable=False)
#
#     follower_id = Column(u'follower_id', Integer, ForeignKey('tr_follower.id'), nullable=False)
#
#     def __init__(self, center, name = "NewGeo", state = True, shape = 0, radius = 100, color = "#00ff00"):
#         self.name = name
#         self.state = state
#         self.shape = shape
#         self.center = center
#         self.radius = radius
#         self.color = color
#
#     def __repr__(self):
#         return "<FGeo(id='%d', name='%s', shape='%d', center='%s', radius='%d', vertices='%s', color='%s')>" % \
#                                         (self.id, self.name, self.shape, self.center, self.radius, self.vertices, self.color)


class TrDLocation(DeclarativeBase):
    __tablename__ = 'tr_dlocation'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #column definitions
    id = Column(u'id', Integer, primary_key=True)
    lat_log = Column(u'lat_log', String(20), nullable=False)
    altitude = Column(u'altitude', String(20))
    accuracy = Column(u'accuracy', Integer)
    speed = Column(u'speed', SmallInteger)
    creation_date = Column(u'creation_date', TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)
    device_id = Column(u'device_id', Integer, ForeignKey('tr_device.id'), nullable=False)

    def __init__(self, lat_log, creation_date, device_id, altitude=null, accuracy=null, speed=null):
        self.lat_log = lat_log
        self.altitude = altitude
        self.accuracy = accuracy
        self.speed = speed
        self.creation_date = creation_date
        self.device_id = device_id

    def __repr__(self):
        return "<DLocation(id='%d', lat_log='%s', altitude='%d', accuracy='%d', speed='%d', creation_date='%s', device_id='%d')>" % \
                                        (self.id, self.lat_log, self.altitude, self.accuracy, self.speed, self.creation_date, self.device_id)


# class TrULocation(DeclarativeBase):
#     __tablename__ = 'tr_ulocation'
#
#     __table_args__ = {'mysql_engine': 'InnoDB'}
#
#     #colomn definition
#     id = Column(u'id', Integer, primary_key=True)
#     lat_log = Column(u'lat_log', String(20), nullable=False)
#     accuracy = Column(u'accuracy', Integer, nullable=False)
#     battery = Column(u'battery', SmallInteger, nullable=True)
#     speed = Column(u'speed', SmallInteger, nullable=True)
#     creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())
#     user_id = Column(u'user_id', Integer, ForeignKey('b_user.ID'), nullable=False)
#
#     def __init__(self, lat_log, accuracy, creation_date, user_id, battery=null, speed=null):
#         self.lat_log = lat_log
#         self.accuracy = accuracy
#         self.battery = battery
#         self.speed = speed
#         self.creation_date = creation_date
#         self.user_id = user_id
#
#     def __repr__(self):
#         return "UserLocation(id='%d', lat_log='%s', accuracy='%d' creation_date='%s', user_id='%d')>" % \
#                 (self.id, self.lat_log, self.accuracy, self.creation_date, self.user_id)
#
#
# class TrFollower(DeclarativeBase):
#     __tablename__ = 'tr_follower'
#
#     __table_args__ = {'mysql_engine': 'InnoDB'}
#
#     #colomn definition
#     id = Column(u'id', Integer, primary_key=True)
#     alias = Column(u'alias', String(20), nullable=True)
#     state = Column(u'state', Boolean, nullable=False)
#     master_id = Column(u'master_id', Integer, ForeignKey('b_user.ID'), nullable=False)
#     slave_id = Column(u'slave_id', Integer, ForeignKey('b_user.ID'), nullable=False)
#     hw_id = Column(u'hw_id', String(20))
#
#     #relation definitions
#     geos = relationship("TrFGeozone", backref="tr_follower", cascade="all,delete")


class TrPushToken(DeclarativeBase):
    __tablename__ = 'tr_ptoken'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    id = Column(u'id', Integer, primary_key=True)
    hardware_id = Column(u'hardware_id', String(40), nullable=False)
    platform = Column(u'platform', CHAR(length=1), nullable=False)
    token = Column(u'token', Text(4096), nullable=False)
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())
    user_id = Column(u'user_id', Integer, ForeignKey('b_user.ID'), nullable=False)

    def __init__(self, hardware_id, platform, token, user_id):
        self.hardware_id = hardware_id
        self.platform = platform
        self.token = token
        self.user_id = user_id


class TrHelp(DeclarativeBase):
    __tablename__ = 'tr_help'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    id = Column(u'id', Integer, primary_key=True)
    message = Column(u'message', String(140), nullable=False)
    lat_log = Column(u'lat_log', String(20), nullable=False)
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())
    vehicle_id = Column(u'vehicle_id', Integer, ForeignKey('tr_vehicle.id'), nullable=False)

    def __init__(self, message, lat_log, vehicle_id):
        self.message = message
        self.lat_log = lat_log
        self.vehicle_id = vehicle_id


class TrRoadNews(DeclarativeBase):
    __tablename__ = 'tr_roadnews'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    id = Column(u'id', Integer, primary_key=True)
    title = Column(u'title', String(255), nullable=False)
    link = Column(u'link', String(255))
    desc = Column(u'desc', UnicodeText, nullable=False)
    fulltext = Column(u'fulltext', UnicodeText)
    latitude = Column(u'latitude', DECIMAL(precision=10, scale=8))
    longitude = Column(u'longitude', DECIMAL(precision=11, scale=8))
    pic = Column(u'pic', String(20))
    tag = Column(u'tag', String(255))
    last_modified = Column(u'last_modified', TIMESTAMP(), nullable=False, onupdate=func.now())
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())

    def __init__(self, title, link, desc, ftext, latitude=None, longitude=None, pic=None, tag=None,):
        self.title = title
        self.link = link
        self.desc = desc
        self.ftext = ftext
        self.latitude = latitude
        self.longitude = longitude
        self.pic = pic
        self.tag = tag


class TrPlace(DeclarativeBase):
    __tablename__ = 'tr_place'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    id = Column(u'id', Integer, primary_key=True)
    title = Column(u'title', String(255), nullable=False)
    desc = Column(u'desc', UnicodeText)
    longitude = Column(u'longitude', DECIMAL(precision=11, scale=8))
    latitude = Column(u'latitude', DECIMAL(precision=10, scale=8))
    type = Column(u'type', String(30), nullable=False)
    last_modified = Column(u'last_modified', TIMESTAMP(), nullable=False, onupdate=func.now())
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())
    user_id = Column(u'user_id', Integer, ForeignKey('b_user.ID'), nullable=False)

    def __init__(self, user_id, title, longitude, latitude, type, desc=None):
        self.title = title
        self.longitude = longitude
        self.latitude = latitude
        self.type = type
        self.desc = desc
        self.user_id = user_id

# try:
#     TrPushToken.__table__.drop(engine)
# except:
#     pass
# metadata.create_all(engine)

# try:
#     TrTestGeozone.__table__.drop(engine)
# except:
#     pass
# metadata.create_all(engine)

# try:
#     TrFGeozone.__table__.drop(engine)
# except:
#     pass
# metadata.create_all(engine)


# try:
#     TrDGeozone.__table__.drop(engine)
#     TrDLocation.__table__.drop(engine)
#     TrPushToken.__table__.drop(engine)
#     TrHelp.__table__.drop(engine)
#     TrDevice.__table__.drop(engine)
#     TrVehicle.__table__.drop(engine)
#     TrFeed.__table__.drop(engine)
# except:
#     pass
# metadata.create_all(engine)
