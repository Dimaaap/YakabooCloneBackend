from wtforms import Form, StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Optional


class NewPostOfficeEditForm(Form):
    address = StringField("Address: ", validators=[DataRequired(message="Address is required")])
    active = BooleanField("Is Active: ")
    weight_to = IntegerField("Weight To: ", validators=[
        Optional(),
        NumberRange(min=1, message="Weight can`t be < 1")])
    city_title = StringField("City Title: ", validators=[DataRequired(message="City title is required")])

