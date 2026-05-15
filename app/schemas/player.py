from datetime import datetime

from pydantic import BaseModel, Field


class PlayerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    position: str = Field(min_length=2, max_length=50)
    number: int = Field(gt=0)


class PlayerResponse(PlayerCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }
