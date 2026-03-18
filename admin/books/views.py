from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.models import db_helper
from .fields_setter import FieldsSetter
from .forms import BookEditForm, BookCreateForm
from .schema import BooksForAdminList, EditBook, CreateBook
from ..config import templates
from . import crud
from ..utils import convert_alchemy_datetime
from .helpers import prepare_data_to_db

router = APIRouter(tags=["Books For Admin Page"])


@router.get("/list", name="admin_books_list", response_class=HTMLResponse)
async def books_list(request: Request, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    books = await crud.get_books_for_admin_page(session)
    books = [book.model_dump() for book in books]

    for book in books:
        book["created_date"] = convert_alchemy_datetime(book["created_date"])

    fields = list(BooksForAdminList.model_fields.keys())
    link_fields = ["book_info_id", "authors_names", "translators_names",
                   "illustrators_names", "literature_period_title",
                   "book_seria_title", "notebook_category_title",
                   "notebook_subcategory_title", "subcategories_title",
                   "categories_title", "double_subcategories_title",
                   "publishing_title", "edition_group_title",
                   "book_images"]

    return templates.TemplateResponse(
        "pages/list.html",
        context={
            "request": request,
            "data": books,
            "page_title": "All Books",
            "model_name": "Book",
            "fields": fields,
            "is_editable": True,
            "is_deletable": True,
            "can_create": True,
            "link_fields": link_fields,
        }
    )


@router.get("/create", response_class=HTMLResponse)
async def create_book_page(request: Request,
                           session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form = BookCreateForm()

    setter_clas = FieldsSetter(session, form)
    await setter_clas.main()

    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Book",
            "model_name": "Book"
        }
    )


@router.post("/create", name="admin_create_book", response_class=HTMLResponse)
async def create_book_submit(request: Request, session: AsyncSession=Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    data = dict(form_data)
    form = BookCreateForm()

    prepare_data_to_db(form_data)

    setter = FieldsSetter(session, form)
    await setter.main()

    form.process(await request.form())

    if form.validate():
        book_data = CreateBook(**data)
        await crud.create_book(session, book_data)

        return RedirectResponse(
            url=request.url_for("admin_books_list"),
            status_code=status.HTTP_303_SEE_OTHER
        )
    return templates.TemplateResponse(
        "pages/create.html",
        {
            "request": request,
            "form": form,
            "page_title": "Create Book",
            "model_name": "Book"
        }
    )



@router.get("/{book_id}", response_class=HTMLResponse)
async def get_book_by_id(request: Request, book_id: int,
                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    book = await crud.get_book_field_data(session, book_id)
    data = book.model_dump()

    return templates.TemplateResponse(
        "pages/detail.html",
        context={
            "request": request,
            "data": data,
            "page_title": "Books",
            "model_name": "Book"
        }
    )


@router.get('/{book_id}/edit', response_class=HTMLResponse)
async def edit_book_by_id(request: Request, book_id: int,
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    book = await crud.get_book_field_data(session, book_id)

    identifier = book.title
    form = BookEditForm(data=book.model_dump())

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Book",
            "model_name": "Book",
            "identifier": identifier
        }
    )


@router.post("/{book_id}/edit", name="admin_edit_book", response_class=HTMLResponse)
async def edit_book_submit(request: Request, book_id: int,
                           session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    form_data = await request.form()
    form = BookEditForm(data=form_data)

    book = await crud.get_book_field_data(session, book_id)
    identifier = book.title

    if form.validate():
        book_data = EditBook(**form.data)
        await crud.update_book(session, book_id, book_data)

        return RedirectResponse(
            url=request.url_for("admin_edit_book", book_id = book_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "form": form,
            "page_title": "Edit Book",
            "model_name": "Book",
            "identifier": identifier
        }
    )