from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.models import db_helper
from .schema import UkrpostOfficesForAdmin
from ..config import templates
from . import crud