from src.dtos.database.base import BaseRequestDTO, BaseResponseDTO, BaseDTO
from src.enums.type import Type


class Album(BaseDTO):
    name: str
    picture_url: str
    description: str
    co_prod: str
    type: Type
    user_id: int


class CreateAlbumRequestDTO(BaseRequestDTO):
    name: str
    picture_url: str
    description: str
    co_prod: str
    type: Type
    user_id: int


class UpdateAlbumRequestDTO(BaseRequestDTO):
    name: str
    picture_url: str
    description: str
    co_prod: str
    type: Type
    user_id: int


class AlbumResponseDTO(BaseResponseDTO):
    name: str
    picture_url: str
    description: str
    co_prod: str
    type: Type
    user_id: int


class AlbumsResponseDTO(BaseResponseDTO):
    albums: list[Album]
