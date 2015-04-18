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
    

class TrUserFeedFav(DeclarativeBase):
    __tablename__ = 'tr_user_feed_fav'

    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(u'id', Integer, primary_key=True)
    uf_id = Column(u'uf_id', Integer, ForeignKey('tr_user_feed.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    feed_news_id = Column(u'feed_news_id', Integer, ForeignKey('tr_feed_news.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)


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

    def __init__(self, url, guid, title, link, published, feed_id, desc=None, fulltext=None, pic=None):
        self.url = url
        self.guid = guid
        self.title = title
        self.link = link
        self.pic = pic
        self.desc = desc
        self.fulltext = fulltext
        self.published = published
        self.feed_id = feed_id
