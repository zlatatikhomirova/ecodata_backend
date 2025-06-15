from typing import TYPE_CHECKING

from uuid import UUID as PyUUID, uuid4

from sqlalchemy.dialects.postgresql import UUID


from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    func,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import BaseSqlModel

if TYPE_CHECKING:
    from .pollutions_rel_models import PollutionsNearPlace
    from .plant_rel_models import Plant
    from .organization_rel_models import Organization

class HouseNumber(BaseSqlModel):
    __tablename__ = "house_numbers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String, nullable=False)

    # rel
    # one2m
    addresses: Mapped[list["Address"]] = relationship(back_populates="house_number")


class Street(BaseSqlModel):
    __tablename__ = "streets"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # rel
    # one2m
    street_settlement_associations: Mapped[list["StreetSettlementAssociation"]] = relationship(back_populates="street")


class Country(BaseSqlModel):
    __tablename__ = "countries"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # rel
    # one2m
    regions: Mapped[list["Region"]] = relationship(back_populates="country")

class Region(BaseSqlModel):
    __tablename__ = "regions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    country_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("countries.id"), nullable=False
    )

    # rel
    # m2one
    country: Mapped["Country"] = relationship(back_populates="regions")
    
    # one2m
    districts: Mapped[list["District"]] = relationship(back_populates="region")


class District(BaseSqlModel):
    __tablename__ = "districts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    region_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("regions.id"), nullable=False
    )

    # rel
    # m2one
    region: Mapped["Region"] = relationship(back_populates="districts")
    
    # one2m
    settlements: Mapped[list["Settlement"]] = relationship(back_populates="district")


class SettlementType(BaseSqlModel):
    __tablename__ = "settlement_types"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # rel
    # one2m
    settlements: Mapped[list["Settlement"]] = relationship(back_populates="settlement_type")

class Settlement(BaseSqlModel):
    __tablename__ = "settlements"
    
    __table_args__ = (
        UniqueConstraint("name", "district_id", "settlement_type_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    district_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("districts.id"), nullable=False
    )
    settlement_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("settlement_types.id"), nullable=False
    )

    # rel
    # m2one
    settlement_type: Mapped["SettlementType"] = relationship(back_populates="settlements")
    district: Mapped["District"] = relationship(back_populates="settlements")
    
    # one2m
    street_settlement_associations: Mapped[list["StreetSettlementAssociation"]] = relationship(back_populates="settlement")


class StreetSettlementAssociation(BaseSqlModel):
    __tablename__ = "street_settlement_associations"
    
    __table_args__ = (
        UniqueConstraint("street_id", "settlement_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    street_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("streets.id")
    )
    settlement_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("settlements.id")
    )

    # rel
    # m2one
    street: Mapped["Street"] = relationship(back_populates="street_settlement_associations")
    settlement: Mapped["Settlement"] = relationship(back_populates="street_settlement_associations")
    
    # one2m
    addresses: Mapped[list["Address"]] = relationship(back_populates="street_settlement_association")

class Address(BaseSqlModel):
    __tablename__ = "addresses"

    __table_args__ = (
        UniqueConstraint("house_number_id", "street_settlement_association_id"),
    )

    id: Mapped[PyUUID] = mapped_column(
        UUID, primary_key=True, default=uuid4, server_default=func.gen_random_uuid()
    )
    house_number_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("house_numbers.id")
    )
    street_settlement_association_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("street_settlement_associations.id")
    )

    # rel
    # m2one
    street_settlement_association: Mapped["StreetSettlementAssociation"] = relationship(back_populates="addresses")
    house_number: Mapped["HouseNumber"] = relationship(back_populates="addresses")
    
    # one2m
    pollutions_near_place_list: Mapped[list["PollutionsNearPlace"]] = relationship(back_populates="address")
    plants: Mapped[list["Plant"]] = relationship(back_populates="address")
    organizations: Mapped[list["Organization"]] = relationship(back_populates="address")
