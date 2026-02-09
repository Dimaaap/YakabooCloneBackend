import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..contacts.schemas import ContactsSchema, ContactsCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["contacts"])

SIX_DAYS = 24 * 3600 * 6


@router.get("/all", response_model=list[ContactsSchema])
async def get_all_contacts(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_contacts = await redis_client.get("contacts")
    if cached_contacts:
        return json.loads(cached_contacts)
    contacts = await crud.get_all_contacts(session)
    await redis_client.set("contacts", json.dumps([contact.model_dump() for contact in contacts]),
                           ex=SIX_DAYS)
    return contacts


@router.post("/create")
async def create_contact(contact: ContactsCreate,
                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_contact = await crud.create_contact(session, contact)
    if new_contact:
        await redis_client.delete("contacts")
        return new_contact


@router.delete("/{contact_id}")
async def delete_contact_by_id(contact_id: int,
                               session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    deleted_contact = await crud.delete_contact_by_id(contact_id, session)
    if deleted_contact:
        await redis_client.delete("contacts")
        return {"message": f"The contact with id { contact_id } has been deleted"}
    else:
        return {"error": deleted_contact}