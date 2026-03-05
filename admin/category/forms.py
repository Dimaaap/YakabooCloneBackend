from wtforms import Form, StringField
from wtforms.validators import DataRequired


class BookCategoryEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    slug = StringField("Slug: ", validators=[DataRequired()])