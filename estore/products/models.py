from estore import db
from datetime import datetime

#Create Tables for Brand and Category
class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)

class Brands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)

#Table for Product
class Product(db.Model):
    #Define Searchable property

    __searchable__ = ['name', 'desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer, nullable=False, default=0)
    stock = db.Column(db.Integer, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    colors = db.Column(db.Text, nullable=False)
    descr = db.Column(db.Text, nullable=False)
    

    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'),nullable=False)
    brand = db.relationship('Brands', backref=db.backref('brands', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'),nullable=False)
    category = db.relationship('Categories', backref=db.backref('categories', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image.jpg')

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}')"