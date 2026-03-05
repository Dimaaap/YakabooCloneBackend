from wtforms import Form, StringField, BooleanField
from wtforms.validators import DataRequired


class FooterEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    link = StringField("Link: ", validators=[DataRequired()])
    active = BooleanField("Is active: ")

