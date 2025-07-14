import json

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import AuthorSchema, AuthorCreate, ImageBase
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["authors"])
REDIS_KEY = 'authors'


@router.get("/all", response_model=list[AuthorSchema])
async def get_all_authors(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_authors = await redis_client.get(REDIS_KEY)

    if cached_authors:
        return json.loads(cached_authors)

    authors = await crud.get_all_authors(session)
    await redis_client.set(REDIS_KEY, json.dumps([author.model_dump() for author in authors], default=str))
    return authors


@router.get('/first-letter/{letter}', response_model=list[AuthorSchema])
async def get_author_by_first_name(
        letter: str | None,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    cached_authors = await redis_client.get(REDIS_KEY)

    if cached_authors:
        authors_list = json.loads(cached_authors)
        res = []
        for author in authors_list:
            if author["first_name"][0].lower() == letter.lower() or author["last_name"][0].lower() == letter.lower():
                res.append(author)
        return res
    else:
        authors = await crud.get_all_authors(session)
        await redis_client.set(REDIS_KEY, json.dumps([author.model_dump() for author in authors], default=str))
        return await crud.get_author_by_name_first_letter(letter, session)


@router.get("/{slug}", response_model=AuthorSchema)
async def get_author_by_slug(
        slug: str, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    cached_authors = await redis_client.get(REDIS_KEY)
    if cached_authors:
        authors_list = json.loads(cached_authors)
        for author in authors_list:
            if author['slug'] == slug:
                return author
    else:
        authors = await crud.get_all_authors(session)
        await redis_client.set(REDIS_KEY, json.dumps([author.model_dump() for author in authors]))
        return await crud.get_author_by_slug(slug, session)


@router.get('/search/', response_model=list[AuthorSchema])
async def search_authors(
        query: str = Query(...),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    cached_authors = await redis_client.get(REDIS_KEY)

    if cached_authors:
        authors_list = json.loads(cached_authors)
        res = []
        for author in authors_list:
            if (
                    query.lower() in author['first_name'].lower()
                    or query.lower() in author['last_name'].lower()
                    or query.lower() in f"{author['first_name'].lower()}{author['last_name'].lower()}"
            ):
                res.append(author)
        return res
    else:
        authors = await crud.get_all_authors(session)
        await redis_client.set(REDIS_KEY, json.dumps([author.model_dump() for author in authors], default=str))
        return await crud.get_authors_by_query(query, session)


@router.get("/image_path", response_model=list[ImageBase])
async def get_all_images(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_all_author_images(session)


@router.get("/{author_id}/images", response_model=list[ImageBase])
async def get_all_images_by_author_id(
        author_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_all_author_images_by_author_id(session, author_id)


@router.post("/create")
async def create_author(author: AuthorCreate,
                        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    new_author = await crud.create_author(session, author)
    if new_author:
        await redis_client.delete(REDIS_KEY)
        return new_author
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(new_author))


@router.delete("/{author_id}")
async def delete_author_by_id(author_id: int,
                              session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    success = await crud.delete_author_by_id(session, author_id)
    if success:
        return {"message": f"Author with id {author_id} has been deleted"}
    else:
        return {"message": "Deleting error"}


@router.get("/author/{author_id}/books")
async def get_all_author_books(author_id: int,
                               session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    ...