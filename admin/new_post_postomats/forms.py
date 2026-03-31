from wtforms import Form, StringField, BooleanField, SelectField
from wtforms.validators import DataRequired


class NewPostPostomatCommonFieldsMixin:
    address = StringField("Address: ", validators=[DataRequired(message="Address is required")])
    active = BooleanField("Is Active: ")


class NewPostPostomatEditForm(Form, NewPostPostomatCommonFieldsMixin):
    city_title = StringField("City Title: ", validators=[DataRequired(message="City title is required")])


class NewPostPostomatCreateForm(Form, NewPostPostomatCommonFieldsMixin):
    city_id = SelectField("City: ", coerce=int,
                          validators=[DataRequired(message="City id is required")])


