from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os
from estore.config import Config
from flask_msearch import Search



#Create an Instance of the classes
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
search = Search()

photos = UploadSet('photos', IMAGES)


login_manager.login_view = 'admin.admin_login'
login_manager.login_message_category = 'info'

#Define function Create_app
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    configure_uploads(app, photos)
    patch_request_class(app)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    search.init_app(app)

    



    #import routes
    from estore.main.routes import main
    from estore.admin.routes import admin
    from estore.products.routes import products
    from estore.carts.routes import carts
    from estore.users.routes import users

    #Register Blueprints
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(products)
    app.register_blueprint(carts)
    app.register_blueprint(users)


    #Return app
    return app
