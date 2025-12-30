import httpx #async-capable HTTP client library used to call external APIs
import hashlib
import json

from typing import Optional, List #are used for function signatures and by FastAPI to infer parameter types and generate OpenAPI docs.
#Query: used to declare and document query parameters (their defaults, validators, descriptions).
from fastapi import APIRouter, Query, HTTPException
from starlette import status

from app.schemas.movie import MovieOut
from app.core.config import tmdb_client
from app.api.deps.db import DbDependency
from app.core.cache import get_cache, set_cache, delete_cache


router = APIRouter(
    prefix="/discover",
    tags=["discover"]
)


# Utility function to map our clean parameters to TMDB's format
def build_tmdb_params(
        genre: Optional[List[int]],
        min_rating: Optional[float],
        min_votes: Optional[float],
        release_year: Optional[int],
        sort_by: str, #Defaulting to popularity from the website
) -> dict: #Returns a dict of strings/numbers suitable for passing to httpx as params.
    """
    Constructs the parameters dictionary for the recommendations endpoint
    """
    params = {
        "sort_by": sort_by,
        "include_adult": "false",
        "include_video": "false",
    }

    if genre:
        params["with_genres"] = ",".join(map(str, genre))

    if min_rating is not None:
        params["vote_average.gte"] = min_rating

    if min_votes is not None:
        params["vote_count.gte"] = min_votes

    if release_year is not None:
        params["primary_release_year"] = release_year

    return params


def discover_cache_key(params: dict) -> str:
    raw = json.dumps(params, sort_keys=True)
    hashed = hashlib.md5(raw.encode()).hexdigest()
    return f"discover:{hashed}"


@router.get("/", response_model=List[MovieOut], status_code=status.HTTP_200_OK)
async def get_recommendations(
    genre: Optional[List[int]] = Query(None, description="List of TMDB genre IDs to include"),
    min_rating: Optional[float] = Query(None, ge=0.0, le=10.0, description= "Minimum average rating (0.0 to 10.0)."),
    min_votes: Optional[float] = Query(None, ge=1.0, description="Minimum number of votes required."),
    release_year: Optional[int] = Query(None, ge=1888, description="Filter by release year"),
    sort_by: str = Query("popularity.desc", description="Sorting key (e.g., popularity.desc, vote_average.desc, release_date.desc).")
    ):
    """
    Generates movie recommendations based on various filtering criteria
    using the TMDB Discover API
    """
    tmdb_params = build_tmdb_params(genre, min_rating, min_votes, release_year, sort_by)

    cache_key = discover_cache_key(tmdb_params)
    cached = await get_cache(cache_key)
    if cached:
        return [MovieOut.model_validate(m) for m in cached]

    try:
        response = await tmdb_client.get("/discover/movie", params=tmdb_params)
        response.raise_for_status()
        results = response.json().get("results", [])
        data_out = [MovieOut.model_validate(m) for m in results]
        #save in the db only validated data
        await set_cache(cache_key, [m.model_dump() for m in data_out], ttl=300)
        return data_out

    except httpx.HTTPStatusError as e:
        if e.response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication error with TMDB.")
        raise HTTPException(status_code=e.response.status_code, detail=(f"TMDB API error: {e.response.text}"))
    except httpx.RequestError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service unavailable")
