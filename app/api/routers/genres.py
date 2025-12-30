from typing import List
import httpx
from fastapi import APIRouter, HTTPException
from starlette import status

from app.core.config import tmdb_client
from app.core.cache import get_cache, set_cache
from app.api.deps.db import DbDependency
from app.schemas.genre import GenreOut  # Pydantic-schema


router = APIRouter(
    prefix="/genre",
    tags=["genre"]
)

CACHE_TTL = 86400  # 24h

@router.get("/", response_model=List[GenreOut], status_code=status.HTTP_200_OK)
async def get_genres(db: DbDependency):
    """
    Generates a list of genres and their IDs.
    """
    cache_key = "genres:all"
    cached = await get_cache(cache_key)
    if cached:
        return [GenreOut.model_validate(g) for g in cached]

    try:
        response = await tmdb_client.get("/genre/movie/list")
        response.raise_for_status()
        data = response.json()["genres"]
        await set_cache(cache_key, [GenreOut.model_validate(g).model_dump() for g in data], ttl=CACHE_TTL)
        return [GenreOut.model_validate(g) for g in data]

    except httpx.HTTPStatusError as e:
        if e.response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication error with TMDB.")
        raise HTTPException(status_code=e.response.status_code, detail=(f"TMDB API error: {e.response.text}"))
    except httpx.RequestError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service unavailable")
