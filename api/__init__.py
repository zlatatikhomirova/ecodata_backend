from fastapi import APIRouter

from .place import router as place_router
from .specialist import router as specialist_router
from .plant import router as plant_router
from .research import router as research_router
from .article import router as article_router


router = APIRouter()

router.include_router(place_router)
router.include_router(specialist_router)
router.include_router(plant_router)
router.include_router(research_router)
router.include_router(article_router)