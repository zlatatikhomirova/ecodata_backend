from typing import TYPE_CHECKING
from uuid import UUID as PyUUID, uuid4

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseSqlModel

if TYPE_CHECKING:
    from .address_rel_models import Address


class PollutionType(BaseSqlModel):
    __tablename__ = "pollution_types"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    # rel
    # one2m
    pollutions_near_place_list: Mapped[list["PollutionsNearPlace"]] = relationship(
        "PollutionsNearPlace", back_populates="pollution_type"
    )

class PollutionsNearPlace(BaseSqlModel):
    __tablename__ = "pollutions_near_place_list"
    
    address_id: Mapped[PyUUID] = mapped_column(
        UUID, ForeignKey("addresses.id")
    )
    pollution_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("pollution_types.id"), primary_key=True
    )

    # rel
    # m2one
    address: Mapped["Address"] = relationship(
        back_populates="pollutions_near_place_list"
    )
    pollution_type: Mapped["PollutionType"] = relationship(
        back_populates="pollutions_near_place_list"
    )
