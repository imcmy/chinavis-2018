import os
from flask import Blueprint
import pymysql
import json
import datetime

base_dir = os.path.dirname(__file__) + '/json_statics/'

db = pymysql.connect("123.206.64.248", "root", "chinavis2018", "chinavis", charset='utf8')
cursor = db.cursor()

data = Blueprint('data', __name__, url_prefix='/')


@data.route('/test', methods=['GET', 'POST'])
def test():
    return "连接成功"


@data.route('/<int:post_id>', methods=['GET', 'POST'])
def Person_data(post_id):
    if(post_id == 1487 or post_id == 1284):
        da = json.loads(open(os.path.join(base_dir, post_id.__str__()+'.json')).read())
        return jsonify(da)
    else:
        data = {
            'ip': '',
            'department': '',
            'email_subject': '',
            'check_day_time': '',
            'domain': '',
            'domain_rank': '',
        }
        ips = json.loads(open(os.path.join(base_dir,'ip_id.json')).read())
        for ipp in ips:
            if ipp['id'] == post_id.__str__():
               data['ip'] = ipp ['ip']
        #data['ip'] = ip
        #data['ip'] = getip(post_id)
        email = getemail(post_id)
        data['email_subject'] = getsubject(email)
        data['department'] = getperson_department(post_id)
        data['check_day_time'] = getcheck_time(post_id)
        data['domain'] = getdomain(post_id)
        data['domain_rank'] = getdomain_rank(post_id)
        data['tag_count'] = get_tag_count(post_id)
        data['receive_email_subject'] = getreceiver(email)
        return json.dumps(data, ensure_ascii=False)

# def getip(id):
#     sql = "select `ip` from link WHERE `id` LIKE '%d'  " % id
#     cursor.execute(sql)
#     rows = cursor.fetchall()
#     if len(rows) != 0:
#         for line in rows:
#             ip = line[0]
#         return ip
#     else:
#         return None

def get_tag_count(id):
    sql = 'SELECT tag,record FROM weblog_record WHERE id LIKE "%s" ' % id
    cursor.execute(sql)
    rows = cursor.fetchall()
    tag = []
    if (len(rows) != 0):
        for line in rows:
            if (line[0] == '开发'):
                kaifa_dict = {'name': '开发',
                              'value': line[1], }
                tag.append(kaifa_dict)
            elif (line[0] == '办公'):
                bangong_dict = {'name': '办公',
                                'value': line[1], }
                tag.append(bangong_dict)
            elif (line[0] == '娱乐'):
                yule_dict = {'name': '娱乐',
                             'value': line[1], }
                tag.append(yule_dict)
            elif (line[0] == '技术'):
                jishu_dict = {'name': '技术',
                              'value': line[1], }
                tag.append(jishu_dict)
            elif (line[0] == '招聘'):
                zhaopin_dict = {'name': '招聘',
                                'value': line[1], }
                tag.append(zhaopin_dict)
            elif (line[0] == '搜索'):
                sousuo_dict = {'name': '搜索',
                               'value': line[1], }
                tag.append(sousuo_dict)
            elif (line[0] == '购物'):
                gouwu_dict = {'name': '购物',
                              'value': line[1], }
                tag.append(gouwu_dict)
            elif (line[0] == '赌博'):
                dubo_dict = {'name': '赌博',
                             'value': line[1], }
                tag.append(dubo_dict)
        return tag
    else:
        return None

def getdomain(id):
    ips = json.loads(open(os.path.join(base_dir,'ip_id.json')).read())
    ip = ''
    for ipp in ips:
        if ipp['id'] == id.__str__():
           ip = ipp ['ip']
    #ip = getip(id)
    sql = "select `host` from weblog WHERE `sip` LIKE '%s'" % ip
    cursor.execute(sql)
    rows = cursor.fetchall()
    domain_list = []
    domain = []
    list = [1] * 10000
    if (len(rows) != 0):
        for line in rows:
            doo = urltodomain(line[0])
            if doo not in domain_list and doo != None:
                domain_list.append(doo)
            elif (doo != None):
                list[domain_list.index(doo)] += 1
            else:
                pass
        for id in range(len(domain_list)):
            domain_dict = {'name': '',
                           'value': '',
                           'tag':''}
            domain_dict['name'] = domain_list[id]
            domain_dict['tag'] = getdomaintag(domain_list[id])
            domain_dict['value'] = list[id]
            domain.append(domain_dict)
        return domain
    else:
        return None


def getdomain_rank(id):
    ips = json.loads(open(os.path.join(base_dir,'ip_id.json')).read())
    ip = ''
    for ipp in ips:
        if ipp['id'] == id.__str__():
           ip = ipp ['ip']
    #ip = getip(id)
    sql = "select `host` from weblog WHERE `sip` LIKE '%s'" % ip
    cursor.execute(sql)
    rows = cursor.fetchall()
    domain_list = []
    domain2 = []
    domain_rank = []
    list = [1] * 10000
    if len(rows) != 0:
        for line in rows:
            if line[0] not in domain_list and line[0] != '':
                domain_list.append(line[0])
            elif line[0] != '':
                list[domain_list.index(line[0])] += 1
            else:
                pass
        for id in range(len(domain_list)):
            domain = []
            domain.append(domain_list[id])
            domain.append(list[id])
            domain2.append(domain)
        rank = sorted(domain2, key=lambda domai: domai[1], reverse=True)
        if len(rank) >= 5:
            for id in range(0, 5):
                domain_rank.append(urltodomain(rank[id][0]))
        else:
            for id in range(len(rank)):
                domain_rank.append(urltodomain(rank[id][0]))
        return domain_rank
    else:
        return None


def getcheck_time(id):
    sql = "select  `checkin`,`checkout`,`day` from checking2 WHERE id  LIKE '%d'  " % id
    cursor.execute(sql)
    rows = cursor.fetchall()
    arraylist = []
    if len(rows) != 0:
        for line in rows:
            time_list = []
            start = line[0]
            end = line[1]
            st = start.split(' ')
            en = end.split(' ')
            day = line[2]
            str = datetime.date.strftime(day, '%Y-%m-%d')
            time_list.append(str)
            if start == '0' and end == '0':
                result = 0
                time_list.append(result)
                time_list.append('0')
                time_list.append('0')
            else:
                date1 = datetime.datetime.strptime(start, '%Y/%m/%d %H:%M')
                date2 = datetime.datetime.strptime(end, '%Y/%m/%d %H:%M')
                an = date2 - date1
                an = an.total_seconds()
                time_list.append(round(an / 3600, 1))
                time_list.append(st[1])
                time_list.append(en[1])
            arraylist.append(time_list)
        return arraylist
    else:
        return None


def getsubject(email):
    subjectlist = []
    res = []
    num = [1] * 2000
    sql = "SELECT `subject` FROM email WHERE `sender` LIKE '%s'" % email
    cursor.execute(sql)
    subject = cursor.fetchall()
    if len(subject) != 0:
        for line in subject:
            if line[0] not in res:
                res.append(line[0])
            else:
                num[res.index(line[0])] += 1
        for id in range(len(res)):
            sub = {"name": "",
                   "value": ""}
            sub["name"] = res[id]
            sub["value"] = num[id]
            subjectlist.append(sub)
        return subjectlist
    else:
        return None


def getemail(id):
    sql = "SELECT `email` FROM link WHERE `id` LIKE '%s' " % id
    cursor.execute(sql)
    email = cursor.fetchall()
    if len(email) != 0:
        for line in email:
            return line[0]
    else:
        return None


def getperson_department(id):
    sql = "select `department`,`position` from department WHERE id  LIKE '%d'  " % id
    cursor.execute(sql)
    department = {
        "department": "",
        "position": "",
    }
    res = cursor.fetchall()
    if len(res) != 0:
        for line in res:
            department['department'] = line[0]
            department['position'] = line[1]
        return department
    else:
        return None


def urltodomain(url):
    sql = "select `domain` from urldomain WHERE `url` LIKE '%s'  " % url
    cursor.execute(sql)
    rows = cursor.fetchall()
    if (len(rows) != 0):
        for line in rows:
            domain = line[0]
            return domain
    else:
        return None

def getdomaintag(domain):
    sql = "select tag from domain_tag WHERE `domain` LIKE '%s'  " % domain
    cursor = db.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    if (len(rows) != 0):
        for line in rows:
            tag = line[0]
            return tag
    else:
        return None

def getreceiver(email):
    subjectlist = []
    res = []
    num = [1] * 20000
    # email = '%' + email + '%'
    sql = "SELECT `subject` FROM email WHERE `receiver` LIKE '%s' " % email
    cursor.execute(sql)
    subject = cursor.fetchall()
    if (len(subject) != 0):
        for line in subject:
            if (line[0] not in res):
                res.append(line[0])
            else:
                num[res.index(line[0])] += 1
        for id in range(len(res)):
            sub = {"name": "",
                   "value": "",
                   }
            sub["value"] = num[id]
            if(len(res[id])>20):
                sub["name"] = res[id][0:21]
            else:
                sub["name"] = res[id]
            subjectlist.append(sub)
        return subjectlist
    else:
        return None

def strintodatetime(str):
    date_time = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M')
    return date_time


def datetimeintostr(date_time):
    str = datetime.datetime.strftime(date_time, '%Y-%m-%d %H:%M')
    return str


def time_list():
    list = []
    for k1 in range(1, 31):
        if k1 < 10:
            k1 = k1.__str__()
            k1 = '0' + k1
        for k2 in range(0, 24):
            if k2 < 10:
                k2 = k2.__str__()
                k2 = '0' + k2
            str = '2017-11-' + k1.__str__() + ' ' + k2.__str__() + ':00'

            list.append(str)
    return list


# @data.route('/tcp/<int:post_id>', methods=['GET', 'POST'])
# def dataa(post_id):
#     ips = json.loads(open(os.path.join(base_dir,'ip_id.json')).read())
#     for ipp in ips:
#         if ipp['id'] == post_id.__str__():
#             ip = ipp ['ip']
#     tcp = {'time':[],
#            'uplink_length':[],
#            'downlink_length':[]}
#     time_date_list = time_list()
#     tcp['time'] = time_date_list
#     uplink = [0] * 720
#     downlink = [0] * 720
#     tcps = json.loads(open(os.path.join(base_dir,'tcplog.json')).read())
#     for tc in tcps:
#         line = []
#         if tc['sip'] == ip:
#             line.append(tc['stime'])
#             line.append(tc['uplink_length'])
#             line.append(tc['downlink_length'])
#             timee = line[0]
#             for idd in time_date_list:
#                  if(idd[0:13] == timee[0:13]):
#                      ti = time_date_list.index(idd)
#                      uplink[ti] += line[1]
#                      downlink[ti] += line[2]
#
#     tcp['uplink_length'] = uplink
#     tcp['downlink_length'] = downlink
#     return json.dumps(tcp,ensure_ascii=False)




