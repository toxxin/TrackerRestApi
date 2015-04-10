__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"


from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlautocode_gen import DeclarativeBase


association_table_user_feed = Table('tr_user_feed', DeclarativeBase.metadata,
    Column(u'id', Integer, primary_key=True),
    Column(u'user_id', Integer, ForeignKey('tr_user.id'), nullable=False),
    Column(u'feed_id', Integer, ForeignKey('tr_feed.id'), nullable=False)
    )


class TrFeed(DeclarativeBase):
    __tablename__ = 'tr_feed'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    id = Column(u'id', Integer, primary_key=True)
    title = Column(u'title', String(255), nullable=False)
    link = Column(u'link', String(255), nullable=False)
    type = Column(u'type', CHAR(1))
    pic = Column(u'pic', String(20), nullable=True)

    #relation definitions
    news = relationship("TrFeedNews", foreign_keys="TrFeedNews.feed_id", cascade="all,delete")

    def __init__(self, title, link, type=None, pic=None):
        self.title = title
        self.link = link
        self.type = type
        self.pic = pic


class TrFeedNews(DeclarativeBase):
    __tablename__ = 'tr_feed_news'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    id = Column(u'id', Integer, primary_key=True)
    url = Column(u'url', String(255), nullable=False)
    guid = Column(u'guid', String(255), unique=True, nullable=False)
    title = Column(u'title', String(255), nullable=False)
    link = Column(u'link', String(255), nullable=False)
    pic = Column(u'pic', String(255))
    desc = Column(u'desc', UnicodeText, nullable=True)
    fulltext = Column(u'fulltext', UnicodeText, nullable=True)
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())
    published = Column(u'published', TIMESTAMP(), nullable=False)
    feed_id = Column(u'feed_id', Integer, ForeignKey('tr_feed.id'), nullable=False)

    def __init__(self, url, guid, title, link, desc, fulltext, published, feed_id, pic=None):
        self.url = url
        self.guid = guid
        self.title = title
        self.link = link
        self.pic = pic
        self.desc = desc
        self.fulltext = fulltext
        self.published = published
        self.feed_id = feed_id


class TrFavFeed(DeclarativeBase):
    __tablename__ = 'tr_fav_feed'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    id = Column(u'id', Integer, primary_key=True)
    link = Column(u'link', String(255), nullable=False)
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())
    user_feed_id = Column(u'user_feed_id', Integer, ForeignKey('tr_user_feed.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    def __init__(self, link, user_feed_id):
        self.link = link
        self.user_feed_id = user_feed_id


class TrFavFeedTest(DeclarativeBase):
    __tablename__ = 'tr_fav_feed_test'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    #colomn definition
    u_id = Column(u'u_id', Integer, ForeignKey('tr_user.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    f_id = Column(u'f_id', Integer, ForeignKey('tr_feed.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    p_id = Column(u'p_id', Integer, ForeignKey('tr_feed_news.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    creation_date = Column(u'creation_date', TIMESTAMP(), nullable=False, default=func.now())

    def __init__(self, u_id, f_id, p_id):
        self.u_id = u_id
        self.f_id = f_id
        self.p_id = p_id
