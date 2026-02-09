from sqlalchemy import or_, and_, func

from core.models import Publishing, BookSeria
from core.models.book_info import BookFormats, BookLanguages
from core.models.authors import Author
from core.models.book import Book
from core.models.book_info import BookInfo

CUSTOM_FILTERS = {
    "winter-esupport": lambda: Book.book_info.has(BookInfo.is_has_winter_esupport.is_(True)),
    "ebook": lambda: Book.book_info.has(BookInfo.is_has_esupport.is_(True)),
    "national-kashback": lambda: Book.book_info.has(BookInfo.is_has_cashback.is_(True)),
    "promo": lambda: Book.is_promo.is_(True)
}


class BookFilter:
    def __init__(self, filters):
        self.filters = filters

    def authors(self):
        val = self.filters.authors

        if not val:
            return None

        names = []

        for item in val:
            names.extend(name.strip() for name in item.split(",") if name.strip())

        if not names:
            return None

        return Book.authors.any(
            or_(
                *[
                    func.concat(Author.first_name, " ", Author.last_name)
                    .ilike(f"%{name}%")
                    for name in names
                ]
            )
        )


    def languages(self):
        val = self.filters.languages

        if not val:
            return None

        enums = []
        for item in val:
            for lang in item.split(","):
                try:
                    enums.append(BookLanguages(lang.strip()).name)
                except ValueError:
                    continue

        if not enums:
            return None

        return Book.book_info.has(BookInfo.language.in_(enums))


    def book_types(self):
        val = self.filters.bookTypes

        if not val:
            return None

        enums = []
        for item in val:
            for book_type in item.split(","):
                try:
                    enums.append(BookFormats(book_type.strip()).name)
                except ValueError:
                    continue
        if not enums:
            return None

        return Book.book_info.has(BookInfo.format.in_(enums))

    def in_stock(self):
        if self.filters.in_stock is None:
            return None

        return Book.book_info.has(BookInfo.in_stock == self.filters.in_stock)

    def price_min(self):
        if self.filters.price_min is None:
            return None

        return Book.price >= self.filters.price_min

    def price_max(self):
        if self.filters.price_max is None:
            return None

        return Book.price <= self.filters.price_max

    def categories(self):
        val = self.filters.categories

        if not val:
            return None

        values = []
        for item in val:
            values.extend(v.strip() for v in item.split(",") if v.strip())
        if not values:
            return None

        return Book.category.in_(values)

    def publishers(self):
        val = self.filters.publishers
        if not val:
            return None

        values = []
        for item in val:
            values.extend(v.strip() for v in item.split(",") if v.strip())

        if not values:
            return None

        return Book.publishing.has(Publishing.title.in_(values))

    def series(self):
        val = self.filters.series
        if not val:
            return None

        values = []
        for item in val:
            values.extend(v.strip() for v in item.split(",") if v.strip())

        if not values:
            return None

        return Book.seria.has(BookSeria.title.in_(values))

    def custom(self):
        if not self.filters.filters:
            return None

        expressions = []

        for raw in self.filters.filters:
            flags = raw.split(",")
            for flag in flags:
                flag = flag.strip()
                expr = CUSTOM_FILTERS.get(flag)
                if expr:
                    expressions.append(expr())

        if not expressions:
            return None

        return and_(*expressions)

    def apply(self):
        conditions = []

        for expr in (
            self.authors(),
            self.languages(),
            self.book_types(),
            self.in_stock(),
            self.categories(),
            self.series(),
            self.publishers(),
            self.price_min(),
            self.price_max(),
            self.custom()
        ):
            if expr is not None:
                conditions.append(expr)
        return conditions