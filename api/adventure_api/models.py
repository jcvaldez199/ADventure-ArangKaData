from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
import datetime

db = SQLAlchemy()

class Customer(UserMixin, db.Model):
    """ Customer mod """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

class Video(db.Model):
    """ Video """
    filename = db.Column(db.String(50), primary_key=True)
    thumbnail = db.Column(db.String(50))
    userid = db.Column(db.Integer,
                       db.ForeignKey('Customer.id'),
                       primary_key=True
                       )

class Route(db.Model):
    """ Route """
    name = db.Column(db.String(),
                     primary_key=True,
                     unique=True,
                     nullable=False
                     )

class Location(db.Model):
    """ Location """
    locname = db.Column(db.String(50), primary_key=True)
    routename = db.Column(db.String(),
                          db.ForeignKey('Route.name'),
                          nullable=False,
                          primary_key=True
                         )
    userid = db.Column(db.Integer, db.ForeignKey('Customer.id'))

class Request(db.Model):
    """ Request """
    id = db.Column(db.Integer, primary_key=True)
    routename = db.Column(db.String(),
                          db.ForeignKey('Route.name'),
                          nullable=False
                         )
    userid = db.Column(db.Integer,
                       db.ForeignKey('Customer.userid'),
                       nullable=False
                       )
    videoname = db.Column(db.String(50),
                          db.ForeignKey('Video.filename'),
                          nullable=False
                          )
    locname = db.Column(db.String(50),
                        db.ForeignKey('Location.locname'),
                        nullable=False
                        )
    date_created = db.Column(db.Date, default=datetime.datetime.now())
    date_decision = db.Column(db.Date)
    approved = db.Column(db.Boolean, default=False)
    remarks = db.Column(db.Text)



