from wtforms import Form, StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class PublishingEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    slug = StringField("Slug: ", validators=[DataRequired()])
    logo = StringField("Logo src: ")
    short_description = TextAreaField("Short description: ")
    long_description = TextAreaField("Long description: ")
    visible = BooleanField("Is Visible: ")