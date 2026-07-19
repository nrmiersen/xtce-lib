"""Algorithm models."""

from abc import ABC
from typing import Any, Self

from pydantic import Field

from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy, XtceUnsupportedError
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from ._util import XtceValue, coerce, uncoerce, unwrap
from .calibrator import MathOperation
from .common import NameDescriptionBase
from .enum import BitOrder, ChecksumTypeName, ParityForm, ReferencePoint
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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.ConstantType) -> Self:
        return cls(
            constant_name=unwrap(raw_obj.constant_name),
            value=coerce(raw_obj.value),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.ConstantType) -> Self:
        return cls(
            constant_name=unwrap(raw_obj.constant_name),
            value=coerce(raw_obj.value),
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ConstantType:
        return xtce_1_2.ConstantType(
            constant_name=self.constant_name,
            value=uncoerce(self.value),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ConstantType:
        return xtce_1_3.ConstantType(
            constant_name=self.constant_name,
            value=uncoerce(self.value),
        )


class AlgorithmText(XtceBaseModel):
    """Define code for an algorithm with a specified language."""

    text: str = ""
    """The algorithm code as a string."""

    language: str = "pseudo"
    """The language of the algorithm code."""

    @classmethod
    def _from_v1_1(
        cls: type[Self], raw_obj: xtce_1_1.SimpleAlgorithmType.AlgorithmText
    ) -> Self:
        return cls(text=raw_obj.value, language=raw_obj.language)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.AlgorithmTextType) -> Self:
        return cls(text=raw_obj.value, language=raw_obj.language)

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.AlgorithmTextType) -> Self:
        return cls(text=raw_obj.value, language=raw_obj.language)

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.SimpleAlgorithmType.AlgorithmText:
        return xtce_1_1.SimpleAlgorithmType.AlgorithmText(
            value=self.text,
            language=self.language,
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.AlgorithmTextType:
        return xtce_1_2.AlgorithmTextType(value=self.text, language=self.language)

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.AlgorithmTextType:
        return xtce_1_3.AlgorithmTextType(value=self.text, language=self.language)


class ExternalAlgorithm(XtceBaseModel):
    """Define an external algorithm with its implementation details."""

    implementation_name: str = Field(..., examples=["InControl", "Neptune", "OpenC3"])
    """The name of the implementation for the external algorithm."""

    algorithm_location: str
    """The location of the external algorithm implementation."""

    @classmethod
    def _from_v1_1(
        cls: type[Self],
        raw_obj: xtce_1_1.SimpleAlgorithmType.ExternalAlgorithmSet.ExternalAlgorithm,
    ) -> Self:
        return cls(
            implementation_name=raw_obj.implementation_name,
            algorithm_location=raw_obj.algorithm_location,
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.ExternalAlgorithmType) -> Self:
        return cls(
            implementation_name=raw_obj.implementation_name,
            algorithm_location=raw_obj.algorithm_location,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.ExternalAlgorithmType) -> Self:
        return cls(
            implementation_name=raw_obj.implementation_name,
            algorithm_location=raw_obj.algorithm_location,
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.SimpleAlgorithmType.ExternalAlgorithmSet.ExternalAlgorithm:
        return xtce_1_1.SimpleAlgorithmType.ExternalAlgorithmSet.ExternalAlgorithm(
            implementation_name=self.implementation_name,
            algorithm_location=self.algorithm_location,
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ExternalAlgorithmType:
        return xtce_1_2.ExternalAlgorithmType(
            implementation_name=self.implementation_name,
            algorithm_location=self.algorithm_location,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ExternalAlgorithmType:
        return xtce_1_3.ExternalAlgorithmType(
            implementation_name=self.implementation_name,
            algorithm_location=self.algorithm_location,
        )


class SimpleAlgorithm(NameDescriptionBase, ABC):
    """Define shared attributes for algorithms."""

    algorithm_text: AlgorithmText | None = None
    """Free-form algorithm code."""

    external_algorithms: list[ExternalAlgorithm] = Field(default_factory=list)
    """List of external algorithms associated with this simple algorithm.

    Multiple external algorithms are allowed because XTCE documents may be used across
    multiple ground systems.

    """

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.SimpleAlgorithmType) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.SimpleAlgorithmType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_2(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_2(raw_obj.ancillary_data_set),
            algorithm_text=AlgorithmText._from_v1_2(raw_obj.algorithm_text)
            if raw_obj.algorithm_text
            else None,
            external_algorithms=[
                ExternalAlgorithm._from_v1_2(algo)
                for algo in raw_obj.external_algorithm_set.external_algorithm
            ]
            if raw_obj.external_algorithm_set
            and raw_obj.external_algorithm_set.external_algorithm
            else [],
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.SimpleAlgorithmType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_3(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_3(raw_obj.ancillary_data_set),
            algorithm_text=AlgorithmText._from_v1_3(raw_obj.algorithm_text)
            if raw_obj.algorithm_text
            else None,
            external_algorithms=[
                ExternalAlgorithm._from_v1_3(algo)
                for algo in raw_obj.external_algorithm_set.external_algorithm
            ]
            if raw_obj.external_algorithm_set
            and raw_obj.external_algorithm_set.external_algorithm
            else [],
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.SimpleAlgorithmType:
        return xtce_1_1.SimpleAlgorithmType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_1(policy),
            ancillary_data_set=self._ancillary_data_to_v1_1(policy),
            algorithm_text=self.algorithm_text._to_v1_1(policy)
            if self.algorithm_text
            else None,
            external_algorithm_set=xtce_1_1.SimpleAlgorithmType.ExternalAlgorithmSet(
                external_algorithm=[
                    algo._to_v1_1(policy) for algo in self.external_algorithms
                ]
            )
            if self.external_algorithms
            else None,
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.SimpleAlgorithmType:
        return xtce_1_2.SimpleAlgorithmType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_2(policy),
            ancillary_data_set=self._ancillary_data_to_v1_2(policy),
            algorithm_text=self.algorithm_text._to_v1_2(policy)
            if self.algorithm_text
            else None,
            external_algorithm_set=xtce_1_2.ExternalAlgorithmSetType(
                external_algorithm=[
                    algo._to_v1_2(policy) for algo in self.external_algorithms
                ]
            )
            if self.external_algorithms
            else None,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.SimpleAlgorithmType:
        return xtce_1_3.SimpleAlgorithmType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_3(policy),
            ancillary_data_set=self._ancillary_data_to_v1_3(policy),
            algorithm_text=self.algorithm_text._to_v1_3(policy)
            if self.algorithm_text
            else None,
            external_algorithm_set=xtce_1_3.ExternalAlgorithmSetType(
                external_algorithm=[
                    algo._to_v1_3(policy) for algo in self.external_algorithms
                ]
            )
            if self.external_algorithms
            else None,
        )


class InputAlgorithm(SimpleAlgorithm):
    """Define an input algorithm with additional input parameters."""

    inputs: list[InputParameterInstanceRef | Constant] = Field(default_factory=list)
    """The list of input parameters for the input algorithm."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.InputAlgorithmType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_1(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_1(raw_obj.ancillary_data_set),
            algorithm_text=AlgorithmText._from_v1_1(raw_obj.algorithm_text)
            if raw_obj.algorithm_text
            else None,
            external_algorithms=[
                ExternalAlgorithm._from_v1_1(algo)
                for algo in raw_obj.external_algorithm_set.external_algorithm
            ]
            if raw_obj.external_algorithm_set
            and raw_obj.external_algorithm_set.external_algorithm
            else [],
            inputs=[
                InputParameterInstanceRef._from_v1_1(inp)
                if isinstance(
                    inp, xtce_1_1.InputAlgorithmType.InputSet.ParameterInstanceRef
                )
                else Constant._from_v1_1(inp)
                for inp in raw_obj.input_set.choice
            ]
            if raw_obj.input_set and raw_obj.input_set.choice
            else [],
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.InputAlgorithmType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_2(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_2(raw_obj.ancillary_data_set),
            algorithm_text=AlgorithmText._from_v1_2(raw_obj.algorithm_text)
            if raw_obj.algorithm_text
            else None,
            external_algorithms=[
                ExternalAlgorithm._from_v1_2(algo)
                for algo in raw_obj.external_algorithm_set.external_algorithm
            ]
            if raw_obj.external_algorithm_set
            and raw_obj.external_algorithm_set.external_algorithm
            else [],
            inputs=[
                InputParameterInstanceRef._from_v1_2(inp)
                if isinstance(inp, xtce_1_2.InputParameterInstanceRefType)
                else Constant._from_v1_2(inp)
                for inp in raw_obj.input_set.choice
            ]
            if raw_obj.input_set and raw_obj.input_set.choice
            else [],
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.InputAlgorithmType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_3(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_3(raw_obj.ancillary_data_set),
            algorithm_text=AlgorithmText._from_v1_3(raw_obj.algorithm_text)
            if raw_obj.algorithm_text
            else None,
            external_algorithms=[
                ExternalAlgorithm._from_v1_3(algo)
                for algo in raw_obj.external_algorithm_set.external_algorithm
            ]
            if raw_obj.external_algorithm_set
            and raw_obj.external_algorithm_set.external_algorithm
            else [],
            inputs=[
                InputParameterInstanceRef._from_v1_3(inp)
                if isinstance(inp, xtce_1_3.InputParameterInstanceRefType)
                else Constant._from_v1_3(inp)
                for inp in raw_obj.input_set.choice
            ]
            if raw_obj.input_set and raw_obj.input_set.choice
            else [],
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.InputAlgorithmType:
        return xtce_1_1.InputAlgorithmType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_1(policy),
            ancillary_data_set=self._ancillary_data_to_v1_1(policy),
            algorithm_text=self.algorithm_text._to_v1_1(policy)
            if self.algorithm_text
            else None,
            external_algorithm_set=xtce_1_1.SimpleAlgorithmType.ExternalAlgorithmSet(
                external_algorithm=[
                    algo._to_v1_1(policy) for algo in self.external_algorithms
                ]
            )
            if self.external_algorithms
            else None,
            input_set=xtce_1_1.InputAlgorithmType.InputSet(
                choice=[inp._to_v1_1(policy) for inp in self.inputs]
            )
            if self.inputs
            else None,
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.InputAlgorithmType:
        return xtce_1_2.InputAlgorithmType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_2(policy),
            ancillary_data_set=self._ancillary_data_to_v1_2(policy),
            algorithm_text=self.algorithm_text._to_v1_2(policy)
            if self.algorithm_text
            else None,
            external_algorithm_set=xtce_1_2.ExternalAlgorithmSetType(
                external_algorithm=[
                    algo._to_v1_2(policy) for algo in self.external_algorithms
                ]
            )
            if self.external_algorithms
            else None,
            input_set=xtce_1_2.InputSetType(
                choice=[inp._to_v1_2(policy) for inp in self.inputs]
            )
            if self.inputs
            else None,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.InputAlgorithmType:
        return xtce_1_3.InputAlgorithmType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_3(policy),
            ancillary_data_set=self._ancillary_data_to_v1_3(policy),
            algorithm_text=self.algorithm_text._to_v1_3(policy)
            if self.algorithm_text
            else None,
            external_algorithm_set=xtce_1_3.ExternalAlgorithmSetType(
                external_algorithm=[
                    algo._to_v1_3(policy) for algo in self.external_algorithms
                ]
            )
            if self.external_algorithms
            else None,
            input_set=xtce_1_3.InputSetType(
                choice=[inp._to_v1_3(policy) for inp in self.inputs]
            )
            if self.inputs
            else None,
        )


class ArgumentInputAlgorithm(SimpleAlgorithm):
    """Define an argument input algorithm with additional input parameters or arguments."""

    inputs: list[InputParameterInstanceRef | ArgumentInstanceRef | Constant] = Field(
        default_factory=list
    )
    """The list of input parameters or arguments for the input algorithm."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(
        cls: type[Self], raw_obj: xtce_1_2.ArgumentInputAlgorithmType
    ) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_2(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_2(raw_obj.ancillary_data_set),
            algorithm_text=AlgorithmText._from_v1_2(raw_obj.algorithm_text)
            if raw_obj.algorithm_text
            else None,
            external_algorithms=[
                ExternalAlgorithm._from_v1_2(algo)
                for algo in raw_obj.external_algorithm_set.external_algorithm
            ]
            if raw_obj.external_algorithm_set
            and raw_obj.external_algorithm_set.external_algorithm
            else [],
            inputs=[
                InputParameterInstanceRef._from_v1_2(inp)
                if isinstance(inp, xtce_1_2.InputParameterInstanceRefType)
                else ArgumentInstanceRef._from_v1_2(inp)
                for inp in raw_obj.input_set.choice
            ]
            if raw_obj.input_set and raw_obj.input_set.choice
            else [],
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], raw_obj: xtce_1_3.ArgumentInputAlgorithmType
    ) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_3(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_3(raw_obj.ancillary_data_set),
            algorithm_text=AlgorithmText._from_v1_3(raw_obj.algorithm_text)
            if raw_obj.algorithm_text
            else None,
            external_algorithms=[
                ExternalAlgorithm._from_v1_3(algo)
                for algo in raw_obj.external_algorithm_set.external_algorithm
            ]
            if raw_obj.external_algorithm_set
            and raw_obj.external_algorithm_set.external_algorithm
            else [],
            inputs=[
                InputParameterInstanceRef._from_v1_3(inp)
                if isinstance(inp, xtce_1_3.InputParameterInstanceRefType)
                else ArgumentInstanceRef._from_v1_3(inp)
                if isinstance(inp, xtce_1_3.ArgumentInstanceRefType)
                else Constant._from_v1_3(inp)
                for inp in raw_obj.input_set.choice
            ]
            if raw_obj.input_set and raw_obj.input_set.choice
            else [],
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ArgumentInputAlgorithmType:
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

        return xtce_1_2.ArgumentInputAlgorithmType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_2(policy),
            ancillary_data_set=self._ancillary_data_to_v1_2(policy),
            algorithm_text=self.algorithm_text._to_v1_2(policy)
            if self.algorithm_text
            else None,
            external_algorithm_set=xtce_1_2.ExternalAlgorithmSetType(
                external_algorithm=[
                    algo._to_v1_2(policy) for algo in self.external_algorithms
                ]
            )
            if self.external_algorithms
            else None,
            input_set=xtce_1_2.ArgumentInputSetType(
                choice=[inp._to_v1_2(policy) for inp in inputs]
            )
            if self.inputs
            else None,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ArgumentInputAlgorithmType:
        return xtce_1_3.ArgumentInputAlgorithmType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_3(policy),
            ancillary_data_set=self._ancillary_data_to_v1_3(policy),
            algorithm_text=self.algorithm_text._to_v1_3(policy)
            if self.algorithm_text
            else None,
            external_algorithm_set=xtce_1_3.ExternalAlgorithmSetType(
                external_algorithm=[
                    algo._to_v1_3(policy) for algo in self.external_algorithms
                ]
            )
            if self.external_algorithms
            else None,
            input_set=xtce_1_3.ArgumentInputSetType(
                choice=[inp._to_v1_3(policy) for inp in self.inputs]
            )
            if self.inputs
            else None,
        )


class TriggeredMathOperation(MathOperation):
    trigger_set: TriggerSet
    output_parameter_ref: str = Field(
        ...,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )


class MathAlgorithm(NameDescriptionBase):
    math_operation: TriggeredMathOperation


class InputOutputAlgorithm(InputAlgorithm):
    outputs: list[OutputParameterRef] = Field(default_factory=list, min_length=1)
    thread: bool = Field(default=False)


class InputOutputTriggerAlgorithm(InputOutputAlgorithm):
    triggers: TriggerSet | None = Field(default=None)
    trigger_container: str | None = Field(
        default=None,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
    )
    priority: int | None = Field(default=None)


class Checksum(XtceBaseModel):
    input_algorithm: InputAlgorithm | None = Field(default=None)
    bits_from_reference: int = Field(default=0, ge=0)
    reference: ReferencePoint = Field(default=ReferencePoint.START)
    name: ChecksumTypeName
    hash_size_in_bits: int | None = Field(default=None, ge=1)
    parameter_ref: str | None = Field(
        default=None,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )


class CRC(XtceBaseModel):
    polynomial: bytes
    init_remainder: bytes | None = Field(default=None)
    final_xor: bytes | None = Field(default=None)
    width: int = Field(..., ge=1)
    reflect_data: bool = Field(default=False)
    reflect_remainder: bool = Field(default=False)
    direction: BitOrder = Field(default=BitOrder.MOST_SIGNIFICANT_BIT_FIRST)
    bits_from_reference: int = Field(default=0, ge=0)
    reference: ReferencePoint = Field(default=ReferencePoint.START)
    parameter_ref: str | None = Field(
        default=None,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )


class XOR(XtceBaseModel):
    bits_from_reference: int = Field(default=0, ge=0)
    reference: ReferencePoint = Field(default=ReferencePoint.START)
    parameter_ref: str | None = Field(
        default=None,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )


class Parity(XtceBaseModel):
    parity_form: ParityForm
    bits_from_reference: int = Field(default=0, ge=0)
    reference: ReferencePoint = Field(default=ReferencePoint.START)
    parameter_ref: str | None = Field(
        default=None,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )


# TODO probably write base class for Checksum, CRC, XOR, Parity
