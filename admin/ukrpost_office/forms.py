from wtforms import Form, StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired, NumberRange


class UkrpostOfficeEditForm(Form):
    office_number = IntegerField("Office Number: ", validators=[
        DataRequired(message="Office number is required"),
        NumberRange(min=1, message="Office number can`t be < 1")
    ])

    address = StringField("Address: ", validators=[DataRequired(message="Address is required")])
    active = BooleanField("Is Active: ")

    city_title = StringField("City Title: ", validators=[DataRequired(message="City title is required")])