from estore import db
from datetime import datetime
import json



class Customer(db.Model):
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

#define class to dump orders into database
class JsonEncodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        #If there are no items
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.loads(value)



#Create table for customer orders
class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(50), nullable=False, unique=True)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    customer_id = db.Column(db.String(50), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    orders = db.Column(JsonEncodedDict)

    def __repr__(self):
        return f"CustomerOrder('{self.invoice}', '{self.customer_id}')"