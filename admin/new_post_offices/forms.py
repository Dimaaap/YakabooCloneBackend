from wtforms import Form, StringField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional


class NewPostOfficeCommonFieldsMixin:
    address = StringField("Address: ", validators=[DataRequired(message="Address is required")])
    active = BooleanField("Is Active: ")
    weight_to = IntegerField("Weight To: ", validators=[
        Optional(),
        NumberRange(min=1, message="Weight can`t be < 1")])


class NewPostOfficeEditForm(Form, NewPostOfficeCommonFieldsMixin):
    city_title = StringField("City Title: ", validators=[DataRequired(message="City title is required")])


class NewPostOfficeCreateForm(Form, NewPostOfficeCommonFieldsMixin):
    city_id = SelectField("City: ", coerce=int,
                          validators=[DataRequired(message="City is required")])
