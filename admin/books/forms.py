from wtforms import Form, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Optional


class BookEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    slug = StringField("Slug: ", validators=[DataRequired()])
    price = IntegerField("Price: ", validators=[
        DataRequired(), NumberRange(min=0, message="Price can`t be < 0")
    ])
    is_top = BooleanField("Is top: ")
    is_promo = BooleanField("Is promo: ")
    is_in_chart = BooleanField("Is in chart: ")
    promo_price = IntegerField("Promo price: ", validators=[
        Optional(),
        NumberRange(min=0, message="Promo price can`t be < 0")
    ])
    is_notebook = BooleanField("Is notebook: ")
