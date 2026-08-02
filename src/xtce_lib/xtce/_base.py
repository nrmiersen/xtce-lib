"""Base classes for the unified XTCE model."""

from __future__ import annotations

import logging
from abc import ABC
from enum import Enum
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Literal,
    Self,
    TypeVar,
    assert_never,
    overload,
)

from pydantic import BaseModel, ConfigDict

from xtce_lib.common.validation import ValidationReport, XtceSemanticError
from xtce_lib.common.xtce_path import XtcePath
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import (
    DowngradePolicy,
    XtceDowngradeError,
    XtceUnsupportedError,
)

if TYPE_CHECKING:
    from xtce_lib.common.xtce_registry import XtceRegistry


log = logging.getLogger(__name__)
T = TypeVar("T")


class XtceBaseModel(BaseModel, ABC):
    """Base model class for the unified XTCE model."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_assignment=True,
        from_attributes=True,
        extra="forbid",
    )

    _v1_1_type: ClassVar[type | None] = None
    _v1_2_type: ClassVar[type | None] = None
    _v1_3_type: ClassVar[type | None] = None

    def validate_semantics(
        self,
        report: ValidationReport[XtceSemanticError],
        registry: XtceRegistry,
        scope: XtcePath,
    ) -> None:
        """Validate this object's semantics."""
        pass

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create this model from an xsdata-generated object of any
        version.
        """
        match version:
            case XtceVersion.V1_1:
                return cls._from_v1_1(raw_obj)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> Any:
        """Convert this model to the xsdata equivalent."""
        match version:
            case XtceVersion.V1_1:
                return self._to_v1_1(policy)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)

    @classmethod
    def _from_v1_1_kwargs(cls: type[Self], obj: Any) -> dict[str, Any]:
        return {}

    @classmethod
    def _from_v1_2_kwargs(cls: type[Self], obj: Any) -> dict[str, Any]:
        return {}

    @classmethod
    def _from_v1_3_kwargs(cls: type[Self], obj: Any) -> dict[str, Any]:
        return {}

    @classmethod
    def _from_v1_1(cls: type[Self], obj: Any) -> Self:
        if cls._v1_1_type is None:
            raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)
        kwargs = cls._from_v1_1_kwargs(obj)
        return cls(**kwargs)

    @classmethod
    def _from_v1_2(cls: type[Self], obj: Any) -> Self:
        if cls._v1_2_type is None:
            raise XtceUnsupportedError(XtceVersion.V1_2, cls.__name__)
        kwargs = cls._from_v1_2_kwargs(obj)
        return cls(**kwargs)

    @classmethod
    def _from_v1_3(cls: type[Self], obj: Any) -> Self:
        if cls._v1_3_type is None:
            raise XtceUnsupportedError(XtceVersion.V1_3, cls.__name__)
        kwargs = cls._from_v1_3_kwargs(obj)
        return cls(**kwargs)

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        return {}

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        return {}

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        return {}

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        target_class = self._v1_1_type
        if target_class is None:
            raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)
        return target_class(**self._to_v1_1_kwargs(policy))

    def _to_v1_2(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        target_class = self._v1_2_type
        if target_class is None:
            raise XtceUnsupportedError(XtceVersion.V1_2, self.__class__.__name__)
        return target_class(**self._to_v1_2_kwargs(policy))

    def _to_v1_3(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        target_class = self._v1_3_type
        if target_class is None:
            raise XtceUnsupportedError(XtceVersion.V1_3, self.__class__.__name__)
        return target_class(**self._to_v1_3_kwargs(policy))

    @staticmethod
    def _handle_downgrade(message: str, policy: DowngradePolicy) -> None:
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
        target_version: XtceVersion,
        policy: DowngradePolicy,
        *,
        empty_value: Any = None,
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

    def _enforce_required_field(
        self,
        field_name: str,
        current_value: Any,
        target_version: XtceVersion,
        policy: DowngradePolicy,
        *,
        empty_value: Any = None,
        fallback: Any = None,
    ) -> Any:
        """Enforce when a field is required in the target version but is currently
        empty.
        """
        if current_value != empty_value:
            return current_value

        message = (
            f"Missing Required Field: The attribute '{field_name}' is required in "
            f"XTCE version {target_version.value} but is currently unset."
        )

        # If there is a fallback, can be treated normally
        if fallback is not None:
            self._handle_downgrade(message + f" Using fallback '{fallback}'.", policy)
            return fallback

        # If there is no fallback, this is an actual error
        log.error(message)
        raise ValueError(message)

    def _enforce_list_length(
        self,
        field_name: str,
        current_value: list[Any] | None,
        min_length: int,
        max_length: int,
        target_version: XtceVersion,
        policy: DowngradePolicy,
        *,
        fallback: Any,
    ) -> Any:
        """Enforce when a list field's length is not allowed in the target version."""
        if current_value is None or min_length <= len(current_value) <= max_length:
            return current_value

        message = (
            f"Incompatible List Length: The attribute '{field_name}' has length "
            f"{len(current_value)} which is not allowed in XTCE version "
            f"{target_version.value}."
        )

        # If there is a fallback, can be treated normally
        if fallback is not None:
            self._handle_downgrade(message + f" Using fallback '{fallback}'.", policy)
            return fallback

        # If there is no fallback, this is an actual error
        log.error(message)
        raise ValueError(message)

    @overload
    def _enforce_restricted_type(
        self,
        field_name: str,
        current_value: Any,
        allowed_types: tuple[type[T], ...],
        target_version: XtceVersion,
        policy: DowngradePolicy,
        *,
        require_match: Literal[True],
    ) -> T: ...

    @overload
    def _enforce_restricted_type(
        self,
        field_name: str,
        current_value: Any,
        allowed_types: tuple[type[Any], ...],
        target_version: XtceVersion,
        policy: DowngradePolicy,
        *,
        require_match: Literal[False] = False,
    ) -> Any: ...

    def _enforce_restricted_type(
        self,
        field_name: str,
        current_value: Any,
        allowed_types: tuple[type[Any], ...],
        target_version: XtceVersion,
        policy: DowngradePolicy,
        *,
        require_match: bool = False,
    ) -> Any:
        """Enforce when a field's type is not allowed in the target version."""
        if isinstance(current_value, allowed_types):
            return current_value

        message = (
            f"Incompatible Type Warning: The attribute '{field_name}' has type "
            f"'{type(current_value)}' which is not allowed in XTCE version "
            f"{target_version.value} and will be lost during export."
        )
        self._handle_downgrade(message, policy)

        if require_match:
            raise TypeError(
                f"attribute '{field_name}' must be one of {allowed_types}, "
                f"got {type(current_value)}"
            )

        return current_value


class XtceBaseEnum(str, Enum):
    """Base class for unified XTCE enumerations."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_2, cls.__name__)

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_3, cls.__name__)

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_2, self.__class__.__name__)

    def _to_v1_3(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_3, self.__class__.__name__)

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create this model from an xsdata-generated object of any
        version.
        """
        match version:
            case XtceVersion.V1_1:
                return cls._from_v1_1(raw_obj)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> Any:
        """Convert this model to the xsdata equivalent."""
        match version:
            case XtceVersion.V1_1:
                return self._to_v1_1(policy)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)

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

    def _enforce_unmapped_value(
        self,
        target_version: XtceVersion,
        policy: DowngradePolicy,
        fallback: Any = None,
    ) -> Any:
        """Handle an enum value that does not exist in the target XTCE version."""
        message = (
            f"Incompatible Value Warning: The enum value '{self.name}' in "
            f"{self.__class__.__name__} does not exist in XTCE version "
            f"{target_version.value.version} and will be lost during export."
        )
        self._handle_downgrade(message, policy)

        return fallback
