import httpx
from fastapi import HTTPException
from app.core.config import tmdb_client
from app.core.cache import get_cache, set_cache


async def get_movie_by_id(movie_id: int) -> dict:
    cache_key = f"tmdb:movie:{movie_id}"
    cached = await get_cache(cache_key)
    if cached:
        return cached

    try:
        response = await tmdb_client.get(f"/movie/{movie_id}")
        response.raise_for_status()
        data = response.json()
        await set_cache(cache_key, data, ttl=3600)  #1h
        return data

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Movie not found in TMDB")
        raise HTTPException(status_code=e.response.status_code, detail="TMDB API error")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="TMDB service unavailable")
