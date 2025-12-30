from fastapi import APIRouter, Path
from starlette import status
from typing import List

from app.schemas.movie import MovieOut
from app.api.deps.db import DbDependency
from app.api.deps.user import UserDependency
from app.core.cache import get_cache, set_cache, delete_cache
from app.api.services.favourite_service import get_favourites, add_favourite, remove_favourite


router = APIRouter(
    prefix="/favourites",
    tags=["favourites"]
)


@router.get("/", response_model=List[MovieOut], status_code=status.HTTP_200_OK)
async def get_favourite_movies(
        db: DbDependency,
        user: UserDependency
):
    cache_key = f"favourites:user:{user.id}"
    cached = await get_cache(cache_key)
    if cached:
        return [MovieOut.model_validate(m) for m in cached]

    favourites = await get_favourites(db, user.id)
    favourites_out = [MovieOut.model_validate(m) for m in favourites]
    await set_cache(cache_key, [m.model_dump() for m in favourites_out], ttl=300)
    return favourites_out


@router.post("/{movie_id}", status_code=status.HTTP_200_OK) #Since movie_id is in the path, use Path
async def mark_movie_as_favourite(
        db: DbDependency,
        user: UserDependency,
        movie_id: int = Path(..., gt=0, description="A unique movie ID to mark it as favourite")
):
    await add_favourite(db, user.id, movie_id)
    await delete_cache(f"favourites:user:{user.id}")
    return {"message": "Movie added to favourites"}


@router.delete("/{movie_id}", status_code=status.HTTP_200_OK)
async def delete_movie_from_favourite(
        db: DbDependency,
        user: UserDependency,
        movie_id: int = Path(..., gt=0, description="A unique movie ID to delete"),
):
    await remove_favourite(db, user.id, movie_id)
    await delete_cache(f"favourites:user:{user.id}")
    return {"message": "Movie removed from favourites"}
