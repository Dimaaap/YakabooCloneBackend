from wtforms import Form, StringField, BooleanField, SelectField
from wtforms.validators import DataRequired


class CityEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    is_visible = BooleanField("Is visible: ")
    region = StringField("Region: ")
    country_id = SelectField("Country: ",
                                coerce=int,
                                validators=[DataRequired()])


class CityCreateForm(CityEditForm):
    ...