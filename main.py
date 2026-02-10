from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from sqladmin import Admin

from admin import admin_models
from entities import router
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
admin = Admin(app, db_helper.engine, base_url=os.getenv("ADMIN_URL"))
app.include_router(router)

for admin_model in admin_models:
    admin.add_view(admin_model)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    uvicorn.run("main:app", port=int(os.getenv("BACKEND_PORT")), reload=True)