import os
from .models import Email
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


@view.route('/emails', methods=('GET',))
def emails():
    # tmp_nodes = list()
    # tmp_edges = list()
    # for email in Email.query.all():
    #     if email.sender.endswith('hightech.com'):
    #         tmp_nodes.append(email.sender)
    #         receivers = email.receiver.split(';')
    #         for receiver in receivers:
    #             if receiver.endswith('hightech.com'):
    #                 tmp_edges.append((email.sender, receiver))
    # nodes = list()
    # for node in set(tmp_nodes):
    #     nodes.append({"id": node, "name": node, "weight": tmp_nodes.count(node)})
    # edges = list()
    # for index, edge in enumerate(set(tmp_edges)):
    #     edges.append({"id": index, "source": edge[0], "target": edge[1], "weight": tmp_edges.count(edge)})
    #
    # return jsonify({"nodes": nodes, "links": edges})
    resp = make_response(open(os.path.join(base_dir, 'emails.json')).read())
    resp.headers["Content-type"] = "application/json;charset=UTF-8"
    return resp
