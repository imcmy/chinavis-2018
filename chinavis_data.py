from flask import Flask
import pymysql
import json
import datetime

app = Flask(__name__)

db = pymysql.connect("123.206.64.248", "root", "chinavis2018", "chinavis", charset='utf8')
cursor = db.cursor()


@app.route('/')
def hello_world():
    return 'Hello World!!!'


@app.route('/<int:post_id>', methods=['GET', 'POST'])
def Person_data(post_id):
    data = {
        'ip': '',
        'department': '',
        'email_subject': '',
        'check_day_time': '',
    }
    data['ip'] = getip(post_id)
    email = getemail(post_id)
    data['email_subject'] = getsubject(email)
    data['department'] = getperson_deparment(post_id)
    data['check_day_time'] = getcheck_time(post_id)
    return json.dumps(data, ensure_ascii=False)


def getip(id):
    sql = "select `ip` from link WHERE `id` LIKE '%d'  " % id
    cursor.execute(sql)
    rows = cursor.fetchall()
    if (len(rows) != 0):
        for line in rows:
            ip = line[0]
        return ip
    else:
        return None


# def getcheckin(id):
#     sql = "select checkin from checking WHERE id  LIKE '%d'  " % id
#     cursor.execute(sql)
#     checkinlist = []
#     checkins = cursor.fetchall()
#     if (len(checkins) != 0):
#         for line in checkins:
#             checkinlist.append(line[0])
#         return checkinlist
#     else:
#         return None


def getcheck_time(id):
    sql = "select  `checkin`,`checkout`,`day` from checking WHERE id  LIKE '%d'  " % id
    cursor.execute(sql)
    rows = cursor.fetchall()
    arraylist = []
    if (len(rows) != 0):
        for line in rows:
            time_list = []
            start = line[0]
            end = line[1]
            day = line[2]
            str = datetime.date.strftime(day, '%Y-%m-%d')
            time_list.append(str)
            if (start == '0' and end == '0'):
                result = 0
                time_list.append(result)
            else:
                date1 = datetime.datetime.strptime(start, '%Y/%m/%d %H:%M')
                date2 = datetime.datetime.strptime(end, '%Y/%m/%d %H:%M')
                an = date2 - date1
                an = an.total_seconds()
                time_list.append(round(an / 3600, 1))
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
            sub["name"] = res[id]
            sub["value"] = num[res.index(res[id])]
            subjectlist.append(sub)
        return subjectlist
    else:
        return None


def getemail(id):
    sql = "SELECT `email` FROM link WHERE `id` LIKE '%d' " % id
    cursor.execute(sql)
    email = cursor.fetchall()
    if (len(email) != 0):
        for line in email:
            return line[0]
    else:
        return None


def getperson_deparment(id):
    sql = "select `department`,`position` from department WHERE id  LIKE '%d'  " % id
    cursor.execute(sql)
    department = {
        "department": "",
        "position": "",
    }
    res = cursor.fetchall()
    if (len(res) != 0):
        for line in res:
            department['department'] = line[0]
            department['position'] = line[1]
        return department
    else:
        return None


if __name__ == '__main__':
    app.run()
    db.close()
