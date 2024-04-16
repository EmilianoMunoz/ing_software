from app import db
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Reserve(db.Model):
    __tablename__ = 'reserves'

    id = db.Column('id', db.Integer, primary_key=True)
    since = db.Column('since', db.DateTime)
    until = db.Column('until', db.DateTime)
    id_user = db.Column('id_user', db.Integer, db.ForeignKey('users.id'))
    id_cabin = db.Column('id_cabin', db.Integer, db.ForeignKey('cabins.id'))
    
    user = db.relationship('User', backref='user_reserve')

    