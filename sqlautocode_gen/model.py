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
    type = Column(u'type', VARCHAR(length=45, collation=u'utf8_unicode_ci'), nullable=False)

    vehicles = relationship("TrVehicle", foreign_keys="TrVehicle.user_id", cascade="all,delete")

    tokens = relationship("TrPushToken", foreign_keys="TrPushToken.user_id", cascade="all,delete")

    feeds = relationship("TrFeed", secondary=association_table_user_feed)

    places = relationship("TrPlace", foreign_keys="TrPlace.user_id", cascade="all,delete")

    groups = relationship("TrGroup", foreign_keys="TrGroup.user_id", cascade="all,delete")
    
    locations = relationship("TrUserLocation", foreign_keys="TrUserLocation.user_id", cascade="all,delete")

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

    def __init__(self, login, auth_code, type, active='Y', authenticated=False, token=None, session=None):
        self.login = login
        self.authenticated = authenticated
        self.auth_code = auth_code
        self.active = active
        self.token = token
        self.session = session
        self.type = type


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


class TrPushToken(DeclarativeBase):
    __tablename__ = 'tr_ptoken'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    id = Column(u'id', Integer, primary_key=True)
    hardware_id = Column(u'hardware_id', String(255), nullable=False, unique=True)
    platform = Column(u'platform', CHAR(length=1), nullable=False)
    token = Column(u'token', Text(4096), nullable=False)
    last_modified = Column(u'last_modified', TIMESTAMP(), nullable=False, onupdate=func.now())
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


class TrVehicleTax(DeclarativeBase):
    __tablename__ = 'tr_vehicle_tax'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    id = Column(u'id', Integer, primary_key=True)
    tax = Column('tax', UnicodeText, nullable=False)
    last_modified = Column(u'last_modified', TIMESTAMP(), nullable=False, onupdate=func.now())
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())
    region_id = Column(u'region_id', Integer, ForeignKey('tr_region.id'), nullable=False)

    def __init__ (self, tax, region_id):
        self.title = tax
        self.region_id = region_id


# try:
#     TrFGeozone.__table__.drop(engine)
# except:
#     pass
# metadata.create_all(engine)
