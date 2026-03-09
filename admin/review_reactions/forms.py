from wtforms import Form, StringField, BooleanField, DateTimeField
from wtforms.validators import DataRequired


class ReviewReactionsEditForm(Form):
    user_email = StringField("User Email: ", validators=[DataRequired()])
    review_title = StringField("Review Title: ", validators=[DataRequired()])
    is_like = BooleanField("Is like: ")
    created_at = DateTimeField("Created at: ")