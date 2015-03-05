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

    vehicles = relationship("TrVehicle", foreign_keys="TrVehicle.user_id", cascade="all,delete")

    tokens = relationship("TrPushToken", foreign_keys="TrPushToken.user_id", cascade="all,delete")

    feeds = relationship("TrFeed", secondary=association_table_user_feed)

    places = relationship("TrPlace", foreign_keys="TrPlace.user_id", cascade="all,delete")

    groups = relationship("TrGroup", foreign_keys="TrGroup.user_id", cascade="all,delete")

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        # return True if self.active == 'Y' else False
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def get_auth_token(self):
        return make_secure_token("123456")

    def __init__(self, login, auth_code, active='Y', authenticated=False, token=None, session=None):
        self.login = login
        self.authenticated = authenticated
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
    user_id = Column(u'user_id', Integer, ForeignKey('tr_user.id'), nullable=False)

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


class TrPushToken(DeclarativeBase):
    __tablename__ = 'tr_ptoken'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    id = Column(u'id', Integer, primary_key=True)
    hardware_id = Column(u'hardware_id', String(40), nullable=False)
    platform = Column(u'platform', CHAR(length=1), nullable=False)
    token = Column(u'token', Text(4096), nullable=False)
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())
    user_id = Column(u'user_id', Integer, ForeignKey('tr_user.id'), nullable=False)

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
    user_id = Column(u'user_id', Integer, ForeignKey('tr_user.id'), nullable=False)

    def __init__(self, user_id, title, longitude, latitude, type, desc=None):
        self.title = title
        self.longitude = longitude
        self.latitude = latitude
        self.type = type
        self.desc = desc
        self.user_id = user_id


class TrRegion(DeclarativeBase):
    __tablename__ = 'tr_region'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    id = Column(u'id', Integer, primary_key=True)
    title = Column(u'title', String(255), nullable=False)
    region_ids = Column(u'region_ids', String(255), nullable=False)
    last_modified = Column(u'last_modified', TIMESTAMP(), nullable=False, onupdate=func.now())
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())

    def __init__ (self, title, region_ids):
        self.title = title
        self.region_ids = region_ids


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
