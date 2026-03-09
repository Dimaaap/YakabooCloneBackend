from wtforms import Form, StringField, DateTimeField
from wtforms.validators import DataRequired


class PromoCodeUsageEditForm(Form):
    user_email = StringField("User Email: ", validators=[DataRequired()])
    promo_code_title = StringField("Promo Code Title: ", validators=[DataRequired()])
    used_at = DateTimeField("Used At: ", format="%Y-%m-%d %H:%M:%S")
