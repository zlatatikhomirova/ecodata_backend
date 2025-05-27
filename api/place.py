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


class PlaceModel(BaseModel):
    country: str
    region: str
    city: str
    district: str
    type_of_settlement: str


@router.post("/")
async def place_create(
    place: PlaceModel,
    service: Annotated[BaseService, Depends(place_service)]
):
    result = await service.create(place)
    return result


@router.patch("/{id}")
async def place_update(
    place: PlaceModel,
    service: Annotated[BaseService, Depends(place_service)],
    id: str
):
    result = await service.update(id, place)
    return result


@router.delete("/{id}")
async def place_delete(
    service: Annotated[BaseService, Depends(place_service)],
    id: str
):
    result = await service.delete(id)
    return result