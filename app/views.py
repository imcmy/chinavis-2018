import os
from .models import User, Email
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
    # categoryNames = {"0": "总经理",
    #                  "1": "人力资源",
    #                  "2": "财务",
    #                  "3.1": "研发小组1组长",
    #                  "3.1.1": "研发小组1-1",
    #                  "3.1.2": "研发小组1-2",
    #                  "3.1.3": "研发小组1-3",
    #                  "3.1.4": "研发小组1-4",
    #                  "3.1.5": "研发小组1-5",
    #                  "3.1.6": "研发小组1-6",
    #                  "3.1.7": "研发小组1-7",
    #                  "3.1.8": "研发小组1-8",
    #                  "3.1.9": "研发小组1-9",
    #                  "3.2": "研发小组2组长",
    #                  "3.2.1": "研发小组2-1",
    #                  "3.2.2": "研发小组2-2",
    #                  "3.2.3": "研发小组2-3",
    #                  "3.2.4": "研发小组2-4",
    #                  "3.2.5": "研发小组2-5",
    #                  "3.2.6": "研发小组2-6",
    #                  "3.2.7": "研发小组2-7",
    #                  "3.2.8": "研发小组2-8",
    #                  "3.2.9": "研发小组2-9",
    #                  "3.2.10": "研发小组2-10",
    #                  "3.2.11": "研发小组2-11",
    #                  "3.3": "研发小组3组长",
    #                  "3.3.1": "研发小组3-1",
    #                  "3.3.2": "研发小组3-2",
    #                  "3.3.3": "研发小组3-3",
    #                  "3.3.4": "研发小组3-4",
    #                  "3.3.5": "研发小组3-5",
    #                  "3.3.6": "研发小组3-6",
    #                  "3.3.7": "研发小组3-7"}
    # categories = {user.email: categoryNames[user.depart] for user in User.query.all()
    #               if user.depart is not None}
    #
    # tmp_nodes = dict()
    # tmp_edges = list()
    # for email in Email.query.all():
    #     if email.sender.endswith('hightech.com') and email.sender[0].isdigit():
    #         tmp_nodes.setdefault(categories[email.sender], 0)
    #         tmp_nodes[categories[email.sender]] += 1
    #         receivers = email.receiver.split(';')
    #         for receiver in receivers:
    #             if receiver.endswith('hightech.com') and receiver[0].isdigit():
    #                 tmp_edges.append(
    #                     (categories[email.sender], categories[receiver]))
    # nodes = list()
    # # for user in User.query.all():
    # #     if user.depart is not None:
    # #         if user.depart == '0':
    # #             department = '总经理'
    # #         elif user.depart == '1':
    # #             department = '人力资源'
    # #         elif user.depart == '2':
    # #             department = '财务'
    # #         else:
    # #             department = '研发小组' + user.depart.split('.')[1]
    # #         nodes.append({"id": user.email, "name": user.email,
    # #                       "weight": tmp_nodes[categories[user.email]], "category": department})
    # for category, count in tmp_nodes.items():
    #     nodes.append({"id": category, "name": category,
    #                   "weight": count, "category": category})
    # edges = list()
    # for index, edge in enumerate(set(tmp_edges)):
    #     edges.append(
    #         {"id": index, "source": edge[0], "target": edge[1], "weight": tmp_edges.count(edge)})
    #
    # return jsonify({"categories": [{"name": category} for category in categories.values()], "nodes": nodes, "links": edges})
    resp = make_response(open(os.path.join(base_dir, 'emails.json')).read())
    resp.headers["Content-type"] = "application/json;charset=UTF-8"
    return resp
