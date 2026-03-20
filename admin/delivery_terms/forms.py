from wtforms import Form, IntegerField
from wtforms.validators import NumberRange, Optional


positive_num_validator = [Optional(), NumberRange(min=0, message="Price can`t be < 0")]

class DeliveryTermEditForm(Form):
    yakaboo_shop_price = IntegerField("Yakaboo Shop Price: ",
                                      validators=positive_num_validator)
    new_post_office_price = IntegerField("New Post Office Price: ",
                                         validators=positive_num_validator)
    new_post_department_price = IntegerField("New Post Department Price: ",
                                             validators=positive_num_validator)
    new_post_courier_price = IntegerField("New Post Courier Price: ",
                                          validators=positive_num_validator)
    meest_post_price = IntegerField("Meest Post Price: ",
                                    validators=positive_num_validator)
    ukrpost_department_price = IntegerField("Ukrpost Department Price: ",
                                            validators=positive_num_validator)
    ukrpost_courier_price = IntegerField("Ukrpost Courier Price: ",
                                         validators=positive_num_validator)


class DeliveryTermCreateForm(Form):
    ...

