__author__ = 'Anton Glukhov'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlautocode_gen.model import DeclarativeBase

import unittest


engine = create_engine('mysql://tracker_db:2wsxCDE#@localhost:3306/trackerdb' + '?charset=utf8', echo=False, encoding='utf8')
metadata = DeclarativeBase.metadata
metadata.bind = engine

Session = sessionmaker()

from flask_jsonrpc.proxy import ServiceProxy
server = ServiceProxy('http://localhost:5000/api')

def suite():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromName('device.suite'))
    # suite.addTests(loader.loadTestsFromName('geo.suite'))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
