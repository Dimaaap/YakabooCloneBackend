from wtforms import Form, StringField
from wtforms.validators import DataRequired


class AuthorFactsForm(Form):
    fact_text = StringField("fact_text", validators=[DataRequired()])
