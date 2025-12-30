import asyncio

from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.repositories import favourite_repo
from app.api.services.tmdb_service import get_movie_by_id
from app.core.cache import delete_cache
from app.db.repositories.audit_repo import log_action_task


async def get_favourites(db: Session, user_id: int) -> List[dict]:
    movie_ids = favourite_repo.get_user_favourites(db, user_id)
    movies = await asyncio.gather(*(get_movie_by_id(mid) for mid in movie_ids))
    return movies


async def add_favourite(db: Session, user_id: int, movie_id: int):
    if favourite_repo.is_favourite(db, user_id, movie_id):
        raise HTTPException(400, "Movie already in favourites.")
    await get_movie_by_id(movie_id) #Validate TMDB movie exists
    favourite_repo.add_favourites(db, user_id,movie_id)

    db.commit()
    await delete_cache(f"favourites:user:{user_id}")
    log_action_task.delay(
        action="add_favourite",
        admin_id=user_id,
        target_user_id=movie_id
    )


async def remove_favourite(db: Session, user_id: int, movie_id: int):
    if not favourite_repo.is_favourite(db, user_id, movie_id):
        raise HTTPException(404, "Movie is not in favourites")
    favourite_repo.remove_favourite(db, user_id, movie_id)

    db.commit()
    await delete_cache(f"favourites:user:{user_id}")
    log_action_task.delay(
        action="remove_favourite",
        admin_id=user_id,
        target_user_id=movie_id
    )
