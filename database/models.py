from datetime import datetime
import re
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, ForeignKey, MetaData, Numeric, String, Table
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class BaseSqlModel:
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)

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
    country: Mapped[str] = mapped_column(String)
    region: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    district: Mapped[str] = mapped_column(String)
    type_of_settlement: Mapped[str] = mapped_column(String)
    
    plants: Mapped[list["Plant"]] = relationship(back_populates="place")


class Specialist(BaseSqlModel):
    surname: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    job_title: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    orchid: Mapped[str] = mapped_column(String)


class Plant(BaseSqlModel):
    form: Mapped[str] = mapped_column(String)
    sheet_type: Mapped[str] = mapped_column(String)
    family: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    place_id = mapped_column(ForeignKey(Place.id))
    
    place: Mapped[Place] = relationship(back_populates="plants")


class Research(BaseSqlModel):
    name: Mapped[str] = mapped_column(String, nullable=False)
    target: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String)
    plant_id = mapped_column(ForeignKey(Plant.id))


class Article(BaseSqlModel):
    name: Mapped[str] = mapped_column(String, nullable=False)
    plant_id = mapped_column(ForeignKey(Plant.id))
    journal_name: Mapped[str] = mapped_column(String)
    link: Mapped[str] = mapped_column(String)
    file: Mapped[str] = mapped_column(String)


class Laboratory(BaseSqlModel):
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    
    
class Leaf(BaseSqlModel):
    plant_id = mapped_column(ForeignKey(Plant.id))
    date_of_measurement: Mapped[datetime] = mapped_column(DateTime)
    side_of_the_world: Mapped[str] = mapped_column(String)
    unit: Mapped[str] = mapped_column(String, nullable=False)
    photo: Mapped[str] = mapped_column(String, nullable=False)
    location_on_the_plant: Mapped[str] = mapped_column(String, nullable=False)
    
    
class BioChem(BaseSqlModel):
    chlorophyll_a: Mapped[float] = mapped_column(Numeric)
    chlorophyll_b: Mapped[float] = mapped_column(Numeric)
    carotenoids: Mapped[float] = mapped_column(Numeric)
    phenols: Mapped[float] = mapped_column(Numeric)
    anthocyanins: Mapped[float] = mapped_column(Numeric)
    peroxidase: Mapped[float] = mapped_column(Numeric)
    vitamin_c: Mapped[float] = mapped_column(Numeric)
    unit: Mapped[str] = mapped_column(String, nullable=False)
    note: Mapped[str] = mapped_column(String, nullable=False)
    analysis_date: Mapped[datetime] = mapped_column(DateTime)
    laboratory_id = mapped_column(ForeignKey(Laboratory.id))
    plant_id = mapped_column(ForeignKey(Plant.id))
    
    
class MorphologicalFeature(BaseSqlModel):
    area: Mapped[float] = mapped_column(Numeric)
    length: Mapped[float] = mapped_column(Numeric)
    left_second_vein_length: Mapped[float] = mapped_column(Numeric)
    right_second_vein_length: Mapped[float] = mapped_column(Numeric)
    left_btw_first_n_second_veins_ends_dist: Mapped[float] = mapped_column(Numeric)
    right_btw_first_n_second_veins_ends_dist: Mapped[float] = mapped_column(Numeric)
    left_btw_first_n_second_veins_begins_dist: Mapped[float] = mapped_column(Numeric)
    right_btw_first_n_second_veins_begins_dist: Mapped[float] = mapped_column(Numeric)
    left_btw_second_n_central_veins_angle: Mapped[float] = mapped_column(Numeric)
    right_btw_second_n_central_veins_angle: Mapped[float] = mapped_column(Numeric)
    left_halfs_width: Mapped[float] = mapped_column(Numeric)
    right_halfs_width: Mapped[float] = mapped_column(Numeric)
    leaf_id = mapped_column(ForeignKey(Leaf.id))

    
order_mtm_product_table = Table(
    'specialist_in_research',
    BaseSqlModel.metadata,
    Column('research_id', ForeignKey('research.id')),
    Column('specialist_id', ForeignKey('specialist.id')),
)

    