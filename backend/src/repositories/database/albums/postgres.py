from dataclasses import dataclass

from sqlalchemy import select, delete

from src.models.albums import Album
from src.repositories.converters.sqlalchemy import model_to_response_dto, models_to_dto, request_dto_to_model
from src.repositories.database.albums.base import BaseAlbumRepository
from src.repositories.database.base import SQLAlchemyRepository
from src.repositories.dtos.albums import (
    AlbumResponseDTO,
    CreateAlbumRequestDTO,
    AlbumsResponseDTO,
    UpdateAlbumRequestDTO
)


@dataclass
class AlbumRepository(SQLAlchemyRepository, BaseAlbumRepository):
    async def create_album(self, album: CreateAlbumRequestDTO) -> None:
        album = request_dto_to_model(model=Album, request_dto=album)
        self.session.add(album)
        await self.session.flush()

    async def get_album_by_id(self, album_id: int) -> AlbumResponseDTO | None:
        album = await self.session.get(Album, album_id)
        return model_to_response_dto(response_dto=AlbumResponseDTO, model=album)

    async def edit_album(self, album: UpdateAlbumRequestDTO) -> None:
        album = request_dto_to_model(model=Album, request_dto=album)
        await self.session.merge(album)

    async def get_all_albums(self) -> AlbumsResponseDTO:
        query = select(Album)
        albums = list(await self.session.scalars(query))
        return AlbumsResponseDTO(albums=models_to_dto(models=albums, dto=AlbumResponseDTO))

    async def get_all_user_albums(self, user_id: int) -> AlbumsResponseDTO:
        query = select(Album).where(Album.user_id == user_id)
        albums = list(await self.session.scalars(query))
        return AlbumsResponseDTO(albums=models_to_dto(models=albums, dto=AlbumResponseDTO))

    async def delete_album(self, album_id: int, user_id: int) -> None:
        query = delete(Album).where(Album.id == album_id, Album.user_id == user_id)
        await self.session.execute(query)