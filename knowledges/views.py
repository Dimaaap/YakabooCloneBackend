import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import KnowledgeSchema, KnowledgeCreate
from core.models import db_helper
from . import crud
from config import redis_client

router = APIRouter(tags=["knowledge"])


@router.get("/all", response_model=list[KnowledgeSchema])
async def get_all_knowledge(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):

    cached_knowledge = await redis_client.get("knowledge")
    if cached_knowledge:
        return json.loads(cached_knowledge)
    knowledge = await crud.get_all_knowledge(session)
    await redis_client.set("knowledge", json.dumps([kn.model_dump() for kn in knowledge]))
    return knowledge


@router.get("/in-sidebar", response_model=list[KnowledgeSchema])
async def get_sidebar_knowledge(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_knowledge = await redis_client.get("sidebar_knowledge")
    if cached_knowledge:
        kn_list = []
        for kn in json.loads(cached_knowledge):
            if kn["in_sidebar"]:
                kn_list.append(kn)
        return kn_list
    knowledge = await crud.get_sidebar_knowledge(session)
    await redis_client.set("sidebar_knowledge", json.dumps([kn.model_dump() for kn in knowledge]))
    return knowledge


@router.post("/create")
async def create_knowledge(
        knowledge: KnowledgeCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    new_knowledge = await crud.create_knowledge(session=session, title=knowledge.title, slug=knowledge.slug,
                                                is_active=knowledge.is_active, content=knowledge.content)
    if new_knowledge:
        await redis_client.delete("knowledge")
        return new_knowledge


@router.get("/slug", response_model=KnowledgeSchema)
async def get_knowledge_by_slug(slug: str,
                                session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cached_knowledge = await redis_client.get("knowledge")
    if cached_knowledge:
        try:
            knowledge_list = json.loads(cached_knowledge)
            for kn in knowledge_list:
                if kn.get("slug") == slug:
                    return kn
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        knowledge = await crud.get_knowledge_by_slug(session=session, slug=slug)
        return knowledge


@router.delete("/{knowledge_slug}")
async def delete_knowledge_by_slug(knowledge_slug: str,
                                   session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    deleted_knowledge = await crud.delete_knowledge_by_slug(slug=knowledge_slug, session=session)
    if deleted_knowledge:
        await redis_client.delete("knowledge")
        return {"message": f"The knowledge with slug {knowledge_slug} has been deleted"}
    else:
        return {"error": deleted_knowledge}