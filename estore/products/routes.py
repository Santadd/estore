from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required
from estore import db, photos
from estore.products.forms import AddCategoryForm, AddBrandForm, AddProductForm
from estore.products.models import Categories, Brands, Product
import secrets
import os

products = Blueprint('products', __name__)

#Route to add Category
@products.route('/add_category', methods=['GET','POST'])
def add_category():
    form = AddCategoryForm()
    if form.validate_on_submit():
        category = Categories(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash(f'The Category "{form.name.data}" has been added to the database.', 'success')
        return redirect(url_for('products.add_category'))
    return render_template('products/add_brand_or_cat.html', title='Add Category Page', form=form, categories='categories')

#Route to add Brand
@products.route('/add_brand', methods=['GET','POST'])
def add_brand():
    form = AddBrandForm()
    if form.validate_on_submit():
        brand = Brands(name=form.name.data)
        db.session.add(brand)
        db.session.commit()
        flash(f'The Brand "{form.name.data}" has been added to the database.', 'success')
        return redirect(url_for('products.add_brand'))
    return render_template('products/add_brand_or_cat.html', title='Add Brand Page', form=form, brands='brands')

@products.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    brands = Brands.query.all()
    categories = Categories.query.all()
    form = AddProductForm()
    if form.validate_on_submit():

        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        descr = form.descr.data
        stock = form.stock.data
        colors = form.colors.data
        brand = request.form.get('brand')
        category = request.form.get('category')

        #Hash photos before saving into directory
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(16) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(16) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(16) + ".")

        #Add product details
        addpro = Product(name=name, price=price, discount=discount, colors=colors, descr=descr, 
            stock=stock, brand_id=brand, category_id=category, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        db.session.commit()
        flash(f"The product has been added to your database", 'success')
        return redirect(request.referrer)
    return render_template('products/add_product.html', title='Add Product Page', form=form, brands=brands, categories=categories)

#Route to view Products
@products.route('/view_products', methods=['GET', 'POST'])
@login_required
def view_products():
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template('products/view_products.html', title='View Products Page', products=products)

#Route to view Brands
@products.route('/view_brands', methods=['GET', 'POST'])
@login_required
def view_brands():
    brands = Brands.query.order_by(Brands.id.desc()).all()
    return render_template('products/view_brand_or_cat.html', title='View Brands Page', brands=brands)

#Route to view Categories
@products.route('/view_categories', methods=['GET', 'POST'])
@login_required
def view_categories():
    categories = Categories.query.order_by(Categories.id.desc()).all()
    return render_template('products/view_brand_or_cat.html', title='View Categories Page', categories=categories)

#Route to Update Categories
@products.route('/update_category/<int:id>', methods=['GET', 'POST'])
@login_required
def update_category(id):
    
    form = AddCategoryForm()
    category = Categories.query.get_or_404(id)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash(f'Category has been Updated!', 'success')
        return redirect(url_for('products.view_categories'))
    return render_template('products/update_brand_or_cat.html', title='Update Categories Page', category=category, form=form)

#Route to Update Brands
@products.route('/update_brand/<int:id>', methods=['GET', 'POST'])
@login_required
def update_brand(id):

    form = AddBrandForm()
    brand = Brands.query.get_or_404(id)
    if form.validate_on_submit():
        brand.name = form.name.data
        db.session.commit()
        flash(f'Brand has been Updated!', 'success')
        return redirect(url_for('products.view_brands'))
    return render_template('products/update_brand_or_cat.html', title='Update Brands Page', brand=brand, form=form)

#Route to update products
@products.route('/update_product/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    form = AddProductForm()
    product = Product.query.get_or_404(id)

    #Update details on POST
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.colors = form.colors.data
        product.stock = form.stock.data
        product.descr = form.descr.data
        product.brand_id = request.form.get('brand')
        product.category_id = request.form.get('category')

        #replace existing image with the new one in the image folder
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/products/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(16) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(16) + ".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/products/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(16) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(16) + ".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/products/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(16) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(16) + ".")

        
        db.session.commit()
        flash('Product has been Updated successfully', 'success')
        return redirect(url_for('products.view_products'))
    form.colors.data = product.colors
    form.descr.data = product.descr
    return render_template('products/update_product.html', title='Update Product Page', form=form, product=product)

#Route to delete categories 
@products.route('/delete_category/<int:id>/', methods=['POST'])
def delete_category(id):

    category = Categories.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash(f'The category "{category.name}" was deleted!', 'success')
        return redirect(url_for('products.view_categories'))

#Route to delete brands
@products.route('/delete_brand/<int:id>/', methods=['POST'])
def delete_brand(id):

    brand = Brands.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand "{brand.name}" was deleted!', 'success')
        return redirect(url_for('products.view_brands'))

#Route to delete products
@products.route('/delete_product/<int:id>/', methods=['POST'])
def delete_product(id):

    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        #Unlink Images from Images Folder
        try:
            os.unlink(os.path.join(current_app.root_path, "static/products/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/products/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/products/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product "{product.name}" was deleted!', 'success')
        return redirect(url_for('products.view_products'))
    else:
        flash("Can't delete Product", "danger")
        return redirect(url_for('products.view_products'))