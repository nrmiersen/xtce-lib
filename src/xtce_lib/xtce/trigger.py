"""Trigger models."""

from __future__ import annotations

from abc import ABC
from decimal import Decimal
from typing import TYPE_CHECKING, Annotated, Any

from pydantic import AfterValidator, Field

from xtce_lib.common.validation import ValidationReport, XtceSemanticError
from xtce_lib.common.xtce_path import XtcePath, require_regex
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from ._pattern import EXPD_NAME_REF_W_PATH, NAME_REF_W_PATH

if TYPE_CHECKING:
    from xtce_lib.common.xtce_registry import XtceRegistry


class BaseTrigger(XtceBaseModel, ABC):
    """Base class for triggers."""


class OnParameterUpdateTrigger(BaseTrigger):
    """A reference to a parameter that triggers an event when the telemetry parameter is
    updated with a new value.
    """

    ref: Annotated[XtcePath, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))] = (
        Field(
            ...,
            examples=[
                "/ConkSat/Bus/BatteryVoltage",
                "../Bus/BatteryVoltage",
                "../Payload/Camera/ExposureTime",
            ],
            json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
        )
    )
    """A Unix-like path to a parameter.

    Reference to the parameter whose update triggers this algorithm to evaluate.

    Can only reference parameters, cannot reference array elements or aggregate members.

    """

    def validate_semantics(
        self,
        report: ValidationReport[XtceSemanticError],
        registry: XtceRegistry,
        scope: XtcePath,
    ) -> None:
        """Validate this object's semantics.

        Rules:
            - The reference must not contain an array index or aggregate member.
            - The reference must exist.
            - The reference must be an instance of Parameter.

        """
        if self.ref.contains_array or self.ref.contains_aggregate:
            report.add_error(
                XtceSemanticError(
                    scope=scope,
                    message=f"reference '{self.ref}' contains an array index or "
                    "aggregate member, but a standalone ParameterRef must reference a "
                    "parameter only",
                )
            )

        from .parameter import Parameter

        try:
            result = registry.resolve(self.ref, scope)
            if not isinstance(result.target, Parameter):
                report.add_error(
                    XtceSemanticError(
                        scope=scope,
                        message=f"reference '{self.ref}' resolved to a "
                        f"'{type(result.target).__name__}' type, "
                        f"but a 'Parameter' type was expected",
                    )
                )

        except KeyError:
            report.add_error(
                XtceSemanticError(
                    scope=scope,
                    message=f"reference '{self.ref}' does not resolve to a valid object "
                    f"from scope '{scope}'",
                )
            )

    _v1_1_type = xtce_1_1.TriggerSetType.OnParameterUpdateTrigger
    _v1_2_type = xtce_1_2.OnParameterUpdateTriggerType
    _v1_3_type = xtce_1_3.OnParameterUpdateTriggerType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.TriggerSetType.OnParameterUpdateTrigger
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.parameter_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.OnParameterUpdateTriggerType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.parameter_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.OnParameterUpdateTriggerType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.parameter_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["parameter_ref"] = str(self.ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["parameter_ref"] = str(self.ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["parameter_ref"] = str(self.ref)
        return kwargs


class OnContainerUpdateTrigger(BaseTrigger):
    """A reference to a container that triggers an event when the container is updated
    with a new value.
    """

    ref: Annotated[XtcePath, AfterValidator(require_regex(NAME_REF_W_PATH))] = Field(
        ...,
        examples=[
            "/Telemetry/Power/PowerStatus",
            "../Thermal/ThermalStatus",
            "Command/ExecutionReport",
        ],
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to a sequence container.

    Reference to the container whose update/receipt triggers this algorithm to evaluate.

    """

    def validate_semantics(
        self,
        report: ValidationReport[XtceSemanticError],
        registry: XtceRegistry,
        scope: XtcePath,
    ) -> None:
        """Validate this object's semantics.

        Rules:
            - The reference must not contain an array index or aggregate member.
            - The reference must exist.
            - The reference must be an instance of SequenceContainer.

        """
        if self.ref.contains_array or self.ref.contains_aggregate:
            report.add_error(
                XtceSemanticError(
                    scope=scope,
                    message=f"reference '{self.ref}' contains an array index or "
                    "aggregate member, but a ContainerRef must reference a sequence "
                    "container only",
                )
            )

        from .container import SequenceContainer

        try:
            result = registry.resolve(self.ref, scope)
            if not isinstance(result.target, SequenceContainer):
                report.add_error(
                    XtceSemanticError(
                        scope=scope,
                        message=f"reference '{self.ref}' resolved to a "
                        f"'{type(result.target).__name__}' type, "
                        f"but a 'SequenceContainer' type was expected",
                    )
                )

        except KeyError:
            report.add_error(
                XtceSemanticError(
                    scope=scope,
                    message=f"reference '{self.ref}' does not resolve to a valid "
                    f"object from scope '{scope}'",
                )
            )

    _v1_1_type = xtce_1_1.TriggerSetType.OnContainerUpdateTrigger
    _v1_2_type = xtce_1_2.OnContainerUpdateTriggerType
    _v1_3_type = xtce_1_3.OnContainerUpdateTriggerType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.TriggerSetType.OnContainerUpdateTrigger
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.container_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.OnContainerUpdateTriggerType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.container_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.OnContainerUpdateTriggerType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["ref"] = XtcePath(obj.container_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["container_ref"] = str(self.ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["container_ref"] = str(self.ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["container_ref"] = str(self.ref)
        return kwargs


class OnPeriodicRateTrigger(BaseTrigger):
    """A periodic time basis to trigger an event."""

    fire_rate_sec: float = Field(..., ge=0)
    """The periodic rate in time in which this algorithm is triggered to evaluate."""

    _v1_1_type = xtce_1_1.TriggerSetType.OnPeriodicRateTrigger
    _v1_2_type = xtce_1_2.OnPeriodicRateTriggerType
    _v1_3_type = xtce_1_3.OnPeriodicRateTriggerType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.TriggerSetType.OnPeriodicRateTrigger
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["fire_rate_sec"] = int(obj.fire_rate_in_seconds)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.OnPeriodicRateTriggerType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["fire_rate_sec"] = obj.fire_rate_in_seconds
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.OnPeriodicRateTriggerType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["fire_rate_sec"] = obj.fire_rate_in_seconds
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["fire_rate_in_seconds"] = Decimal(self.fire_rate_sec)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["fire_rate_in_seconds"] = self.fire_rate_sec
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["fire_rate_in_seconds"] = self.fire_rate_sec
        return kwargs


class TriggerSet(XtceBaseModel):
    """A set of triggers that are used to initiate the processing of an algorithm.

    A trigger may be based on an update of a parameter, receipt of a container, or on a
    time basis. Triggers may also have a maximum rate that limits how often the trigger
    can be invoked.

    """

    triggers: list[
        OnParameterUpdateTrigger | OnContainerUpdateTrigger | OnPeriodicRateTrigger
    ] = Field(default_factory=list)
    """The list of triggers that can initiate the processing of an algorithm."""

    name: str | None = Field(default=None)
    """The optional name of this trigger set."""

    trigger_rate: int = Field(default=1, ge=0)
    """The maximum rate at which the triggers in this set can be invoked.

    Default is once per second. Setting to 0 means no limit.

    """

    def validate_semantics(
        self,
        report: ValidationReport[XtceSemanticError],
        registry: XtceRegistry,
        scope: XtcePath,
    ) -> None:
        """Validate this object's semantics.

        Rules:
            - All triggers in the set must be semantically valid.

        """
        for trigger in self.triggers:
            trigger.validate_semantics(report, registry, scope)

    _v1_1_type = xtce_1_1.TriggerSetType
    _v1_2_type = xtce_1_2.TriggerSetType
    _v1_3_type = xtce_1_3.TriggerSetType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.TriggerSetType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["triggers"] = [
            OnParameterUpdateTrigger._from_v1_1(trigger)
            if isinstance(trigger, xtce_1_1.TriggerSetType.OnParameterUpdateTrigger)
            else OnContainerUpdateTrigger._from_v1_1(trigger)
            if isinstance(trigger, xtce_1_1.TriggerSetType.OnContainerUpdateTrigger)
            else OnPeriodicRateTrigger._from_v1_1(trigger)
            for trigger in obj.choice
        ]
        kwargs["name"] = obj.name
        kwargs["trigger_rate"] = obj.trigger_rate
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.TriggerSetType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["triggers"] = [
            OnParameterUpdateTrigger._from_v1_2(trigger)
            if isinstance(trigger, xtce_1_2.OnParameterUpdateTriggerType)
            else OnContainerUpdateTrigger._from_v1_2(trigger)
            if isinstance(trigger, xtce_1_2.OnContainerUpdateTriggerType)
            else OnPeriodicRateTrigger._from_v1_2(trigger)
            for trigger in obj.choice
        ]
        kwargs["name"] = obj.name
        kwargs["trigger_rate"] = obj.trigger_rate
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.TriggerSetType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["triggers"] = [
            OnParameterUpdateTrigger._from_v1_3(trigger)
            if isinstance(trigger, xtce_1_3.OnParameterUpdateTriggerType)
            else OnContainerUpdateTrigger._from_v1_3(trigger)
            if isinstance(trigger, xtce_1_3.OnContainerUpdateTriggerType)
            else OnPeriodicRateTrigger._from_v1_3(trigger)
            for trigger in obj.choice
        ]
        kwargs["name"] = obj.name
        kwargs["trigger_rate"] = obj.trigger_rate
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["choice"] = [trigger._to_v1_1(policy) for trigger in self.triggers]
        kwargs["name"] = self.name
        kwargs["trigger_rate"] = self.trigger_rate
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["choice"] = [trigger._to_v1_2(policy) for trigger in self.triggers]
        kwargs["name"] = self.name
        kwargs["trigger_rate"] = self.trigger_rate
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["choice"] = [trigger._to_v1_3(policy) for trigger in self.triggers]
        kwargs["name"] = self.name
        kwargs["trigger_rate"] = self.trigger_rate
        return kwargs
