from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.repositories.dtos.tracks import TracksResponseDTO, TrackResponseDTO, UpdateTrackRequestDTO


@dataclass
class BaseTracksRepository(ABC):
    @abstractmethod
    async def get_user_tracks(self, user_id: int) -> TracksResponseDTO:
        ...

    @abstractmethod
    async def get_all_tracks(self) -> TracksResponseDTO:
        ...

    @abstractmethod
    async def get_track_by_id(self, track_id: int) -> TrackResponseDTO | None:
        ...

    @abstractmethod
    async def update_track(self, track: UpdateTrackRequestDTO) -> None:
        ...

    @abstractmethod
    async def delete_track(self, track_id: int, user_id: int) -> None:
        ...
