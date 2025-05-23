from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from banners import router as banners_router
from sidebar import router as sidebars_router
from email_subs import router as subs_router
from knowledges import router as knowledge_router
from users import router as auth_router
from wishlists import router as wishlist_router
from authors import router as authors_router
from categories import router as categories_router
from promotion_categories import router as promo_categories_router
from promotions import router as promo_router
from publishing import router as publishing_router
from interesting import router as interesting_router
from footers import router as footer_router
from game_series import router as game_series_router
from game_brands import router as game_brands_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(banners_router)
app.include_router(sidebars_router)
app.include_router(subs_router)
app.include_router(knowledge_router)
app.include_router(auth_router)
app.include_router(wishlist_router)
app.include_router(authors_router)
app.include_router(categories_router)
app.include_router(promo_categories_router)
app.include_router(promo_router)
app.include_router(publishing_router)
app.include_router(interesting_router)
app.include_router(footer_router)
app.include_router(game_series_router)
app.include_router(game_brands_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home_page():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8003, reload=True)