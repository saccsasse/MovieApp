# uvicorn main:app --reload

from fastapi import FastAPI

from app.core.config import tmdb_client
from app.db.session import engine
from app.api.routers import admin, movies, discover, genres, user, favourites
from app.db.models import user as models
from app.core.redis import init_redis, close_redis


app = FastAPI(title="Movie API")
models.Base.metadata.create_all(bind=engine)


app.include_router(admin.router)
app.include_router(movies.router)
app.include_router(discover.router)
app.include_router(genres.router)
app.include_router(user.router)
app.include_router(favourites.router)


@app.on_event("startup")
async def startup():
    await init_redis()

@app.on_event("shutdown")
async def shutdown():
    await close_redis()
    await tmdb_client.aclose()