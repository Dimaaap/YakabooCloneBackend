from wtforms import Form, StringField, BooleanField
from wtforms.validators import DataRequired


class DoubleSubCategoryEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    slug = StringField("Slug: ", validators=[DataRequired()])
    is_visible = BooleanField("Is visible: ")
