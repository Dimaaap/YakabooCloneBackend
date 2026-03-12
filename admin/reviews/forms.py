from wtforms import Form, StringField, IntegerField, TextAreaField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Optional


class ReviewEditForm(Form):
    rate = IntegerField("Rate: ", validators=[
        DataRequired(),
        NumberRange(min=1, max=5, message="Rate should be between 1 and 5")
    ])
    title = StringField("Title: ")
    comment = TextAreaField("Comment: ", validators=[DataRequired()])
    user_name = StringField("User name: ", validators=[DataRequired()])
    created_date = DateTimeField("Created date: ", format="%m/%d/%Y %I:%M %p")
    is_validated = BooleanField("Is Validated: ")
    likes_count = IntegerField("Likes count: ", validators=[
        Optional(),
        NumberRange(min=0, message="Likes count can`t be < 0")
    ])
    dislikes_count = IntegerField("Dislikes count: ", validators=[
        Optional(),
        NumberRange(min=0, message="Dislikes count can`t be < 0")
    ])
    user_email = StringField("User email: ", validators=[DataRequired()])
    book_title = StringField("Book title: ", validators=[DataRequired()])