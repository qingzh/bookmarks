#! -*- coding:utf8 -*-

from .views import app 
from flask.json import dumps, loads
from flask import (
    Blueprint, url_for, jsonify, render_template, Response)

alarm = Blueprint('alarm', __name__)
logger = app.logger

@alarm.route('/status')
def greeting():
    return jsonify(status="success", service=True)

