from typing import List

from fastapi import UploadFile, File, APIRouter, Depends, status

from src.schemas.albums import SAlbumBase, SAlbumResponse, SAlbumDeleteResponse
from src.services.albums import AlbumsRepository
from src.utils.albums import unique_album_filename
from src.utils.dependencies import get_current_user
from src.schemas.auth import SUser
from src.services import MediaRepository


albums = APIRouter(prefix="/albums", tags=["Albums"])


@albums.get(
    path="/my",
    summary="albums by current user",
    response_model=List[SAlbumResponse],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": List[SAlbumResponse]}},
)
async def get_user_albums(
    user: SUser = Depends(get_current_user),
) -> List[SAlbumResponse]:
    response = await AlbumsRepository.find_all(user=user)
    return [SAlbumResponse.from_db_model(album) for album in response]


@albums.get(
    path="/all",
    summary="Get all albums",
    response_model=List[SAlbumResponse],
    responses={status.HTTP_200_OK: {"model": List[SAlbumResponse]}},
)
async def all_albums() -> List[SAlbumResponse]:
    response = await AlbumsRepository.find_all()
    return [SAlbumResponse.from_db_model(album) for album in response]


@albums.get(
    path="/get_one/{album_id}",
    summary="Get one album by id",
    response_model=SAlbumResponse,
    responses={status.HTTP_200_OK: {"model": SAlbumResponse}},
)
async def get_one_album(album_id: int) -> SAlbumResponse:
    response = await AlbumsRepository.find_one_by_id(album_id)
    return SAlbumResponse.from_db_model(album=response)


@albums.post(
    path="/add",
    summary="Init a album with file",
    response_model=SAlbumResponse,
    responses={status.HTTP_200_OK: {"model": SAlbumResponse}},
)
async def add_albums(
    file: UploadFile = File(...), user: SUser = Depends(get_current_user)
) -> SAlbumResponse:
    file_info = await unique_album_filename(file) if file else None
    file_url = await MediaRepository.upload_file("AUDIOFILES", file_info, file)

    data = {
        "title": "Unknown title",
        "file_url": file_url,
        "prod_by": user.username,
        "user_id": user.id,
        "type": "album",
    }

    response = await AlbumsRepository.add_one(data)
    return SAlbumResponse.from_db_model(album=response)


@albums.post(
    path="/picture/{albums_id}",
    summary="Update a picture for one album by id",
    response_model=SAlbumResponse,
    responses={status.HTTP_200_OK: {"model": SAlbumResponse}},
)
async def update_pic_albums(
    albums_id: int,
    file: UploadFile = File(...),
) -> SAlbumResponse:
    file_info = await unique_album_filename(file) if file else None
    file_url = await MediaRepository.upload_file("PICTURES", file_info, file)

    data = {"picture_url": file_url}

    response = await AlbumsRepository.edit_one(albums_id, data)
    return SAlbumResponse.from_db_model(album=response)


@albums.post(
    path="/release/{album_id}",
    summary="Release one album by id",
    response_model=SAlbumResponse,
    responses={status.HTTP_200_OK: {"model": SAlbumResponse}},
)
async def release_albums(
    album_id: int,
    albums_data: SAlbumBase,
) -> SAlbumResponse:
    data = {
        "name": albums_data.title,
        "description": albums_data.description,
        "co_prod": albums_data.co_prod,
    }

    response = await AlbumsRepository.edit_one(album_id, data)
    return SAlbumResponse.from_db_model(album=response)


@albums.put(
    path="/update/{album_id}",
    summary="Edit album (title, description, prod_by) by id",
    response_model=SAlbumResponse,
    responses={status.HTTP_200_OK: {"model": SAlbumResponse}},
)
async def update_albums(
    album_id: int,
    albums_data: SAlbumBase,
) -> SAlbumResponse:
    data = {
        "name": albums_data.title,
        "description": albums_data.description,
        "prod_by": albums_data.prod_by,
    }

    response = await AlbumsRepository.edit_one(album_id, data)

    return SAlbumResponse.from_db_model(album=response)


@albums.delete(
    path="/delete/{album_id}",
    summary="Delete album by id",
    response_model=SAlbumDeleteResponse,
    responses={status.HTTP_200_OK: {"model": SAlbumDeleteResponse}},
)
async def delete_albums(album_id: int) -> SAlbumDeleteResponse:
    await AlbumsRepository.delete(id_=album_id)

    return SAlbumDeleteResponse