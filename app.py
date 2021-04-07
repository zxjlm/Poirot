"""
@project : Poirot
@author  : harumonia
@mail   : zxjlm233@163.com
@ide    : PyCharm
@time   : 2021-04-07 16:46:18
@description: None
"""
import time

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import config

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'Poirot%%harumonia'


@app.route('/')
def index():
    """
    返回主页
    :return:
    """
    return 'hex'


@app.route('/time')
def ret_time():
    return {'time': time.time()}
