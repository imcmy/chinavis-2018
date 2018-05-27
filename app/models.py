from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'link'

    id = db.Column(db.String(255), primary_key=True)
    ip = db.Column(db.String(255))
    email = db.Column(db.String(255))
    level = db.Column(db.Integer)
    depart = db.Column(db.String(255))

    def __repr__(self):
        return '<User %r>' % self.id


class Email(db.Model):
    __tablename__ = 'email'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    proto = db.Column(db.String(255))
    sip = db.Column(db.String(255))
    sport = db.Column(db.Integer)
    dip = db.Column(db.String(255))
    dport = db.Column(db.Integer)
    sender = db.Column(db.String)
    receiver = db.Column(db.String)
    subject = db.Column(db.String)


class WebRecord(db.Model):
    __tablename__ = 'weblog_record'

    uuid = db.Column(db.Integer, primary_key=True)
    depart = db.Column(db.String(255))
    id = db.Column(db.String(4))
    tag = db.Column(db.String(255))
    record = db.Column(db.Integer)


class Login(db.Model):
    __tablename__ = 'login'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    user = db.Column(db.String(255))
    proto = db.Column(db.String(255))
    sip = db.Column(db.String(255))
    sport = db.Column(db.Integer)
    dip = db.Column(db.String(255))
    dport = db.Column(db.Integer)
    state = db.Column(db.String(255))


class TcpLog(db.Model):
    __tablename__ = 'tcpLog'

    id = db.Column(db.Integer, primary_key=True)
    stime = db.Column(db.DateTime)
    dtime = db.Column(db.DateTime)
    proto = db.Column(db.String(255))
    sip = db.Column(db.String(255))
    sport = db.Column(db.Integer)
    dip = db.Column(db.String(255))
    dport = db.Column(db.Integer)
    uplink_length = db.Column(db.Integer)
    downlink_length = db.Column(db.Integer)
