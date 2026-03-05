from wtforms import Form, StringField, BooleanField
from wtforms.validators import DataRequired


class BookTranslatorEditForm(Form):
    first_name = StringField("First Name: ", validators=[DataRequired()])
    last_name = StringField("Last Name: ")
    slug = StringField("Slug: ", validators=[DataRequired()])
    is_active = BooleanField("Is Active: ")