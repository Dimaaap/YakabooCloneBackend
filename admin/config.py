from pathlib import Path

from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent
templates_dir = BASE_DIR / "templates"

templates = Jinja2Templates(directory=templates_dir)