from sqlalchemy import Column, Integer, String, Boolean, Float, Date
from app.db.session import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    original_language = Column(String(255), nullable=False, default="en")
    original_title = Column(String(255), nullable=False)
    overview = Column(String(1000))
    popularity = Column(Float, nullable=False)
    poster_path = Column(String(1000))
    release_date = Column(Date, nullable=True)
    title = Column(String(255), nullable=False)
    video = Column(Boolean, nullable=False, default=False)
    vote_average = Column(Float)
    vote_count = Column(Integer)
