from typing import TYPE_CHECKING
from uuid import UUID as PyUUID, uuid4

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import (
    ForeignKey,
    String,
    Date,
    Integer,
    ForeignKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseSqlModel

if TYPE_CHECKING:
    from .organization_rel_models import Organization
    from .research_plant_assoc_rel_models import ResearchPlantAssociation
    from .measurement_rel_models import MeasurementUnit


class BiochemAnalysis(BaseSqlModel):
    __tablename__ = "biochem_analyses"

    __table_args__ = (
        ForeignKeyConstraint(
            ["research_id", "plant_id"],
            [
                "research_plant_associations.research_id",
                "research_plant_associations.plant_id",
            ],
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date)  # type: ignore
    additional_info: Mapped[str] = mapped_column(String)
    research_id: Mapped[PyUUID] = mapped_column(UUID)
    plant_id: Mapped[PyUUID] = mapped_column(UUID)

    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id")
    )
    s3_key: Mapped[str] = mapped_column(String, unique=True)

    # rel
    # m2one
    research_plant_association: Mapped["ResearchPlantAssociation"] = relationship(
        back_populates="biochem_analysis_list"
    )
    organization: Mapped["Organization"] = relationship(
        back_populates="biochem_analysis_list"
    )

    # one2m
    biochem_analysis_feature_associations: Mapped[
        list["BiochemAnalysisFeatureAssociation"]
    ] = relationship(back_populates="biochem_analysis")


class BiochemFeature(BaseSqlModel):
    __tablename__ = "biochem_features"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    measurement_unit_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("measurement_units.id")
    )

    # rel
    # m2one
    measurement_unit: Mapped["MeasurementUnit"] = relationship(
        back_populates="biochem_features"
    )

    # one2m
    biochem_analysis_feature_associations: Mapped[
        list["BiochemAnalysisFeatureAssociation"]
    ] = relationship(back_populates="biochem_feature")


class BiochemAnalysisFeatureAssociation(BaseSqlModel):
    __tablename__ = "biochem_analysis_feature_associations"

    biochem_analysis_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("biochem_analyses.id"), primary_key=True
    )
    biochem_feature_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("biochem_features.id"), primary_key=True
    )
    value: Mapped[int] = mapped_column(Integer)

    # rel
    # m2one
    biochem_feature: Mapped["BiochemFeature"] = relationship(
        back_populates="biochem_analysis_feature_associations"
    )
    biochem_analysis: Mapped["BiochemAnalysis"] = relationship(
        back_populates="biochem_analysis_feature_associations"
    )
