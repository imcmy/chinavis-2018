from flask import Blueprint
import pymysql
import json
import datetime


db = pymysql.connect("123.206.64.248", "root", "chinavis2018", "chinavis", charset='utf8')
cursor = db.cursor()

data = Blueprint('data', __name__, url_prefix='/')


@data.route('/<int:post_id>', methods=['GET', 'POST'])
def Person_data(post_id):
    data = {
        'ip': '',
        'department': '',
        'email_subject': '',
        'check_day_time': '',
        'domain': '',
        'domain_rank': '',
        # TOP 5
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
    if len(rows) != 0:
        for line in rows:
            if line[0] not in domain_list and line[0] != '':
                domain_list.append(line[0])
            elif line[0] != '':
                list[domain_list.index(line[0])] += 1
            else:
                pass
        for id in range(len(domain_list)):
            domain_dict = {'name': '',
                           'value': ''}
            domain_dict['name'] = domain_list[id]
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
                domain_rank.append(rank[id][0])
        else:
            for id in range(len(rank)):
                domain_rank.append(rank[id][0])
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


# def urltodomain(url):
#     sql = "select `domain` from url_domain WHERE `url` LIKE '%s'  " % url
#     cursor.execute(sql)
#     rows = cursor.fetchall()
#     if (len(rows) != 0):
#         for line in rows:
#             domain = line[0]
#         return domain
#     else:
#         return None
