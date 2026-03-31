from wtforms import Form, BooleanField, StringField, SelectField
from wtforms.validators import Optional


def coerce_optional_int(value):
    if value in ("", None, 0, "0"):
        return None
    return int(value)


class PaymentMethodCommonFieldsMixin:
    cart_or_scholar_pack = BooleanField("Cart Or Scholar Pack: ")
    winter_e_support = BooleanField("Winter E Support: ")
    e_book = BooleanField("E-Book: ")
    upon_receipt = BooleanField("Upon receipt: ")
    prepay = BooleanField("Prepayment: ")
    privat_bank_parts = BooleanField("PrivatBank Parts: ")
    monobank_parts = BooleanField("Monobank Parts: ")


class PaymentMethodEditForm(Form, PaymentMethodCommonFieldsMixin):
    country_title = StringField("Country Title: ")
    city_title = StringField("City Title: ")


class PaymentMethodCreateForm(Form, PaymentMethodCommonFieldsMixin):
    country_id = SelectField("Country: ", coerce=coerce_optional_int,
                             validators=[Optional()])
    city_id = SelectField("City: ", coerce=coerce_optional_int,
                          validators=[Optional()])