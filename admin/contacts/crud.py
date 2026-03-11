from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from admin.authors.errors import NotFoundInDbError
from admin.contacts.schema import ContactsForAdminList, EditContacts
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


async def get_contact_field_data(session: AsyncSession, contact_id: int) -> ContactsForAdminList:
    statement = (
        select(Contacts)
        .where(Contacts.id == contact_id)
    )

    result = await session.execute(statement)
    contact = result.scalars().first()

    return ContactsForAdminList.model_validate(contact)


async def get_contact_by_id(session: AsyncSession, contact_id: int) -> Contacts | bool:
    contact = await session.get(Contacts, contact_id)

    if not contact:
        return False
    return contact


async def update_contact(session: AsyncSession, contact_id: int, data: EditContacts) -> bool:
    contact = await get_contact_by_id(session, contact_id)

    if not contact:
        raise NotFoundInDbError("Contact not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(contact, field, value)

    await session.commit()
    await session.refresh(contact)
    return True