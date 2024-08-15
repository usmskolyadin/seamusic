from dataclasses import dataclass

from sqlalchemy import select, delete

from src.models.beatpacks import Beatpack
from src.repositories.converters.sqlalchemy import request_dto_to_model, model_to_response_dto, models_to_dto
from src.repositories.database.base import SQLAlchemyRepository
from src.repositories.database.beatpacks.base import BaseBeatpacksRepository
from src.repositories.dtos.beatpacks import (
    Beatpack as _Beatpack,
    BeatpackResponseDTO,
    BeatpacksResponseDTO,
    CreateBeatpackRequestDTO,
    UpdateBeatpackRequestDTO
)


@dataclass
class BeatpacksRepository(BaseBeatpacksRepository, SQLAlchemyRepository):
    async def get_user_beatpacks(self, user_id: int) -> BeatpacksResponseDTO:
        query = select(Beatpack).filter_by(user_id=user_id)
        beatpacks = list(await self.session.scalars(query))
        return BeatpacksResponseDTO(beats=models_to_dto(models=beatpacks, dto=_Beatpack))

    async def get_all_beatpacks(self) -> BeatpacksResponseDTO:
        query = select(Beatpack)
        beatpacks = list(await self.session.scalars(query))
        return BeatpacksResponseDTO(beats=models_to_dto(models=beatpacks, dto=_Beatpack))

    async def get_one_beatpack(self, beatpack_id: int) -> BeatpackResponseDTO | None:
        return model_to_response_dto(
            model=await self.session.get(Beatpack, beatpack_id),
            response_dto=BeatpackResponseDTO
        )

    async def add_beatpack(self, beatpack: CreateBeatpackRequestDTO) -> None:
        beatpack = request_dto_to_model(model=Beatpack, request_dto=beatpack)
        self.session.add(beatpack)

    async def update_beatpack(self, beatpack: UpdateBeatpackRequestDTO) -> None:
        beatpack = request_dto_to_model(model=Beatpack, request_dto=beatpack)
        await self.session.merge(beatpack)

    async def delete_beatpack(self, beatpack_id: int, user_id: int) -> None:
        query = delete(Beatpack).filter_by(id=beatpack_id, user_id=user_id)
        await self.session.execute(query)
