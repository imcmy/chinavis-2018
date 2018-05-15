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
