from wtforms import (Form, StringField, BooleanField, DateField, IntegerField,
                     SelectField, DateTimeField, ValidationError)
from wtforms.validators import DataRequired, Email, Length, NumberRange
import phonenumbers

from core.models.user import UserStatusEnum


class UserEditForm(Form):
    first_name = StringField("First Name: ", validators=[DataRequired(), Length(min=2, max=200)])
    last_name = StringField("Last Name: ", validators=[DataRequired(), Length(min=2, max=200)])
    phone_number = StringField("Phone: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[DataRequired(), Email(), Length(min=6, max=40)])
    is_staff = BooleanField("Staff: ")
    is_active = BooleanField("Active: ")
    is_verified = BooleanField("Verified: ")
    is_subscribed_to_news = BooleanField("Subscribed to News: ")

    birth_date = DateField("Birth Date: ")
    bonuses = IntegerField("Bonuses: ", validators=[NumberRange(min=0, message="Bouneses count can`t be < 0")])
    level = SelectField("Level: ", choices=[(status.value, status.name) for status in UserStatusEnum],
                        validators=[DataRequired()])

    def validate_phone_number(self, field):
        if len(field.data) > 16:
            raise ValidationError("Invalid phone number")
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError("Invalid phone number")
        except:
            input_number = phonenumbers.parse("+380"+field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError("Invalid phone number")