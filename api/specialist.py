from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

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
    surname: str
    name: str
    last_name: str
    job_title: str
    phone: str
    email: EmailStr
    orchid: str 


@router.post("/")
async def specialist_create(
    specialist: SpecialistModel,
    service: Annotated[BaseService, Depends(specialist_service)]
):
    result = await service.create(specialist)
    return result


@router.patch("/{id}")
async def specialist_update(
    specialist: SpecialistModel,
    service: Annotated[BaseService, Depends(specialist_service)],
    id: str
):
    result = await service.update(id, specialist)
    return result


@router.delete("/{id}")
async def specialist_delete(
    service: Annotated[BaseService, Depends(specialist_service)],
    id: str
):
    result = await service.delete(id)
    return result