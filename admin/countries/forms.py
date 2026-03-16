from wtforms import Form, StringField, BooleanField
from wtforms.validators import DataRequired, Regexp

PATTERN = r"^[A-Za-zА-Яа-яІіЇїЄєҐґ'’ \-]+$"

class CountryEditForm(Form):
    title = StringField("Title: ", validators=[
        DataRequired(),
        Regexp(PATTERN, message="Неправильний формат даних")
    ])
    is_visible = BooleanField("Is visible: ")


class CountryCreateForm(CountryEditForm):
    ...