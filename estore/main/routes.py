from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required
from estore import db, search
from estore.products.models import Product, Brands, Categories

main = Blueprint('main', __name__)

def feat_items():
    #Featured Items
    feat_items = Product.query.filter(Product.stock > 0).order_by(Product.id.asc()).limit(3).all()
    return feat_items

@main.route('/')
@main.route('/home')
def home():
    #Display last three items in slider section
    items = Product.query.filter(Product.stock > 0).order_by(Product.id.desc()).limit(3).all()
    #Featured Items
    feat_items = Product.query.filter(Product.stock > 0).order_by(Product.id.asc()).limit(3).all()
    categories = Categories.query.all()
    return render_template('main/homepage.html', title='Home Page', items=items, feat_items=feat_items, categories=categories)


#Route to search items in products
@main.route('/search_products')
def search_products():
    #Query from the products page 
    searchword = request.args.get('q')
    product = Product.query.msearch(searchword, fields=['name', 'descr'])
    return render_template('main/search_result.html', title='Search Results Page', product=product)

#Display categories
@main.route('/prod_categories')
def disp_categories():
    products = Product.query.filter(Product.stock > 0).order_by(Product.id.desc()).limit(3).all()
    categories = db.session.query(Categories).join(Product, Categories.id == Product.category_id)
    
    return render_template('main/product_categories.html', title='Categories Page', 
                            categories=categories, products=products, feat_items = feat_items())

#Display category/ list
@main.route('/display_category_list', methods=['GET', 'POST'])
def disp_category_list():
    page = request.args.get('page', 1, type=int)
    categories = Categories.query.all()
    products = Product.query.filter(Product.stock > 0).order_by(Product.id.desc()).paginate(page=page, per_page=3)
    
    return render_template('main/category_list.html', title='Category List Page', 
        categories=categories, feat_items=feat_items(), products=products)

@main.route('/search_page_number', methods=['POST', 'GET'])
def search_page():
    page_number = request.form.get('page_number')

    if request.method == 'POST':
        page_number = request.form.get('page_number')
        return redirect(url_for('main.disp_category_list', page=page_number))
  
    return redirect(url_for('main.disp_category_list', page=page_number))

#Display single product details
@main.route('/product_details/<int:id>')
def product_details(id):

    product = Product.query.get_or_404(id)
    return render_template('main/product_details.html', title='Product Details Page', product=product)


@main.route('/')
@main.route('/pages')
def lay():
    return render_template('includes/pages_layout.html', title='Home Page') 