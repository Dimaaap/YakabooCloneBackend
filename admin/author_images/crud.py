from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from admin.author_images.schema import AuthorImagesForAdminPage
from core.models import AuthorImage


async def get_author_images_for_admin_page(session: AsyncSession):
    statement = (
        select(AuthorImage)
        .options(joinedload(AuthorImage.author))
        .order_by(AuthorImage.id)
    )

    result = await session.execute(statement)
    author_images = result.unique().scalars().all()

    for image in author_images:
        image.author_name = f"{image.author.first_name} {image.author.last_name}"

    return [
        AuthorImagesForAdminPage.model_validate(image)
        for image in author_images
    ]


async def get_author_image_field_data(session: AsyncSession, author_image_id: int) -> AuthorImagesForAdminPage:
    statement = (
        select(AuthorImage)
        .options(joinedload(AuthorImage.author))
        .where(AuthorImage.id == author_image_id)
    )

    result = await session.execute(statement)
    author_image = result.scalars().first()

    author_image.author_name = f"{author_image.author.first_name} {author_image.author.last_name}"

    return AuthorImagesForAdminPage.model_validate(author_image)