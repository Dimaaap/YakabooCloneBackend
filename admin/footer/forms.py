from wtforms import Form, StringField, BooleanField, SelectField
from wtforms.validators import DataRequired

from core.models.footer import FooterCategory


class FooterEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    link = StringField("Link: ", validators=[DataRequired()])
    active = BooleanField("Is active: ")


class FooterCreateForm(FooterEditForm):
    category = SelectField("Category: ",
                           choices=[(cat.value, cat.name) for cat in FooterCategory],
                           validators=[DataRequired()])
