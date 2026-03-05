from wtforms import Form, StringField, BooleanField
from wtforms.validators import DataRequired


class InterestingEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    slug = StringField("Slug: ", validators=[DataRequired()])
    visible = BooleanField("Is visible: ")
    link = StringField("Link: ", validators=[DataRequired()])
