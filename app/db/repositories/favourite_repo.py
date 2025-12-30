from sqlalchemy.orm import Session
from typing import Optional
from fastapi import Query
from app.db.models.favourite import Favourite


def get_user_favourites(db: Session, user_id: int):
    return [fav.movie_id for fav in db.query(Favourite).filter(Favourite.user_id == user_id).all()]


def add_favourites(db: Session, user_id: int, movie_id: int):
    fav = Favourite(user_id = user_id, movie_id = movie_id)
    db.add(fav)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def remove_favourite(db: Session, user_id: int, movie_id: int):
    fav = db.query(Favourite).filter(Favourite.user_id == user_id, Favourite.movie_id == movie_id).first()
    if fav:
        db.delete(fav)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise e


def is_favourite(db: Session, user_id: int, movie_id: int) -> bool:
    return db.query(Favourite).filter_by(user_id=user_id, movie_id=movie_id).first() is not None
