from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .deps import place_service
from services.base import BaseService


router = APIRouter(prefix='/place', tags=['Place'])


@router.get("/")
async def place_list(
    service: Annotated[BaseService, Depends(place_service)]
):
    items = await service.get_all()
    return items


@router.get("/{id}")
async def place_detail(
    service: Annotated[BaseService, Depends(place_service)],
    id: str
):
    item = await service.get_one(id)
    return item


class PlantModel(BaseModel):
    country: str
    region: str
    city: str
    district: str
    type_of_settlement: str


@router.post("/")
async def place_create(
    plant: PlantModel,
    service: Annotated[BaseService, Depends(place_service)]
):
    result = await service.create(plant)
    return result


@router.patch("/{id}")
async def plant_update(
    plant: PlantModel,
    service: Annotated[BaseService, Depends(place_service)],
    id: str
):
    result = await service.update(id, plant)
    return result


@router.delete("/{id}")
async def plant_delete(
    service: Annotated[BaseService, Depends(place_service)],
    id: str
):
    result = await service.delete(id)
    return result