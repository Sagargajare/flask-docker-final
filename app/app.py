"""
Created on 03/01/2021

file:           app.py
description:

@author: Almoutaz
"""
import os.path

from flask import Flask
from flask import request
from flask import jsonify
import cv2

from time import gmtime, strftime
import logging
import sys
import uuid

import api_bridge
import app_utils
import constants
import mrz_parser

""" The flask app for serving predictions """
app = Flask(__name__, static_folder='')

#setting_err = app_utils.load_settings(app)
setting_err = app_utils.load_settings(app, 'localhost')

if setting_err:
    logging.error(setting_err)
    sys.exit()

# -------------------------------------
# Routes
# -------------------------------------

# force browser to hold no cache. Otherwise old result might return.
@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

@app.route('/')
def homepage():
    api_detail = "Document scanner api: Version " + constants.api_ver
    return api_detail

@app.route('/document-scanner', methods=['GET','POST'])
def document_scanner():
    """ check card image param """
    if ('card_file' not in request.files):
        return jsonify({'result': '<h3>Sorry,<br/>no exist content image file.</h3>'})
    card_file = request.files['card_file']

    # get request time string
    subdir = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    file_path = upload_request_images(card_file, subdir)

    img = cv2.imread(file_path)
    w = img.shape[1]
    h = img.shape[0]

    scan_result = api_bridge.scan_mrz(img, w, h)

    parser = mrz_parser.mrzParser(str(scan_result.decode('utf-8')))
    parser.process()

    ret = jsonify({ 'passportType': parser.passportType,
                    'countryCode': parser.countryCode,
                    'surname': parser.surname,
                    'givenname': parser.givenname,
                    'passportNumber': parser.passportNumber,
                    'nationality': parser.nationality,
                    'birthday': parser.birthday,
                    'sex': parser.sex,
                    'expirationDate': parser.expirationDate,
                    'personalNumber': parser.personalNumber,
                    'optionalData': parser.optionalData})
    return ret

def upload_request_images(content, subdir):
    """ Upload request image to folder """
    request_dir = os.path.join("request", subdir)
    if not os.path.exists(request_dir):
        os.makedirs(request_dir)

    file_name = content.filename
    file_path = os.path.join(request_dir, file_name)
    content.save(file_path)
    return file_path

# -------------------------------------
# Another way to run:
# -------------------------------------
if __name__ == '__main__':
    # if app.config["APP_SETTINGS_LEVEL"] == 'production':
    #     #app.run(ssl_context='adhoc', debug=False)
    #     app.run(debug=False)
    # else:
    #     #app.run(ssl_context='adhoc', debug=True)
    app.run(host="0.0.0.0")
