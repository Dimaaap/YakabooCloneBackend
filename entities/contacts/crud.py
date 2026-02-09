import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ..contacts.schemas import ContactsSchema, ContactsCreate
from core.models import Contacts, db_helper
from data_strorage import CONTACTS


async def create_contact(session: AsyncSession, contact: ContactsCreate) -> Contacts:
    contact = Contacts(**contact.model_dump())
    try:
        session.add(contact)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return contact


async def get_all_contacts(session: AsyncSession) -> list[ContactsSchema]:
    statement = select(Contacts).order_by(Contacts.id)
    result: Result = await session.execute(statement)
    contacts = result.scalars().all()
    return [ContactsSchema.model_validate(contact) for contact in contacts]


async def delete_contact_by_id(contact_id: int, session: AsyncSession):
    statement = delete(Contacts).where(Contacts.id == contact_id)
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        return False


async def main():
    async with db_helper.session_factory() as session:
        for contact in CONTACTS:
            contact = ContactsCreate(**contact)
            await create_contact(session, contact)


if __name__ == "__main__":
    import sys

    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # Windows fix
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())