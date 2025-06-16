from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import selectinload

from ..models import Article, BioChem, Laboratory, Leaf, MorphologicalFeature, Place, Plant, Research, Specialist
from ..config.session import PostgresSession

from .base import SqlRepo
        
        
class PlaceRepo(SqlRepo):
    
    def __init__(self):
        super().__init__(Place)
        
        
class SpecialistRepo(SqlRepo):
    
    def __init__(self):
        super().__init__(Specialist)
        
        
class PlantRepo(SqlRepo):
    
    def __init__(self):
        super().__init__(Plant)
        
    async def get(self, id: UUID):
        stmt = select(Plant).options(selectinload(Plant.place)).where(Plant.id == id)
        item = (await self.session.execute(stmt)).scalar_one_or_none()
        return item 
        

class ResearchRepo(SqlRepo):
    
    def __init__(self):
        super().__init__(Research)
        
    async def get(self, id: UUID):
        stmt = select(Research).options(selectinload(Research.plant)).where(Research.id == id)
        item = (await self.session.execute(stmt)).scalar_one_or_none()
        return item 
        
        
class ArticleRepo(SqlRepo):
    
     def __init__(self):
        super().__init__(Article)
        
        
class LaboratoryRepo(SqlRepo):
    
     def __init__(self, session):
        super().__init__(Laboratory)
        
        
class LeafRepo(SqlRepo):
    
     def __init__(self):
        super().__init__(Leaf) 
        
        
class BioChemRepo(SqlRepo):
    
     def __init__(self):
        super().__init__(BioChem)
        
        
class MorphologicalFeatureRepo(SqlRepo):
    
     def __init__(self):
        super().__init__(MorphologicalFeature) 