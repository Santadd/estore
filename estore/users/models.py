from flask.app import Flask
from flask_login.mixins import UserMixin
from sqlalchemy.orm import backref
from estore import db, login_manager
from datetime import date, datetime

@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))

class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False) 
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"Customer('{self.username}', '{self.email}')"

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    street_add = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    postcode = db.Column(db.String(50), nullable=False)
    mobile_no = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    date_created= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    ccustomer = db.relationship('Customer', backref=db.backref('customer', lazy=True))

    def __repr__(self):
        return f"Address('{self.email}', '{self.mobile_no}', '{self.first_name}', '{self.last_name}')"