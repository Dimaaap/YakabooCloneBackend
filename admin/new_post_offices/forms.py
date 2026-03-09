from wtforms import Form, StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired, NumberRange


class NewPostOfficeEditForm(Form):
    number = IntegerField("Office Number: ", validators=[DataRequired(message="Office number is required"),
                                                         NumberRange(min=0, message="Office number can`t be < 1")])
    address = StringField("Address: ", validators=[DataRequired(message="Address is required")])
    active = BooleanField("Is Active: ")
    weight_to = IntegerField("Weight To: ", validators=[NumberRange(min=1, message="Weight can`t be < 1")])
    city_title = StringField("City Title: ", validators=[DataRequired(message="City title is required")])

