from wtforms import Form, StringField, BooleanField
from wtforms.validators import DataRequired


class CityEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    is_visible = BooleanField("Is visible: ")
    region = StringField("Region: ")


