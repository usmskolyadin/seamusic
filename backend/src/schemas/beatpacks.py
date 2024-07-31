from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict

from src.models.beatpacks import Beatpack


class BeatCreate(BaseModel):
    id: int


class BeatpackCreate(BaseModel):
    title: str
    description: str
    beats: List[BeatCreate]


class BeatResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class SBeatpackEditResponse(BaseModel):
    response: str = "Beat pack edited"


class SBeatpackDeleteResponse(BaseModel):
    response: str = "Beat pack deleted"


class SBeatpackResponse(BaseModel):
    id: int
    description: str
    is_available: bool
    title: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_db_model(cls, beatpack: Beatpack) -> "SBeatpackResponse":
        return cls(
            id=beatpack.id,
            description=beatpack.description,
            is_available=beatpack.is_available,
            title=beatpack.title,
            created_at=beatpack.created_at,
            updated_at=beatpack.updated_at,
        )