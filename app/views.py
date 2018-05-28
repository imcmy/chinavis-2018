import os
import json
import datetime
from .models import User, Email, WebRecord, Login, TcpLog
from flask import Blueprint, request, jsonify, make_response

view = Blueprint('view', __name__, url_prefix='/')

base_dir = os.path.dirname(__file__) + '/json_statics/'


@view.route('/', methods=('GET', 'POST'))
def hello():
    return "Hello World"


@view.route('/users', methods=('GET',))
def users():
    resp = make_response(open(os.path.join(base_dir, 'struct.json')).read())
    resp.headers["Content-type"] = "application/json;charset=UTF-8"
    return resp


@view.route('/emails_full', methods=('GET',))
def emails_full():
    resp = make_response(open(os.path.join(base_dir, 'emails_full.json')).read())
    resp.headers["Content-type"] = "application/json;charset=UTF-8"
    return resp


def category_name(depart, email):
    category_names = {"0": "总经理",
                     "1": "人力资源",
                     # "2": "财务",
                     "3.1": "研发小组1组长",
                     "3.1.1": "研发小组1-1",
                     "3.1.2": "研发小组1-2",
                     "3.1.3": "研发小组1-3",
                     "3.1.4": "研发小组1-4",
                     "3.1.5": "研发小组1-5",
                     "3.1.6": "研发小组1-6",
                     "3.1.7": "研发小组1-7",
                     "3.1.8": "研发小组1-8",
                     "3.1.9": "研发小组1-9",
                     "3.2": "研发小组2组长",
                     "3.2.1": "研发小组2-1",
                     "3.2.2": "研发小组2-2",
                     "3.2.3": "研发小组2-3",
                     "3.2.4": "研发小组2-4",
                     "3.2.5": "研发小组2-5",
                     "3.2.6": "研发小组2-6",
                     "3.2.7": "研发小组2-7",
                     "3.2.8": "研发小组2-8",
                     "3.2.9": "研发小组2-9",
                     "3.2.10": "研发小组2-10",
                     "3.2.11": "研发小组2-11",
                     "3.3": "研发小组3组长",
                     "3.3.1": "研发小组3-1",
                     "3.3.2": "研发小组3-2",
                     "3.3.3": "研发小组3-3",
                     "3.3.4": "研发小组3-4",
                     "3.3.5": "研发小组3-5",
                     "3.3.6": "研发小组3-6",
                     "3.3.7": "研发小组3-7"}
    if depart in category_names:
        return category_names[depart]
    elif depart == '2':
        return '财务-' + email
    else:
        return email


@view.route('/emails_fin', methods=('GET',))
def emails_fin():
    resp = make_response(open(os.path.join(base_dir, 'emails_fin.json')).read())
    resp.headers["Content-type"] = "application/json;charset=UTF-8"
    return resp


@view.route('/emails', methods=('GET',))
def emails():
    # categories = {user.email: category_name(user.depart, user.email) for user in User.query.all()
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


@view.route('/weblog_record_users/<group_id>', methods=('GET',))
def weblog_record_users(group_id):
    # logs = []
    # tags = ['办公', '购物', '娱乐', '搜索', '开发', '技术', '赌博', '招聘']
    # for user in User.query.all():
    #     records = WebRecord.query.filter_by(id=user.id)
    #     values = [0] * len(tags)
    #     for record in records:
    #         index = tags.index(record.tag)
    #         values[index] = record.record
    #     logs.append({"value": values, "name": record.id, "depart": record.depart})
    # return jsonify(logs)
    # resp = make_response(open(os.path.join(base_dir, 'weblog_record_users.json')).read())
    # resp.headers["Content-type"] = "application/json;charset=UTF-8"
    # return resp
    groups = []
    users = json.loads(open(os.path.join(base_dir, 'weblog_record_users.json')).read())
    for user in users:
        if user['depart'].startswith(group_id):
            groups.append(user)
    return jsonify(groups)


@view.route('/weblog_record_groups/<group_id>', methods=('GET',))
def weblog_record_groups(group_id):
    # tags = ['办公', '购物', '娱乐', '搜索', '开发', '技术', '赌博', '招聘']
    # logs = [{"value": [0] * len(tags), "name": "1067", "depart": "0"},
    #         {"value": [0] * len(tags), "name": "人力资源", "depart": "1"},
    #         {"value": [0] * len(tags), "name": "财务", "depart": "2"},
    #         {"value": [0] * len(tags), "name": "研发部门1", "depart": "3.1"},
    #         {"value": [0] * len(tags), "name": "研发部门2", "depart": "3.2"},
    #         {"value": [0] * len(tags), "name": "研发部门3", "depart": "3.3"}]
    # for user in User.query.all():
    #     records = WebRecord.query.filter_by(id=user.id)
    #     for record in records:
    #         index = tags.index(record.tag)
    #         if record.depart.startswith('0'):
    #             logs[0]['value'][index] += record.record
    #         elif record.depart.startswith('1'):
    #             logs[1]['value'][index] += record.record
    #         elif record.depart.startswith('2'):
    #             logs[2]['value'][index] += record.record
    #         elif record.depart.startswith('3.1'):
    #             logs[3]['value'][index] += record.record
    #         elif record.depart.startswith('3.2'):
    #             logs[4]['value'][index] += record.record
    #         elif record.depart.startswith('3.3'):
    #             logs[5]['value'][index] += record.record
    # return jsonify(logs)
    # resp = make_response(open(os.path.join(base_dir, 'weblog_record_groups.json')).read())
    # resp.headers["Content-type"] = "application/json;charset=UTF-8"
    # return resp
    groups = json.loads(open(os.path.join(base_dir, 'weblog_record_groups.json')).read())
    for group in groups:
        if group['depart'] == group_id:
            return jsonify(group)
    return jsonify(groups)


@view.route('/login/<user_id>', methods=('GET',))
def login(user_id):
    ip = User.query.filter_by(id=user_id).first().ip
    logins = []
    for log in Login.query.filter_by(sip=ip):
        hour = str(log.time.hour).zfill(2) + ":" + ("30" if log.time.minute > 30 else "00")
        logins.append([log.sip, log.user, log.time.day, hour, log.dip, log.state])
    parallels = [sorted(list({log[i] for log in logins})) for i in range(6)]
    return jsonify({"data": logins, "parallels": parallels})


@view.route('/tcplog/<id_or_ip>', methods=('GET',))
def tcpLog(id_or_ip):
    if len(id_or_ip) == 4:
        ip = User.query.filter_by(id=id_or_ip).first().ip
    else:
        ip = id_or_ip
    x_axis = []
    for day in range(1, 31):
        for hour in range(24):
            a_hour = datetime.datetime(2017, 11, day) + datetime.timedelta(hours=hour)
            x_axis.append(str(a_hour))
    up_axis = [0] * len(x_axis)
    down_axis = [0] * len(x_axis)
    protocols = ["smtp", "ssh", "ftp", "tds", "mysql", "mongodb", "postgresql", "sftp", "http"]
    protocol_axis = [{"name": protocol, "type": "line", "data": [0] * len(x_axis)} for protocol in protocols]
    for log in TcpLog.query.filter_by(sip=ip):
        key = x_axis.index(str(datetime.datetime(2017, 11, log.stime.day, hour=log.stime.hour)))
        up_axis[key] += log.uplink_length
        down_axis[key] += log.downlink_length
        for protocol in protocol_axis:
            if protocol['name'] == log.proto:
                protocol['data'][key] += (log.uplink_length + log.downlink_length)
                break
    return jsonify({'xAxis': x_axis, "upAxis": up_axis, "downAxis": down_axis,
                    "protocols": protocol_axis, "legend": protocols})
