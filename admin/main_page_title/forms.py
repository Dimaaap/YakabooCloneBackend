from wtforms import Form, StringField, BooleanField, DateTimeField
from wtforms.validators import DataRequired


class MainPageTitleEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    active = BooleanField("Is Active: ")


class MainPageTitleCreateForm(MainPageTitleEditForm):
    ...