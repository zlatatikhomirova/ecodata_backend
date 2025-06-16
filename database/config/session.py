from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession


class PostgresSession:
    def __init__(self):
        self._async_session = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=create_async_engine(
                echo=True,
                url="postgresql+asyncpg://user:password@localhost:5252/ecodata_db",
            ),
        )()

    def get_async(self) -> AsyncSession:
        return self._async_session
    

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker
from asyncio import current_task

class DatabaseHelper:
    def __init__(self, url_: str, echo_: bool = False):
        self.engine = create_async_engine(
            url=url_,
            echo=echo_,
            # url=settings.db_url,
            # echo=settings.db_echo
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
    
    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    # session dependency, через который будем работать 
    # с асинхронной базой данных
    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()

    # session dependency, через который будем работать 
    # с асинхронной базой данных
    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()
        
db_helper = DatabaseHelper(url_=settings.db.url, echo_=settings.db.echo)

