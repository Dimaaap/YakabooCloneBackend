from typing import TYPE_CHECKING
from datetime import datetime

import enum
from sqlalchemy import String, Boolean, Integer, Text, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .city import City
    from .countries import Country
    from .new_post_offices import NewPostOffice
    from .new_post_postomats import NewPostPostomat
    from .ukrpost_office import UkrpostOffice
    from .meest_post_office import MeestPostOffice
    from .promo_code_usage import PromoCodeUsage


class DeliveryMethods(str, enum.Enum):
    ukrpostOffice = "ukrpostOffice"
    ukrpostCourier = "ukrpostCourier"
    newPostCourier = "newPostCourier"
    meestPost = "meestPost"
    newPostToOffice = "newPostToOffice"
    newPostToMailBox = "newPostToMailBox"
    YakabooShop = "YakabooShop"


class PaymentMethods(str, enum.Enum):
    scholarPack = "scholarPack"
    eSupport = "eSupport"
    eBook = "eBook"
    cashOrCart = "cashOrCart"
    prepay = "prepay"
    privatePay = "privatePay"
    monoPay = "monoPay"


class OrderStatus(str, enum.Enum):
    ORDERED = "ORDERED"
    DELIVERED = "DELIVERED"
    FINISHED = "FINISHED"


class Order(Base):

    for_charity: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    other_person_get: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    delivery_method: Mapped[DeliveryMethods] = mapped_column(SQLEnum(DeliveryMethods,
                                                                     name="delivery_method", create_type=True),
                                                             default=DeliveryMethods.ukrpostOffice,
                                                             server_default=DeliveryMethods.ukrpostOffice.value)
    getter_first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    getter_last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    getter_phone_number: Mapped[str] = mapped_column(String(10), nullable=True)
    need_call: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    participant: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    have_questions: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")

    new_post_courier_delivery_address: Mapped[str] = mapped_column(String(255), nullable=True)
    new_post_courier_delivery_apartment_number: Mapped[int] = mapped_column(Integer, nullable=True)
    new_post_courier_house_number: Mapped[int] = mapped_column(Integer, nullable=True)
    new_post_delivery_address: Mapped[str] = mapped_column(String(255), nullable=True)
    ukrpost_courier_address: Mapped[str] = mapped_column(String(255), nullable=True)
    ukrpost_courier_apartment_number: Mapped[int] = mapped_column(Integer, nullable=True)
    ukrpost_courier_house_number: Mapped[int] = mapped_column(Integer, nullable=True)
    ukrpost_user_first_name_for_courier: Mapped[str] = mapped_column(String(255), nullable=True)
    ukrpost_courier_user_middle_name_for_courier: Mapped[str] = mapped_column(String(255), nullable=True)
    ukrpost_user_name_for_courier: Mapped[str] = mapped_column(String(255), nullable=True)
    ukrpost_office_user_name: Mapped[str] = mapped_column(String(255), nullable=True)
    ukrpost_office_user_middle_name: Mapped[str] = mapped_column(String(255), nullable=True)
    ukrpost_office_user_last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    ukrpost_post_index: Mapped[int] = mapped_column(Integer, nullable=True)

    payment_method: Mapped[PaymentMethods] = mapped_column(SQLEnum(PaymentMethods,
                                                                   name="payment_method_type", create_type=True),
                                                           default=PaymentMethods.scholarPack,
                                                           server_default=PaymentMethods.scholarPack.value)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), server_default=func.now())
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus,
                                                        name="order_status_type", create_type=True),
                                                default=OrderStatus.ORDERED,
                                                server_default=OrderStatus.ORDERED.value)
    total_sum: Mapped[int] = mapped_column(Integer)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship("User", back_populates="orders")
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=True)
    city: Mapped["City"] = relationship("City", back_populates="orders")
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), nullable=True)
    country: Mapped["Country"] = relationship("Country", back_populates="orders")
    new_post_office_number: Mapped[int] = mapped_column(ForeignKey("new_post_offices.id"), nullable=True)
    new_post_office: Mapped["NewPostOffice"] = relationship("NewPostOffice", back_populates="orders")
    new_post_postomat_id: Mapped[int] = mapped_column(ForeignKey("new_post_postomats.id"), nullable=True)
    new_post_postomat: Mapped["NewPostPostomat"] = relationship("NewPostPostomat", back_populates="orders")
    ukrpost_office_id: Mapped[int] = mapped_column(ForeignKey("ukrpost_offices.id"), nullable=True)
    ukrpost_office: Mapped["UkrpostOffice"] = relationship("UkrpostOffice", back_populates="orders")
    meest_office_id: Mapped[int] = mapped_column(ForeignKey("meest_post_offices.id"), nullable=True)
    meest_office: Mapped["MeestPostOffice"] = relationship("MeestPostOffice", back_populates="orders")
    promo_usage_id: Mapped[int] = mapped_column(ForeignKey("promo_code_usages.id", ondelete="SET NULL"),
                                                nullable=True)
    promo_usage: Mapped["PromoCodeUsage"] = relationship("PromoCodeUsage", back_populates="order", uselist=False)

    def __str__(self):
        return f"{self.__class__.__name__}(getter first name = {self.getter_first_name}, id={ self.id })"
