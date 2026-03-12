from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.payment_methods.schema import PaymentMethodsForAdmin, EditPaymentMethod
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


async def get_payment_methods_field_data(session: AsyncSession, payment_method_id: int) -> PaymentMethodsForAdmin:
    statement = (
        select(PaymentMethod)
        .options(
            joinedload(PaymentMethod.city),
            joinedload(PaymentMethod.country),
        )
        .where(PaymentMethod.id == payment_method_id)
    )

    result = await session.execute(statement)
    method = result.scalars().first()

    method.city_title = method.city.title if method.city else None
    method.country_title = method.country.title if method.country else None
    return PaymentMethodsForAdmin.model_validate(method)


async def get_payment_method_by_id(session: AsyncSession, method_id: int) -> PaymentMethod | bool:
    payment_method = await session.get(PaymentMethod, method_id)

    if not payment_method:
        return False

    return payment_method


async def update_payment_method(session: AsyncSession, method_id: int, data: EditPaymentMethod) -> bool:
    payment_method = await get_payment_method_by_id(session, method_id)

    if not payment_method:
        raise NotFoundInDbError("Payment Method not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(payment_method, field, value)

    await session.commit()
    await session.refresh(payment_method)
    return True