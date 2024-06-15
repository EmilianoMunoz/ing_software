from app import db
from dataclasses import dataclass

@dataclass(init=False)
class Cabin(db.Model):

    __tablename__ = 'cabins'
    id = db.Column('id', db.Integer, primary_key=True)
    type = db.Column('type', db.String(255))
    level = db.Column('level', db.String(255))
    capacity = db.Column('capacity', db.Integer)


    