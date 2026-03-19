from wtforms import StringField, BooleanField, Form
from wtforms.validators import DataRequired


class BookSeriaEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    slug = StringField("Slug: ", validators=[DataRequired()])
    is_active = BooleanField("Is Active: ")


class BookSeriaCreateForm(BookSeriaEditForm):
    ...

