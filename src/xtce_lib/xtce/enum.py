"""Unified XTCE enumerations."""

import operator
from enum import StrEnum
from typing import Any, Callable, Self

from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseEnum

# TODO update all docstrings. not worried for now while just trying to get alpha released


class BitOrder(StrEnum):
    """The bit order of the data encoding."""

    MOST_SIGNIFICANT_BIT_FIRST = "mostSignificantBitFirst"
    LEAST_SIGNIFICANT_BIT_FIRST = "leastSignificantBitFirst"


class Endian(StrEnum):
    """The endianness of the data encoding."""

    BIG = "mostSignificantByteFirst"
    LITTLE = "leastSignificantByteFirst"


class FloatEncoding(XtceBaseEnum):
    """The encoding of a floating point value."""

    IEEE754_1985 = "IEEE754_1985"
    IEEE754 = "IEEE754"
    MILSTD_1750_A = "MILSTD_1750A"
    DEC = "DEC"
    IBM = "IBM"
    TI = "TI"

    @classmethod
    def _from_v1_1(
        cls: type[Self], encoding: xtce_1_1.FloatDataEncodingTypeEncoding
    ) -> Self:
        return cls(encoding.value)

    @classmethod
    def _from_v1_2(cls: type[Self], encoding: xtce_1_2.FloatEncodingType) -> Self:
        return cls(encoding.value)

    @classmethod
    def _from_v1_3(cls: type[Self], encoding: xtce_1_3.FloatEncodingType) -> Self:
        return cls(encoding.value)

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.FloatDataEncodingTypeEncoding:
        # XTCE 1.1 only supports IEEE754_1985 and MILSTD_1750A
        try:
            return xtce_1_1.FloatDataEncodingTypeEncoding(self.value)
        except ValueError:
            return self._enforce_unmapped_value(
                XtceVersion.V1_1,
                policy,
                fallback=xtce_1_1.FloatDataEncodingTypeEncoding.IEEE754_1985,
            )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.FloatEncodingType:
        return xtce_1_2.FloatEncodingType(self.value)

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.FloatEncodingType:
        return xtce_1_3.FloatEncodingType(self.value)


class IntegerEncoding(XtceBaseEnum):
    """The encoding of an integer value."""

    UNSIGNED = "unsigned"
    SIGN_MAGNITUDE = "signMagnitude"
    TWOS_COMPLEMENT = "twosComplement"
    ONES_COMPLEMENT = "onesComplement"
    BCD = "BCD"
    PACKED_BCD = "packedBCD"

    @classmethod
    def _from_v1_1(
        cls: type[Self], encoding: xtce_1_1.IntegerDataEncodingTypeEncoding
    ) -> Self:
        # XTCE 1.1 misspells "complement" as "compliment"
        name = {
            "twosCompliment": "TWOS_COMPLEMENT",
            "onesCompliment": "ONES_COMPLEMENT",
        }.get(encoding.value)
        return cls[name] if name is not None else cls(encoding.value)

    @classmethod
    def _from_v1_2(cls: type[Self], encoding: xtce_1_2.IntegerEncodingType) -> Self:
        return cls(encoding.value)

    @classmethod
    def _from_v1_3(cls: type[Self], encoding: xtce_1_3.IntegerEncodingType) -> Self:
        return cls(encoding.value)

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.IntegerDataEncodingTypeEncoding:
        # XTCE 1.1 misspells "complement" as "compliment"
        name = {
            "TWOS_COMPLEMENT": "TWOS_COMPLIMENT",
            "ONES_COMPLEMENT": "ONES_COMPLIMENT",
        }.get(self.name, self.name)
        return xtce_1_1.IntegerDataEncodingTypeEncoding[name]

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.IntegerEncodingType:
        return xtce_1_2.IntegerEncodingType(self.value)

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.IntegerEncodingType:
        return xtce_1_3.IntegerEncodingType(self.value)


class StringEncoding(XtceBaseEnum):
    """The encoding of a string value."""

    US_ASCII = "US-ASCII"
    ISO_8859_1 = "ISO-8859-1"
    WINDOWS_1252 = "Windows-1252"
    UTF_8 = "UTF-8"
    UTF_16 = "UTF-16"
    """Encoded bits must be prepended with a byte order mark.

    The byte order mark indicates if the encoding is big or little endian.

    """

    UTF_16_LE = "UTF-16LE"
    """Encoded bits will always be represented as little endian.

    Bits are not prepended with a byte order mark.

    """

    UTF_16_BE = "UTF-16BE"
    """Encoded bits will always be represented as big endian.

    Bits are not prepended with a byte order mark.

    """

    UTF_32 = "UTF-32"
    """Encoded bits must be prepended with a byte order mark.

    The byte order mark indicates if the encoding is big or little endian.

    """

    UTF_32_LE = "UTF-32LE"
    """Encoded bits will always be represented as little endian.

    Bits are not prepended with a byte order mark.

    """

    UTF_32_BE = "UTF-32BE"
    """Encoded bits will always be represented as big endian.

    Bits are not prepended with a byte order mark.

    """

    @classmethod
    def _from_v1_1(
        cls: type[Self], encoding: xtce_1_1.StringDataEncodingTypeEncoding
    ) -> Self:
        return cls(encoding.value)

    @classmethod
    def _from_v1_2(cls: type[Self], encoding: xtce_1_2.StringEncodingType) -> Self:
        return cls(encoding.value)

    @classmethod
    def _from_v1_3(cls: type[Self], encoding: xtce_1_3.StringEncodingType) -> Self:
        return cls(encoding.value)

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.StringDataEncodingTypeEncoding:
        # XTCE 1.1 only has UTF-8 and UTF-16
        try:
            return xtce_1_1.StringDataEncodingTypeEncoding[self.name]
        except KeyError:
            return self._enforce_unmapped_value(
                XtceVersion.V1_1,
                policy,
                fallback=xtce_1_1.StringDataEncodingTypeEncoding.UTF_8,
            )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.StringEncodingType:
        return xtce_1_2.StringEncodingType[self.name]

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.StringEncodingType:
        return xtce_1_3.StringEncodingType[self.name]


class SystemType(StrEnum):
    """The type attribute represents what from a space enterprise this SpaceSystem
    element represents.

    See the enumerations for specific details. Unknown is the default for backwards
    compatibility, though it should be avoided in newer documents.

    Attributes:
        ASSET: An form of asset monitored and/or controlled by the enterprise
            that may participate in a larger group and may be subdivided into
            internal components.
        ASSET_GROUP: A grouping of assets that make sense to aggregate together
            in the data model, such as a fleet or constellation.
        ASSET_COMPONENT: Internal systems of assets permit managing the structure
            of XTCE documents by decomposing the internal structures of interest
            to tighten the scope of an individual SpaceSystem element. The
            XInclude facility is also available at the SpaceSystem element for
            managing the size of XTCE documents, in addition to the internal
            organization.
        UNKNOWN: The default enumeration is meant for backwards compatibility
            with earlier versions and should be avoided.

    """

    ASSET = "asset"
    ASSET_GROUP = "assetGroup"
    ASSET_COMPONENT = "assetComponent"
    UNKNOWN = "unknown"


class UnitForm(StrEnum):
    """Defines enumerated values to categorize a unit associated with a telemetered
    value.

    Typically the unit refers to the calibrated (engineering) value. In some cases
    the unit may be associated with the uncalibrated or raw values. Uncalibrated and
    raw here are typically synonymous, but there are exceptions.

    Attributes:
        CALIBRATED: The unit of measure for this value refers to the
            engineer/calibrated value.
        UNCALIBRATED: The unit of measure for this value refers to the pre-
            calibrated data, after extraction from the data stream, when in the
            local native data type. This is unusual, but present in some cases.
        RAW: The unit of measure for this value refers to the raw binary value
            from the data stream, prior to conversion to the local native data
            type and application of calibrators.

    """

    CALIBRATED = "calibrated"
    UNCALIBRATED = "uncalibrated"
    RAW = "raw"


class ValidationStatus(StrEnum):
    """The validation status of the document."""

    UNKNOWN = "Unknown"
    WORKING = "Working"
    DRAFT = "Draft"
    TEST = "Test"
    VALIDATED = "Validated"
    RELEASED = "Released"
    WITHDRAWN = "Withdrawn"


class RangeForm(StrEnum):
    """Defines the valid range forms.

    Attributes:
        OUTSIDE: The range is (-inf, minimum) and (maximum, inf) - that is a range where
            acceptable values must be less than the minimum and greater than the
            maximum.
        INSIDE: The range is (minimum, maximum) - that is acceptable values are between
            the minimum and maximum (either the min or max may be inclusive or
            exclusive).

    """

    OUTSIDE = "outside"
    """The range is (-inf, minimum) and (maximum, inf) - that is a range where acceptable values must be less than the minimum and greater than the maximum."""

    INSIDE = "inside"
    """The range is (minimum, maximum) - that is acceptable values are between the minimum and maximum (either the min or max may be inclusive or exclusive)."""


class ChangeSpan(StrEnum):
    """Defines the change span options for a change alarm."""

    CHANGE_PER_SECOND = "changePerSecond"
    """The change rate is measured per second."""

    CHANGE_PER_SAMPLE = "changePerSample"
    """The change rate is measured per sample."""


class ChangeBasis(StrEnum):
    """Defines the basis for measuring the change rate in a change alarm."""

    ABSOLUTE_CHANGE = "absoluteChange"
    """The change rate is measured as an absolute change."""

    PERCENTAGE_CHANGE = "percentageChange"
    """The change rate is measured as a percentage change."""


class ConcernLevel(StrEnum):
    """Defines six levels of concern for alarms: Normal, Watch, Warning, Distress,
    Critical, and Severe, in that order of concern from least to most.
    """

    NORMAL = "normal"
    WATCH = "watch"
    WARNING = "warning"
    DISTRESS = "distress"
    CRITICAL = "critical"
    SEVERE = "severe"


class TimeUnits(XtceBaseEnum):
    """Base time units of measure.

    It is best practice to avoid days, months, and years due to ambiguity involving leap
    seconds and leap days. If these are used, the system should document how the leaps
    are handled.

    """

    SECONDS = "seconds"
    MILLISECONDS = "milliseconds"
    """Not supported by XTCE 1.2."""

    MICROSECONDS = "microseconds"
    """Not supported by XTCE 1.2."""

    NANOSECONDS = "nanoseconds"
    """Not supported by XTCE 1.2."""

    PICOSECONDS = "picoseconds"
    MINUTES = "minutes"
    """Not supported by XTCE 1.2."""

    HOURS = "hours"
    """Not supported by XTCE 1.2."""

    DAYS = "days"
    MONTHS = "months"
    YEARS = "years"

    @classmethod
    def _from_v1_1(cls: type[Self], unit: xtce_1_1.TimeUnits) -> Self:
        mapping = {
            xtce_1_1.TimeUnits.SECONDS: "seconds",
            xtce_1_1.TimeUnits.PICO_SECONDS: "picoseconds",
            xtce_1_1.TimeUnits.DAYS: "days",
            xtce_1_1.TimeUnits.MONTHS: "months",
            xtce_1_1.TimeUnits.YEARS: "years",
        }

        return cls(mapping[unit])

    @classmethod
    def _from_v1_2(cls: type[Self], unit: xtce_1_2.TimeUnitsType) -> Self:
        mapping = {
            xtce_1_2.TimeUnitsType.SECONDS: "seconds",
            xtce_1_2.TimeUnitsType.PICO_SECONDS: "picoseconds",
            xtce_1_2.TimeUnitsType.DAYS: "days",
            xtce_1_2.TimeUnitsType.MONTHS: "months",
            xtce_1_2.TimeUnitsType.YEARS: "years",
        }

        return cls(mapping[unit])

    @classmethod
    def _from_v1_3(cls: type[Self], unit: xtce_1_3.TimeUnitsType) -> Self:
        return cls(unit.value)

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.TimeUnits:
        mapping = {
            TimeUnits.SECONDS: xtce_1_1.TimeUnits.SECONDS,
            TimeUnits.PICOSECONDS: xtce_1_1.TimeUnits.PICO_SECONDS,
            TimeUnits.DAYS: xtce_1_1.TimeUnits.DAYS,
            TimeUnits.MONTHS: xtce_1_1.TimeUnits.MONTHS,
            TimeUnits.YEARS: xtce_1_1.TimeUnits.YEARS,
        }

        try:
            return mapping[self]
        except KeyError:
            return self._enforce_unmapped_value(
                XtceVersion.V1_1,
                policy,
                fallback=xtce_1_1.TimeUnits.SECONDS,
            )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.TimeUnitsType:
        mapping = {
            TimeUnits.SECONDS: xtce_1_2.TimeUnitsType.SECONDS,
            TimeUnits.PICOSECONDS: xtce_1_2.TimeUnitsType.PICO_SECONDS,
            TimeUnits.DAYS: xtce_1_2.TimeUnitsType.DAYS,
            TimeUnits.MONTHS: xtce_1_2.TimeUnitsType.MONTHS,
            TimeUnits.YEARS: xtce_1_2.TimeUnitsType.YEARS,
        }

        try:
            return mapping[self]
        except KeyError:
            return self._enforce_unmapped_value(
                XtceVersion.V1_2,
                policy,
                fallback=xtce_1_2.TimeUnitsType.SECONDS,
            )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.TimeUnitsType:
        return xtce_1_3.TimeUnitsType(self.value)


class TimeAssociationUnits(XtceBaseEnum):
    """Base time units of measure.

    It is best practice to avoid days, months, and years due to ambiguity involving leap
    seconds and leap days. If these are used, the system should document how the leaps
    are handled.

    """

    SECONDS = "seconds"
    MILLISECONDS = "milliseconds"
    MICROSECONDS = "microseconds"
    NANOSECONDS = "nanoseconds"
    PICOSECONDS = "picoseconds"
    """Not supported by XTCE 1.2."""

    MINUTES = "minutes"
    HOURS = "hours"
    """Not supported by XTCE 1.2."""

    DAYS = "days"
    MONTHS = "months"
    """Not supported by XTCE 1.2."""

    YEARS = "years"

    @classmethod
    def _from_v1_2(cls: type[Self], unit: xtce_1_2.TimeAssociationUnitType) -> Self:
        mapping = {
            xtce_1_2.TimeAssociationUnitType.SI_SECOND: "seconds",
            xtce_1_2.TimeAssociationUnitType.SI_MILLSECOND: "milliseconds",
            xtce_1_2.TimeAssociationUnitType.SI_MICROSECOND: "microseconds",
            xtce_1_2.TimeAssociationUnitType.SI_NANOSECOND: "nanoseconds",
            xtce_1_2.TimeAssociationUnitType.MINUTE: "minutes",
            xtce_1_2.TimeAssociationUnitType.DAY: "days",
            xtce_1_2.TimeAssociationUnitType.JULIAN_YEAR: "years",
        }

        return cls(mapping[unit])

    @classmethod
    def _from_v1_3(cls: type[Self], unit: xtce_1_3.TimeAssociationUnitType) -> Self:
        return cls(unit.value)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.TimeAssociationUnitType:
        mapping = {
            TimeAssociationUnits.SECONDS: xtce_1_2.TimeAssociationUnitType.SI_SECOND,
            TimeAssociationUnits.MILLISECONDS: xtce_1_2.TimeAssociationUnitType.SI_MILLSECOND,
            TimeAssociationUnits.MICROSECONDS: xtce_1_2.TimeAssociationUnitType.SI_MICROSECOND,
            TimeAssociationUnits.NANOSECONDS: xtce_1_2.TimeAssociationUnitType.SI_NANOSECOND,
            TimeAssociationUnits.MINUTES: xtce_1_2.TimeAssociationUnitType.MINUTE,
            TimeAssociationUnits.DAYS: xtce_1_2.TimeAssociationUnitType.DAY,
            TimeAssociationUnits.YEARS: xtce_1_2.TimeAssociationUnitType.JULIAN_YEAR,
        }

        try:
            return mapping[self]
        except KeyError:
            return self._enforce_unmapped_value(
                XtceVersion.V1_2,
                policy,
                fallback=xtce_1_2.TimeAssociationUnitType.SI_SECOND,
            )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.TimeAssociationUnitType:
        return xtce_1_3.TimeAssociationUnitType(self.value)


class TelemetryDataSource(StrEnum):
    """A telemetered Parameter is one that will have values in telemetry.

    A derived Parameter is one that is calculated, usually by an Algorithm. A constant
    Parameter is one that is used as a constant in the system (e.g. a vehicle id). A
    local Parameter is one that is used purely by the software locally (e.g. a ground
    command counter). A ground Parameter is one that is generated by an asset which is
    not the spacecraft.

    """

    TELEMETERED = "telemetered"
    DERIVED = "derived"
    CONSTANT = "constant"
    LOCAL = "local"
    GROUND = "ground"


class ReferenceLocation(StrEnum):
    """The location may be relative to the start of the container (containerStart),
    relative to the end of the previous entry (previousEntry), relative to the end of
    the container (containerEnd), or relative to the entry that follows this one
    (nextEntry).

    If going forward (containerStart and previousEntry) then the location refers to the
    start of the Entry. If going backwards (containerEnd and nextEntry) then, the
    location refers to the end of the entry.

    """

    CONTAINER_START = "containerStart"
    CONTAINER_END = "containerEnd"
    PREVIOUS_ENTRY = "previousEntry"
    NEXT_ENTRY = "nextEntry"


class Basis(StrEnum):
    """The basis for the rate of updates.

    Attributes:
        PER_SECOND: The rate is measured per second.
        PER_CONTAINER_UPDATE: The rate is measured per container update.

    """

    PER_SECOND = "perSecond"
    """The rate is measured per second."""

    PER_CONTAINER_UPDATE = "perContainerUpdate"
    """The rate is measured per container update."""


class PcmType(StrEnum):
    """The type of PCM encoding.

    Attributes:
        NRZL: Non-return-to-zero-level encoding.
        NRZM: Non-return-to-zero-mark encoding.
        NRZS: Non-return-to-zero-space encoding.
        BI_PHASE_L: Bi-phase-level encoding.
        BI_PHASE_M: Bi-phase-mark encoding.
        BI_PHASE_S: Bi-phase-space encoding.

    """

    NRZL = "NRZL"
    """Non-return-to-zero-level encoding."""

    NRZM = "NRZM"
    """Non-return-to-zero-mark encoding."""

    NRZS = "NRZS"
    """Non-return-to-zero-space encoding."""

    BI_PHASE_L = "BiPhaseL"
    """Bi-phase-level encoding."""

    BI_PHASE_M = "BiPhaseM"
    """Bi-phase-mark encoding."""

    BI_PHASE_S = "BiPhaseS"
    """Bi-phase-space encoding."""


class FlagBit(StrEnum):
    """The type of bits used in a flag.

    Attributes:
        ZEROS: The flag is composed of zeros.
        ONES: The flag is composed of ones.

    """

    ZEROS = "zeros"
    """The flag is composed of zeros."""

    ONES = "ones"
    """The flag is composed of ones."""


class ReferencePoint(StrEnum):
    """The reference point from which the bits are counted.

    Attributes:
        START: The start of the reference.
        END: The end of the reference.

    """

    START = "start"
    """The start of the reference."""
    END = "end"
    """The end of the reference."""


class ChecksumType(StrEnum):
    """The available checksum types.

    Attributes:
        UNIX_SUM
        SUM8
        SUM16
        SUM24
        SUM32
        FLETCHER4
        FLETCHER8
        FLETCHER16
        FLETCHER32
        ADLER32
        LUHN
        VERHOEFF
        DAMM
        CUSTOM

    """

    UNIX_SUM = "unix_sum"
    SUM8 = "sum8"
    SUM16 = "sum16"
    SUM24 = "sum24"
    SUM32 = "sum32"
    FLETCHER4 = "fletcher4"
    FLETCHER8 = "fletcher8"
    FLETCHER16 = "fletcher16"
    FLETCHER32 = "fletcher32"
    ADLER32 = "adler32"
    LUHN = "luhn"
    VERHOEFF = "verhoeff"
    DAMM = "damm"
    CUSTOM = "custom"


class ParityForm(StrEnum):
    """Defines the form of parity.

    Attributes:
        EVEN: Even parity.
        ODD: Odd parity.

    """

    EVEN = "Even"
    """Even parity."""
    ODD = "Odd"
    """Odd parity."""


class MathOperator(StrEnum):
    """Mathematical operators used in math operations.

        Available operator groups:
        - Arithmetic: ADD, SUBTRACT, MULTIPLY, DIVIDE, MODULO, POWER, REVERSE_POWER
        - Scalar math: MIN, MAX, EXP, LN, LOG, RECIPROCAL, FACTORIAL, ABS, DIV, INT
        - Trigonometric: COS, SIN, TAN, ACOS, ASIN, ATAN, ATAN2
        - Hyperbolic: COSH, SINH, TANH, ACOSH, ASINH, ATANH
        - Stack: DROP, DUP, OVER, SWAP
        - Bitwise: LEFT_SHIFT, RIGHT_SHIFT, BITWISE_AND, BITWISE_OR, BITWISE_XOR,
            BITWISE_NOT
        - Logical: LOGICAL_AND, LOGICAL_OR, LOGICAL_NOT
        - Comparison: EQUAL, NOT_EQUAL, GREATER_THAN, GREATER_THAN_OR_EQUAL,
            LESS_THAN, LESS_THAN_OR_EQUAL

    Stack behavior is described using the notation ``before -- after``.

    """

    ADD = "+"
    """Addition: ``x1 x2 -- x1+x2``."""
    SUBTRACT = "-"
    """Subtraction: ``x1 x2 -- x1-x2``."""

    MULTIPLY = "*"
    """Multiplication: ``x1 x2 -- x1*x2``."""

    DIVIDE = "/"
    """Division: ``x1 x2 -- x1/x2``."""

    MODULO = "%"
    """Modulo: ``x1 x2 -- x3`` where ``x3`` is the remainder of ``x1 / x2``."""

    POWER = "^"
    """Power function: ``x1 x2 -- x1**x2``."""

    REVERSE_POWER = "y^x"
    """Reverse power function: ``x1 x2 -- x2**x1``."""

    MIN = "min"
    """Minimum of two values: ``x1 x2 -- min(x1, x2)``."""

    MAX = "max"
    """Maximum of two values: ``x1 x2 -- max(x1, x2)``."""

    EXP = "e^x"
    """Exponentiation: ``x -- exp(x)``."""

    LN = "ln"
    """Natural logarithm: ``x -- ln(x)``."""

    LOG = "log"
    """Base-10 logarithm: ``x -- log(x)``."""

    RECIPROCAL = "1/x"
    """Inversion: ``x -- 1/x``."""

    FACTORIAL = "x!"
    """Factorial: ``x -- x!``."""

    ABS = "abs"
    """Absolute value: ``x -- abs(x)``."""

    DIV = "div"
    """Euclidean division quotient: ``x -- div(x)``."""

    INT = "int"
    """Integer part: ``x -- int(x)``."""

    COS = "cos"
    """Cosine in radians: ``x -- cos(x)``."""

    SIN = "sin"
    """Sine in radians: ``x -- sin(x)``."""

    TAN = "tan"
    """Tangent in radians: ``x -- tan(x)``."""

    ACOS = "acos"
    """Arccosine in radians: ``x -- acos(x)``."""

    ASIN = "asin"
    """Arcsine in radians: ``x -- asin(x)``."""

    ATAN = "atan"
    """Arctangent in radians: ``x -- atan(x)``."""

    ATAN2 = "atan2"
    """Two-argument arctangent in radians: ``x1 x2 -- atan2(x2, x1)``."""

    COSH = "cosh"
    """Hyperbolic cosine: ``x -- cosh(x)``."""

    SINH = "sinh"
    """Hyperbolic sine: ``x -- sinh(x)``."""

    TANH = "tanh"
    """Hyperbolic tangent: ``x -- tanh(x)``."""

    ACOSH = "acosh"
    """Hyperbolic arccosine: ``x -- acosh(x)``."""

    ASINH = "asinh"
    """Hyperbolic arcsine: ``x -- asinh(x)``."""

    ATANH = "atanh"
    """Hyperbolic arctangent: ``x -- atanh(x)``."""

    DROP = "drop"
    """Remove the top item from the stack: ``x --``."""

    DUP = "dup"
    """Duplicate the top item on the stack: ``x -- x x``."""

    OVER = "over"
    """Duplicate the second item onto the top of the stack: ``x1 x2 -- x1 x2 x1``."""

    SWAP = "swap"
    """Swap the top two stack items: ``x1 x2 -- x2 x1``."""

    LEFT_SHIFT = "<<"
    """Signed bitwise left shift: ``x1 x2 -- x1 << x2``."""

    RIGHT_SHIFT = ">>"
    """Signed bitwise right shift: ``x1 x2 -- x1 >> x2``."""

    BITWISE_AND = "&"
    """Bitwise and: ``x1 x2 -- x1 & x2``."""

    BITWISE_OR = "|"
    """Bitwise or: ``x1 x2 -- x1 | x2``."""

    BITWISE_XOR = "xor"
    """Bitwise exclusive or: ``x1 x2 -- x1 xor x2``."""

    BITWISE_NOT = "~"
    """Bitwise not: ``x -- ~x``.

    The result can only be 0 or 1.

    """

    LOGICAL_AND = "&&"
    """Logical and: ``x1 x2 -- x1 && x2``."""

    LOGICAL_OR = "||"
    """Logical or: ``x1 x2 -- x1 || x2``."""

    LOGICAL_NOT = "!"
    """Logical not: ``x -- !x``."""

    EQUAL = "=="
    """Equal to: ``x1 x2 -- x1 == x2``."""

    NOT_EQUAL = "!="
    """Not equal to: ``x1 x2 -- x1 != x2``."""

    GREATER_THAN = ">"
    """Greater than: ``x1 x2 -- x1 > x2``."""

    GREATER_THAN_OR_EQUAL = ">="
    """Greater than or equal to: ``x1 x2 -- x1 >= x2``."""

    LESS_THAN = "<"
    """Less than: ``x1 x2 -- x1 < x2``."""

    LESS_THAN_OR_EQUAL = "<="
    """Less than or equal to: ``x1 x2 -- x1 <= x2``."""

    @property
    def required_operands(self) -> int:
        """The number of operands this operator pops off the stack."""
        if self in {
            self.EXP,
            self.LN,
            self.LOG,
            self.RECIPROCAL,
            self.FACTORIAL,
            self.ABS,
            self.DIV,
            self.INT,
            self.COS,
            self.SIN,
            self.TAN,
            self.ACOS,
            self.ASIN,
            self.ATAN,
            self.COSH,
            self.SINH,
            self.TANH,
            self.ACOSH,
            self.ASINH,
            self.ATANH,
            self.DROP,
            self.DUP,
            self.BITWISE_NOT,
            self.LOGICAL_NOT,
        }:
            return 1
        if self in {
            self.ADD,
            self.SUBTRACT,
            self.MULTIPLY,
            self.DIVIDE,
            self.MODULO,
            self.POWER,
            self.REVERSE_POWER,
            self.MIN,
            self.MAX,
            self.ATAN2,
            self.OVER,
            self.SWAP,
            self.LEFT_SHIFT,
            self.RIGHT_SHIFT,
            self.BITWISE_AND,
            self.BITWISE_OR,
            self.BITWISE_XOR,
            self.LOGICAL_AND,
            self.LOGICAL_OR,
            self.EQUAL,
            self.NOT_EQUAL,
            self.GREATER_THAN,
            self.GREATER_THAN_OR_EQUAL,
            self.LESS_THAN,
            self.LESS_THAN_OR_EQUAL,
        }:
            return 2
        raise ValueError(f"unknown operator: {self}")

    @property
    def pushed_operands(self) -> int:
        """The number of results this operator pushes back onto the stack."""
        if self == self.DROP:
            return 0  # (x -- )
        if self == self.DUP:
            return 2  # (x -- x x)
        if self == self.SWAP:
            return 2  # (x1 x2 -- x2 x1)
        if self == self.OVER:
            return 3  # (x1 x2 -- x1 x2 x1)
        return 1


class ComparisonOperator(StrEnum):
    """Comparison operators for use in conditions."""

    EQ = "=="
    """Equal to."""

    NEQ = "!="
    """Not equal to."""

    LT = "<"
    """Less than."""

    LTE = "<="
    """Less than or equal to."""

    GT = ">"
    """Greater than."""

    GTE = ">="
    """Greater than or equal to."""

    @classmethod
    def _from_v1_1(cls: type[Self], unit: xtce_1_1.ComparisonOperatorsType) -> Self:
        return cls(unit.value)

    @classmethod
    def _from_v1_2(cls: type[Self], unit: xtce_1_2.ComparisonOperatorsType) -> Self:
        return cls(unit.value)

    @classmethod
    def _from_v1_3(cls: type[Self], unit: xtce_1_3.ComparisonOperatorsType) -> Self:
        return cls(unit.value)

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.ComparisonOperatorsType:
        return xtce_1_1.ComparisonOperatorsType(self.value)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ComparisonOperatorsType:
        return xtce_1_2.ComparisonOperatorsType(self.value)

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ComparisonOperatorsType:
        return xtce_1_3.ComparisonOperatorsType(self.value)

    @property
    def func(self) -> Callable[[Any, Any], bool]:
        """Return the Python operator module function for this comparison."""
        mapping = {
            self.EQ: operator.eq,
            self.NEQ: operator.ne,
            self.LT: operator.lt,
            self.LTE: operator.le,
            self.GT: operator.gt,
            self.GTE: operator.ge,
        }
        return mapping[self]

    def __call__(self, left: Any, right: Any) -> bool:
        """Evaluate this comparison operator for two operands."""
        return self.func(left, right)


class Radix(StrEnum):
    """Define the radix for numerical values."""

    DECIMAL = "Decimal"
    """Decimal radix (i.e. 1, 2, 3, ...)."""

    HEXADECIMAL = "Hexadecimal"
    """Hexadecimal radix (i.e. 0x1, 0x2, 0x3, ...)."""

    OCTAL = "Octal"
    """Octal radix (i.e. 0o1, 0o2, 0o3, ...)."""

    BINARY = "Binary"
    """Binary radix (i.e. 0b1, 0b10, 0b11, ...)."""


class FloatingPointNotation(StrEnum):
    """Define the notation to use for floating point numbers."""

    NORMAL = "normal"
    """Normal floating point notation (e.g., 123.45)."""
    SCIENTIFIC = "scientific"
    """Scientific floating point notation (e.g., 1.2345e2)."""

    ENGINEERING = "engineering"
    """Engineering floating point notation (e.g., 123.45e0)."""


class EpochTime(StrEnum):
    """Union values of common epoch definitions for document convenience."""

    TAI = "TAI"
    J2000 = "J2000"
    UNIX = "UNIX"
    GPS = "GPS"


class ConsequenceLevel(StrEnum):
    """Defines the criticality level of a command.

    Criticality levels follow ISO 14950.

    Attributes:
        NORMAL: Normal command. Corresponds to ISO 14950 Level D telecommand
            criticality.
        VITAL: Command that is not a critical command but is essential to the
            success of the mission and, if sent at the wrong time, could cause
            momentary loss of the mission. Corresponds to ISO 14950 Level C
            telecommand criticality.
        CRITICAL: Command that, if executed at the wrong time or in the wrong
            configuration, could cause irreversible loss or damage for the
            mission. Corresponds to ISO 14950 Level B telecommand criticality.
            Some space programs have called this "restricted" and may be
            implemented with a secondary confirmation before transmission.
        FORBIDDEN: Command that is not expected to be used for nominal or
            foreseeable contingency operations, that is included for unforeseen
            contingency operations, and that could cause irreversible damage if
            executed at the wrong time or in the wrong configuration.
            Corresponds to ISO 14950 Level A telecommand criticality. Some space
            programs have called this "prohibited".
        USER1: In the event that a program uses this value, that program will
            need to define the meaning of this value to their system.
        USER2: In the event that a program uses this value, that program will
            need to define the meaning of this value to their system.

    """

    NORMAL = "normal"
    VITAL = "vital"
    CRITICAL = "critical"
    FORBIDDEN = "forbidden"
    USER1 = "user1"
    USER2 = "user2"


class VerifierType(StrEnum):
    """An enumerated list of verifier types."""

    RELEASE = "release"
    TRANSFERRED_TO_RANGE = "transferredToRange"
    SENT_FROM_RANGE = "sentFromRange"
    RECEIVED = "received"
    ACCEPTED = "accepted"
    QUEUED = "queued"
    EXECUTING = "executing"
    COMPLETE = "complete"
    FAILED = "failed"


class TimeWindowIsRelativeTo(StrEnum):
    """Defines the reference point for a time window."""

    COMMAND_RELEASE = "commandRelease"
    """Reference point is the command release time."""
    TIME_LAST_VERIFIER_PASSED = "timeLastVerifierPassed"
    """Reference point is the time the last verifier passed."""
