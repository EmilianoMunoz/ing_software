from app import db
from dataclasses import dataclass

@dataclass(init=False)
class User(db.Model):
    
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255))
    surname = db.Column('surname', db.String(255))
    email = db.Column('email', db.String(255))
    password = db.Column('password', db.String(255))
    

    

    