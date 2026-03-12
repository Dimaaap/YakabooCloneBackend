from wtforms import Form, StringField, IntegerField, BooleanField, DateTimeField, SelectField
from wtforms.validators import DataRequired, NumberRange

from core.models.promo_code import DiscountTypes


class PromoCodesEditForm(Form):
    code = StringField("Code: ", validators=[DataRequired()])
    discount = IntegerField("Discount: ",
                            validators=[NumberRange(min=0, max=100, message="Discount should be in range 1-100")])
    active = BooleanField("Active: ")
    max_uses = IntegerField("Maximum uses: ", validators=[
        DataRequired(),
        NumberRange(min=1, message="Max Uses can`t be < 1")
    ])
    current_uses = IntegerField("Current uses: ", validators=[
        DataRequired(),
        NumberRange(min=1, message="Current Uses can`t be < 1")
    ])
    discount_type = SelectField("Discount Type: ",
                                choices=[
                                    (disc.value, disc.name) for disc in DiscountTypes
                                ],
                                validators=[DataRequired()]
)

    expires_at = DateTimeField("Expires at: ", validators=[DataRequired()])