import logging
import httpx

from typing import List
from fastapi import APIRouter, HTTPException
from starlette import status

from app.schemas.movie import MovieOut
from app.core.config import tmdb_client
from app.api.deps.db import DbDependency
from app.core.cache import get_cache, set_cache


router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)

CACHE_TTL = 300  # 5 min

@router.get("/popular", response_model=List[MovieOut], status_code=status.HTTP_200_OK)
async def get_popular_movies(db: DbDependency):
    """
    Fetches a list of currently popular movies from TMDB.
    """
    cache_key = "movies:popular"
    cached = await get_cache(cache_key)
    if cached:
        return [MovieOut.model_validate(m) for m in cached]

    try:
        response = await tmdb_client.get("/movie/popular") #it lets the server handle other requests while waiting for TMDB
        response.raise_for_status() #raise an exception for bad status codes
        data = response.json()["results"]
        await set_cache(cache_key, [MovieOut.model_validate(m).model_dump() for m in data], ttl=CACHE_TTL)
        return [MovieOut.model_validate(m) for m in data]

    except httpx.HTTPStatusError as e:
        logging.error(f"TMDB API error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail="External API error")
    except httpx.RequestError as e:
        logging.error(f"Network error: {e}")
        return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Network connection error")
