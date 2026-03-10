from wtforms import Form, TextAreaField
from wtforms.validators import DataRequired


class AuthorFactsForm(Form):
    fact_text = TextAreaField("fact_text", validators=[DataRequired()])
