from wtforms import Form, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class SidebarsEditForm(Form):
    title = StringField("Title: ", validators=[DataRequired()])
    slug = StringField("Slug: ", validators=[DataRequired()])
    icon = StringField("Icon src: ")
    visible = BooleanField("Is visible: ")
    order_number = IntegerField("Order number: ",
                                validators=[DataRequired(),
                                            NumberRange(min=0, message="Order number can`t be < 0")])
    is_clickable = BooleanField("Is clickable: ")
    link = StringField("Link: ")