from wtforms import Form, TextAreaField, SelectField
from wtforms.validators import DataRequired


class AuthorFactsForm(Form):
    fact_text = TextAreaField("fact_text", validators=[DataRequired()])

    author_id = SelectField("Author: ",
                            coerce=int,
                            validators=[DataRequired()])


class CreateAuthorFactsForm(AuthorFactsForm):
    ...