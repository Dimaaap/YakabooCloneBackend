from pathlib import Path

from fastapi.templating import Jinja2Templates

from admin.utils import inject_entities

BASE_DIR = Path(__file__).resolve().parent.parent
templates_dir = BASE_DIR / "templates"

templates = Jinja2Templates(directory=templates_dir, context_processors=[inject_entities])