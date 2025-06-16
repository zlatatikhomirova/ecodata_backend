import aiohttp
from database.repos.repository import (
    ArticleRepo,
    PlaceRepo,
    PlantRepo,
    ResearchRepo,
    SpecialistRepo,
)
from services.base import BaseService
from services.s3 import S3Service
from s3_storage.minio import BaseMinioRepo
from core.settings import settings


async def s3_file_service():
    async with aiohttp.ClientSession() as session:
        yield S3Service(BaseMinioRepo(settings.s3_settings, session))


def place_service():
    return BaseService(PlaceRepo())


def specialist_service():
    return BaseService(SpecialistRepo())


def plant_service():
    return BaseService(PlantRepo())


def research_service():
    return BaseService(ResearchRepo())


def article_service():
    return BaseService(ArticleRepo())
