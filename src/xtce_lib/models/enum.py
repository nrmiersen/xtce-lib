"""Unified XTCE enumerations."""

from enum import Enum


class BitOrder(str, Enum):
    """The bit order of the data encoding."""

    MOST_SIGNIFICANT_BIT_FIRST = "mostSignificantBitFirst"
    LEAST_SIGNIFICANT_BIT_FIRST = "leastSignificantBitFirst"


class Endian(str, Enum):
    """The endianness of the data encoding."""

    BIG = "mostSignificantByteFirst"
    LITTLE = "leastSignificantByteFirst"


class FloatEncoding(str, Enum):
    """The encoding of a floating point value."""

    IEEE754_1985 = "IEEE754_1985"
    IEEE754 = "IEEE754"
    MILSTD_1750_A = "MILSTD_1750A"
    DEC = "DEC"
    IBM = "IBM"
    TI = "TI"


class IntegerEncoding(str, Enum):
    """The encoding of an integer value."""

    UNSIGNED = "unsigned"
    SIGN_MAGNITUDE = "signMagnitude"
    TWOS_COMPLEMENT = "twosComplement"
    ONES_COMPLEMENT = "onesComplement"
    BCD = "BCD"
    PACKED_BCD = "packedBCD"


class StringEncoding(str, Enum):
    """The encoding of a string value.

    Attributes:
        US_ASCII:
        ISO_8859_1:
        WINDOWS_1252:
        UTF_8:
        UTF_16: With UTF-16, encoded bits must be prepended with a Byte Order
            Mark.  This mark indicates whether the data is encoded in big or
            little endian.
        UTF_16_LE: With UTF-16LE, encoded bits will always be represented as
            little endian.  Bits are not prepended with a Byte Order Mark.
        UTF_16_BE: With UTF-16BE, encoded bits will always be represented as big
            endian.  Bits are not prepended with a Byte Order Mark.
        UTF_32: With UTF-32, encoded bits must be prepended with a Byte Order
            Mark.  This mark indicates whether the data is encoded in big or
            little endian.
        UTF_32_LE: With UTF-32LE, encoded bits will always be represented as
            little endian.  Bits are not prepended with a Byte Order Mark.
        UTF_32_BE: With UTF-32BE, encoded bits will always be represented as big
            endian.  Bits are not prepended with a Byte Order Mark.

    """

    US_ASCII = "US-ASCII"
    ISO_8859_1 = "ISO-8859-1"
    WINDOWS_1252 = "Windows-1252"
    UTF_8 = "UTF-8"
    UTF_16 = "UTF-16"
    UTF_16_LE = "UTF-16LE"
    UTF_16_BE = "UTF-16BE"
    UTF_32 = "UTF-32"
    UTF_32_LE = "UTF-32LE"
    UTF_32_BE = "UTF-32BE"


class SystemType(str, Enum):
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
            to tighten the scope of an individual SpaceSystem element.  The
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


class UnitForm(str, Enum):
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
            local native data type.  This is unusual, but present in some cases.
        RAW: The unit of measure for this value refers to the raw binary value
            from the data stream, prior to conversion to the local native data
            type and application of calibrators.

    """

    CALIBRATED = "calibrated"
    UNCALIBRATED = "uncalibrated"
    RAW = "raw"


class ValidationStatus(str, Enum):
    """The validation status of the document."""

    UNKNOWN = "Unknown"
    WORKING = "Working"
    DRAFT = "Draft"
    TEST = "Test"
    VALIDATED = "Validated"
    RELEASED = "Released"
    WITHDRAWN = "Withdrawn"


class RangeForm(str, Enum):
    """Defines inside and outside enumerated terms, where the term outside means the
    range is (-inf, minimum) and (maximum, inf) -- that is a range where acceptable
    values must be less than the minimum and greater than the maximum, and the term
    inside means the range is (minimum, maximum) -- that is acceptable values are
    between the minimum and maximum (either the min or max may be inclusive or
    exclusive).
    """

    OUTSIDE = "outside"
    INSIDE = "inside"


class ChangeSpan(str, Enum):
    """Defines a changePerSecond and changePerSample for use in rate of change alarms.

    Used by ChangeAlarmRangesType.
    """

    CHANGE_PER_SECOND = "changePerSecond"
    CHANGE_PER_SAMPLE = "changePerSample"


class ChangeBasis(str, Enum):
    """Defines absoluteChange and percentageChange for use in rate of change alarms.

    Used by ChangeAlarmRangesType.
    """

    ABSOLUTE_CHANGE = "absoluteChange"
    PERCENTAGE_CHANGE = "percentageChange"


class ConcernLevel(str, Enum):
    """Defines six levels: Normal, Watch, Warning, Distress, Critical and Severe, in
    that order of concern from least to most.

    These level definitions are used throughout the alarm definitions. An
    implementation should interpret these as best to match their uniqueness and
    provide documentation on how this standard maps to their implementation. Not all
    are likely to be provided, with some either ignored, promoted or demoted to
    others, or warned on input. There exist some reasonable usage recommendations in
    the user community.

    Attributes:
        NORMAL: The case of "normal" or "no concern level" is generally the
            default.  This value can be useful when describing an exception or
            disabling when the more typical case is a non-normal concern level.
        WATCH: DEPRECATED: The lowest level of concern.  Systems that support
            only 3 or 4 concern levels have been observed to promote "watch" to
            "warning" during data processing, if this enumeration is not
            explicitly supported.  This value may not exist in future versions of
            this specification.
        WARNING: A level of concern to be interpreted by the user as less than
            the highest possible concern.  This is intended by the specification
            to be quite vague.  The project operational concept will explicitly
            define how these are to be used.
        DISTRESS: A level of concern to be interpreted by the user as greater
            than the least concern but not yet rising to the highest possible
            concern.  This is intended by the specification to be quite vague.
            The project operational concept will explicitly define how these are
            to be used.
        CRITICAL: A level of concern to be interpreted by the user as the highest
            possible concern.  This is intended by the specification to be quite
            vague.  The project operational concept will explicitly define how
            these are to be used.
        SEVERE: DEPRECATED: The highest level of concern.  Systems that support
            only 3 or 4 concern levels have been observed to demote "severe" to
            "critical" during data processing, if this enumeration is not
            explicitly supported.  This value may not exist in future versions of
            this specification.

    """

    NORMAL = "normal"
    WATCH = "watch"
    WARNING = "warning"
    DISTRESS = "distress"
    CRITICAL = "critical"
    SEVERE = "severe"


class TimeUnits(str, Enum):
    """Base time unit of measure.

    It is best practice to avoid days, months, and years due to ambiguity involving
    leap seconds and leap days. If these are used, the system should document how
    the leaps are handled.
    """

    SECONDS = "seconds"
    MILLISECONDS = "milliseconds"
    MICROSECONDS = "microseconds"
    NANOSECONDS = "nanoseconds"
    PICOSECONDS = "picoseconds"
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    MONTHS = "months"
    YEARS = "years"


# TODO TimeAssociationUnitType also exists but is identical to TimeUnitType


class TelemetryDataSource(str, Enum):
    """A telemetered Parameter is one that will have values in telemetry.

    A derived Parameter is one that is calculated, usually by an Algorithm. A
    constant Parameter is one that is used as a constant in the system (e.g. a
    vehicle id). A local Parameter is one that is used purely by the software
    locally (e.g. a ground command counter). A ground Parameter is one that is
    generated by an asset which is not the spacecraft.
    """

    TELEMETERED = "telemetered"
    DERIVED = "derived"
    CONSTANT = "constant"
    LOCAL = "local"
    GROUND = "ground"


class ReferenceLocation(str, Enum):
    """The location may be relative to the start of the container (containerStart),
    relative to the end of the previous entry (previousEntry), relative to the end
    of the container (containerEnd), or relative to the entry that follows this one
    (nextEntry).

    If going forward (containerStart and previousEntry) then the location refers to
    the start of the Entry. If going backwards (containerEnd and nextEntry) then,
    the location refers to the end of the entry.
    """

    CONTAINER_START = "containerStart"
    CONTAINER_END = "containerEnd"
    PREVIOUS_ENTRY = "previousEntry"
    NEXT_ENTRY = "nextEntry"


class Basis(str, Enum):
    """Defines to type of update rates: perSecond and perContainerUpdate.

    See RateInStreamType.
    """

    PER_SECOND = "perSecond"
    PER_CONTAINER_UPDATE = "perContainerUpdate"


class PcmType(str, Enum):
    NRZL = "NRZL"
    NRZM = "NRZM"
    NRZS = "NRZS"
    BI_PHASE_L = "BiPhaseL"
    BI_PHASE_M = "BiPhaseM"
    BI_PHASE_S = "BiPhaseS"


class FlagBit(str, Enum):
    ZEROS = "zeros"
    ONES = "ones"


class ReferencePoint(str, Enum):
    START = "start"
    END = "end"


class ChecksumTypeName(Enum):
    """Attributes:
    UNIX_SUM:
    SUM8:
    SUM16:
    SUM24:
    SUM32:
    FLETCHER4:
    FLETCHER8:
    FLETCHER16:
    FLETCHER32:
    ADLER32:
    LUHN:
    VERHOEFF:
    DAMM:
    CUSTOM: Document a custom checksum algorithm in the InputAlgorithm
        element.

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


class ParityForm(str, Enum):
    EVEN = "Even"
    ODD = "Odd"


class MathOperators(str, Enum):
    """Mathematical operators used in the math operation.

    Behavior of each operator on the stack is described using notation (before --
    after), where "before" represents the stack before execution of the operator and
    "after" represent the stack after execution.

    Attributes:
        PLUS_SIGN: addition (x1 x2 -- x1+x2)
        HYPHEN_MINUS: subtraction (x1 x2 -- x1-x2)
        ASTERISK: multiplication (x1 x2 -- x1*x2)
        SOLIDUS: division (x1 x2 -- x1/x2)
        PERCENT_SIGN: modulo (x1 x2 -- x3) Divide x1 by x2, giving the modulo x3
        CIRCUMFLEX_ACCENT: power function (x1 x2 -- x1**x2)
        Y_X: reverse power function (x1 x2 -- x2**x1)
        LN: natural (base e) logarithm (x -- ln(x))
        LOG: base-10 logarithm (x-- log(x))
        E_X: exponentiation (x -- exp(x))
        VALUE_1_X: inversion (x -- 1/x)
        X: factorial (x -- x!)
        TAN: tangent (x -- tan(x)) radians
        COS: cosine (x -- cos(x)) radians
        SIN: sine (x -- sin(x)) radians
        ATAN: arctangent (x -- atan(x)) radians
        ATAN2: arctangent (x1 x2 -- atan2(x2, x1)) radians
        ACOS: arccosine (x -- acos(x)) radians
        ASIN: arcsine (x -- asin(x)) radians
        TANH: hyperbolic tangent (x -- tanh(x))
        COSH: hyperbolic cosine (x -- cosh(x))
        SINH: hyperbolic sine (x -- sinh(x))
        ATANH: hyperbolic arctangent (x -- atanh(x))
        ACOSH: hyperbolic arccosine (x -- acosh(x))
        ASINH: hyperbolic arcsine (x -- asinh(x))
        SWAP: swap the top two stack items (x1 x2 -- x2 x1)
        DROP: Remove top item from the stack (x -- )
        DUP: Duplicate top item on the stack (x -- x x)
        OVER: Duplicate top item on the stack (x1 x2 -- x1 x2 x1)
        LESS_THAN_SIGN_LESS_THAN_SIGN: signed bitwise left shift (x1 x2 -- x1
            &lt;&lt; x2)
        GREATER_THAN_SIGN_GREATER_THAN_SIGN: signed bitwise right shift (x1 x2 --
            x1 &gt;&gt; x2)
        AMPERSAND: bitwise and (x1 x2 -- x1 &amp; x2)
        VERTICAL_LINE: bitwise or (x1 x2 -- x1 | x2)
        AMPERSAND_AMPERSAND: logical and (x1 x2 -- x1 &amp;&amp; x2)
        VERTICAL_LINE_VERTICAL_LINE: logical or (x1 x2 -- x1 || x2)
        EXCLAMATION_MARK: logical not (x1 x2 -- x1 ! x2)
        ABS: absolute value (x1 -- abs(x1))
        DIV: Euclidean division quotient (x1 -- div(x1))
        INT: integer part (x1 -- int(x1))
        GREATER_THAN_SIGN: greater than x,y (x1 x2 -- x1 &gt; x2)
        GREATER_THAN_SIGN_EQUALS_SIGN: greater than or equal x,y (x1 x2 -- x1
            &gt;= x2)
        LESS_THAN_SIGN: less than x,y (x1 x2 -- x1 &lt; x2)
        LESS_THAN_SIGN_EQUALS_SIGN: less than or equal x,y (x1 x2 -- x1 &lt;= x2)
        EQUALS_SIGN_EQUALS_SIGN: equal x,y (x1 x2 -- x1 == x2)
        EXCLAMATION_MARK_EQUALS_SIGN: not equal x,y (x1 x2 -- x1 != x2)
        MIN: minimum of x,y (x1 x2 -- min(x1, x2))
        MAX: maximum of x,y (x1 x2 -- max(x1, x2))
        XOR: Bitwise exclusive or (XOR) (x1 x2 -- x1 xor x2)
        TILDE: Bitwise not operation (x1 x2 -- x1 ~ x2) The result of this can
            only be 0 or 1

    """

    PLUS_SIGN = "+"
    HYPHEN_MINUS = "-"
    ASTERISK = "*"
    SOLIDUS = "/"
    PERCENT_SIGN = "%"
    CIRCUMFLEX_ACCENT = "^"
    Y_X = "y^x"
    LN = "ln"
    LOG = "log"
    E_X = "e^x"
    VALUE_1_X = "1/x"
    X = "x!"
    TAN = "tan"
    COS = "cos"
    SIN = "sin"
    ATAN = "atan"
    ATAN2 = "atan2"
    ACOS = "acos"
    ASIN = "asin"
    TANH = "tanh"
    COSH = "cosh"
    SINH = "sinh"
    ATANH = "atanh"
    ACOSH = "acosh"
    ASINH = "asinh"
    SWAP = "swap"
    DROP = "drop"
    DUP = "dup"
    OVER = "over"
    LESS_THAN_SIGN_LESS_THAN_SIGN = "<<"
    GREATER_THAN_SIGN_GREATER_THAN_SIGN = ">>"
    AMPERSAND = "&"
    VERTICAL_LINE = "|"
    AMPERSAND_AMPERSAND = "&&"
    VERTICAL_LINE_VERTICAL_LINE = "||"
    EXCLAMATION_MARK = "!"
    ABS = "abs"
    DIV = "div"
    INT = "int"
    GREATER_THAN_SIGN = ">"
    GREATER_THAN_SIGN_EQUALS_SIGN = ">="
    LESS_THAN_SIGN = "<"
    LESS_THAN_SIGN_EQUALS_SIGN = "<="
    EQUALS_SIGN_EQUALS_SIGN = "=="
    EXCLAMATION_MARK_EQUALS_SIGN = "!="
    MIN = "min"
    MAX = "max"
    XOR = "xor"
    TILDE = "~"


class ComparisonOperator(str, Enum):
    """Operators to use when testing a boolean condition for a validity check."""

    EQUALS_SIGN_EQUALS_SIGN = "=="
    EXCLAMATION_MARK_EQUALS_SIGN = "!="
    LESS_THAN_SIGN = "<"
    LESS_THAN_SIGN_EQUALS_SIGN = "<="
    GREATER_THAN_SIGN = ">"
    GREATER_THAN_SIGN_EQUALS_SIGN = ">="


class Radix(str, Enum):
    """Specifies the number base."""

    DECIMAL = "Decimal"
    HEXADECIMAL = "Hexadecimal"
    OCTAL = "Octal"
    BINARY = "Binary"


class FloatingPointNotation(str, Enum):
    NORMAL = "normal"
    SCIENTIFIC = "scientific"
    ENGINEERING = "engineering"


class EpochTime(str, Enum):
    """Union values of common epoch definitions for document convenience."""

    TAI = "TAI"
    J2000 = "J2000"
    UNIX = "UNIX"
    GPS = "GPS"
