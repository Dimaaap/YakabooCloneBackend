from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.contacts.schema import ContactsForAdminList
from core.models import Contacts


async def get_contacts_list_for_admin_page(session: AsyncSession) -> list[ContactsForAdminList]:
    statement = (
        select(Contacts)
        .order_by(Contacts.id)
    )

    result = await session.execute(statement)
    contacts = result.scalars().all()

    return [
        ContactsForAdminList.model_validate(contact)
        for contact in contacts
    ]
