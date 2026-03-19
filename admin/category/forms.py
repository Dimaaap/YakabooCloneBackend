from wtforms import Form, StringField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Optional


class BookCategoryEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    slug = StringField("Slug: ", validators=[DataRequired()])


class BookCategoryCreateForm(BookCategoryEditForm):
    banner_images = TextAreaField("Images: ", validators=[Optional()])
    subcategories_ids = SelectMultipleField("Subcategories: ", coerce=int,
                                            validators=[Optional()])

