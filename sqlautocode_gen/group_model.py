# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlautocode_gen import DeclarativeBase


association_table_user_group = Table('tr_user_group', DeclarativeBase.metadata,
Column(u'id', Integer, primary_key=True),
Column(u'user_id', Integer, ForeignKey('tr_user.id'), nullable=False),
Column(u'group_id', Integer, ForeignKey('tr_group.id'), nullable=False)
)


class TrGroup(DeclarativeBase):
    __tablename__ = 'tr_group'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    id = Column(u'id', Integer, primary_key=True)
    title = Column(u'title', String(255), nullable=False)
    desc = Column(u'desc', String(255), nullable=False)
    pic = Column(u'pic', String(255), nullable=False)
    invitation = Column(u'invitation', Boolean, nullable=False, default=False)
    meeting = Column(u'meeting', Boolean, nullable=False, default=False)
    help = Column(u'help', Boolean, nullable=False, default=False)
    last_modified = Column(u'last_modified', TIMESTAMP(), nullable=False, onupdate=func.now())
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())

    #relation definitions
    user_id = relationship("TrUser", foreign_keys="TrUser.id", cascade="all,delete")

    def __init__(self, user_id, title, desc, pic=None, invitation=False, meeting=False, help=False):
        self.title = title
        self.desc = desc
        self.pic = pic
        self.invitation = invitation
        self.meeting = meeting
        self.help = help
        self.user_id = user_id
