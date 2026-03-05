from wtforms import Form, StringField, BooleanField
from wtforms.validators import DataRequired


class ContactEditForm(Form):
   social_title = StringField("Social Title: ", validators=[DataRequired()])
   link = StringField("Link: ", validators=[DataRequired()])
   icon_title = StringField("Icon Title: ")
   is_active = BooleanField("Is Active: ")
