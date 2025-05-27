from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import selectinload

from .models import Article, BioChem, Laboratory, Leaf, MorphologicalFeature, Place, Plant, Research, Specialist
from .session import PostgresSession


class SqlRepo:

    def __init__(self, model) -> None:
        self.session = PostgresSession().get_async()
        self.model = model

    @staticmethod
    def new_id() -> UUID:
        return uuid4()

    async def get_all(self):
        stmt = select(self.model)
        return (await self.session.execute(stmt)).scalars().all()

    async def get(self, id: UUID):
        stmt = select(self.model).where(self.model.id == id)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def create(self, item: dict[str, Any]) -> None:
        try:
            print(self.model)
            stmt = insert(self.model).values(**item)
            await self.session.execute(stmt)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

    async def update(self, id: UUID, changes: dict[str, Any]) -> None:
        stmt = update(self.model).where(self.model.id == id).values(**changes)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, id: UUID) -> None:
        stmt = delete(self.model).where(self.model.id == id)
        await self.session.execute(stmt)
        await self.session.commit()
        
        
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