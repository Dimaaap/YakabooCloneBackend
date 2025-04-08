from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from banners import router as banners_router
from sidebar import router as sidebars_router
from email_subs import router as subs_router
from knowledges import router as knowledge_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(banners_router)
app.include_router(sidebars_router)
app.include_router(subs_router)
app.include_router(knowledge_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://loclahost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home_page():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8003, reload=True)