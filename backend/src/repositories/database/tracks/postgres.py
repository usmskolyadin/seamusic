from dataclasses import dataclass

from sqlalchemy import select, delete

from src.models.tracks import Track
from src.repositories.database.base import SQLAlchemyRepository
from src.repositories.converters.sqlalchemy import request_dto_to_model, models_to_dto, model_to_response_dto
from src.repositories.database.tracks.base import BaseTracksRepository
from src.repositories.dtos.tracks import UpdateTrackRequestDTO, TrackResponseDTO, TracksResponseDTO, Track as _Track


@dataclass
class TracksRepository(SQLAlchemyRepository, BaseTracksRepository):
    async def get_user_tracks(self, user_id: int) -> TracksResponseDTO:
        query = select(Track).filter_by(user_id=user_id)
        tracks = list(await self.session.scalars(query))
        return TracksResponseDTO(tracks=models_to_dto(models=tracks, dto=_Track))

    async def get_all_tracks(self) -> TracksResponseDTO:
        query = select(Track)
        tracks = list(await self.session.scalars(query))
        return TracksResponseDTO(tracks=models_to_dto(models=tracks, dto=_Track))

    async def get_track_by_id(self, track_id: int) -> TrackResponseDTO | None:
        track = await self.session.get(Track, track_id)
        return model_to_response_dto(model=track, response_dto=TrackResponseDTO)

    async def update_track(self, track: UpdateTrackRequestDTO) -> None:
        track = request_dto_to_model(model=Track, request_dto=track)
        await self.session.merge(track)

    async def delete_track(self, track_id: int, user_id: int) -> None:
        query = delete(Track).filter_by(id=track_id, user_id=user_id)
        await self.session.execute(query)