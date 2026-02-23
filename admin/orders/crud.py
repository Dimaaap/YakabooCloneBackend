from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.orders.schema import OrdersForAdmin
from core.models import Order


async def get_orders_for_admin_page(session: AsyncSession) -> list[OrdersForAdmin]:
    statement = (
        select(Order)
        .options(
            joinedload(Order.city),
            joinedload(Order.user),
            joinedload(Order.country),
            joinedload(Order.new_post_office),
            joinedload(Order.new_post_postomat),
            joinedload(Order.ukrpost_office),
            joinedload(Order.meest_office),
            joinedload(Order.promo_usage)
        )
        .order_by(Order.id)
    )

    result = await session.execute(statement)
    orders = result.scalars().all()

    for order in orders:
        order.user_email = order.user.email
        order.city_title = order.city.title
        order.country_title = order.country.title
        order.new_post_number = order.new_post_office.number
        order.new_post_postomat = order.new_post_postomat.id
        order.new_post_ukrpost_office = order.ukrpost_office.id
        order.meest_post_office = order.meest_office.id
        order.promo_usage = order.promo_usage.id

    return [
        OrdersForAdmin.model_validate(order)
        for order in orders
    ]

