from fastapi import HTTPException, status
from sqlalchemy import select, Result, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import SubcategoryBanner, Subcategory
from book_subcategory_banners.schema import BookSubcategoryBannerSchema, BookSubcategoryBannerCreate


async def create_book_subcategory_banner(
        session: AsyncSession,
        book_subcategory_banner: BookSubcategoryBannerCreate
) -> BookSubcategoryBannerSchema:
    banner = SubcategoryBanner(**book_subcategory_banner.model_dump())

    try:
        session.add(banner)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return banner


async def get_all_book_subcategory_banners(session: AsyncSession) -> list[SubcategoryBanner]:
    statement = select(SubcategoryBanner).order_by(SubcategoryBanner.id)

    result: Result = await session.execute(statement)
    subcategory_banners = result.scalars().all()
    return [BookSubcategoryBannerSchema.model_validate(banner) for banner in subcategory_banners]


async def get_book_subcategory_banner_by_slug(session: AsyncSession, slug: str):
    statement = select(SubcategoryBanner).where(SubcategoryBanner.slug == slug)

    result: Result = await session.execute(statement)
    subcategory_banner = result.scalars().first()

    return subcategory_banner or []


async def get_book_subcategory_banner_by_id(session: AsyncSession, banner_id: int):
    statement = select(SubcategoryBanner).where(SubcategoryBanner.id == banner_id)

    result: Result = await session.execute(statement)
    subcategory_banner = result.scalars().first()

    return subcategory_banner or []


async def delete_book_subcategory_banner_by_id(session: AsyncSession, banner_id: int):
    statement = delete(SubcategoryBanner).where(SubcategoryBanner.id == banner_id)

    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as e:
        return False


