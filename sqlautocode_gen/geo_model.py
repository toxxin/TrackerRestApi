__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlautocode_gen import DeclarativeBase


class TrDGeozone(DeclarativeBase):
    """Shape params:    0: circle, 1: square, 2: random"""
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

    def __init__(self, name, device_id, state=True, shape=0, center="0.0,0.0", radius=0, color="#ffffff"):
        self.name = name
        self.state = state
        self.shape = shape
        self.center = center
        self.radius = radius
        self.color = color
        self.device_id = device_id
