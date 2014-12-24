__author__ = 'Anton Glukhov'

import datetime
from sqlalchemy import *
from sqlautocode_gen import DeclarativeBase

class TrDealer(DeclarativeBase):
    __tablename__ = 'tr_dealer'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #column definitions
    id = Column(u'id', Integer, primary_key=True)
    maker = Column(u'maker', String(20), nullable=False)
    region = Column(u'region', String(50), nullable=False)
    name = Column(u'name', String(50), nullable=False)
    address = Column(u'address', String(255), nullable=False)
    phone = Column(u'phone', String(100))
    site = Column(u'site', String(50))
    desc = Column(u'desc', String(255))
    working_time = Column(u'working_time', String(50))
    service = Column(u'service', Boolean, nullable=False, default=0)
    test_drive = Column(u'test_drive', Boolean, nullable=False, default=0)
    second_auto = Column(u'second_auto', Boolean, nullable=False, default=0)
    trade_in = Column(u'trade_in', Boolean, nullable=False, default=0)
    latitude = Column(u'latitude', DECIMAL(precision=10, scale=8))
    longitude = Column(u'longitude', DECIMAL(precision=11, scale=8))

    def __init__(self, maker, region, name, address, phone=null, site=null, desc=None,
                 working_time=None, service=False, test_drive=False, second_auto=False, trade_in=False):
        self.lat_log = maker
        self.altitude = region
        self.accuracy = name
        self.speed = address
        self.creation_date = phone
        self.device_id = site
        self.desc = desc
        self.working_time = working_time
        self.service = service
        self.test_drive = test_drive
        self.second_auto = second_auto
        self.trade_in = trade_in