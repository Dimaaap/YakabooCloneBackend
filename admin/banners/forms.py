from wtforms import StringField, BooleanField, Form
from wtforms.validators import DataRequired


class BannerEditForm(Form):
    image_src = StringField("Image src: ", validators=[DataRequired()])
    link = StringField("Link: ")
    visible = BooleanField("Is Visible: ")
    in_all_books_page = BooleanField("Is In All Book Page: ")


class BannerCreateForm(BannerEditForm):
    ...
