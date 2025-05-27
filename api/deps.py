from database.repository import PlaceRepo, PlantRepo, SpecialistRepo
from services.base import BaseService


def place_service():
    return BaseService(PlaceRepo())


def specialist_service():
    return BaseService(SpecialistRepo())


def plant_service():
    return BaseService(PlantRepo())
