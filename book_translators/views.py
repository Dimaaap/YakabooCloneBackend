import json

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import BookTranslatorSchema, BookTranslatorCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["Book Translators"])
REDIS_KEY = "translators"


@router.get("/all", response_model=list[BookTranslatorSchema])
async def get_all_translators(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_translators = await redis_client.get(REDIS_KEY)

    if cached_translators:
        return json.loads(cached_translators)

    translators = await crud.get_all_translators(session)
    await redis_client.set(REDIS_KEY, json.dumps([translator.model_dump() for translator in translators], default=str))
    return translators


@router.get("/{slug}", response_model=BookTranslatorSchema)
async def get_translator_by_slug(slug: str, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_translators = await redis_client.get(REDIS_KEY)

    if cached_translators:
        translators_list = json.loads(cached_translators)
        for translator in translators_list:
            if translator["slug"] == slug:
                return translator
    else:
        translators = await crud.get_all_translators(session)
        await redis_client.set(REDIS_KEY, json.dumps([translator.model_dump() for translator in translators]))
        return await crud.get_translator_by_slug(slug, session)


@router.get("/search/", response_model=list[BookTranslatorSchema])
async def search_translators(
        query: str = Query(...),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    cached_translators = await redis_client.get(REDIS_KEY)

    if cached_translators:
        translators_list = json.loads(cached_translators)
        res = []
        for translator in translators_list:
            if(
                query.lower() in translator["first_name"].lower()
                or query.lower() in translator["last_name"].lower()
                or query.lower() in f"{translator["first_name"].lower}{translator["last_name"].lower()}"
            ):
                res.append(translator)
        return res
    else:
        translators = await crud.get_all_translators(session)
        await redis_client.set(REDIS_KEY, json.dumps([translator.model_dump() for translator in translators], default=str))
        return await crud.get_translators_by_query(query, session)


@router.post("/create")
async def create_translator(translator: BookTranslatorCreate,
                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_translator = await crud.create_translator(session, translator)
    if new_translator:
        await redis_client.delete(REDIS_KEY)
        return new_translator
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(new_translator))


@router.delete("/{translator_id}")
async def delete_translator_by_id(translator_id: int,
                                  session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    success = await crud.delete_translator_by_id(session, translator_id)
    if success:
        return {"message": f"Translator with id {translator_id} has been deleted"}
    else:
        return {"message": "Deleting error"}


@router.get("/translator/{translator_id}/books")
async def get_all_translator_books(translator_id: int,
                                   session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    books = await crud.get_all_translator_books_by_translator_id(session, translator_id)
    return books
