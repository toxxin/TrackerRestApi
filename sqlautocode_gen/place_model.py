__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlautocode_gen import DeclarativeBase


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
