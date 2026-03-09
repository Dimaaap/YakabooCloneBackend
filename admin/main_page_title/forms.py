from wtforms import Form, StringField, BooleanField, DateTimeField
from wtforms.validators import DataRequired


class MainPageTitleEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    active = BooleanField("Is Active: ")
    created_at = DateTimeField("Created at: ", validators=[DataRequired()])
    updated_at = DateTimeField("Updated at: ", validators=[DataRequired()])