import os

#set base directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'abdcefgh'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:newpasssql@localhost/estore'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'static/products/images')
