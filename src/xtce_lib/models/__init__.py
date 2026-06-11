"""Unified XTCE model module."""

from typing import Any

from xtce_lib.models._base import XtceBaseModel

from .arguments import (
    AbsoluteTimeArgument,
    AggregateArgument,
    ArrayArgument,
    BinaryArgument,
    BooleanArgument,
    EnumeratedArgument,
    FloatArgument,
    IntegerArgument,
    RelativeTimeArgument,
    StringArgument,
)
from .array import Dimension
from .codec import (
    BinaryDataEncoding,
    DataEncoding,
    DiscreteLookupList,
    DynamicValue,
    FloatDataEncoding,
    IntegerDataEncoding,
    StringDataEncoding,
)
from .commands import CommandMetadata
from .common import (
    Alias,
    AncillaryData,
)
from .datatypes import BaseData, IntegerData
from .enums import (
    BitOrder,
    Endian,
    FloatEncoding,
    IntegerEncoding,
    StringEncoding,
    SystemType,
    UnitForm,
    ValidationStatus,
)
from .match import DiscreteLookup, MatchCriteria
from .parameters import (
    AbsoluteTimeParameter,
    AggregateParameter,
    ArrayParameter,
    BinaryParameter,
    BooleanParameter,
    EnumeratedParameter,
    FloatParameter,
    IntegerParameter,
    Parameter,
    RelativeTimeParameter,
    StringParameter,
)
from .processing import (
    CRC,
    XOR,
    BaseCalibrator,
    Calibrator,
    Checksum,
    ContextCalibrator,
    InputAlgorithm,
    InputOutputTriggerAlgorithm,
    LinearAdjustment,
    MathAlgorithm,
    Parity,
    SimpleAlgorithm,
)
from .references import ParameterInstance, ParameterRef
from .space_system import SpaceSystem
from .stream import CustomStream, FixedFrameStream, VariableFrameStream
from .telemetry import TelemetryMetadata

__all__ = [
    "AbsoluteTimeArgument",
    "AggregateArgument",
    "ArrayArgument",
    "BinaryArgument",
    "BooleanArgument",
    "EnumeratedArgument",
    "FloatArgument",
    "IntegerArgument",
    "RelativeTimeArgument",
    "StringArgument",
    "Dimension",
    "BinaryDataEncoding",
    "DataEncoding",
    "DiscreteLookupList",
    "DynamicValue",
    "FloatDataEncoding",
    "IntegerDataEncoding",
    "StringDataEncoding",
    "CommandMetadata",
    "Alias",
    "AncillaryData",
    "BaseData",
    "IntegerData",
    "BitOrder",
    "Endian",
    "FloatEncoding",
    "IntegerEncoding",
    "StringEncoding",
    "SystemType",
    "UnitForm",
    "ValidationStatus",
    "DiscreteLookup",
    "MatchCriteria",
    "AbsoluteTimeParameter",
    "AggregateParameter",
    "ArrayParameter",
    "BinaryParameter",
    "BooleanParameter",
    "EnumeratedParameter",
    "FloatParameter",
    "IntegerParameter",
    "Parameter",
    "RelativeTimeParameter",
    "StringParameter",
    "CRC",
    "XOR",
    "BaseCalibrator",
    "Calibrator",
    "Checksum",
    "ContextCalibrator",
    "InputAlgorithm",
    "InputOutputTriggerAlgorithm",
    "LinearAdjustment",
    "MathAlgorithm",
    "Parity",
    "SimpleAlgorithm",
    "ParameterInstance",
    "ParameterRef",
    "SpaceSystem",
    "CustomStream",
    "FixedFrameStream",
    "VariableFrameStream",
    "TelemetryMetadata",
]


def _rebuild_all_models(
    base_class: type[XtceBaseModel], namespace: dict[str, Any]
) -> None:
    """Recursively find and rebuild all Pydantic models.

    This resolves forward references for all models in the module.
    """
    for subclass in base_class.__subclasses__():
        try:
            subclass.model_rebuild(_types_namespace=namespace)
            _rebuild_all_models(subclass, namespace)
        except Exception as e:
            raise RuntimeError(
                f"Error rebuilding model {subclass.__name__}: {e}"
            ) from e


_rebuild_all_models(XtceBaseModel, globals())
