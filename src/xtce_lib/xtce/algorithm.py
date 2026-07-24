"""Algorithm models."""

from abc import ABC
from typing import Annotated, Any, Self

from pydantic import AfterValidator, Field

from xtce_lib.common.xtce_path import XtcePath, require_regex
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy, XtceUnsupportedError
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from ._pattern import EXPD_NAME_REF_W_PATH, NAME_REF_W_PATH
from ._util import XtceValue, coerce, uncoerce, unwrap
from .calibrator import MathOperation, ThisParameterOperand, ValueOperand
from .common import AncillaryData, NameDescriptionBase
from .enum import BitOrder, ChecksumType, MathOperator, ParityForm, ReferencePoint
from .reference import (
    ArgumentInstanceRef,
    InputParameterInstanceRef,
    OutputParameterRef,
    ParameterInstanceRef,
)
from .trigger import TriggerSet


class Constant(XtceBaseModel):
    """Define a constant value used in algorithms."""

    constant_name: str
    """The name of the constant."""

    value: XtceValue
    """The value of the constant."""

    @classmethod
    def _from_v1_1(
        cls: type[Self], raw_obj: xtce_1_1.InputAlgorithmType.InputSet.Constant
    ) -> Self:
        return cls(
            constant_name=unwrap(raw_obj.constant_name),
            value=coerce(raw_obj.value),
        )

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

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.InputAlgorithmType.InputSet.Constant:
        return xtce_1_1.InputAlgorithmType.InputSet.Constant(
            constant_name=self.constant_name,
            value=uncoerce(self.value),
        )

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
    """Define an argument input algorithm with additional input parameters or
    arguments.
    """

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

    @classmethod
    def _from_v1_1(
        cls: type[Self], raw_obj: xtce_1_1.MathAlgorithmType.MathOperation
    ) -> Self:
        # MathAlgorithmType.MathOperation is roughly equivalent to
        # TriggeredMathOperationType in XTCE 1.2+
        return cls(
            operation=[
                ValueOperand(value=float(item))
                if isinstance(item, float)
                else MathOperator(value=item.value)
                if isinstance(item, xtce_1_1.MathOperatorsType)
                else ParameterInstanceRef(ref=XtcePath(item.parameter_ref))
                if isinstance(item, xtce_1_1.ParameterInstanceRefType)
                else ThisParameterOperand()
                for item in raw_obj.choice
            ],
            trigger_set=TriggerSet._from_v1_1(raw_obj.trigger_set),
            output_parameter_ref=XtcePath(raw_obj.output_parameter_ref),
        )

    @classmethod
    def _from_v1_2(
        cls: type[Self], raw_obj: xtce_1_2.TriggeredMathOperationType
    ) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            ancillary_data=[
                AncillaryData._from_v1_2(data)
                for data in raw_obj.ancillary_data_set.ancillary_data
            ]
            if raw_obj.ancillary_data_set
            else [],
            operation=[
                ValueOperand(value=item.value)
                if isinstance(item, xtce_1_2.MathOperationCalibratorType.ValueOperand)
                else ThisParameterOperand()
                if isinstance(
                    item, xtce_1_2.MathOperationCalibratorType.ThisParameterOperand
                )
                else MathOperator(value=item.value)
                if isinstance(item, xtce_1_2.MathOperatorsType)
                else ParameterInstanceRef(
                    ref=XtcePath(item.parameter_ref),
                    instance=item.instance,
                    use_calibrated_value=item.use_calibrated_value,
                )
                for item in raw_obj.choice
            ],
            trigger_set=TriggerSet._from_v1_2(raw_obj.trigger_set),
            output_parameter_ref=XtcePath(raw_obj.output_parameter_ref),
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], raw_obj: xtce_1_3.TriggeredMathOperationType
    ) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            ancillary_data=[
                AncillaryData._from_v1_3(data)
                for data in raw_obj.ancillary_data_set.ancillary_data
            ]
            if raw_obj.ancillary_data_set
            else [],
            operation=[
                ValueOperand(value=item.value)
                if isinstance(item, xtce_1_3.MathOperationCalibratorType.ValueOperand)
                else ThisParameterOperand()
                if isinstance(
                    item, xtce_1_3.MathOperationCalibratorType.ThisParameterOperand
                )
                else MathOperator(value=item.value)
                if isinstance(item, xtce_1_3.MathOperatorsType)
                else ParameterInstanceRef(
                    ref=XtcePath(item.parameter_ref),
                    instance=item.instance,
                    use_calibrated_value=item.use_calibrated_value,
                )
                for item in raw_obj.choice
            ],
            trigger_set=TriggerSet._from_v1_3(raw_obj.trigger_set),
            output_parameter_ref=XtcePath(raw_obj.output_parameter_ref),
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.MathAlgorithmType.MathOperation:
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

        return xtce_1_1.MathAlgorithmType.MathOperation(
            choice=[
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
            ],
            trigger_set=self.trigger_set._to_v1_1(policy),
            output_parameter_ref=str(self.output_parameter_ref),
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.TriggeredMathOperationType:
        # XTCE 1.2 uses type xtce:NameReferenceType instead for some reason
        validator = require_regex(NAME_REF_W_PATH)
        validator(self.output_parameter_ref)

        return xtce_1_2.TriggeredMathOperationType(
            name=self.name,
            short_description=self.short_description,
            ancillary_data_set=xtce_1_2.AncillaryDataSetType(
                ancillary_data=[data._to_v1_2(policy) for data in self.ancillary_data]
            ),
            choice=[
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
            ],
            trigger_set=self.trigger_set._to_v1_2(policy),
            output_parameter_ref=str(self.output_parameter_ref),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.TriggeredMathOperationType:
        return xtce_1_3.TriggeredMathOperationType(
            name=self.name,
            short_description=self.short_description,
            ancillary_data_set=xtce_1_3.AncillaryDataSetType(
                ancillary_data=[data._to_v1_3(policy) for data in self.ancillary_data]
            ),
            choice=[
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
            ],
            trigger_set=self.trigger_set._to_v1_3(policy),
            output_parameter_ref=str(self.output_parameter_ref),
        )


class MathAlgorithm(NameDescriptionBase):
    """Define a simple mathematical operation."""

    math_operation: TriggeredMathOperation
    """The mathematical operation."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.MathAlgorithmType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_1(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_1(raw_obj.ancillary_data_set),
            math_operation=TriggeredMathOperation._from_v1_1(raw_obj.math_operation),
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.MathAlgorithmType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_2(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_2(raw_obj.ancillary_data_set),
            math_operation=TriggeredMathOperation._from_v1_2(raw_obj.math_operation),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.MathAlgorithmType) -> Self:
        return cls(
            name=raw_obj.name,
            short_description=raw_obj.short_description,
            long_description=raw_obj.long_description,
            aliases=cls._aliases_from_v1_3(raw_obj.alias_set),
            ancillary_data=cls._ancillary_data_from_v1_3(raw_obj.ancillary_data_set),
            math_operation=TriggeredMathOperation._from_v1_3(raw_obj.math_operation),
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.MathAlgorithmType:
        return xtce_1_1.MathAlgorithmType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_1(policy),
            ancillary_data_set=self._ancillary_data_to_v1_1(policy),
            math_operation=self.math_operation._to_v1_1(policy),
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.MathAlgorithmType:
        return xtce_1_2.MathAlgorithmType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_2(policy),
            ancillary_data_set=self._ancillary_data_to_v1_2(policy),
            math_operation=self.math_operation._to_v1_2(policy),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.MathAlgorithmType:
        return xtce_1_3.MathAlgorithmType(
            name=self.name,
            short_description=self.short_description,
            long_description=self.long_description,
            alias_set=self._aliases_to_v1_3(policy),
            ancillary_data_set=self._ancillary_data_to_v1_3(policy),
            math_operation=self.math_operation._to_v1_3(policy),
        )


class InputOutputAlgorithm(InputAlgorithm):
    """Define an algorithm that has both inputs and outputs."""

    outputs: list[OutputParameterRef] = Field(default_factory=list)
    """List of output parameters for the algorithm."""

    thread: bool = False
    """Indicates whether the algorithm runs in its own thread."""

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: xtce_1_1.InputOutputAlgorithmType) -> Self:
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
            outputs=[
                OutputParameterRef._from_v1_1(out)
                for out in raw_obj.output_set.output_parameter_ref
            ]
            if raw_obj.output_set and raw_obj.output_set.output_parameter_ref
            else [],
            thread=bool(raw_obj.thread),
        )

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.InputOutputAlgorithmType) -> Self:
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
            outputs=[
                OutputParameterRef._from_v1_2(out)
                for out in raw_obj.output_set.output_parameter_ref
            ]
            if raw_obj.output_set and raw_obj.output_set.output_parameter_ref
            else [],
            thread=raw_obj.thread,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.InputOutputAlgorithmType) -> Self:
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
            outputs=[
                OutputParameterRef._from_v1_3(out)
                for out in raw_obj.output_set.output_parameter_ref
            ]
            if raw_obj.output_set and raw_obj.output_set.output_parameter_ref
            else [],
            thread=raw_obj.thread,
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.InputOutputAlgorithmType:
        return xtce_1_1.InputOutputAlgorithmType(
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
            output_set=xtce_1_1.InputOutputAlgorithmType.OutputSet(
                output_parameter_ref=[out._to_v1_1(policy) for out in self.outputs]
            )
            if self.outputs
            else None,
            thread=self.thread,
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.InputOutputAlgorithmType:
        return xtce_1_2.InputOutputAlgorithmType(
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
            output_set=xtce_1_2.OutputSetType(
                output_parameter_ref=[out._to_v1_2(policy) for out in self.outputs]
            )
            if self.outputs
            else None,
            thread=self.thread,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.InputOutputAlgorithmType:
        return xtce_1_3.InputOutputAlgorithmType(
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
            output_set=xtce_1_3.OutputSetType(
                output_parameter_ref=[out._to_v1_3(policy) for out in self.outputs]
            )
            if self.outputs
            else None,
            thread=self.thread,
        )


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

    @classmethod
    def _from_v1_1(
        cls: type[Self], raw_obj: xtce_1_1.InputOutputTriggerAlgorithmType
    ) -> Self:
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
            outputs=[
                OutputParameterRef._from_v1_1(out)
                for out in raw_obj.output_set.output_parameter_ref
            ]
            if raw_obj.output_set and raw_obj.output_set.output_parameter_ref
            else [],
            triggers=TriggerSet._from_v1_1(raw_obj.trigger_set)
            if raw_obj.trigger_set is not None
            else None,
            trigger_container=XtcePath(raw_obj.trigger_container)
            if raw_obj.trigger_container is not None
            else None,
            priority=raw_obj.priority,
            thread=bool(raw_obj.thread),
        )

    @classmethod
    def _from_v1_2(
        cls: type[Self], raw_obj: xtce_1_2.InputOutputTriggerAlgorithmType
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
                else Constant._from_v1_2(inp)
                for inp in raw_obj.input_set.choice
            ]
            if raw_obj.input_set and raw_obj.input_set.choice
            else [],
            outputs=[
                OutputParameterRef._from_v1_2(out)
                for out in raw_obj.output_set.output_parameter_ref
            ]
            if raw_obj.output_set and raw_obj.output_set.output_parameter_ref
            else [],
            triggers=TriggerSet._from_v1_2(raw_obj.trigger_set)
            if raw_obj.trigger_set is not None
            else None,
            trigger_container=XtcePath(raw_obj.trigger_container)
            if raw_obj.trigger_container is not None
            else None,
            priority=raw_obj.priority,
            thread=raw_obj.thread,
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], raw_obj: xtce_1_3.InputOutputTriggerAlgorithmType
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
                else Constant._from_v1_3(inp)
                for inp in raw_obj.input_set.choice
            ]
            if raw_obj.input_set and raw_obj.input_set.choice
            else [],
            outputs=[
                OutputParameterRef._from_v1_3(out)
                for out in raw_obj.output_set.output_parameter_ref
            ]
            if raw_obj.output_set and raw_obj.output_set.output_parameter_ref
            else [],
            triggers=TriggerSet._from_v1_3(raw_obj.trigger_set)
            if raw_obj.trigger_set is not None
            else None,
            trigger_container=XtcePath(raw_obj.trigger_container)
            if raw_obj.trigger_container is not None
            else None,
            priority=raw_obj.priority,
            thread=raw_obj.thread,
        )

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.InputOutputTriggerAlgorithmType:
        return xtce_1_1.InputOutputTriggerAlgorithmType(
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
            output_set=xtce_1_1.InputOutputAlgorithmType.OutputSet(
                output_parameter_ref=[out._to_v1_1(policy) for out in self.outputs]
            )
            if self.outputs
            else None,
            thread=self.thread,
            trigger_set=self.triggers._to_v1_1(policy) if self.triggers else None,
            trigger_container=str(self.trigger_container)
            if self.trigger_container
            else None,
            priority=self.priority,
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.InputOutputTriggerAlgorithmType:
        return xtce_1_2.InputOutputTriggerAlgorithmType(
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
            output_set=xtce_1_2.OutputSetType(
                output_parameter_ref=[out._to_v1_2(policy) for out in self.outputs]
            )
            if self.outputs
            else None,
            thread=self.thread,
            trigger_set=self.triggers._to_v1_2(policy) if self.triggers else None,
            trigger_container=str(self.trigger_container)
            if self.trigger_container
            else None,
            priority=self.priority,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.InputOutputTriggerAlgorithmType:
        return xtce_1_3.InputOutputTriggerAlgorithmType(
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
            output_set=xtce_1_3.OutputSetType(
                output_parameter_ref=[out._to_v1_3(policy) for out in self.outputs]
            )
            if self.outputs
            else None,
            trigger_set=self.triggers._to_v1_3(policy) if self.triggers else None,
            trigger_container=str(self.trigger_container)
            if self.trigger_container
            else None,
            priority=self.priority,
            thread=self.thread,
        )


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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.ChecksumType) -> Self:
        return cls(
            input_algorithm=InputAlgorithm._from_v1_2(raw_obj.input_algorithm)
            if raw_obj.input_algorithm
            else None,
            bits_from_reference=raw_obj.bits_from_reference or 0,
            reference=ReferencePoint(raw_obj.reference.value),
            name=ChecksumType(raw_obj.name.value),
            hash_size_bits=raw_obj.hash_size_in_bits,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.ChecksumType) -> Self:
        return cls(
            input_algorithm=InputAlgorithm._from_v1_3(raw_obj.input_algorithm)
            if raw_obj.input_algorithm
            else None,
            bits_from_reference=raw_obj.bits_from_reference or 0,
            reference=ReferencePoint(raw_obj.reference.value),
            name=ChecksumType(raw_obj.name.value),
            hash_size_bits=raw_obj.hash_size_in_bits,
            parameter_ref=XtcePath(raw_obj.parameter_ref)
            if raw_obj.parameter_ref
            else None,
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ChecksumType:
        self._enforce_unsupported_field(
            field_name="parameter_ref",
            current_value=self.parameter_ref,
            empty_value=None,
            target_version=XtceVersion.V1_2,
            policy=policy,
        )

        return xtce_1_2.ChecksumType(
            input_algorithm=self.input_algorithm._to_v1_2(policy)
            if self.input_algorithm
            else None,
            bits_from_reference=self.bits_from_reference,
            reference=xtce_1_2.ReferencePointType(self.reference.value),
            name=xtce_1_2.ChecksumTypeName(self.name.value),
            hash_size_in_bits=self.hash_size_bits,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ChecksumType:
        return xtce_1_3.ChecksumType(
            input_algorithm=self.input_algorithm._to_v1_3(policy)
            if self.input_algorithm
            else None,
            bits_from_reference=self.bits_from_reference,
            reference=xtce_1_3.ReferencePointType(self.reference.value),
            name=xtce_1_3.ChecksumTypeName(self.name.value),
            hash_size_in_bits=self.hash_size_bits,
            parameter_ref=str(self.parameter_ref)
            if self.parameter_ref is not None
            else None,
        )


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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.Crctype) -> Self:
        return cls(
            polynomial=raw_obj.polynomial,
            init_remainder=raw_obj.init_remainder,
            final_xor=raw_obj.final_xor,
            width=raw_obj.width or 1,
            reflect_data=raw_obj.reflect_data,
            reflect_remainder=raw_obj.reflect_remainder,
            bits_from_reference=raw_obj.bits_from_reference or 0,
            reference=ReferencePoint(raw_obj.reference.value),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.Crctype) -> Self:
        return cls(
            polynomial=raw_obj.polynomial,
            init_remainder=raw_obj.init_remainder,
            final_xor=raw_obj.final_xor,
            width=raw_obj.width or 1,
            reflect_data=raw_obj.reflect_data,
            reflect_remainder=raw_obj.reflect_remainder,
            direction=BitOrder(raw_obj.direction.value),
            bits_from_reference=raw_obj.bits_from_reference or 0,
            reference=ReferencePoint(raw_obj.reference.value),
            parameter_ref=XtcePath(raw_obj.parameter_ref)
            if raw_obj.parameter_ref is not None
            else None,
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.Crctype:
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

        return xtce_1_2.Crctype(
            polynomial=self.polynomial,
            init_remainder=self.init_remainder,
            final_xor=self.final_xor,
            width=self.width,
            reflect_data=self.reflect_data,
            reflect_remainder=self.reflect_remainder,
            bits_from_reference=self.bits_from_reference,
            reference=xtce_1_2.ReferencePointType(self.reference.value),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.Crctype:
        return xtce_1_3.Crctype(
            polynomial=self.polynomial,
            init_remainder=self.init_remainder,
            final_xor=self.final_xor,
            width=self.width,
            reflect_data=self.reflect_data,
            reflect_remainder=self.reflect_remainder,
            direction=xtce_1_3.BitOrderType(self.direction.value),
            bits_from_reference=self.bits_from_reference,
            reference=xtce_1_3.ReferencePointType(self.reference.value),
        )


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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_2, cls.__name__)

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.Xortype) -> Self:
        return cls(
            bits_from_reference=raw_obj.bits_from_reference,
            reference=ReferencePoint(raw_obj.reference.value),
            parameter_ref=XtcePath(raw_obj.parameter_ref)
            if raw_obj.parameter_ref is not None
            else None,
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_2, self.__class__.__name__)

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.Xortype:
        return xtce_1_3.Xortype(
            bits_from_reference=self.bits_from_reference,
            reference=xtce_1_3.ReferencePointType(self.reference.value),
            parameter_ref=str(self.parameter_ref)
            if self.parameter_ref is not None
            else None,
        )


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

    @classmethod
    def _from_v1_1(cls: type[Self], raw_obj: Any) -> Self:
        raise XtceUnsupportedError(XtceVersion.V1_1, cls.__name__)

    @classmethod
    def _from_v1_2(cls: type[Self], raw_obj: xtce_1_2.ParityType) -> Self:
        return cls(
            parity_form=ParityForm(raw_obj.type_value.value),
            bits_from_reference=raw_obj.bits_from_reference,
            reference=ReferencePoint(raw_obj.reference.value),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], raw_obj: xtce_1_3.ParityType) -> Self:
        return cls(
            parity_form=ParityForm(raw_obj.type_value.value),
            bits_from_reference=raw_obj.bits_from_reference,
            reference=ReferencePoint(raw_obj.reference.value),
            parameter_ref=XtcePath(raw_obj.parameter_ref)
            if raw_obj.parameter_ref is not None
            else None,
        )

    def _to_v1_1(self, policy: DowngradePolicy = DowngradePolicy.STRICT) -> Any:
        raise XtceUnsupportedError(XtceVersion.V1_1, self.__class__.__name__)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ParityType:
        self._enforce_unsupported_field(
            field_name="parameter_ref",
            current_value=self.parameter_ref,
            empty_value=None,
            target_version=XtceVersion.V1_2,
            policy=policy,
        )

        return xtce_1_2.ParityType(
            type_value=xtce_1_2.ParityFormType(self.parity_form.value),
            bits_from_reference=self.bits_from_reference,
            reference=xtce_1_2.ReferencePointType(self.reference.value),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ParityType:
        return xtce_1_3.ParityType(
            type_value=xtce_1_3.ParityFormType(self.parity_form.value),
            bits_from_reference=self.bits_from_reference,
            reference=xtce_1_3.ReferencePointType(self.reference.value),
            parameter_ref=str(self.parameter_ref)
            if self.parameter_ref is not None
            else None,
        )
