from wtforms import Form, StringField, BooleanField
from wtforms.validators import DataRequired


class NewPostPostomatEditForm(Form):
    address = StringField("Address: ", validators=[DataRequired(message="Address is required")])
    active = BooleanField("Is Active: ")
    city_title = StringField("City Title: ", validators=[DataRequired(message="City title is required")])
