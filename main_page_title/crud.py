import asyncio

from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import MainPageTitle, db_helper
from main_page_title.schema import MainPageTitleSchema, MainPageTitleCreate, MainPageTitleUpdate


async def create_main_page_title(session: AsyncSession, main_page_title: MainPageTitleCreate) -> MainPageTitle:
    new_title = MainPageTitle(**main_page_title.model_dump())

    try:
        session.add(new_title)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_title

async def delete_main_page_title_by_id(session: AsyncSession, title_id: int) -> bool:
    statement = delete(MainPageTitle).where(MainPageTitle.id == title_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        await session.rollback()
        return False


async def get_all_main_page_titles(session: AsyncSession) -> list[MainPageTitleSchema]:
    statement = select(MainPageTitle).order_by(MainPageTitle.id)
    result: Result = await session.execute(statement)
    main_page_title = result.scalars().all()
    return [MainPageTitleSchema.model_validate(page_title) for page_title in main_page_title]


async def get_active_main_page_title(session: AsyncSession) -> MainPageTitleSchema:
    statement = select(MainPageTitle).where(MainPageTitle.active)
    result: Result = await session.execute(statement)
    active_page_title = result.scalars().first()
    return MainPageTitleSchema.model_validate(active_page_title)


async def update_active_main_page_title(session: AsyncSession, title_id: int,
                                        page_data: MainPageTitleUpdate) -> MainPageTitleSchema:
    main_page_title = await session.get(MainPageTitle, title_id)
    if not main_page_title:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")

    for key, value in page_data.model_dump(exclude_unset=True).items():
        setattr(main_page_title, key, value)

    try:
        await session.commit()
        await session.refresh(main_page_title)

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return MainPageTitleSchema.model_validate(main_page_title)