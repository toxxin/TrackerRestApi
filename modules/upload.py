__author__ = 'Anton Glukhov'

import os

from flask import request
from werkzeug.utils import secure_filename
from TrackerRestApi import app, Session, engine
from sqlautocode_gen.model import TrVehicle

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ['jpg', 'jpeg']

@app.route('/upload', methods=['POST'])
def upload():

    session = Session()

    file = request.files['file']
    vehicle_id = request.headers.get('vehicle_id')

    print "Vehicle id: %d" % vehicle_id
    print "Filename: %s" % file.filename

    v = session.query(TrVehicle).get(vehicle_id)

    if v is None:
        session.close()
        return ("Error: Vehicle doesn't exist.")

    if v.pic is not None:
        try:
            os.remove(app.config.get('VEHICLES_IMG_PATH') + '/' + v.pic)
        except:
            pass

    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)

        engine.execute(" \
            UPDATE tr_vehicle SET pic=concat( \
                  substring('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', rand(@seed:=round(rand(" + str(v.id) + ")*4294967296))*62+1, 1), \
                  substring('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', rand(@seed:=round(rand(@seed)*4294967296))*62+1, 1), \
                  substring('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', rand(@seed:=round(rand(@seed)*4294967296))*62+1, 1), \
                  substring('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', rand(@seed:=round(rand(@seed)*4294967296))*62+1, 1), \
                  substring('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', rand(@seed:=round(rand(@seed)*4294967296))*62+1, 1), \
                  substring('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', rand(@seed:=round(rand(@seed)*4294967296))*62+1, 1), \
                  substring('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', rand(@seed:=round(rand(@seed)*4294967296))*62+1, 1), \
                  substring('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', rand(@seed)*62+1, 1), \
                  '.jpg' \
                 ) \
            WHERE id="+ str(v.id) + "; \
        ")

        session.refresh(v)

        file.save(os.path.join(app.config.get('VEHICLES_IMG_PATH'), v.pic + ".jpg"))

        # try:
        #     v.pic = "new_file"
        #     session.merge(v)
        #     session.commit()
        # except:
        #     session.rollback()
        #     raise ServerError("Can't upload")
        # finally:
        #     session.close()

        return "Vehicle pic"
    else:
        session.close()
        return "Error: incorrect file."


@app.route('/test1', methods=['POST', 'GET'])
def test1():
    return 'Test'
