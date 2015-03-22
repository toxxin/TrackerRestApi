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
    desc = Column(u'desc', String(255))
    pic = Column(u'pic', String(255), nullable=False)
    invitation = Column(u'invitation', Boolean, nullable=False, default=False)
    meeting = Column(u'meeting', Boolean, nullable=False, default=False)
    help = Column(u'help', Boolean, nullable=False, default=False)
    last_modified = Column(u'last_modified', TIMESTAMP(), nullable=False, onupdate=func.now())
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())
    user_id = Column(u'user_id', Integer, ForeignKey('tr_user.id'), nullable=False)

    #relation definitions
    users = relationship("TrUser", secondary=association_table_user_group)

    meetings = relationship("TrGroupMeeting", foreign_keys="TrGroupMeeting.group_id", cascade="all,delete")

    def __init__(self, user_id, title, desc=None, pic="Default", invitation=False, meeting=False, help=False):
        self.title = title
        self.desc = desc
        self.pic = pic
        self.invitation = invitation
        self.meeting = meeting
        self.help = help
        self.user_id = user_id


class TrGroupComment(DeclarativeBase):
    __tablename__ = 'tr_group_comment'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    id = Column(u'id', Integer, primary_key=True)
    message = Column(u'message', UnicodeText, nullable=False)
    last_modified = Column(u'last_modified', TIMESTAMP(), nullable=False, onupdate=func.now())
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())
    user_group_id = Column(u'user_group_id', Integer, ForeignKey('tr_user_group.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    def __init__(self, message, user_group_id):
        self.message = message
        self.user_group_id = user_group_id


class TrGroupMeeting(DeclarativeBase):
    __tablename__ = 'tr_group_meeting'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    id = Column(u'id', Integer, primary_key=True)
    title = Column(u'title', UnicodeText, nullable=False)
    last_modified = Column(u'last_modified', TIMESTAMP(), nullable=False, onupdate=func.now())
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())
    time = Column(u'time', TIMESTAMP(), nullable=False)
    group_id = Column(u'group_id', Integer, ForeignKey('tr_group.id'), nullable=False)

    def __init__(self, title, time, group_id):
        self.title = title
        self.time = time
        self.group_id = group_id
