from database.repository import PlaceRepo, PlantRepo
from services.base import BaseService


def place_service():
    return BaseService(PlaceRepo())