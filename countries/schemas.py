from pydantic import BaseModel, ConfigDict

from cities.schemas import CitiesSchema
from delivery_terms.schemas import DeliveryTermSchema
from payment_methods.schema import PaymentMethodSchema


class CountriesBase(BaseModel):
    title: str
    is_visible: bool = True
    cities: list[CitiesSchema] = []


class CountriesCreate(CountriesBase):
    pass


class CountriesUpdate(CountriesCreate):
    pass


class CountriesUpdatePartial(CountriesUpdate):
    title: str | None = None
    is_active: bool | None = None
    cities: list[int] | None = None


class CountriesSchema(CountriesBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    delivery_terms: DeliveryTermSchema | None = None
    payment_methods: PaymentMethodSchema | None = None