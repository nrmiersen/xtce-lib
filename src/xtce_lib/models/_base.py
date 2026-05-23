"""Base classes for the unified XTCE model."""

from pydantic import BaseModel, ConfigDict


class XtceBaseModel(BaseModel):
    """Base model class for the unified XTCE model."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_assignment=True,
        from_attributes=True,
        extra="forbid",
    )
