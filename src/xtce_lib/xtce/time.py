"""Time models."""

import datetime
from typing import Any, Self, assert_never

from pydantic import Field, model_validator
from xsdata.models.datatype import XmlDate, XmlDateTime

from xtce_lib.common.validation import ValidationReport, XtceSemanticError
from xtce_lib.common.xtce_path import XtcePath
from xtce_lib.common.xtce_registry import XtceRegistry
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from ._util import unwrap
from .enum import EpochTime, TimeUnits
from .reference import ParameterInstanceRef


class TimeAssociation(ParameterInstanceRef):
    """Describes a time association between this element and a reference time.

    This allows for specifying which AbsoluteTimeParameter to use to time-stamp this
    element.

    """

    interpolate_time: bool = Field(default=True)
    """If `True`, then the current value of the AbsoluteTimeParameter will be projected
    to current time.

    For example, if the AbsoluteTimeParameter was received 10 seconds ago, then 10
    seconds will be added to the value before time-stamping this element.

    """

    offset: float | datetime.date | None = Field(default=None)
    """An optional offset to apply to the value of the AbsoluteTimeParameter before
    time-stamping this element.

    The offset is specified in units of the `unit` field.

    `datetime.date` is only supported by XTCE 1.1. XTCE 1.2 and later only support a
    `float` offset.

    """

    unit: TimeUnits = Field(default=TimeUnits.SECONDS)
    """The time units of the `offset` field."""

    def validate_semantics(
        self,
        report: ValidationReport[XtceSemanticError],
        registry: XtceRegistry,
        scope: XtcePath,
    ) -> None:
        """Validate this object's semantics.

        Rules:
            - The parameter type referenced by the Parameter must be a
                AbsoluteTimeParameter.

        """
        # Verify ref is exists and is a Parameter
        super().validate_semantics(report, registry, scope)

        # Verify Parameter.type_ref is a AbsoluteTimeParameter
        # TODO need parameter type classes to be defined before semantic validation can be implemented


class ReferenceTime(XtceBaseModel):
    """Represents the origin of a time type.

    Either an epoch or a reference time association can be used, but not both.

    """

    offset_from: ParameterInstanceRef | None = Field(default=None)
    """Used to specify that this time type is relative to a reference time
    association.
    """

    epoch: datetime.date | datetime.datetime | EpochTime | None = Field(
        default=None,
        examples=[
            datetime.date(2020, 1, 1),
            datetime.datetime(2020, 1, 1, 12, 0, 0),
            EpochTime.J2000,
        ],
    )
    """Used to specify that this time type is relative to an epoch.

    If using a `datetime.date`, the time is assumed to be 00:00:00.

    `datetime.datetime` is only supported by XTCE 1.2 and later.

    """

    @model_validator(mode="after")
    def validate_inputs(self) -> Self:
        """Validate that only one of `offset_from` and `epoch` is provided."""
        if self.offset_from is None and self.epoch is None:
            raise ValueError("one of 'offset_from' and 'epoch' must be provided")
        if self.offset_from is not None and self.epoch is not None:
            raise ValueError("only one of 'offset_from' and 'epoch' can be provided")
        return self

    def validate_semantics(
        self,
        report: ValidationReport[XtceSemanticError],
        registry: XtceRegistry,
        scope: XtcePath,
    ) -> None:
        """Validate this object's semantics.

        Rules:
            - If `offset_from` is provided:
                - The reference must exist.
                - The reference must be an instance of Parameter.
                - The parameter type referenced by the Parameter must be a
                    RelativeTimeParameter or AbsoluteTimeParameter.

        """
        if self.offset_from is not None:
            from .parameter import Parameter

            # Verify ref is exists and is a Parameter
            try:
                result = registry.resolve(self.offset_from.ref, scope)
                if not isinstance(result.target, Parameter):
                    report.add_error(
                        XtceSemanticError(
                            scope=scope,
                            message=f"reference '{self.offset_from.ref}' resolved to a "
                            f"'{type(result.target).__name__}' type, "
                            f"but a 'Parameter' type was expected",
                        )
                    )

            except KeyError:
                report.add_error(
                    XtceSemanticError(
                        scope=scope,
                        message=f"reference '{self.offset_from.ref}' does not resolve "
                        f"to a valid object from scope '{scope}'",
                    )
                )

            # Verify Parameter.type_ref is a RelativeTimeParameter or
            # AbsoluteTimeParameter
            # TODO need parameter type classes to be defined before semantic validation can be implemented

    @classmethod
    def _from_v1_1(cls: type[Self], reference_time: xtce_1_1.ReferenceTimeType) -> Self:

        def unpack_epoch(
            reference_time: xtce_1_1.ReferenceTimeType,
        ) -> datetime.date | EpochTime | None:
            match reference_time.offset_from_or_epoch:
                case XmlDate():
                    return reference_time.offset_from_or_epoch.to_date()
                case xtce_1_1.EpochTypeValue():
                    return EpochTime(reference_time.offset_from_or_epoch.value)
                case xtce_1_1.ParameterInstanceRefType():
                    return None
                case None:
                    raise ValueError(
                        "invalid XTCE XML: missing a value for OffsetFrom and Epoch"
                    )
                case _:
                    assert_never(reference_time.offset_from_or_epoch)

        return cls(
            offset_from=(
                ParameterInstanceRef.from_xsdata(
                    reference_time.offset_from_or_epoch, XtceVersion.V1_1
                )
                if isinstance(
                    reference_time.offset_from_or_epoch,
                    xtce_1_1.ParameterInstanceRefType,
                )
                else None
            ),
            epoch=unpack_epoch(reference_time),
        )

    @classmethod
    def _from_v1_2(cls: type[Self], reference_time: xtce_1_2.ReferenceTimeType) -> Self:

        def unpack_epoch(
            reference_time: xtce_1_2.ReferenceTimeType,
        ) -> datetime.date | datetime.datetime | EpochTime | None:
            match reference_time.offset_from_or_epoch:
                case XmlDate():
                    return reference_time.offset_from_or_epoch.to_date()
                case XmlDateTime():
                    return reference_time.offset_from_or_epoch.to_datetime()
                case xtce_1_2.EpochTimeEnumsType():
                    return EpochTime(reference_time.offset_from_or_epoch.value)
                case xtce_1_2.ParameterInstanceRefType():
                    return None
                case None:
                    raise ValueError(
                        "invalid XTCE XML: missing a value for OffsetFrom and Epoch"
                    )
                case _:
                    assert_never(reference_time.offset_from_or_epoch)

        return cls(
            offset_from=(
                ParameterInstanceRef.from_xsdata(
                    reference_time.offset_from_or_epoch, XtceVersion.V1_2
                )
                if isinstance(
                    reference_time.offset_from_or_epoch,
                    xtce_1_2.ParameterInstanceRefType,
                )
                else None
            ),
            epoch=unpack_epoch(reference_time),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], reference_time: xtce_1_3.ReferenceTimeType) -> Self:

        def unpack_epoch(
            reference_time: xtce_1_3.ReferenceTimeType,
        ) -> datetime.date | datetime.datetime | EpochTime | None:
            match reference_time.offset_from_or_epoch:
                case XmlDate():
                    return reference_time.offset_from_or_epoch.to_date()
                case XmlDateTime():
                    return reference_time.offset_from_or_epoch.to_datetime()
                case xtce_1_3.EpochTimeEnumsType():
                    return EpochTime(reference_time.offset_from_or_epoch.value)
                case xtce_1_3.ParameterInstanceRefType():
                    return None
                case None:
                    raise ValueError(
                        "invalid XTCE XML: missing a value for OffsetFrom and Epoch"
                    )
                case _:
                    assert_never(reference_time.offset_from_or_epoch)

        return cls(
            offset_from=(
                ParameterInstanceRef.from_xsdata(
                    reference_time.offset_from_or_epoch, XtceVersion.V1_3
                )
                if isinstance(
                    reference_time.offset_from_or_epoch,
                    xtce_1_3.ParameterInstanceRefType,
                )
                else None
            ),
            epoch=unpack_epoch(reference_time),
        )

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create a ReferenceTime from an xsdata-generated
        ReferenceTimeType object of any version.
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

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.ReferenceTimeType:
        version = XtceVersion.V1_1

        self._enforce_restricted_type(
            field_name="epoch",
            current_type=type(self.epoch),
            allowed_types=(datetime.date, EpochTime),
            target_version=version,
            policy=policy,
        )

        def pack_epoch(
            epoch: datetime.date | datetime.datetime | EpochTime | None,
        ) -> XmlDate | xtce_1_1.EpochTypeValue:
            match epoch:
                case datetime.datetime():
                    # If this is used, an exception/warning may be raised above
                    # depending on the downgrade policy. If DowngradePolicy.IGNORE is
                    # used, just the time portion will be dropped.
                    return XmlDate.from_datetime(epoch)
                case datetime.date():
                    return XmlDate.from_date(epoch)
                case EpochTime():
                    return xtce_1_1.EpochTypeValue(epoch.value)
                case None:
                    raise ValueError()
                case _:
                    assert_never(epoch)

        return xtce_1_1.ReferenceTimeType(
            offset_from_or_epoch=pack_epoch(self.epoch)
            if self.epoch is not None
            else unwrap(self.offset_from)._to_v1_1(policy)
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ReferenceTimeType:
        def pack_epoch(
            epoch: datetime.date | datetime.datetime | EpochTime | None,
        ) -> XmlDate | XmlDateTime | xtce_1_2.EpochTimeEnumsType:
            match epoch:
                case datetime.datetime():
                    return XmlDateTime.from_datetime(epoch)
                case datetime.date():
                    return XmlDate.from_date(epoch)
                case EpochTime():
                    return xtce_1_2.EpochTimeEnumsType(epoch.value)
                case None:
                    raise ValueError()
                case _:
                    assert_never(epoch)

        return xtce_1_2.ReferenceTimeType(
            offset_from_or_epoch=pack_epoch(self.epoch)
            if self.epoch is not None
            else unwrap(self.offset_from)._to_v1_2(policy)
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ReferenceTimeType:
        def pack_epoch(
            epoch: datetime.date | datetime.datetime | EpochTime | None,
        ) -> XmlDate | XmlDateTime | xtce_1_3.EpochTimeEnumsType:
            match epoch:
                case datetime.datetime():
                    return XmlDateTime.from_datetime(epoch)
                case datetime.date():
                    return XmlDate.from_date(epoch)
                case EpochTime():
                    return xtce_1_3.EpochTimeEnumsType(epoch.value)
                case None:
                    raise ValueError()
                case _:
                    assert_never(epoch)

        return xtce_1_3.ReferenceTimeType(
            offset_from_or_epoch=pack_epoch(self.epoch)
            if self.epoch is not None
            else unwrap(self.offset_from)._to_v1_3(policy)
        )

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> (
        xtce_1_1.ReferenceTimeType
        | xtce_1_2.ReferenceTimeType
        | xtce_1_3.ReferenceTimeType
    ):
        """Convert this ReferenceTime to an xsdata-generated ReferenceTimeType object of
        the specified version.
        """
        match version:
            case XtceVersion.V1_1:
                return self._to_v1_1(policy)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)
