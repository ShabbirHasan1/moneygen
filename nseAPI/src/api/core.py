import json
import os
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, request, redirect, url_for, abort, jsonify, Response
from flask_cors import CORS, cross_origin
from requests_toolbelt.multipart.encoder import MultipartEncoder
from


class PrefixMiddleware:
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]


app = Flask(__name__)
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='')
app.wsgi_app = ProxyFix(app.wsgi_app)
# app = CORS(app)

# Webhook URL
@cross_origin()
@app.route('/webhook', methods=['POST'])
def webhook():
    pass

# Order management URLs
@cross_origin()
@app.route('/order', methods=['GET', 'POST', 'DELETE'])
def order_get_post_delete():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass
    else:
        return jsonify({'msg': 'Bad Request'}), 401

@cross_origin()
@app.route('/order/{order_id}', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
def get_or_modify_specific_order(order_id: int):
    if request.method == 'GET':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'PATCH':
        pass
    elif request.method == 'DELETE':
        pass
    else:
        return jsonify({'msg': 'Bad Request'}), 401

