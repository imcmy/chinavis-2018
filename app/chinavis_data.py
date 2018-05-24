from flask import Blueprint
import pymysql
import json
import datetime


db = pymysql.connect("123.206.64.248", "root", "chinavis2018", "chinavis", charset='utf8')
cursor = db.cursor()

data = Blueprint('data', __name__, url_prefix='/')


@data.route('/test', methods=['GET', 'POST'])
def test():
    return "连接成功"


@data.route('/<int:post_id>', methods=['GET', 'POST'])
def Person_data(post_id):
    data = {
        'ip': '',
        'department': '',
        'email_subject': '',
        'check_day_time': '',
        'domain': '',
        'domain_rank': '',
    }
    data['ip'] = getip(post_id)
    email = getemail(post_id)
    data['email_subject'] = getsubject(email)
    data['department'] = getperson_department(post_id)
    data['check_day_time'] = getcheck_time(post_id)
    data['domain'] = getdomain(post_id)
    data['domain_rank'] = getdomain_rank(post_id)
    return json.dumps(data, ensure_ascii=False)


def getip(id):
    sql = "select `ip` from link WHERE `id` LIKE '%d'  " % id
    cursor.execute(sql)
    rows = cursor.fetchall()
    if len(rows) != 0:
        for line in rows:
            ip = line[0]
        return ip
    else:
        return None


def getdomain(id):
    ip = getip(id)
    sql = "select `host` from weblog WHERE `sip` LIKE '%s'" % ip
    cursor.execute(sql)
    rows = cursor.fetchall()
    domain_list = []
    domain = []
    list = [1] * 10000
    if (len(rows) != 0):
        for line in rows:
            if line[0] not in domain_list and line[0] != '':
                domain_list.append(line[0])
            elif (line[0] != ''):
                list[domain_list.index(line[0])] += 1
            else:
                pass
        for id in range(len(domain_list)):
            domain_dict = {'name': '',
                           'value': '',
                           'tag':''}
            domain_dict['name'] = urltodomain(domain_list[id])
            domain_dict['tag'] = getdomaintag(urltodomain(domain_list[id]))
            domain_dict['value'] = list[id]
            domain.append(domain_dict)
        return domain
    else:
        return None


def getdomain_rank(id):
    ip = getip(id)
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
    sql = "select  `checkin`,`checkout`,`day` from checking WHERE id  LIKE '%d'  " % id
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
    num = [1] * 200
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
    sql = "SELECT `email` FROM link WHERE `id` LIKE '%d' " % id
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


def getuplinkdata(ip):
    count_list = [0] * 721
    res_list = []
    time_date_list = time_list()
    ti = 0
    sql = "SELECT stime,uplink_length FROM tcpLog WHERE sip LIKE '%s'" % ip
    cursor.execute(sql)
    rows = cursor.fetchall()
    result = [0] * 721
    for line in rows:
        timee = line[0]
        for id in time_date_list:
            if (timee > strintodatetime(id) and datetimeintostr(timee)[11:13] != '23'):
                pass
            elif (datetimeintostr(timee)[11:13] == '23' and time_date_list[time_date_list.index(id) - 1] not in result):
                ti = time_date_list.index(id)
                result[ti] = time_date_list[ti]
                count_list[ti] += line[1]
                break
            elif (datetimeintostr(timee)[11:13] == '23' and time_date_list[time_date_list.index(id) - 1] in result):
                ti = time_date_list.index(id)
                count_list[ti] += line[1]
                break
            elif (time_date_list[time_date_list.index(id) - 1] not in result):
                ti = time_date_list.index(id) - 1
                result[ti] = time_date_list[ti]
                count_list[ti] += line[1]
                break
            elif (time_date_list[time_date_list.index(id) - 1] in result):
                ti = time_date_list.index(id) - 1
                count_list[ti] += line[1]
                break
    for id in time_date_list:
        res = []
        if (result[time_date_list.index(id)] == 0):
            res.append(id)
        else:
            res.append(result[time_date_list.index(id)])
        res.append(count_list[time_date_list.index(id)])
        res_list.append(res)
    return res_list


def getdownlinkdata(ip):
    count_list = [0] * 721
    res_list = []
    time_date_list = time_list()
    ti = 0
    sql = "SELECT stime,downlink_length FROM tcpLog WHERE sip LIKE '%s'" % ip
    cursor.execute(sql)
    rows = cursor.fetchall()
    result = [0] * 721
    for line in rows:
        timee = line[0]
        for id in time_date_list:
            if (timee > strintodatetime(id) and datetimeintostr(timee)[11:13] != '23'):
                pass
            elif (datetimeintostr(timee)[11:13] == '23' and time_date_list[time_date_list.index(id) - 1] not in result):
                ti = time_date_list.index(id)
                result[ti] = time_date_list[ti]
                count_list[ti] += line[1]
                break
            elif (datetimeintostr(timee)[11:13] == '23' and time_date_list[time_date_list.index(id) - 1] in result):
                ti = time_date_list.index(id)
                count_list[ti] += line[1]
                break
            elif (time_date_list[time_date_list.index(id) - 1] not in result):
                ti = time_date_list.index(id) - 1
                result[ti] = time_date_list[ti]
                count_list[ti] += line[1]
                break
            elif (time_date_list[time_date_list.index(id) - 1] in result):
                ti = time_date_list.index(id) - 1
                count_list[ti] += line[1]
                break
    for id in time_date_list:
        res = []
        if (result[time_date_list.index(id)] == 0):
            res.append(id)
        else:
            res.append(result[time_date_list.index(id)])
        res.append(count_list[time_date_list.index(id)])
        res_list.append(res)
    return res_list


@data.route('/tcp/<int:post_id>', methods=['GET', 'POST'])
def dataa(post_id):
    ip = getip(post_id)

    da = {"sip": '',
          "uplink_length": '',
          "downlink_length":'',}
    da['sip'] = ip
    da['uplink_length'] = getuplinkdata(ip)
    da['downlink_length'] = getdownlinkdata(ip)
    return json.dumps(da, ensure_ascii=False)


