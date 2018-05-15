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
