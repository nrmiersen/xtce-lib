"""Algorithm models."""

from abc import ABC
from typing import Annotated, Any

from pydantic import AfterValidator, Field

from xtce_lib.common.xtce_path import XtcePath, require_regex
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from ._pattern import EXPD_NAME_REF_W_PATH, NAME_REF_W_PATH
from ._util import XtceValue
from .calibrator import MathOperation, ThisParameterOperand, ValueOperand
from .common import NameDescriptionBase
from .enum import BitOrder, ChecksumType, MathOperator, ParityForm, ReferencePoint
from .reference import (
    ArgumentInstanceRef,
    InputParameterInstanceRef,
    OutputParameterRef,
)
from .trigger import TriggerSet


class Constant(XtceBaseModel):
    """Define a constant value used in algorithms."""

    constant_name: str
    """The name of the constant."""

    value: XtceValue
    """The value of the constant."""

    _v1_1_type = xtce_1_1.InputAlgorithmType.InputSet.Constant
    _v1_2_type = xtce_1_2.ConstantType
    _v1_3_type = xtce_1_3.ConstantType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.InputAlgorithmType.InputSet.Constant
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["constant_name"] = obj.constant_name
        kwargs["value"] = obj.value
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ConstantType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["constant_name"] = obj.constant_name
        kwargs["value"] = obj.value
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ConstantType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["constant_name"] = obj.constant_name
        kwargs["value"] = obj.value
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["constant_name"] = self.constant_name
        kwargs["value"] = self.value
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["constant_name"] = self.constant_name
        kwargs["value"] = self.value
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["constant_name"] = self.constant_name
        kwargs["value"] = self.value
        return kwargs


class AlgorithmText(XtceBaseModel):
    """Define code for an algorithm with a specified language."""

    text: str = ""
    """The algorithm code as a string."""

    language: str = "pseudo"
    """The language of the algorithm code."""

    _v1_1_type = xtce_1_1.SimpleAlgorithmType.AlgorithmText
    _v1_2_type = xtce_1_2.AlgorithmTextType
    _v1_3_type = xtce_1_3.AlgorithmTextType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.SimpleAlgorithmType.AlgorithmText
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["text"] = obj.value
        kwargs["language"] = obj.language
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.AlgorithmTextType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["text"] = obj.value
        kwargs["language"] = obj.language
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.AlgorithmTextType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["text"] = obj.value
        kwargs["language"] = obj.language
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["value"] = self.text
        kwargs["language"] = self.language
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["value"] = self.text
        kwargs["language"] = self.language
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["value"] = self.text
        kwargs["language"] = self.language
        return kwargs


class ExternalAlgorithm(XtceBaseModel):
    """Define an external algorithm with its implementation details."""

    implementation_name: str = Field(..., examples=["InControl", "Neptune", "OpenC3"])
    """The name of the implementation for the external algorithm."""

    algorithm_location: str
    """The location of the external algorithm implementation."""

    _v1_1_type = xtce_1_1.SimpleAlgorithmType.ExternalAlgorithmSet.ExternalAlgorithm
    _v1_2_type = xtce_1_2.ExternalAlgorithmType
    _v1_3_type = xtce_1_3.ExternalAlgorithmType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.SimpleAlgorithmType.ExternalAlgorithmSet.ExternalAlgorithm
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["implementation_name"] = obj.implementation_name
        kwargs["algorithm_location"] = obj.algorithm_location
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ExternalAlgorithmType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["implementation_name"] = obj.implementation_name
        kwargs["algorithm_location"] = obj.algorithm_location
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ExternalAlgorithmType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["implementation_name"] = obj.implementation_name
        kwargs["algorithm_location"] = obj.algorithm_location
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["implementation_name"] = self.implementation_name
        kwargs["algorithm_location"] = self.algorithm_location
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["implementation_name"] = self.implementation_name
        kwargs["algorithm_location"] = self.algorithm_location
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["implementation_name"] = self.implementation_name
        kwargs["algorithm_location"] = self.algorithm_location
        return kwargs


class SimpleAlgorithm(NameDescriptionBase, ABC):
    """Define shared attributes for algorithms."""

    algorithm_text: AlgorithmText | None = None
    """Free-form algorithm code."""

    external_algorithms: list[ExternalAlgorithm] = Field(default_factory=list)
    """List of external algorithms associated with this simple algorithm.

    Multiple external algorithms are allowed because XTCE documents may be used across
    multiple ground systems.

    """

    _v1_1_type = xtce_1_1.SimpleAlgorithmType
    _v1_2_type = xtce_1_2.SimpleAlgorithmType
    _v1_3_type = xtce_1_3.SimpleAlgorithmType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.SimpleAlgorithmType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["algorithm_text"] = (
            AlgorithmText._from_v1_1(obj.algorithm_text) if obj.algorithm_text else None
        )
        kwargs["external_algorithms"] = (
            [
                ExternalAlgorithm._from_v1_1(algo)
                for algo in obj.external_algorithm_set.external_algorithm
            ]
            if obj.external_algorithm_set
            and obj.external_algorithm_set.external_algorithm
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.SimpleAlgorithmType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["algorithm_text"] = (
            AlgorithmText._from_v1_2(obj.algorithm_text) if obj.algorithm_text else None
        )
        kwargs["external_algorithms"] = (
            [
                ExternalAlgorithm._from_v1_2(algo)
                for algo in obj.external_algorithm_set.external_algorithm
            ]
            if obj.external_algorithm_set
            and obj.external_algorithm_set.external_algorithm
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.SimpleAlgorithmType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["algorithm_text"] = (
            AlgorithmText._from_v1_3(obj.algorithm_text) if obj.algorithm_text else None
        )
        kwargs["external_algorithms"] = (
            [
                ExternalAlgorithm._from_v1_3(algo)
                for algo in obj.external_algorithm_set.external_algorithm
            ]
            if obj.external_algorithm_set
            and obj.external_algorithm_set.external_algorithm
            else []
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["algorithm_text"] = (
            self.algorithm_text._to_v1_1(policy) if self.algorithm_text else None
        )
        kwargs["external_algorithm_set"] = (
            xtce_1_1.SimpleAlgorithmType.ExternalAlgorithmSet(
                external_algorithm=[
                    algo._to_v1_1(policy) for algo in self.external_algorithms
                ]
            )
            if self.external_algorithms
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["algorithm_text"] = (
            self.algorithm_text._to_v1_2(policy) if self.algorithm_text else None
        )
        kwargs["external_algorithm_set"] = (
            xtce_1_2.ExternalAlgorithmSetType(
                external_algorithm=[
                    algo._to_v1_2(policy) for algo in self.external_algorithms
                ]
            )
            if self.external_algorithms
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["algorithm_text"] = (
            self.algorithm_text._to_v1_3(policy) if self.algorithm_text else None
        )
        kwargs["external_algorithm_set"] = (
            xtce_1_3.ExternalAlgorithmSetType(
                external_algorithm=[
                    algo._to_v1_3(policy) for algo in self.external_algorithms
                ]
            )
            if self.external_algorithms
            else None
        )
        return kwargs


class InputAlgorithm(SimpleAlgorithm):
    """Define an input algorithm with additional input parameters."""

    inputs: list[InputParameterInstanceRef | Constant] = Field(default_factory=list)
    """The list of input parameters for the input algorithm."""

    _v1_1_type = xtce_1_1.InputAlgorithmType
    _v1_2_type = xtce_1_2.InputAlgorithmType
    _v1_3_type = xtce_1_3.InputAlgorithmType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.InputAlgorithmType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["inputs"] = (
            [
                InputParameterInstanceRef._from_v1_1(inp)
                if isinstance(
                    inp, xtce_1_1.InputAlgorithmType.InputSet.ParameterInstanceRef
                )
                else Constant._from_v1_1(inp)
                for inp in obj.input_set.choice
            ]
            if obj.input_set and obj.input_set.choice
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.InputAlgorithmType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["inputs"] = (
            [
                InputParameterInstanceRef._from_v1_2(inp)
                if isinstance(inp, xtce_1_2.InputParameterInstanceRefType)
                else Constant._from_v1_2(inp)
                for inp in obj.input_set.choice
            ]
            if obj.input_set and obj.input_set.choice
            else []
        )
        kwargs["name"] = obj.name
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.InputAlgorithmType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["inputs"] = (
            [
                InputParameterInstanceRef._from_v1_3(inp)
                if isinstance(inp, xtce_1_3.InputParameterInstanceRefType)
                else Constant._from_v1_3(inp)
                for inp in obj.input_set.choice
            ]
            if obj.input_set and obj.input_set.choice
            else []
        )
        kwargs["name"] = obj.name
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["input_set"] = (
            xtce_1_1.InputAlgorithmType.InputSet(
                choice=[inp._to_v1_1(policy) for inp in self.inputs]
            )
            if self.inputs
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["input_set"] = (
            xtce_1_2.InputSetType(choice=[inp._to_v1_2(policy) for inp in self.inputs])
            if self.inputs
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["input_set"] = (
            xtce_1_3.InputSetType(choice=[inp._to_v1_3(policy) for inp in self.inputs])
            if self.inputs
            else None
        )
        return kwargs


class ArgumentInputAlgorithm(SimpleAlgorithm):
    """Define an argument input algorithm with additional input parameters or
    arguments.
    """

    inputs: list[InputParameterInstanceRef | ArgumentInstanceRef | Constant] = Field(
        default_factory=list
    )
    """The list of input parameters or arguments for the input algorithm."""

    _v1_1_type = xtce_1_1.InputAlgorithmType
    _v1_2_type = xtce_1_2.ArgumentInputAlgorithmType
    _v1_3_type = xtce_1_3.ArgumentInputAlgorithmType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.InputAlgorithmType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["inputs"] = (
            [
                InputParameterInstanceRef._from_v1_1(inp)
                if isinstance(
                    inp, xtce_1_1.InputAlgorithmType.InputSet.ParameterInstanceRef
                )
                else Constant._from_v1_1(inp)
                for inp in obj.input_set.choice
            ]
            if obj.input_set and obj.input_set.choice
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.ArgumentInputAlgorithmType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["inputs"] = (
            [
                InputParameterInstanceRef._from_v1_2(inp)
                if isinstance(inp, xtce_1_2.InputParameterInstanceRefType)
                else ArgumentInstanceRef._from_v1_2(inp)
                for inp in obj.input_set.choice
            ]
            if obj.input_set and obj.input_set.choice
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.ArgumentInputAlgorithmType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["inputs"] = (
            [
                InputParameterInstanceRef._from_v1_3(inp)
                if isinstance(inp, xtce_1_3.InputParameterInstanceRefType)
                else ArgumentInstanceRef._from_v1_3(inp)
                if isinstance(inp, xtce_1_3.ArgumentInstanceRefType)
                else Constant._from_v1_3(inp)
                for inp in obj.input_set.choice
            ]
            if obj.input_set and obj.input_set.choice
            else []
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        inputs = [
            self._enforce_restricted_type(
                field_name=f"inputs[{i}]",
                current_value=inp,
                allowed_types=(InputParameterInstanceRef, Constant),
                target_version=XtceVersion.V1_1,
                policy=policy,
                require_match=True,
            )
            for i, inp in enumerate(self.inputs)
        ]

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["input_set"] = (
            xtce_1_1.InputAlgorithmType.InputSet(
                choice=[inp._to_v1_1(policy) for inp in inputs]
            )
            if self.inputs
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        inputs = [
            self._enforce_restricted_type(
                field_name=f"inputs[{i}]",
                current_value=inp,
                allowed_types=(InputParameterInstanceRef, ArgumentInstanceRef),
                target_version=XtceVersion.V1_2,
                policy=policy,
                require_match=True,
            )
            for i, inp in enumerate(self.inputs)
        ]

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["input_set"] = (
            xtce_1_2.ArgumentInputSetType(
                choice=[inp._to_v1_2(policy) for inp in inputs]
            )
            if self.inputs
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["input_set"] = (
            xtce_1_3.ArgumentInputSetType(
                choice=[inp._to_v1_3(policy) for inp in self.inputs]
            )
            if self.inputs
            else None
        )
        return kwargs


class TriggeredMathOperation(MathOperation):
    """Define a triggered math operation."""

    trigger_set: TriggerSet
    """The set of triggers that initiate this math operation."""

    output_parameter_ref: Annotated[
        XtcePath, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))
    ] = Field(
        ...,
        examples=["TODO"],
        json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
    )
    """A Unix-like path to the parameter to output the math operation to."""

    _v1_1_type = xtce_1_1.MathAlgorithmType.MathOperation
    _v1_2_type = xtce_1_2.TriggeredMathOperationType
    _v1_3_type = xtce_1_3.TriggeredMathOperationType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.MathAlgorithmType.MathOperation
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["trigger_set"] = TriggerSet._from_v1_1(obj.trigger_set)
        kwargs["output_parameter_ref"] = XtcePath(obj.output_parameter_ref)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.TriggeredMathOperationType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["trigger_set"] = TriggerSet._from_v1_2(obj.trigger_set)
        kwargs["output_parameter_ref"] = XtcePath(obj.output_parameter_ref)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.TriggeredMathOperationType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["trigger_set"] = TriggerSet._from_v1_3(obj.trigger_set)
        kwargs["output_parameter_ref"] = XtcePath(obj.output_parameter_ref)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # MathAlgorithmType.MathOperation is roughly equivalent to
        # TriggeredMathOperationType in XTCE 1.2+
        version = XtceVersion.V1_1

        self._enforce_unsupported_field(
            field_name="name",
            current_value=self.name,
            empty_value=None,
            target_version=version,
            policy=policy,
        )
        self._enforce_unsupported_field(
            field_name="short_description",
            current_value=self.short_description,
            empty_value=None,
            target_version=version,
            policy=policy,
        )
        self._enforce_unsupported_field(
            field_name="ancillary_data",
            current_value=self.ancillary_data,
            empty_value=[],
            target_version=version,
            policy=policy,
        )

        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["choice"] = [
            float(item.value)
            if isinstance(item, ValueOperand)
            else object()
            if isinstance(item, ThisParameterOperand)
            else xtce_1_1.MathOperatorsType(value=item.value)
            if isinstance(item, MathOperator)
            else xtce_1_1.ParameterInstanceRefType(
                parameter_ref=str(item.ref),
                instance=item.instance,
                use_calibrated_value=item.use_calibrated_value,
            )
            for item in self.operation
        ]
        kwargs["trigger_set"] = self.trigger_set._to_v1_1(policy)
        kwargs["output_parameter_ref"] = str(self.output_parameter_ref)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        # XTCE 1.2 uses type xtce:NameReferenceType instead for some reason
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.output_parameter_ref)

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["name"] = self.name
        kwargs["short_description"] = self.short_description
        kwargs["ancillary_data_set"] = xtce_1_2.AncillaryDataSetType(
            ancillary_data=[data._to_v1_2(policy) for data in self.ancillary_data]
        )
        kwargs["choice"] = [
            xtce_1_2.MathOperationCalibratorType.ValueOperand(value=str(item.value))
            if isinstance(item, ValueOperand)
            else xtce_1_2.MathOperationCalibratorType.ThisParameterOperand()
            if isinstance(item, ThisParameterOperand)
            else xtce_1_2.MathOperatorsType(value=item.value)
            if isinstance(item, MathOperator)
            else xtce_1_2.ParameterInstanceRefType(
                parameter_ref=str(item.ref),
                instance=item.instance,
                use_calibrated_value=item.use_calibrated_value,
            )
            for item in self.operation
        ]
        kwargs["trigger_set"] = self.trigger_set._to_v1_2(policy)
        kwargs["output_parameter_ref"] = str(self.output_parameter_ref)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["name"] = self.name
        kwargs["short_description"] = self.short_description
        kwargs["ancillary_data_set"] = xtce_1_3.AncillaryDataSetType(
            ancillary_data=[data._to_v1_3(policy) for data in self.ancillary_data]
        )
        kwargs["choice"] = [
            xtce_1_3.MathOperationCalibratorType.ValueOperand(value=str(item.value))
            if isinstance(item, ValueOperand)
            else xtce_1_3.MathOperationCalibratorType.ThisParameterOperand()
            if isinstance(item, ThisParameterOperand)
            else xtce_1_3.MathOperatorsType(value=item.value)
            if isinstance(item, MathOperator)
            else xtce_1_3.ParameterInstanceRefType(
                parameter_ref=str(item.ref),
                instance=item.instance,
                use_calibrated_value=item.use_calibrated_value,
            )
            for item in self.operation
        ]
        kwargs["trigger_set"] = self.trigger_set._to_v1_3(policy)
        kwargs["output_parameter_ref"] = str(self.output_parameter_ref)
        return kwargs


class MathAlgorithm(NameDescriptionBase):
    """Define a simple mathematical operation."""

    math_operation: TriggeredMathOperation
    """The mathematical operation."""

    _v1_1_type = xtce_1_1.MathAlgorithmType
    _v1_2_type = xtce_1_2.MathAlgorithmType
    _v1_3_type = xtce_1_3.MathAlgorithmType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.MathAlgorithmType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["math_operation"] = TriggeredMathOperation._from_v1_1(obj.math_operation)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.MathAlgorithmType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["math_operation"] = TriggeredMathOperation._from_v1_2(obj.math_operation)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.MathAlgorithmType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["math_operation"] = TriggeredMathOperation._from_v1_3(obj.math_operation)
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["math_operation"] = self.math_operation._to_v1_1(policy)
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["math_operation"] = self.math_operation._to_v1_2(policy)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["math_operation"] = self.math_operation._to_v1_3(policy)
        return kwargs


class InputOutputAlgorithm(InputAlgorithm):
    """Define an algorithm that has both inputs and outputs."""

    outputs: list[OutputParameterRef] = Field(default_factory=list)
    """List of output parameters for the algorithm."""

    thread: bool = False
    """Indicates whether the algorithm runs in its own thread."""

    _v1_1_type = xtce_1_1.InputOutputAlgorithmType
    _v1_2_type = xtce_1_2.InputOutputAlgorithmType
    _v1_3_type = xtce_1_3.InputOutputAlgorithmType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.InputOutputAlgorithmType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["outputs"] = (
            [
                OutputParameterRef._from_v1_1(out)
                for out in obj.output_set.output_parameter_ref
            ]
            if obj.output_set and obj.output_set.output_parameter_ref
            else []
        )
        kwargs["thread"] = bool(obj.thread)
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.InputOutputAlgorithmType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["outputs"] = (
            [
                OutputParameterRef._from_v1_2(out)
                for out in obj.output_set.output_parameter_ref
            ]
            if obj.output_set and obj.output_set.output_parameter_ref
            else []
        )
        kwargs["thread"] = obj.thread
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.InputOutputAlgorithmType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["outputs"] = (
            [
                OutputParameterRef._from_v1_3(out)
                for out in obj.output_set.output_parameter_ref
            ]
            if obj.output_set and obj.output_set.output_parameter_ref
            else []
        )
        kwargs["thread"] = obj.thread
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["output_set"] = (
            xtce_1_1.InputOutputAlgorithmType.OutputSet(
                output_parameter_ref=[out._to_v1_1(policy) for out in self.outputs]
            )
            if self.outputs
            else None
        )
        kwargs["thread"] = self.thread
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["output_set"] = (
            xtce_1_2.OutputSetType(
                output_parameter_ref=[out._to_v1_2(policy) for out in self.outputs]
            )
            if self.outputs
            else None
        )
        kwargs["thread"] = self.thread
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["output_set"] = (
            xtce_1_3.OutputSetType(
                output_parameter_ref=[out._to_v1_3(policy) for out in self.outputs]
            )
            if self.outputs
            else None
        )
        kwargs["thread"] = self.thread
        return kwargs


class InputOutputTriggerAlgorithm(InputOutputAlgorithm):
    """Define an algorithm that has both inputs and outputs that can be triggered."""

    triggers: TriggerSet | None = None
    """The set of triggers that can activate this algorithm."""

    trigger_container: Annotated[
        XtcePath | None, AfterValidator(require_regex(NAME_REF_W_PATH))
    ] = Field(
        default=None,
        json_schema_extra={"pattern": NAME_REF_W_PATH},
    )
    """A Unix-like path to a sequence container."""

    priority: int | None = None
    """The priority of this algorithm relative to other algorithms.

    If more than one algorithm is triggered by the same container, the lowest priority
    algorithm should be processed first.

    """

    _v1_1_type = xtce_1_1.InputOutputTriggerAlgorithmType
    _v1_2_type = xtce_1_2.InputOutputTriggerAlgorithmType
    _v1_3_type = xtce_1_3.InputOutputTriggerAlgorithmType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.InputOutputTriggerAlgorithmType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["triggers"] = (
            TriggerSet._from_v1_1(obj.trigger_set)
            if obj.trigger_set is not None
            else None
        )
        kwargs["trigger_container"] = (
            XtcePath(obj.trigger_container)
            if obj.trigger_container is not None
            else None
        )
        kwargs["priority"] = obj.priority
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.InputOutputTriggerAlgorithmType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["triggers"] = (
            TriggerSet._from_v1_2(obj.trigger_set)
            if obj.trigger_set is not None
            else None
        )
        kwargs["trigger_container"] = (
            XtcePath(obj.trigger_container)
            if obj.trigger_container is not None
            else None
        )
        kwargs["priority"] = obj.priority
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.InputOutputTriggerAlgorithmType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["triggers"] = (
            TriggerSet._from_v1_3(obj.trigger_set)
            if obj.trigger_set is not None
            else None
        )
        kwargs["trigger_container"] = (
            XtcePath(obj.trigger_container)
            if obj.trigger_container is not None
            else None
        )
        kwargs["priority"] = obj.priority
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["trigger_set"] = (
            self.triggers._to_v1_1(policy) if self.triggers else None
        )
        kwargs["trigger_container"] = (
            str(self.trigger_container) if self.trigger_container else None
        )
        kwargs["priority"] = self.priority
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["trigger_set"] = (
            self.triggers._to_v1_2(policy) if self.triggers else None
        )
        kwargs["trigger_container"] = (
            str(self.trigger_container) if self.trigger_container else None
        )
        kwargs["priority"] = self.priority
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["trigger_set"] = (
            self.triggers._to_v1_3(policy) if self.triggers else None
        )
        kwargs["trigger_container"] = (
            str(self.trigger_container) if self.trigger_container else None
        )
        kwargs["priority"] = self.priority
        return kwargs


class Checksum(XtceBaseModel):
    """Define a checksum or hash function."""

    input_algorithm: InputAlgorithm | None = None
    """Used to define an algorithm when `name` is `ChecksumType.CUSTOM`."""

    bits_from_reference: int = Field(default=0, ge=0)
    """Number of bits from the reference point to include in the checksum.

    Can be used to skip some initial bits in the checksum calculation.

    """

    reference: ReferencePoint = Field(default=ReferencePoint.START)
    """The reference point from which the bits are counted."""

    name: ChecksumType
    """The type of checksum or hash function."""

    hash_size_bits: int | None = Field(default=None, ge=1)
    """The size of the hash in bits."""

    parameter_ref: Annotated[
        XtcePath | None, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))
    ] = Field(
        default=None,
        examples=[],
        json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
    )
    """A Unix-like path to the parameter that contains the value of this computed
    checksum or hash based on this container.
    """

    _v1_1_type = None
    _v1_2_type = xtce_1_2.ChecksumType
    _v1_3_type = xtce_1_3.ChecksumType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ChecksumType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["input_algorithm"] = (
            InputAlgorithm._from_v1_2(obj.input_algorithm)
            if obj.input_algorithm
            else None
        )
        kwargs["bits_from_reference"] = obj.bits_from_reference or 0
        kwargs["reference"] = ReferencePoint(obj.reference.value)
        kwargs["name"] = ChecksumType(obj.name.value)
        kwargs["hash_size_bits"] = obj.hash_size_in_bits
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ChecksumType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["input_algorithm"] = (
            InputAlgorithm._from_v1_3(obj.input_algorithm)
            if obj.input_algorithm
            else None
        )
        kwargs["bits_from_reference"] = obj.bits_from_reference or 0
        kwargs["reference"] = ReferencePoint(obj.reference.value)
        kwargs["name"] = ChecksumType(obj.name.value)
        kwargs["hash_size_bits"] = obj.hash_size_in_bits
        kwargs["parameter_ref"] = (
            XtcePath(obj.parameter_ref) if obj.parameter_ref else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="parameter_ref",
            current_value=self.parameter_ref,
            empty_value=None,
            target_version=XtceVersion.V1_2,
            policy=policy,
        )

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["input_algorithm"] = (
            self.input_algorithm._to_v1_2(policy) if self.input_algorithm else None
        )
        kwargs["bits_from_reference"] = self.bits_from_reference
        kwargs["reference"] = xtce_1_2.ReferencePointType(self.reference.value)
        kwargs["name"] = xtce_1_2.ChecksumTypeName(self.name.value)
        kwargs["hash_size_in_bits"] = self.hash_size_bits
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["input_algorithm"] = (
            self.input_algorithm._to_v1_3(policy) if self.input_algorithm else None
        )
        kwargs["bits_from_reference"] = self.bits_from_reference
        kwargs["reference"] = xtce_1_3.ReferencePointType(self.reference.value)
        kwargs["name"] = xtce_1_3.ChecksumTypeName(self.name.value)
        kwargs["hash_size_in_bits"] = self.hash_size_bits
        kwargs["parameter_ref"] = (
            str(self.parameter_ref) if self.parameter_ref is not None else None
        )
        return kwargs


class CRC(XtceBaseModel):
    """Define a CRC (Cyclic Redundancy Check) algorithm."""

    polynomial: bytes
    """The polynomial used for the CRC calculation."""

    init_remainder: bytes | None = None
    """An optional initial value to set in the shift register before computing the
    CRC.
    """

    final_xor: bytes | None = None
    """An optional value to be added to the final shift register value before output."""

    width: int = Field(..., ge=1)
    """The number of bits in the shift register."""

    reflect_data: bool = False
    """Endianness of the input data.

    (True=little, False=big).

    """

    reflect_remainder: bool = False
    """Endianness of the output data.

    (True=little, False=big).

    """

    direction: BitOrder = Field(default=BitOrder.MOST_SIGNIFICANT_BIT_FIRST)
    """The direction to perform the CRC calculation."""

    bits_from_reference: int = Field(default=0, ge=0)
    """The number of bits to skip from the reference point before starting the CRC
    calculation.
    """

    reference: ReferencePoint = Field(default=ReferencePoint.START)
    """The reference point from which to start the CRC calculation."""

    parameter_ref: Annotated[
        XtcePath | None, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))
    ] = Field(
        default=None,
        examples=[],
        json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
    )
    """A Unix-like path to the parameter that contains the value of this CRC based on
    this container.
    """

    _v1_1_type = None
    _v1_2_type = xtce_1_2.Crctype
    _v1_3_type = xtce_1_3.Crctype

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.Crctype) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["polynomial"] = obj.polynomial
        kwargs["init_remainder"] = obj.init_remainder
        kwargs["final_xor"] = obj.final_xor
        kwargs["width"] = obj.width or 1
        kwargs["reflect_data"] = obj.reflect_data
        kwargs["reflect_remainder"] = obj.reflect_remainder
        kwargs["bits_from_reference"] = obj.bits_from_reference or 0
        kwargs["reference"] = ReferencePoint(obj.reference.value)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.Crctype) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["polynomial"] = obj.polynomial
        kwargs["init_remainder"] = obj.init_remainder
        kwargs["final_xor"] = obj.final_xor
        kwargs["width"] = obj.width or 1
        kwargs["reflect_data"] = obj.reflect_data
        kwargs["reflect_remainder"] = obj.reflect_remainder
        kwargs["direction"] = BitOrder(obj.direction.value)
        kwargs["bits_from_reference"] = obj.bits_from_reference or 0
        kwargs["reference"] = ReferencePoint(obj.reference.value)
        kwargs["parameter_ref"] = (
            XtcePath(obj.parameter_ref) if obj.parameter_ref is not None else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        version = XtceVersion.V1_2

        self._enforce_unsupported_field(
            field_name="direction",
            current_value=self.direction,
            empty_value=BitOrder.MOST_SIGNIFICANT_BIT_FIRST,
            target_version=version,
            policy=policy,
        )
        self._enforce_unsupported_field(
            field_name="parameter_ref",
            current_value=self.parameter_ref,
            empty_value=None,
            target_version=version,
            policy=policy,
        )

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["polynomial"] = self.polynomial
        kwargs["init_remainder"] = self.init_remainder
        kwargs["final_xor"] = self.final_xor
        kwargs["width"] = self.width
        kwargs["reflect_data"] = self.reflect_data
        kwargs["reflect_remainder"] = self.reflect_remainder
        kwargs["bits_from_reference"] = self.bits_from_reference
        kwargs["reference"] = xtce_1_2.ReferencePointType(self.reference.value)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["polynomial"] = self.polynomial
        kwargs["init_remainder"] = self.init_remainder
        kwargs["final_xor"] = self.final_xor
        kwargs["width"] = self.width
        kwargs["reflect_data"] = self.reflect_data
        kwargs["reflect_remainder"] = self.reflect_remainder
        kwargs["direction"] = xtce_1_3.BitOrderType(self.direction.value)
        kwargs["bits_from_reference"] = self.bits_from_reference
        kwargs["reference"] = xtce_1_3.ReferencePointType(self.reference.value)
        return kwargs


class XOR(XtceBaseModel):
    """Define an XOR (exclusive OR) operation."""

    bits_from_reference: int = Field(default=0, ge=0)
    """The number of bits to skip from the reference point before starting the XOR
    calculation.
    """

    reference: ReferencePoint = Field(default=ReferencePoint.START)
    """The reference point from which to start the XOR calculation."""

    parameter_ref: Annotated[
        XtcePath | None, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))
    ] = Field(
        default=None,
        examples=[],
        json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
    )
    """A Unix-like path to the parameter that contains the value of this XOR based on
    this container.
    """

    _v1_1_type = None
    _v1_2_type = None
    _v1_3_type = xtce_1_3.Xortype

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.Xortype) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["bits_from_reference"] = obj.bits_from_reference
        kwargs["reference"] = ReferencePoint(obj.reference.value)
        kwargs["parameter_ref"] = (
            XtcePath(obj.parameter_ref) if obj.parameter_ref is not None else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["bits_from_reference"] = self.bits_from_reference
        kwargs["reference"] = xtce_1_3.ReferencePointType(self.reference.value)
        kwargs["parameter_ref"] = (
            str(self.parameter_ref) if self.parameter_ref is not None else None
        )
        return kwargs


class Parity(XtceBaseModel):
    """Define a parity value."""

    parity_form: ParityForm
    """The form of the parity (even or odd)."""

    bits_from_reference: int = Field(default=0, ge=0)
    """The number of bits to skip from the reference point before starting the parity
    calculation.
    """

    reference: ReferencePoint = Field(default=ReferencePoint.START)
    """The reference point from which to start the parity calculation."""

    parameter_ref: Annotated[
        XtcePath | None, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))
    ] = Field(
        default=None,
        examples=[],
        json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
    )
    """A Unix-like path to the parameter that contains the value of this parity based on
    this container.
    """

    _v1_1_type = None
    _v1_2_type = xtce_1_2.ParityType
    _v1_3_type = xtce_1_3.ParityType

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.ParityType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["parity_form"] = ParityForm(obj.type_value.value)
        kwargs["bits_from_reference"] = obj.bits_from_reference
        kwargs["reference"] = ReferencePoint(obj.reference.value)
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.ParityType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["parity_form"] = ParityForm(obj.type_value.value)
        kwargs["bits_from_reference"] = obj.bits_from_reference
        kwargs["reference"] = ReferencePoint(obj.reference.value)
        kwargs["parameter_ref"] = (
            XtcePath(obj.parameter_ref) if obj.parameter_ref is not None else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        self._enforce_unsupported_field(
            field_name="parameter_ref",
            current_value=self.parameter_ref,
            empty_value=None,
            target_version=XtceVersion.V1_2,
            policy=policy,
        )

        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["type_value"] = xtce_1_2.ParityFormType(self.parity_form.value)
        kwargs["bits_from_reference"] = self.bits_from_reference
        kwargs["reference"] = xtce_1_2.ReferencePointType(self.reference.value)
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["type_value"] = xtce_1_3.ParityFormType(self.parity_form.value)
        kwargs["bits_from_reference"] = self.bits_from_reference
        kwargs["reference"] = xtce_1_3.ReferencePointType(self.reference.value)
        kwargs["parameter_ref"] = (
            str(self.parameter_ref) if self.parameter_ref is not None else None
        )
        return kwargs
