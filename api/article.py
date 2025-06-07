from typing import Annotated
from fastapi import APIRouter, Depends, File, UploadFile
from pydantic import BaseModel

from services.base import BaseService
from services.s3 import FileDto, S3Service
from storage.minio import BaseMinioRepo
from .deps import article_service, s3_file_service


router = APIRouter(prefix="/article", tags=["Article"])


@router.get("/")
async def article_list(service: Annotated[BaseService, Depends(article_service)]):
    items = await service.get_all()
    return items


@router.get("/{id}")
async def article_detail(
    service: Annotated[BaseService, Depends(article_service)], id: str
):
    item = await service.get_one(id)
    return item


class ArticleModel(BaseModel):
    name: str
    plant_id: str
    journal_name: str
    link: str
    file: str


@router.post("/")
async def article_create(
    a_service: Annotated[BaseService, Depends(article_service)],
    file_storage: Annotated[S3Service, Depends(s3_file_service)],
    file: UploadFile = File(...),
    article: ArticleModel = Depends(),
):
    print(file)
    dto = FileDto(
        filename=file.filename,
        file=file.file,
        size=file.size,
        content_type=file.content_type,
    )
    filename = await file_storage.upload(dto)
    article.file = filename
    result = await a_service.create(article)
    return result


@router.patch("/{id}")
async def article_update(
    article: ArticleModel,
    service: Annotated[BaseService, Depends(article_service)],
    id: str,
):
    result = await service.update(id, article)
    return result


@router.delete("/{id}")
async def article_delete(
    service: Annotated[BaseService, Depends(article_service)], id: str
):
    result = await service.delete(id)
    return result
