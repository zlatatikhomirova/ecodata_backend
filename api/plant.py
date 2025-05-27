from datetime import datetime
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .deps import plant_service
from services.base import BaseService


router = APIRouter(prefix='/plant', tags=['plant'])


@router.get("/")
async def plant_list(
    service: Annotated[BaseService, Depends(plant_service)]
):
    items = await service.get_all()
    return items


@router.get("/{id}")
async def plant_detail(
    service: Annotated[BaseService, Depends(plant_service)],
    id: str
):
    item = await service.get_one(id)
    return item


class PlantModel(BaseModel):
    form: str
    sheet_type: str
    family: str
    type: str
    place_id: UUID 


@router.post("/")
async def plant_create(
    plant: PlantModel,
    service: Annotated[BaseService, Depends(plant_service)]
):
    result = await service.create(plant)
    return result


@router.patch("/{id}")
async def plant_update(
    plant: PlantModel,
    service: Annotated[BaseService, Depends(plant_service)],
    id: str
):
    result = await service.update(id, plant)
    return result


@router.delete("/{id}")
async def plant_delete(
    service: Annotated[BaseService, Depends(plant_service)],
    id: str
):
    result = await service.delete(id)
    return result