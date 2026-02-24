from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.payment_methods.schema import PaymentMethodsForAdmin
from core.models import PaymentMethod


async def get_payment_methods_for_admin_page(session: AsyncSession) -> list[PaymentMethodsForAdmin]:
    statement = (
        select(PaymentMethod)
        .options(
            joinedload(PaymentMethod.city),
            joinedload(PaymentMethod.country),
        )
        .order_by(PaymentMethod.id)
    )

    result = await session.execute(statement)
    payment_methods = result.scalars().all()

    for method in payment_methods:
        method.city_title = method.city.title if method.city else None
        method.country_title = method.country.title if method.country else None

    return [
        PaymentMethodsForAdmin.model_validate(method)
        for method in payment_methods
    ]