from wtforms import Form, StringField, SelectField
from wtforms.validators import DataRequired

from core.models.literature_periods import PeriodTitleType


class LiteraturePeriodsEditForm(Form):
    title = SelectField("Title: ",
                        choices=[(status.value, status.name) for status in PeriodTitleType],
                        validators=[DataRequired()])
    slug = StringField("Slug: ", validators=[DataRequired()])