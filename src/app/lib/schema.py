"""NIAPI Schema."""

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict

from app.utils import camel_case

__all__ = ["BaseModel", "CamelizedBaseModel"]


class BaseModel(_BaseModel):
    """Base Settings."""

    model_config = ConfigDict(
        validate_assignment=True,
        from_attributes=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
    )


class CamelizedBaseModel(BaseModel):
    """Camelized Base pydantic schema."""

    model_config = ConfigDict(populate_by_name=True, alias_generator=camel_case)
