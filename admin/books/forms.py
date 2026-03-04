from wtforms import Form, StringField, BooleanField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, NumberRange


class BookEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    slug = StringField("Slug: ", validators=[DataRequired()])
    price = IntegerField("Price: ", validators=[
        DataRequired(), NumberRange(min=0, message="Price can`t be < 0")
    ])
    is_top = BooleanField("Is top: ")
    is_promo = BooleanField("Is promo: ")
    is_in_chart = BooleanField("Is in chart: ")
    stars = IntegerField("Stars :", validators=[
        NumberRange(min=0, max=5, message="Stars` count should be in range 1-5")
    ])
    promo_price = IntegerField("Promo price: ", validators=[
        NumberRange(min=0, message="Promo price can`t be < 0")
    ])
    created_date = DateTimeField("Created date: ", render_kw={"readonly": True})
    is_notebook = BooleanField("Is notebook: ")
