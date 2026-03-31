from wtforms import Form, StringField, SelectField, BooleanField
from wtforms.validators import DataRequired


class MeestPostOfficeCommonFieldsMixin:
    address = StringField("Address: ", validators=[DataRequired(message="Address is required")])
    active = BooleanField("Is Active: ")


class MeestPostOfficeEditForm(Form, MeestPostOfficeCommonFieldsMixin):
    city_title = StringField("City Title: ", validators=[DataRequired(message="City title is required")])


class MeestPostOfficeCreateForm(Form, MeestPostOfficeCommonFieldsMixin):
    city_id = SelectField("City: ", coerce=int,
                          validators=[DataRequired(message="City id is required")])