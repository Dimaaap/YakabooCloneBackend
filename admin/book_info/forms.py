from wtforms import Form, BooleanField, StringField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, NumberRange

from core.models.book_info import CoverTypes, LiteratureTypes, LiteratureProgramClasses, BookFormats, PageFormats, \
    BookLanguages, PagesType, SizeTypes


class BookInfoEditForm(Form):
    is_stock = BooleanField("In Stock: ")
    visible = BooleanField("Visible: ")
    code = IntegerField("Code: ", validators=[DataRequired()])
    rate = FloatField("Rate: ")
    illustrations = StringField("Illustrations: ")
    ISBN = StringField("ISBN: ", validators=[DataRequired()])
    cover_type = SelectField("Cover Type: ", choices=[(type.value, type.name) for type in CoverTypes],
                             validators=[DataRequired()])
    pages_count = IntegerField("Pages Count: ",
                               validators=[NumberRange(min=1, message="Pages count can`t be < 1")])
    is_has_cashback = BooleanField("Has cashback: ")
    is_has_winter_esupport = BooleanField("Has winter support: ")
    is_has_esupport = BooleanField("Has esupport: ")
    is_for_war = BooleanField("Is Charity For War: ")
    bonuses = IntegerField("Bonuses: ", validators=[NumberRange(min=0, message="Bonuses count can't be < 0")])
    literature_type = SelectField("Literature Type: ",
                                  choices=[(type.value, type.name) for type in LiteratureTypes])
    literature_program_class = SelectField("Literature Program Class: ",
                                           choices=[(program.value, program.name)
                                                    for program in LiteratureProgramClasses ])
    present_edition_and_sets = StringField("Present Edition or Set: ")
    weight = IntegerField("Weight: ", validators=[NumberRange(min=1, message="Weight can`t be < 1")])
    original_name = StringField("Original Name: ")
    format = SelectField("Format: ", choices=[(format.value, format.name) for format in BookFormats])
    pages_format = SelectField("Pages Format: ", choices=[(format.value, format.name) for format in PageFormats])
    language = SelectField("Language: ", choices=[(lang.value, lang.name) for lang in BookLanguages])
    color = StringField("Color: ")
    papers = SelectField("Papers: ", choices=[(paper.value, paper.name) for paper in PagesType])
    size = SelectField("Size: ", choices=[(size.value, size.name) for size in SizeTypes])
    pages_color = StringField("Pages Color: ")
    type = StringField("Type: ")
    edition = IntegerField("Edition: ", validators=[NumberRange(min=0, message="Edition can`t be < 0")])
    book_format = StringField("Book Format: ")
    waiting_from = StringField("Waiting From: ")
    is_free_delivery = BooleanField("Is Free Delivery: ")
    delivery_time = IntegerField("Delivery Time: ",
                                 validators=[NumberRange(min=0, message="Delivery time can`t be < 0")])
    uk_delivery_time = IntegerField("UK Delivery Time: ",
                                    validators=[NumberRange(min=0, message="UK delivery time can`t be < 0")])
    has_color_cut = BooleanField("Has Color Cut: ")
    print = StringField("Print: ")
    publishing_year = IntegerField("Publishing Year: ",
                                   validators=[NumberRange(min=1000, max=3000, message="Incorrect data format")])
    first_published_at = IntegerField("First Published At: ",
                                      validators=[NumberRange(min=1_000, max=3_000, message="Incorrect data format")])
    description = StringField("Description: ")
    characteristics = StringField("Characteristics: ")

