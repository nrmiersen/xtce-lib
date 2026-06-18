"""Base classes for the unified XTCE model."""

import logging
from abc import ABC
from typing import Any, Self

from pydantic import BaseModel, ConfigDict

from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy, XtceDowngradeError

log = logging.getLogger(__name__)


class XtceBaseModel(BaseModel, ABC):
    """Base model class for the unified XTCE model."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_assignment=True,
        from_attributes=True,
        extra="forbid",
    )

    def validate_semantics(self) -> None:
        """Validate the semantic validity of the model.

        This method should be overridden by subclasses.

        """
        # TODO add logic here for passing around the error list
        pass

    def _handle_downgrade(self, message: str, policy: DowngradePolicy) -> None:
        """Handle downgrade reporting according to the specified policy."""
        match policy:
            case DowngradePolicy.STRICT:
                log.error(message)
                raise XtceDowngradeError(message)
            case DowngradePolicy.WARN:
                log.warning(message)
            case DowngradePolicy.IGNORE:
                pass

    def _enforce_unsupported_field(
        self,
        field_name: str,
        current_value: Any,
        empty_value: Any,
        target_version: XtceVersion,
        policy: DowngradePolicy,
    ) -> None:
        """Enforce when a field does not exist in the target version."""
        if current_value == empty_value:
            return

        message = (
            f"Data Loss Warning: The attribute '{field_name}' with value "
            f"'{current_value}' is not supported in XTCE version "
            f"{target_version.value} and will be lost during export."
        )
        self._handle_downgrade(message, policy)

    def _enforce_restricted_value(
        self,
        field_name: str,
        current_value: Any,
        allowed_values: set[Any],
        target_version: XtceVersion,
        policy: DowngradePolicy,
    ) -> None:
        """Enforce when a field's value is not allowed in the target version."""
        if current_value in allowed_values:
            return

        message = (
            f"Incompatible Value Warning: The attribute '{field_name}' has value "
            f"'{current_value}' which is not allowed in XTCE version "
            f"{target_version.value} and will be lost during export."
        )
        self._handle_downgrade(message, policy)

    @classmethod
    # @abstractmethod
    def from_xsdata(cls, raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create an XtceBaseModel from an xsdata-generated object of
        any version.
        """
        pass

    # @abstractmethod
    def to_xsdata(self, version: XtceVersion) -> Any:
        """Convert this XtceBaseModel to an xsdata-generated object of the specified
        version.
        """
        pass
