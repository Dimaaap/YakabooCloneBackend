import re

from wtforms import Form, StringField, BooleanField, DateField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Optional



class AuthorEditForm(Form):
    first_name = StringField("First Name: ", validators=[DataRequired()])
    last_name = StringField("Last Name: ", validators=[DataRequired()])
    slug = StringField("Slug: ", validators=[DataRequired()])
    date_of_birth = DateField("Date of Birth: ", validators=[Optional()])
    is_active = BooleanField("Is Active: ")

    short_description = TextAreaField("Short Description: ", validators=[Optional()])
    description = TextAreaField("Description: ", validators=[Optional()])

    def validate_slug(self, field):
        if not re.match(r'^[A-Za-z0-9-]+$', field.data):
            raise ValidationError("Slug can contain only English letters, numbers and hyphens.")
