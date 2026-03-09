from wtforms import Form, BooleanField, StringField


class PaymentMethodEditForm(Form):
    cart_or_scholar_pack = BooleanField("Cart Or Scholar Pack: " )
    winter_e_support = BooleanField("Winter E Support: ")
    e_book = BooleanField("E-Book: ")
    upon_receipt = BooleanField("Upon receipt: ")
    prepay = BooleanField("Prepayment: ")
    privat_bank_parts = BooleanField("PrivatBank Parts: ")
    monobank_parts = BooleanField("Monobank Parts: ")

    country_title = StringField("Country Title: ")
    city_title = StringField("City Title: ")