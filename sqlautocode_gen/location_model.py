# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2015, Easywhere"
__email__ = "ag@easywhere.ru"

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlautocode_gen import DeclarativeBase


class TrUserLocation(DeclarativeBase):
    __tablename__ = 'tr_group'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    id = Column(u'id', Integer, primary_key=True)
    longitude = Column(u'longitude', DECIMAL(precision=11, scale=8))
    latitude = Column(u'latitude', DECIMAL(precision=10, scale=8))
    last_modified = Column(u'last_modified', TIMESTAMP(), nullable=False, onupdate=func.now())
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())
    timestamp = Column(u'timestamp', TIMESTAMP(), nullable=False)
    user_id = Column(u'user_id', Integer, ForeignKey('tr_user.id'), nullable=False)
    
    def __init__(self, user_id, longitude, latitude, timestamp):
        self.title = title
        self.longitude = longitude
        self.latitude = latitude
        self.timestamp = timestamp
        self.user_id = user_id
