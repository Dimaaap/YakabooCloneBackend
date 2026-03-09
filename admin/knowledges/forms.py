from wtforms import Form, StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired


class KnowledgeEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    slug = StringField("Slug: ", validators=[DataRequired()])
    container_title = StringField("Container Title: ")
    in_sidebar = BooleanField("Is In Sidebar: ")
    is_active = BooleanField("Is Active: ")
    content = TextAreaField("Content: ", validators=[DataRequired()])