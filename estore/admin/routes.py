from flask import render_template, Blueprint, flash, request
from flask.helpers import url_for
from werkzeug.utils import redirect
from estore import bcrypt, db
from flask_login import login_user, logout_user, current_user
from estore.admin.forms import AdminRegistrationForm, AdminLoginForm
from estore.admin.models import Admin


admin = Blueprint('admin', __name__)


@admin.route('/admin_register', methods=['GET','POST'])
def admin_register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        admin = Admin(name=form.name.data, username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(admin)
        db.session.commit()
        flash(f"The username {form.username.data} has been registered successfully!", 'success')
        return redirect(url_for('main.home')) 
    return render_template('admin/admin_register.html', title='Admin Register Page', form=form)

@admin.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = AdminLoginForm()
    if form.validate_on_submit():

        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin, remember=form.remember.data)
            flash(f'Login successful!', 'success')
            return redirect(request.args.get('next') or url_for('main.home'))
        else:
            flash(f'Incorrect email and password. Please try again!', 'danger')
    return render_template('admin/admin_login.html', title='Admin Login Page', form=form)

@admin.route('/admin_logout')
def admin_logout():
    logout_user()
    return redirect(url_for('admin.admin_login'))

