from flask import Flask
import pymysql
import json

app = Flask(__name__)

db = pymysql.connect("123.206.64.248", "root", "chinavis2018", "chinavis", charset='utf8')
cursor = db.cursor()


@app.route('/')
def hello_world():
    return 'Hello World!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'


@app.route('/<int:post_id>', methods=['GET', 'POST'])
def Person_data(post_id):
    data = {
        'ip': '',
        'department': '',
        'email_subject': '',
        'checkin': '',
        'checkout': '',
    }
    data['ip'] = getip(post_id)
    data['checkin'] = getcheckin(post_id)
    email = getemail(post_id)
    data['email_subject'] = getsubject(email)
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


def getcheckin(id):
    sql = "select checkin from checking WHERE id  LIKE '%d'  " % id
    cursor.execute(sql)
    checkinlist = []
    checkins = cursor.fetchall()
    if (len(checkins) != 0):
        for line in checkins:
            checkinlist.append(line[0])
        return checkinlist
    else:
        return None



def getsubject(email):
    subjectlist = []
    res = []
    num = [1] * 200
    sql = "SELECT `subject` FROM email WHERE `sender` LIKE '%s'"  %email
    cursor.execute(sql)
    subject = cursor.fetchall()
    if (len(subject) != 0):
        for line in subject:
           if(line[0] not in res):
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

if __name__ == '__main__':
    app.run()
    db.close()


