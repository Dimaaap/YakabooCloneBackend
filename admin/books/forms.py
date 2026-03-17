from wtforms import Form, StringField, BooleanField, SelectField, IntegerField, SelectMultipleField
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


class BookCreateForm(BookEditForm):
    book_info_id = SelectField("Book Info: ", coerce=int,
                               validators=[DataRequired()])
    author_ids = SelectMultipleField("Authors: ", coerce=int,
                                        validators=[DataRequired()])
    translators_ids = SelectMultipleField("Translators: ", coerce=int,
                                           validators=[Optional()])
    illustrators_ids = SelectMultipleField("Illustrators: ", coerce=int,
                                            validators=[Optional()])
    literature_period_id = SelectField("Literature Period: ", coerce=int,
                                          validators=[Optional()])
    seria_id = SelectField("Book Seria: ", coerce=int,
                                   validators=[Optional()])
    categories_ids = SelectMultipleField("Categories: ", coerce=int,
                                     validators=[Optional()])
    double_subcategories_ids = SelectMultipleField("Double Subcategories: ", coerce=int,
                                               validators=[Optional()])
    publishing_id = SelectField("Publishing: ", coerce=int,
                             validators=[DataRequired()])
