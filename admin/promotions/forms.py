from wtforms import Form, StringField, DateTimeField, BooleanField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired


class PromotionsEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    slug = StringField("Slug: ", validators=[DataRequired()])
    image = StringField("Image: ")
    main_description = TextAreaField("Main Description: ")
    short_description = TextAreaField("Short Description: ")
    long_description = TextAreaField("Long Description: ")
    end_date = DateTimeField("End Date: ")
    is_active = BooleanField("Is Active: ")

    categories_title = SelectMultipleField("Categories: ")