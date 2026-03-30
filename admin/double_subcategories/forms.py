from wtforms import Form, StringField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional



class DoubleSubCategoryEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    slug = StringField("Slug: ", validators=[DataRequired()])
    is_visible = BooleanField("Is visible: ")


class DoubleSubCategoryCreateForm(DoubleSubCategoryEditForm):
    subcategory_id = SelectField("Subcategories: ", coerce=int,
                                            validators=[Optional()])
    images_src = TextAreaField("Images: ", validators=[Optional()])
