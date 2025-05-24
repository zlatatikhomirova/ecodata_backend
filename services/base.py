from typing import TypeVar
from uuid import UUID

from pydantic import BaseModel

from database.repository import SqlRepo


Repo = TypeVar("Repo", bound=SqlRepo)


class BaseService:
    
    def __init__(self, repo: Repo):
        self._repo = repo
        
    async def get_all(self):
        return await self._repo.get_all()
    
    async def get_one(self, id):
        return await self._repo.get(id)
    
    async def create(self, item: BaseModel):
        identity = self._repo.new_id()
        item_dict = item.model_dump()
        item_dict["id"] = identity
        await self._repo.create(item_dict)
        return identity
        
    async def update(self, id: UUID, item: BaseModel):
        await self._repo.update(id, item.model_dump())
        return id
        
    async def delete(self, id: UUID):
        await self._repo.delete(id)
