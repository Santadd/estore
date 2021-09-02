import re
from flask import render_template, redirect, url_for, session, Blueprint, request, flash
from estore import db, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from estore.users.models import Customer

users = Blueprint('users', __name__)

@users.route('/customer_registration', methods=['GET', 'POST'])
def customer_registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    #Get form details from template
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    #hash password before storing into database
    if request.method == 'POST':
        hashed_pw = bcrypt.generate_password_hash(password)
        #Query to see if user details is not in database
        customer = Customer.query.filter_by(email=email).first()
        if customer:
            flash(f'Email already exists!', 'danger')
            return redirect(url_for('users.customer_registration'))
        else:
            user = Customer(first_name=first_name, last_name=last_name, username=username, email=email, password=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created successfully!', 'success')
            return redirect(url_for('users.customer_registration'))
    return render_template('users/user_login_reg_form.html', title='Account Page', registration='registration')

@users.route('/customer_login', methods=['GET','POST'])
def customer_login():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    email = request.form.get('email')
    password= request.form.get('password')
    remember = request.form.get('rememberCheckbox')

    
    if request.method == 'POST':
        user = Customer.query.filter_by(email=email).first() 
        if user and bcrypt.check_password_hash(user.password, password):
            next = request.args.get('next')
            login_user(user, remember=remember)
            flash(f'Login successful', 'success')
            return redirect(next) if next else redirect(url_for('main.home'))
        #Check password hash and user if they exist
        else:
            flash(f'Incorrect username/password!. Please try again', 'danger')
            return redirect(url_for('users.customer_login'))
    return render_template('users/user_login_reg_form.html', title='Account Page', login='login')

@users.route('/customer_logout')
def customer_logout():
    logout_user()
    return redirect(url_for('main.home'))