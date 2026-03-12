from wtforms import Form, StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired, NumberRange


class MeestPostOfficeEditForm(Form):
    address = StringField("Address: ", validators=[DataRequired(message="Address is required")])
    active = BooleanField("Is Active: ")
    city_title = StringField("City Title: ", validators=[DataRequired(message="City title is required")])
