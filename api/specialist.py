from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .deps import specialist_service
from services.base import BaseService


router = APIRouter(prefix='/specialist', tags=['specialist'])


@router.get("/")
async def specialist_list(
    service: Annotated[BaseService, Depends(specialist_service)]
):
    items = await service.get_all()
    return items


@router.get("/{id}")
async def specialist_detail(
    service: Annotated[BaseService, Depends(specialist_service)],
    id: str
):
    item = await service.get_one(id)
    return item


class SpecialistModel(BaseModel):
    country: str
    region: str
    city: str
    district: str
    type_of_settlement: str


@router.post("/")
async def specialist_create(
    plant: SpecialistModel,
    service: Annotated[BaseService, Depends(specialist_service)]
):
    result = await service.create(plant)
    return result


@router.patch("/{id}")
async def plant_update(
    plant: SpecialistModel,
    service: Annotated[BaseService, Depends(specialist_service)],
    id: str
):
    result = await service.update(id, plant)
    return result


@router.delete("/{id}")
async def plant_delete(
    service: Annotated[BaseService, Depends(specialist_service)],
    id: str
):
    result = await service.delete(id)
    return result