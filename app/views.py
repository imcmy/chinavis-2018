import os
from .models import User
from flask import Blueprint, request, jsonify, make_response

view = Blueprint('view', __name__, url_prefix='/')

base_dir = os.path.dirname(__file__)


@view.route('/hello', methods=('GET', 'POST'))
def hello():
    return "Hello World"


@view.route('/users', methods=('GET',))
def users():
    resp = make_response(open(os.path.join(base_dir, 'struct.json')).read())
    resp.headers["Content-type"] = "application/json;charset=UTF-8"
    return resp
