from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, TextAreaField, BooleanField
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired

class AddCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])

class AddBrandForm(FlaskForm):
    name = StringField('Brand Name', validators=[DataRequired()])

#AddProduct Form
class AddProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(message="Invalid Input")])
    stock = IntegerField('Stock', validators=[NumberRange(min=0), InputRequired(message="Invalid Input")])
    discount = IntegerField('Discount', default=0)
    descr = TextAreaField('Description', validators=[DataRequired()])
    colors = TextAreaField('Colors', validators=[DataRequired()])

    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    image_3 = FileField('Image 3', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])