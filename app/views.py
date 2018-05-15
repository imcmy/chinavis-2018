from flask import Blueprint, request

view = Blueprint('view', __name__, url_prefix='/')


@view.route('/hello', methods=('GET', 'POST'))
def hello():
    return "Hello World"
