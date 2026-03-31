from wtforms import Form, StringField, BooleanField
from wtforms.validators import DataRequired


class PromoCategoryEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    slug = StringField("Slug: ", validators=[DataRequired()])
    is_active = BooleanField("Is active: ")


class PromoCategoryCreateForm(PromoCategoryEditForm):
    ...


