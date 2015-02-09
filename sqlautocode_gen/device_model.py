__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlautocode_gen import DeclarativeBase


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
