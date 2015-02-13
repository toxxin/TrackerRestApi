# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

import os

from flask import request
from werkzeug.utils import secure_filename
from TrackerRestApi import app, Session, engine
from sqlautocode_gen.model import TrVehicle

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ['jpg', 'jpeg']

@app.route('/upload/<target>', methods=['POST'])
def upload(target):

    session = Session()

    tbl = {'profile': (TrUser, app.config.get('PROFILES_IMG_PATH')),
           'vehicle': (TrVehicle, app.config.get('VEHICLES_IMG_PATH')),
           'group': (TrGroup, app.config.get('GROUPS_IMG_PATH'))}

    if tbl.get(target) is None:
        session.close()
        return ("Error: Incorrect target.")

    obj = session.query(tbl[target][0]).get(int(request.headers.get('id')))
    if obj is None:
        session.close()
        return ("Error: Object doesn't exist.")

    path = tbl[target][1]

    file = request.files['file']

    app.logger.debug('Object id: %d' % int(request.headers.get('id')))
    app.logger.debug('Filename: %s' % file.filename)

    if file and allowed_file(file.filename):

        if obj.pic is not None:
            app.logger.debug('Field pic is not empty.')
            try:
                app.logger.debug('Trying to delete old file.')
                os.remove(path + obj.pic)
            except:
                pass

        engine.execute(" \
            UPDATE " + obj.__tablename__ + " SET pic=concat( \
                  substring('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', rand(@seed:=round(rand(" + str(obj.id) + ")*4294967296))*62+1, 1), \
                  substring('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', rand(@seed:=round(rand(@seed)*4294967296))*62+1, 1), \
                  substring('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', rand(@seed:=round(rand(@seed)*4294967296))*62+1, 1), \
                  substring('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', rand(@seed:=round(rand(@seed)*4294967296))*62+1, 1), \
                  substring('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', rand(@seed:=round(rand(@seed)*4294967296))*62+1, 1), \
                  substring('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', rand(@seed:=round(rand(@seed)*4294967296))*62+1, 1), \
                  substring('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', rand(@seed:=round(rand(@seed)*4294967296))*62+1, 1), \
                  substring('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', rand(@seed)*62+1, 1), \
                  '.jpg' \
                 ) \
            WHERE id="+ str(obj.id) + "; \
        ")

        session.close()

        s = Session()
        ob = session.query(tbl[target][0]).get(int(request.headers.get('id')))
        file.save(os.path.join(path, ob.pic))
        s.close()

        return "Ok"
    else:
        session.close()
        return "Error: incorrect file."
