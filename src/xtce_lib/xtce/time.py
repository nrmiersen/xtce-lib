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
from .enum import EpochTime, TimeAssociationUnits
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

    unit: TimeAssociationUnits = Field(default=TimeAssociationUnits.SECONDS)
    """The time units of the `offset` field.

    Applicable since: XTCE 1.2. If using XTCE 1.1, the `offset` field is
    assumed to be in seconds.

    """

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

    _v1_1_type = xtce_1_1.TimeAssociationType
    _v1_2_type = xtce_1_2.TimeAssociationType
    _v1_3_type = xtce_1_3.TimeAssociationType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.TimeAssociationType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["interpolate_time"] = obj.interpolate_time
        kwargs["offset"] = obj.offset.to_date() if obj.offset is not None else None
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.TimeAssociationType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["interpolate_time"] = obj.interpolate_time
        kwargs["offset"] = obj.offset
        kwargs["unit"] = TimeAssociationUnits._from_v1_2(obj.unit)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.TimeAssociationType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["interpolate_time"] = obj.interpolate_time
        kwargs["offset"] = obj.offset
        kwargs["unit"] = TimeAssociationUnits._from_v1_3(obj.unit)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        version = XtceVersion.V1_1

        self._enforce_unsupported_field(
            field_name="unit",
            current_value=self.unit,
            empty_value=TimeAssociationUnits.SECONDS,
            target_version=version,
            policy=policy,
        )
        offset = (
            self._enforce_restricted_type(
                field_name="offset",
                current_value=self.offset,
                allowed_types=(datetime.date,),
                target_version=version,
                policy=policy,
                require_match=True,
            )
            if self.offset is not None
            else None
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["interpolate_time"] = self.interpolate_time
        kwargs["offset"] = XmlDate.from_date(offset) if offset is not None else None
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        offset = (
            self._enforce_restricted_type(
                field_name="offset",
                current_value=self.offset,
                allowed_types=(float,),
                target_version=XtceVersion.V1_2,
                policy=policy,
                require_match=True,
            )
            if self.offset is not None
            else None
        )

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["interpolate_time"] = self.interpolate_time
        kwargs["offset"] = offset
        kwargs["unit"] = self.unit._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        offset = (
            self._enforce_restricted_type(
                field_name="offset",
                current_value=self.offset,
                allowed_types=(float,),
                target_version=XtceVersion.V1_3,
                policy=policy,
                require_match=True,
            )
            if self.offset is not None
            else None
        )

        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["interpolate_time"] = self.interpolate_time
        kwargs["offset"] = offset
        kwargs["unit"] = self.unit._to_v1_3(policy)
        return kwargs


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

    _v1_1_type = xtce_1_1.ReferenceTimeType
    _v1_2_type = xtce_1_2.ReferenceTimeType
    _v1_3_type = xtce_1_3.ReferenceTimeType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.ReferenceTimeType) -> dict[str, Any]:
        def unpack_epoch(
            reference_time: xtce_1_1.ReferenceTimeType,
        ) -> datetime.date | EpochTime | None:
            match reference_time.choice:
                case XmlDate():
                    return reference_time.choice.to_date()
                case xtce_1_1.EpochTypeValue():
                    return EpochTime(reference_time.choice.value)
                case xtce_1_1.ParameterInstanceRefType():
                    return None
                case None:
                    raise ValueError(
                        "invalid XTCE XML: missing a value for OffsetFrom and Epoch"
                    )
                case _:
                    assert_never(reference_time.choice)

        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["offset_from"] = (
            ParameterInstanceRef.from_xsdata(obj.choice, XtceVersion.V1_1)
            if isinstance(obj.choice, xtce_1_1.ParameterInstanceRefType)
            else None
        )
        kwargs["epoch"] = unpack_epoch(obj)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ReferenceTimeType) -> dict[str, Any]:
        def unpack_epoch(
            reference_time: xtce_1_2.ReferenceTimeType,
        ) -> datetime.date | datetime.datetime | EpochTime | None:
            match reference_time.choice:
                case XmlDate():
                    return reference_time.choice.to_date()
                case XmlDateTime():
                    return reference_time.choice.to_datetime()
                case xtce_1_2.EpochTimeEnumsType():
                    return EpochTime(reference_time.choice.value)
                case xtce_1_2.ParameterInstanceRefType():
                    return None
                case None:
                    raise ValueError(
                        "invalid XTCE XML: missing a value for OffsetFrom and Epoch"
                    )
                case _:
                    assert_never(reference_time.choice)

        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["offset_from"] = (
            ParameterInstanceRef.from_xsdata(obj.choice, XtceVersion.V1_2)
            if isinstance(obj.choice, xtce_1_2.ParameterInstanceRefType)
            else None
        )
        kwargs["epoch"] = unpack_epoch(obj)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ReferenceTimeType) -> dict[str, Any]:
        def unpack_epoch(
            reference_time: xtce_1_3.ReferenceTimeType,
        ) -> datetime.date | datetime.datetime | EpochTime | None:
            match reference_time.choice:
                case XmlDate():
                    return reference_time.choice.to_date()
                case XmlDateTime():
                    return reference_time.choice.to_datetime()
                case xtce_1_3.EpochTimeEnumsType():
                    return EpochTime(reference_time.choice.value)
                case xtce_1_3.ParameterInstanceRefType():
                    return None
                case None:
                    raise ValueError(
                        "invalid XTCE XML: missing a value for OffsetFrom and Epoch"
                    )
                case _:
                    assert_never(reference_time.choice)

        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["offset_from"] = (
            ParameterInstanceRef.from_xsdata(obj.choice, XtceVersion.V1_3)
            if isinstance(obj.choice, xtce_1_3.ParameterInstanceRefType)
            else None
        )
        kwargs["epoch"] = unpack_epoch(obj)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        if self.epoch is not None:
            self._enforce_restricted_type(
                field_name="epoch",
                current_value=self.epoch,
                allowed_types=(datetime.date, EpochTime),
                target_version=XtceVersion.V1_1,
                policy=policy,
                require_match=True,
            )

        def pack_epoch(
            epoch: datetime.date | datetime.datetime | EpochTime,
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
                case _:
                    assert_never(epoch)

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["choice"] = (
            pack_epoch(self.epoch)
            if self.epoch is not None
            else unwrap(self.offset_from)._to_v1_1(policy)
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        def pack_epoch(
            epoch: datetime.date | datetime.datetime | EpochTime,
        ) -> XmlDate | XmlDateTime | xtce_1_2.EpochTimeEnumsType:
            match epoch:
                case datetime.datetime():
                    return XmlDateTime.from_datetime(epoch)
                case datetime.date():
                    return XmlDate.from_date(epoch)
                case EpochTime():
                    return xtce_1_2.EpochTimeEnumsType(epoch.value)
                case _:
                    assert_never(epoch)

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = (
            pack_epoch(self.epoch)
            if self.epoch is not None
            else unwrap(self.offset_from)._to_v1_2(policy)
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        def pack_epoch(
            epoch: datetime.date | datetime.datetime | EpochTime,
        ) -> XmlDate | XmlDateTime | xtce_1_3.EpochTimeEnumsType:
            match epoch:
                case datetime.datetime():
                    return XmlDateTime.from_datetime(epoch)
                case datetime.date():
                    return XmlDate.from_date(epoch)
                case EpochTime():
                    return xtce_1_3.EpochTimeEnumsType(epoch.value)
                case _:
                    assert_never(epoch)

        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = (
            pack_epoch(self.epoch)
            if self.epoch is not None
            else unwrap(self.offset_from)._to_v1_3(policy)
        )
        return kwargs
