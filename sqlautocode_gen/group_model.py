# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlautocode_gen import DeclarativeBase


class TrGroup(DeclarativeBase):
    __tablename__ = 'tr_group'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    id = Column(u'id', Integer, primary_key=True)
    title = Column(u'title', String(255), nullable=False)
    desc = Column(u'desc', String(255), nullable=False)
    pic = Column(u'pic', String(255), nullable=False)
    type = Column(u'type', CHAR(1))
    pic = Column(u'pic', String(20), nullable=True)
    
    #relation definitions
    user_id = relationship("TrUser", foreign_keys="TrUser.id", cascade="all,delete")

    def __init__(self, title, link, type=None, pic=None):
        self.title = title
        self.link = link
        self.type = type
        self.pic = pic
