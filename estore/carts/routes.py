from operator import sub
from flask import redirect, render_template, url_for, Blueprint, request,session
from flask.globals import session
from flask.helpers import flash
from estore.products.models import Product

carts = Blueprint('carts', __name__)


#Function to merge two dictionaries
def merge_dicts(dict1, dict2):
    #Check to see if instance is dictionary or list

    if isinstance(dict1, list) and isinstance(dict2, list): #If it is a list
        return dict1 + dict2

    elif isinstance(dict1, dict) and isinstance(dict2, dict): #If it is a dictionary
        return dict(list(dict1.items()) + list(dict2.items()))

    return False

@carts.route('/add_cart', methods=['GET', 'POST'])
def add_cart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
        product = Product.query.filter_by(id=product_id).first()
        #Store items in Dictionary if method is a POST and all fields are valid
        if quantity and product_id and colors and request.method == 'POST':
            DictItems = {product_id:{'name': product.name, 'price': float(product.price), 'discount': product.discount,
                        'color': colors, 'quantity': quantity, 'image': product.image_1, 'colors': product.colors}}
            #Check to see if there are items in the session
            if 'Shoppingcart' in session:
                #Update quantity if product is in session
                if product_id in session['Shoppingcart']:
                    for key, value in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            value['quantity'] = int(value['quantity']) + int(quantity)
                #If product is not in session, then add new cart. Merge dictionary
                else:
                    session['Shoppingcart'] = merge_dicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            #Store the items in session if there are none
            else:
                session['Shoppingcart'] = DictItems
                redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@carts.route('/display_cart_items', methods=['GET', 'POST'])
def cart_items():
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

    #Update cart Items
    if request.method == 'POST':
        
        quantity = request.form.get('quantity')
        prod_id = request.form.get('product_id')
        col = request.form.get('col')
        print(col)
        try:
            if 'Shoppingcart' in session:
                session.modified = True
                for key, value in session['Shoppingcart'].items():
                    if key == prod_id:
                        session['Shoppingcart'][key]['quantity'] = quantity
                        value['color'] = col
                        print(session['Shoppingcart'][key]['quantity'])
                        print(value['color'])
                        print(session['Shoppingcart'])
                        flash(f'Cart Item  \" {value["name"]} \"  has been updated successfully', 'success')
                        return redirect(url_for('carts.cart_items'))
        except Exception as e:
            print(e)
            return redirect(url_for('carts.cart_items'))

    return render_template('carts/carts.html', title='Carts Page', vat=vat, 
                            grand_total=grand_total, sub_total=sub_total, shipping_fee=shipping_fee)

#Remove Cart Items
@carts.route('/delete_cart_item/<int:id>', methods=['POST', 'GET'])
def delete_cart_item(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0:
        return redirect(url_for('main.home'))
    
    
    if 'Shoppingcart' in session:
        try:
            session.modified = True
            for key, value in session['Shoppingcart'].items():
                if int(key) == id:
                    session['Shoppingcart'].pop(key, None)
                    flash(f'Cart Item  \" {value["name"]} \"  has been removed from list successfully!', 'success')
                    return redirect(url_for('carts.cart_items'))
        except Exception as e:
            print(e)
            return redirect(url_for('carts.cart_items'))  

#Clear Cart Items
@carts.route('/clear_cart')
def clear_cart():
    try:
        #Remove Shoppingcart session
        session.pop('Shoppingcart', None)
        return redirect(url_for('main.home'))
    except Exception as e:
        print(e)
        return redirect(url_for('main.home'))                 

