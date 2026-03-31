from wtforms import Form, StringField, DateTimeField, BooleanField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Optional


class PromotionsCommonFieldsMixin:
    title = StringField("Title: ", validators=[DataRequired()])
    slug = StringField("Slug: ", validators=[DataRequired()])
    image = StringField("Image: ")
    main_description = TextAreaField("Main Description: ")
    short_description = TextAreaField("Short Description: ")
    long_description = TextAreaField("Long Description: ")
    end_date = DateTimeField("End Date: ")
    is_active = BooleanField("Is Active: ")


class PromotionsEditForm(Form, PromotionsCommonFieldsMixin):
    categories_title = SelectMultipleField("Categories: ")


class PromotionsCreateForm(Form, PromotionsCommonFieldsMixin):
    categories = SelectMultipleField("Categories: ", validators=[Optional()])