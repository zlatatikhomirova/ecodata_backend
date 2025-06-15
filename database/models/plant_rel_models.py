from typing import TYPE_CHECKING
from uuid import UUID as PyUUID, uuid4

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseSqlModel

if TYPE_CHECKING:
    from .address_rel_models import Address
    from .research_plant_assoc_rel_models import ResearchPlantAssociation


class LeafType(BaseSqlModel):
    __tablename__ = "leaf_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    # rel
    # one2m
    plants_descriptions: Mapped[list["PlantDescription"]] = relationship(back_populates="leaf_type")


class Genus(BaseSqlModel):
    __tablename__ = "genus_list"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    # rel
    # one2m
    plants_descriptions: Mapped[list["PlantDescription"]] = relationship(back_populates="genus")

class Species(BaseSqlModel):
    __tablename__ = "species_list"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    # rel
    # one2m
    plants_descriptions: Mapped[list["PlantDescription"]] = relationship(back_populates="species")

class LifeForm(BaseSqlModel):
    __tablename__ = "life_forms"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    # rel
    # one2m
    plants_descriptions: Mapped[list["PlantDescription"]] = relationship(back_populates="life_form")

class PlantDescription(BaseSqlModel):
    __tablename__ = "plants_descriptions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    life_form_id: Mapped[int] = mapped_column(Integer, ForeignKey("life_forms.id"))
    leaf_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("leaf_types.id"))
    genus_id: Mapped[int] = mapped_column(Integer, ForeignKey("genus_list.id"))
    species_id: Mapped[int] = mapped_column(Integer, ForeignKey("species_list.id"))
    description: Mapped[str] = mapped_column(String)

    # rel
    # m2one
    leaf_type: Mapped["LeafType"] = relationship(back_populates="plants_descriptions")
    genus: Mapped["Genus"] = relationship(back_populates="plants_descriptions")
    species: Mapped["Species"] = relationship(back_populates="plants_descriptions")
    life_form: Mapped["LifeForm"] = relationship(back_populates="plants_descriptions")

    # one2m
    plants: Mapped[list["Plant"]] = relationship(back_populates="plant_description")

class Plant(BaseSqlModel):
    __tablename__ = "plants"
    
    id: Mapped[PyUUID] = mapped_column(
        UUID, primary_key=True, default=uuid4, server_default=func.gen_random_uuid()
    )
    address_id: Mapped[PyUUID] = mapped_column(
        UUID, ForeignKey("addresses.id")
    )
    plant_description_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("plants_descriptions.id")
    )
    additional_info: Mapped[str] = mapped_column(String)

    # rel
    # m2one
    plant_description: Mapped["PlantDescription"] = relationship(back_populates="plants")
    address: Mapped["Address"] = relationship(back_populates="plants")

    # one2m
    research_plant_associations: Mapped[list["ResearchPlantAssociation"]] = relationship(back_populates="plant")

   