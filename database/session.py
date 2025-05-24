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
