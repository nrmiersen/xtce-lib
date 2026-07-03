"""Time models."""

import datetime
from typing import Self, assert_never

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

    Only supported by XTCE 1.2 and later. If using XTCE 1.1, the `offset` field is
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

    @classmethod
    def _from_v1_1(
        cls: type[Self], time_association: xtce_1_1.TimeAssociationType
    ) -> Self:
        return cls(
            ref=XtcePath(time_association.parameter_ref),
            instance=time_association.instance,
            use_calibrated_value=time_association.use_calibrated_value,
            interpolate_time=time_association.interpolate_time,
            offset=time_association.offset.to_date()
            if time_association.offset is not None
            else None,
        )

    @classmethod
    def _from_v1_2(
        cls: type[Self], time_association: xtce_1_2.TimeAssociationType
    ) -> Self:
        return cls(
            ref=XtcePath(time_association.parameter_ref),
            instance=time_association.instance,
            use_calibrated_value=time_association.use_calibrated_value,
            interpolate_time=time_association.interpolate_time,
            offset=time_association.offset,
            unit=TimeAssociationUnits._from_v1_2(time_association.unit),
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], time_association: xtce_1_3.TimeAssociationType
    ) -> Self:
        return cls(
            ref=XtcePath(time_association.parameter_ref),
            instance=time_association.instance,
            use_calibrated_value=time_association.use_calibrated_value,
            interpolate_time=time_association.interpolate_time,
            offset=time_association.offset,
            unit=TimeAssociationUnits._from_v1_3(time_association.unit),
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.TimeAssociationType:
        version = XtceVersion.V1_1

        self._enforce_unsupported_field(
            field_name="unit",
            current_value=self.unit,
            empty_value=TimeAssociationUnits.SECONDS,
            target_version=version,
            policy=policy,
        )
        offset = self._enforce_restricted_type(
            field_name="offset",
            current_value=self.offset,
            allowed_types=(datetime.date,),
            target_version=version,
            policy=policy,
            require_match=True,
        )

        return xtce_1_1.TimeAssociationType(
            parameter_ref=str(self.ref),
            instance=self.instance,
            use_calibrated_value=self.use_calibrated_value,
            interpolate_time=self.interpolate_time,
            offset=XmlDate.from_date(offset),
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.TimeAssociationType:
        offset = self._enforce_restricted_type(
            field_name="offset",
            current_value=self.offset,
            allowed_types=(float,),
            target_version=XtceVersion.V1_2,
            policy=policy,
            require_match=True,
        )

        return xtce_1_2.TimeAssociationType(
            parameter_ref=str(self.ref),
            instance=self.instance,
            use_calibrated_value=self.use_calibrated_value,
            interpolate_time=self.interpolate_time,
            offset=offset,
            unit=self.unit._to_v1_2(policy),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.TimeAssociationType:
        offset = self._enforce_restricted_type(
            field_name="offset",
            current_value=self.offset,
            allowed_types=(float,),
            target_version=XtceVersion.V1_3,
            policy=policy,
            require_match=True,
        )

        return xtce_1_3.TimeAssociationType(
            parameter_ref=str(self.ref),
            instance=self.instance,
            use_calibrated_value=self.use_calibrated_value,
            interpolate_time=self.interpolate_time,
            offset=offset,
            unit=self.unit._to_v1_3(policy),
        )


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

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.ReferenceTimeType:
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

        return xtce_1_1.ReferenceTimeType(
            offset_from_or_epoch=pack_epoch(self.epoch)
            if self.epoch is not None
            else unwrap(self.offset_from)._to_v1_1(policy)
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ReferenceTimeType:
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

        return xtce_1_2.ReferenceTimeType(
            offset_from_or_epoch=pack_epoch(self.epoch)
            if self.epoch is not None
            else unwrap(self.offset_from)._to_v1_2(policy)
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ReferenceTimeType:
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

        return xtce_1_3.ReferenceTimeType(
            offset_from_or_epoch=pack_epoch(self.epoch)
            if self.epoch is not None
            else unwrap(self.offset_from)._to_v1_3(policy)
        )
