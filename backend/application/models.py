from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime


db = SQLAlchemy()

# user <--many to many--> role, user_roles

class User(db.Model,UserMixin):
    #required attributes for flask security
    id  = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable =False)
    fs_uniquifier = db.Column(db.String, unique = True, nullable = False)
    active = db.Column(db.Boolean, nullable = False)
    roles = db.relationship('Role', backref = 'bearer', secondary = 'user_roles')
    # more attributes can be added



class Role(db.Model, RoleMixin):    
    #required attributes for flask security
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False, unique = True)
    description = db.Column(db.String)
    # more attributes can be added

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))

class Lot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    addr = db.Column(db.String(255), nullable=False)
    pin = db.Column(db.String(10), nullable=False)
    max_spots = db.Column(db.Integer, nullable=False)
    
class Spot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('lot.id'), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')
    
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('spot.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_in = db.Column(db.DateTime, default=datetime.utcnow)
    time_out = db.Column(db.DateTime, nullable=True)
    rate = db.Column(db.Float, nullable = False)