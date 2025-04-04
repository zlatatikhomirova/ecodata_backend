from datetime import datetime
import re
from uuid import uuid4

from sqlalchemy import UUID, DateTime, ForeignKey, MetaData, String
from sqlalchemy.orm import declared_attr, Mapped, mapped_column
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class BaseSqlModel:
    sid: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)

    @declared_attr
    def __tablename__(cls) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class Place(BaseSqlModel):
    country = mapped_column(String)
    region = mapped_column(String)
    city = mapped_column(String)
    district = mapped_column(String)


class LaboratoryAssistant(BaseSqlModel):
    surname = mapped_column(String)
    name = mapped_column(String)
    last_name = mapped_column(String)
    job_title = mapped_column(String)
    phone = mapped_column(String)
    email = mapped_column(String)


class Plant(BaseSqlModel):
    form: Mapped[str] = mapped_column(String)
    sheet_type = Mapped[str] = mapped_column(String)
    family: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    plant_id = mapped_column(ForeignKey(Place.id))


class Research(BaseSqlModel):
    name: Mapped[str] = mapped_column(String, nullable=False)
    target: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String)
    plant_id = mapped_column(ForeignKey(Plant.id))


class Publication(BaseSqlModel):
    name: Mapped[str] = mapped_column(String, nullable=False)
    plant_id = mapped_column(ForeignKey(Plant.id))
    journal_name: Mapped[str] = mapped_column(String)


class Laboratory(BaseSqlModel):
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
