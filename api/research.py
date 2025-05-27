from datetime import datetime
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .deps import research_service
from services.base import BaseService


router = APIRouter(prefix='/research', tags=['research'])


@router.get("/")
async def research_list(
    service: Annotated[BaseService, Depends(research_service)]
):
    items = await service.get_all()
    return items


@router.get("/{id}")
async def research_detail(
    service: Annotated[BaseService, Depends(research_service)],
    id: str
):
    item = await service.get_one(id)
    return item


class ResearchModel(BaseModel):
    name: str
    target: str
    description: str
    start_date: datetime
    end_date: datetime
    status: str 
    plant_id: UUID 


@router.post("/")
async def research_create(
    research: ResearchModel,
    service: Annotated[BaseService, Depends(research_service)]
):
    result = await service.create(research)
    return result


@router.patch("/{id}")
async def research_update(
    research: ResearchModel,
    service: Annotated[BaseService, Depends(research_service)],
    id: str
):
    result = await service.update(id, research)
    return result


@router.delete("/{id}")
async def research_delete(
    service: Annotated[BaseService, Depends(research_service)],
    id: str
):
    result = await service.delete(id)
    return result