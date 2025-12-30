from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class MovieOut(BaseModel):
    id: int = Field(...,gt=0, description="Unique movie ID")
    original_language: str = Field(default="en")
    original_title: str = Field(...,min_length=1, max_length=100)
    overview: Optional[str] = Field(None, min_length=1, max_length=10000, description="Short info about the movie")
    popularity: float = Field(...,ge=0.0, le=10000.0, description="The movie popularity among users")
    poster_path: Optional[str] = None
    release_date: Optional[date] = None
    title: str = Field(...,min_length=1, max_length=100)
    video: bool
    vote_average: float = Field(...,ge=0.0, le=10.0, description="User's recommendation")
    vote_count: int = Field(...,gt=0)

    model_config = {
        "from_attributes": True
    }