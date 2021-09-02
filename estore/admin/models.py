from estore import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_admin(admin_id):
    return Admin.query.get(int(admin_id))

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    profile = db.Column(db.String(100), default='default.jpg')

    def __repr__(self):
        return f"Admin('{self.username}', '{self.email}')"
