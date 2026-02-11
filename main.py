from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from entities import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    uvicorn.run("main:app", port=int(os.getenv("BACKEND_PORT")), reload=True)