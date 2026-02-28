from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from admin.delivery_terms.schema import DeliveryTermsForAdminList
from core.models import DeliveryTerms


async def get_delivery_terms_list_for_admin_page(session: AsyncSession) -> list[DeliveryTermsForAdminList]:
    statement = (
        select(DeliveryTerms)
        .options(joinedload(DeliveryTerms.country))
        .options(joinedload(DeliveryTerms.city))
        .order_by(DeliveryTerms.id)
    )

    result = await session.execute(statement)
    delivery_terms = result.scalars().all()

    for term in delivery_terms:
        term.country_title = term.country.title if term.country else None
        term.city_title = term.city.title if term.city else None

    return [
        DeliveryTermsForAdminList.model_validate(term)
        for term in delivery_terms
    ]


async def get_delivery_term_field_data(session: AsyncSession, term_id: int) -> DeliveryTermsForAdminList:
    statement = (
        select(DeliveryTerms)
        .options(
            joinedload(DeliveryTerms.country),
            joinedload(DeliveryTerms.city)
        )
        .where(DeliveryTerms.id == term_id)
    )

    result = await session.execute(statement)
    term = result.scalars().first()

    term.country_title = term.country.title if term.country else None
    term.city_title = term.city.title if term.city else None
    return DeliveryTermsForAdminList.model_validate(term)