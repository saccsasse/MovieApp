from pydantic import BaseModel, Field

class GenreOut(BaseModel):
    id: int = Field(..., gt=0, description="Unique genre ID")
    name: str = Field(..., min_length=1, max_length=100, description="Genre name")

    model_config = {
        "from_attributes": True
    }