from flask import render_template, redirect, url_for, session, Blueprint, request, flash, make_response
from estore import db, bcrypt
from flask_login import  current_user
from estore.users.models import Customer, CustomerOrder, Address
import secrets
import pdfkit

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

    if 'customer' in session:
        return redirect(url_for('main.home'))

    email = request.form.get('email')
    password= request.form.get('password')
    remember = request.form.get('rememberCheckbox')

    
    if request.method == 'POST':
        user = Customer.query.filter_by(email=email).first() 
        if user and bcrypt.check_password_hash(user.password, password):
            session['customer'] = email
            flash(f'Login successful', 'success')
            return redirect(url_for('main.home'))
        #Check password hash and user if they exist
        else:
            flash(f'Incorrect username/password!. Please try again', 'danger')
            return redirect(url_for('users.customer_login'))
    return render_template('users/user_login_reg_form.html', title='Account Page', login='login')

@users.route('/customer_logout')
def customer_logout():
    try:
        session.pop('customer', None)
        return redirect(url_for('main.home'))
    except Exception as e:
        print(e)
        return redirect(url_for('main.home'))

@users.route('/checkout', methods=['GET', 'POST'])
def checkout():

    #Check to see if there are items in the shopping cart
    sub_total = 0
    vat = 0
    grand_total = 0
    shipping_fee = 125
    
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0:
        return redirect(url_for('main.home'))
    #If items are there, calculate grandtotal of items
    for key, product in session['Shoppingcart'].items():
        discount_price = product['price']-((product['discount']/100) * (product['price']))
        sub_total += (float(product['quantity']) * discount_price)
        vat += (0.05 * float(product['quantity']) * product['price'])
        grand_total = sub_total + vat + shipping_fee

    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        company = request.form.get('companyName')
        country = request.form.get('country')
        street_add = request.form.get('streetAddress')
        city = request.form.get('cityAddress')
        postcode = request.form.get('postcode')
        email = request.form.get('emailAddress')
        mobile_no = request.form.get('mobileno')
        #Get id of customer if User is logged in
        if 'customer' in session:
            customer = Customer.query.filter_by(email=session['customer']).first()
            customer_id = customer.id
        else:
            customer_id = int(0)
        #Get order details
        invoice = secrets.token_hex(16)
        try:
            #Put orders into database
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
            #Store Address of Customer
            cust_details = Address(first_name=first_name, last_name=last_name, company=company, country=country, street_add=street_add,
                                city=city, postcode=postcode, mobile_no=mobile_no, email=email, customer_id=customer_id)
            db.session.add(cust_details)
            db.session.add(order)
            db.session.commit()
            #Clear carts in session
            session.pop('Shoppingcart')
            flash(f'Your order has been sent successfully!', 'success')
            return redirect(url_for('users.view_orders', invoice=invoice))
        except Exception as e:
            flash('Something went wrong while getting order', 'danger')
            print(e)
            return redirect(url_for('users.checkout'))

    return render_template('users/checkout.html', title='CheckOut Page', vat=vat, 
                            grand_total=grand_total, sub_total=sub_total, shipping_fee=shipping_fee)



@users.route('/view_orders/<invoice>')
def view_orders(invoice):

    if 'customer' in session:
        sub_total = 0
        vat = 0
        grand_total = 0
        shipping_fee = 125
        cust = Customer.query.filter_by(email=session['customer']).first()
        customer_id = cust.id
        customer = Customer.query.filter_by(id=customer_id).first()
        #Get the latest order from customer
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        address = Address.query.filter_by(customer_id=customer_id).order_by(Address.id.desc()).first()

        for key, product in orders.orders.items():
            discount_price = product['price']-((product['discount']/100) * (product['price']))
            sub_total += (float(product['quantity']) * discount_price)
            vat += (0.05 * float(product['quantity']) * product['price'])
            grand_total = sub_total + vat + shipping_fee
    else:
        return redirect(url_for('main.home'))    

    return render_template('users/new_.html', title='Orders Page', customer=customer, orders=orders,
                    sub_total=sub_total, grand_total=grand_total, vat=vat, shipping_fee=shipping_fee, address=address)

@users.route('/get_pdf/<invoice>', methods=['POST'])
def get_pdf(invoice):

    if 'customer' in session:
        sub_total = 0
        vat = 0
        grand_total = 0
        shipping_fee = 125
        if request.method == 'POST':
            cust = Customer.query.filter_by(email=session['customer']).first()
            customer_id = cust.id
            customer = Customer.query.filter_by(id=customer_id).first()
            #Get the latest order from customer
            orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
            address = Address.query.filter_by(customer_id=customer_id).first()

            for key, product in orders.orders.items():
                discount_price = product['price']-((product['discount']/100) * (product['price']))
                sub_total += (float(product['quantity']) * discount_price)
                vat += (0.05 * float(product['quantity']) * product['price'])
                grand_total = sub_total + vat + shipping_fee   

            rendered =  render_template('users/get_orders_pdf.html', title='Orders Page', customer=customer, orders=orders,
                            sub_total=sub_total, grand_total=grand_total, vat=vat, shipping_fee=shipping_fee, address=address)
            
            #Get pdf
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['content-Type'] = 'application/pdf'
            response.headers['content-Dispostion'] = 'inline: filename='+ invoice +'.pdf'
            return response

    return redirect(url_for('users.view_orders'))

@users.route('/view')
def view_pdf():
    return render_template('users/invoice.html')

