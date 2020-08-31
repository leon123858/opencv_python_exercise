# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 19:41:53 2020

@author: a0970
"""

# encoding:utf8

from flask import Response, Flask, request

app = Flask(__name__)

@app.route("/image", methods=['post', 'get'])
def index():
    path = request.args.get('path')
    print(path)
    path =  path

    resp = Response(open(path, 'rb'), mimetype="image/jpeg")
    return resp

app.run(host='0.0.0.0',port=4949, debug=True)