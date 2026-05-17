from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime, XmlDuration

__NAMESPACE__ = "http://www.omg.org/spec/XTCE/20250214"


@dataclass(kw_only=True)
class AlgorithmTextType:
    """
    This optional element may be used to enter Pseudo or actual code for the
    algorithm.

    The language for the algorithm is specified with the language attribute.
    """

    value: str = field(default="")
    language: str = field(
        default="pseudo",
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class AliasType:
    """
    Used to contain an alias (alternate) name or ID for the object.

    For example, a parameter may have a mnemonic, an on-board id, and special IDs
    used by various ground software applications; all of these are alias's. Some
    ground system processing equipment has some severe naming restrictions on
    parameters (e.g., names must less then 12 characters, single case or integral
    id's only); their alias's provide a means of capturing each name in a
    "nameSpace". Note: the name is not reference-able (it cannot be used in a name
    reference substituting for the name of the item of interest). See
    NameDescriptionType.

    Attributes:
        name_space: Aliases should be grouped together in a "namespace" so that
            they can be switched in and out of data extractions.  The namespace
            generally identifies the purpose of the alternate name, whether for
            software variable names, additional operator names, or whatever the
            purpose.
        alias: The alternate name or ID to use.  The alias does not have the
            restrictions that apply to name attributes.  This is useful for
            capturing legacy identifiers for systems with unusual naming
            conventions.  It is also useful for capturing variable names in
            software, amongst other things.
    """

    name_space: str = field(
        metadata={
            "name": "nameSpace",
            "type": "Attribute",
        }
    )
    alias: str = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class AncillaryDataType:
    """
    Use for any other data associated with a named item.

    May be used to include administrative data (e.g., version, CM or tags) or
    potentially any MIME type. Data may be included or given as an href.

    Attributes:
        value:
        name: Identifier for this Ancillary Data characteristic, feature, or
            data.
        mime_type: Optional text encoding method for the element text content of
            this element.  The default is "text/plain".
        href: Optional Uniform Resource Identifier for this characteristic,
            feature, or data.
    """

    value: str = field(default="")
    name: str = field(
        metadata={
            "type": "Attribute",
        }
    )
    mime_type: str = field(
        default="text/plain",
        metadata={
            "name": "mimeType",
            "type": "Attribute",
        },
    )
    href: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArgumentAssignmentType:
    """
    Describe an assignment of an argument with a calibrated/engineering value.

    See ArgumentAssignmentListType.

    Attributes:
        argument_name: The named argument from the base MetaCommand to
            assign/restrict with a value.
        argument_value: Specify value as a string compliant with the XML schema
            (xs) type specified for each XTCE type: integer=xs:integer;
            float=xs:double; string=xs:string; boolean=xs:boolean;
            binary=xs:hexBinary; enum=xs:string from EnumerationList; relative
            time=xs:duration; absolute time=xs:dateTime.  Supplied value must be
            within the ValidRange specified for the type.
    """

    argument_name: str = field(
        metadata={
            "name": "argumentName",
            "type": "Attribute",
            "pattern": r"([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)",
        }
    )
    argument_value: str = field(
        metadata={
            "name": "argumentValue",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class ArgumentInstanceRefType:
    """
    An argument instance is the name of an argument as the reference is always
    resolved locally to the metacommand.

    Attributes:
        argument_ref: Give the name of the argument.  There is no path, this is a
            local reference.
        use_calibrated_value: Typically the calibrated/engineering value is used
            and that is the default.
    """

    argument_ref: str = field(
        metadata={
            "name": "argumentRef",
            "type": "Attribute",
            "pattern": r"([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)",
        }
    )
    use_calibrated_value: bool = field(
        default=True,
        metadata={
            "name": "useCalibratedValue",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class AuthorSetType:
    """
    Describe an unordered collection of authors.

    See AuthorType.

    Attributes:
        author: Contains information about an author, maintainer, or data source
            regarding this document.
    """

    author: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Author",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class BaseComparisonType:
    """
    A base type for comparison related elements that improves the mapping produced
    by data binding tools.
    """


@dataclass(kw_only=True)
class BaseConditionsType:
    """
    A base type for boolean expression related elements that improves the mapping
    produced by data binding tools.
    """


@dataclass(kw_only=True)
class BaseTriggerType:
    """
    A base type for the various triggers, purely to improve the mappings created by
    data binding compilers.
    """


class BasisType(Enum):
    """
    Defines to type of update rates: perSecond and perContainerUpdate.

    See RateInStreamType.
    """

    PER_SECOND = "perSecond"
    PER_CONTAINER_UPDATE = "perContainerUpdate"


class BitOrderType(Enum):
    """
    Defines two bit-order types: most significant bit first and least significant
    bit first.

    See DataEncodingType.
    """

    LEAST_SIGNIFICANT_BIT_FIRST = "leastSignificantBitFirst"
    MOST_SIGNIFICANT_BIT_FIRST = "mostSignificantBitFirst"


class ByteOrderCommonType(Enum):
    """
    Common byte orderings: most significant byte first (also known as big endian)
    and least significant byte first (also known as little endian).
    """

    MOST_SIGNIFICANT_BYTE_FIRST = "mostSignificantByteFirst"
    LEAST_SIGNIFICANT_BYTE_FIRST = "leastSignificantByteFirst"


@dataclass(kw_only=True)
class ByteType:
    byte_significance: int = field(
        metadata={
            "name": "byteSignificance",
            "type": "Attribute",
            "min_inclusive": 0,
        }
    )


class ChangeBasisType(Enum):
    """
    Defines absoluteChange and percentageChange for use in rate of change alarms.

    Used by ChangeAlarmRangesType.
    """

    ABSOLUTE_CHANGE = "absoluteChange"
    PERCENTAGE_CHANGE = "percentageChange"


class ChangeSpanType(Enum):
    """
    Defines a changePerSecond and changePerSample for use in rate of change alarms.

    Used by ChangeAlarmRangesType.
    """

    CHANGE_PER_SECOND = "changePerSecond"
    CHANGE_PER_SAMPLE = "changePerSample"


@dataclass(kw_only=True)
class ChangeValueType:
    """
    Describe a change value used to test verification status.

    See CommandVerifierType.

    Attributes:
        value: Value as a floating point number.
    """

    value: float = field(
        metadata={
            "type": "Attribute",
        }
    )


class CharacterWidthType(Enum):
    VALUE_8 = 8
    VALUE_16 = 16
    VALUE_32 = 32


class ChecksumTypeName(Enum):
    """
    Attributes:
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


class ComparisonOperatorsType(Enum):
    """
    Operators to use when testing a boolean condition for a validity check.
    """

    EQUALS_SIGN_EQUALS_SIGN = "=="
    EXCLAMATION_MARK_EQUALS_SIGN = "!="
    LESS_THAN_SIGN = "<"
    LESS_THAN_SIGN_EQUALS_SIGN = "<="
    GREATER_THAN_SIGN = ">"
    GREATER_THAN_SIGN_EQUALS_SIGN = ">="


class ConcernLevelsType(Enum):
    """
    Defines six levels: Normal, Watch, Warning, Distress, Critical and Severe, in
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


class ConsequenceLevelType(Enum):
    """
    Defines the criticality level of a command.

    Criticality levels follow ISO 14950.

    Attributes:
        NORMAL: Normal command.  Corresponds to ISO 14950 Level D telecommand
            criticality.
        VITAL: Command that is not a critical command but is essential to the
            success of the mission and, if sent at the wrong time, could cause
            momentary loss of the mission.  Corresponds to ISO 14950 Level C
            telecommand criticality.
        CRITICAL: Command that, if executed at the wrong time or in the wrong
            configuration, could cause irreversible loss or damage for the
            mission.  Corresponds to ISO 14950 Level B telecommand criticality.
            Some space programs have called this "restricted" and may be
            implemented with a secondary confirmation before transmission.
        FORBIDDEN: Command that is not expected to be used for nominal or
            foreseeable contingency operations, that is included for unforeseen
            contingency operations, and that could cause irreversible damage if
            executed at the wrong time or in the wrong configuration.
            Corresponds to ISO 14950 Level A telecommand criticality.  Some space
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


@dataclass(kw_only=True)
class ConstantType:
    """
    Names and provides a value for a constant input to the algorithm.

    There are two attributes to Constant, constantName and value. constantName is a
    variable name in the algorithm to be executed. value is the value of the
    constant to be used.

    Attributes:
        constant_name: Supply a name for the constant to be used to access this
            value from within the algorithm.
        value: Supply the constant value in the form of the data type needed in
            the algorithm.
    """

    constant_name: str = field(
        metadata={
            "name": "constantName",
            "type": "Attribute",
        }
    )
    value: str = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class ContainerRefType:
    """
    Holds a reference to a container.

    Attributes:
        container_ref: name of container
    """

    container_ref: str = field(
        metadata={
            "name": "containerRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )


class EpochTimeEnumsType(Enum):
    """
    Union values of common epoch definitions for document convenience.
    """

    TAI = "TAI"
    J2000 = "J2000"
    UNIX = "UNIX"
    GPS = "GPS"


@dataclass(kw_only=True)
class ExternalAlgorithmType:
    """
    This is the external algorithm.

    Multiple entries are provided so that the same database may be used for multiple
    implementation s.
    """

    implementation_name: str = field(
        metadata={
            "name": "implementationName",
            "type": "Attribute",
        }
    )
    algorithm_location: str = field(
        metadata={
            "name": "algorithmLocation",
            "type": "Attribute",
        }
    )


class FlagBitType(Enum):
    ZEROS = "zeros"
    ONES = "ones"


class FloatEncodingSizeInBitsType(Enum):
    """
    Attributes:
        VALUE_16: At the time of this writing, 16 bit encoding size is only valid
            in cases of IEEE754 and vendor specific MILSTD_1750A variation that
            is not a part of the standard.  This is not meant to preclude use in
            the event that future floating point formats may also define this
            value.
        VALUE_32: At the time of this writing, 32 bit encoding size is only valid
            in cases of IEEE754_1985, IEEE754, MILSTD_1750A, DEC, IBM, and TI.
            This is not meant to preclude use in the event that future floating
            point formats may also define this value.  The IEEE754 enumeration
            and the IEEE754_1985 enumeration are allowed in this case and the
            interpretation is the same.
        VALUE_40: At the time of this writing, 40 bit encoding size is only valid
            in the case of TI.  This is not meant to preclude use in the event
            that future floating point formats may also define this value.
        VALUE_48: At the time of this writing, 48 bit encoding size is only valid
            in the case of MILSTD_1750A.  This is not meant to preclude use in
            the event that future floating point formats may also define this
            value.
        VALUE_64: At the time of this writing, 64 bit encoding size is only valid
            in cases of IEEE754_1985, IEEE754, DEC, and IBM.  This is not meant
            to preclude use in the event that future floating point formats may
            also define this value.  The IEEE754 enumeration and the IEEE754_1985
            enumeration are allowed in this case and the interpretation is the
            same.
        VALUE_80: At the time of this writing, 80 bit encoding size is only valid
            in the case of IEEE754_1985.  This is not meant to preclude use in
            the event that future floating point formats may also define this
            value.
        VALUE_128: At the time of this writing, 128 bit encoding size is only
            valid in the case of IEEE754_1985 and IEEE754.  This is not meant to
            preclude use in the event that future floating point formats may also
            define this value.  The IEEE754 enumeration and the IEEE754_1985
            enumeration are allowed in this case and the interpretation is the
            same.
    """

    VALUE_16 = 16
    VALUE_32 = 32
    VALUE_40 = 40
    VALUE_48 = 48
    VALUE_64 = 64
    VALUE_80 = 80
    VALUE_128 = 128


class FloatEncodingType(Enum):
    IEEE754_1985 = "IEEE754_1985"
    IEEE754 = "IEEE754"
    MILSTD_1750_A = "MILSTD_1750A"
    DEC = "DEC"
    IBM = "IBM"
    TI = "TI"


@dataclass(kw_only=True)
class FloatRangeType:
    """
    Describe a floating point based range, several types of ranges are supported --
    one sided and two sided, inclusive or exclusive.

    It would not make sense to set two mins or maxes. Used in a number of locations
    related to ranges: ValidFloatRangeSetType or AlarmRangeType for example.

    Attributes:
        min_inclusive: Minimum decimal/real number value including itself.
        min_exclusive: Minimum decimal/real number value excluding itself.
        max_inclusive: Maximum decimal/real number value including itself.
        max_exclusive: Maximum decimal/real number value excluding itself.
    """

    min_inclusive: None | float = field(
        default=None,
        metadata={
            "name": "minInclusive",
            "type": "Attribute",
        },
    )
    min_exclusive: None | float = field(
        default=None,
        metadata={
            "name": "minExclusive",
            "type": "Attribute",
        },
    )
    max_inclusive: None | float = field(
        default=None,
        metadata={
            "name": "maxInclusive",
            "type": "Attribute",
        },
    )
    max_exclusive: None | float = field(
        default=None,
        metadata={
            "name": "maxExclusive",
            "type": "Attribute",
        },
    )


class FloatSizeInBitsType(Enum):
    VALUE_32 = 32
    VALUE_64 = 64
    VALUE_128 = 128


class FloatingPointNotationType(Enum):
    NORMAL = "normal"
    SCIENTIFIC = "scientific"
    ENGINEERING = "engineering"


@dataclass(kw_only=True)
class HistorySetType:
    """
    Describe an unordered collection of History elements.

    Usage is user defined. See HistoryType.

    Attributes:
        history: Contains a history record related to the evolution of this
            document.
    """

    history: list[str] = field(
        default_factory=list,
        metadata={
            "name": "History",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


class IntegerEncodingType(Enum):
    UNSIGNED = "unsigned"
    SIGN_MAGNITUDE = "signMagnitude"
    TWOS_COMPLEMENT = "twosComplement"
    ONES_COMPLEMENT = "onesComplement"
    BCD = "BCD"
    PACKED_BCD = "packedBCD"


@dataclass(kw_only=True)
class IntegerRangeType:
    """
    Describe an integral based range: minInclusive and maxInclusive.

    Used in a number of locations related to ranges: ValidIntegerRangeSetType for
    example.

    Attributes:
        min_inclusive: Minimum integer value including itself.
        max_inclusive: Maximum integer value including itself.
    """

    min_inclusive: None | int = field(
        default=None,
        metadata={
            "name": "minInclusive",
            "type": "Attribute",
        },
    )
    max_inclusive: None | int = field(
        default=None,
        metadata={
            "name": "maxInclusive",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class LeadingSizeType:
    """
    Like PASCAL strings, the size of the string is given as an integer at the start
    of the string.

    SizeTag must be an unsigned Integer.
    """

    size_in_bits_of_size_tag: int = field(
        default=16,
        metadata={
            "name": "sizeInBitsOfSizeTag",
            "type": "Attribute",
            "min_inclusive": 1,
        },
    )


@dataclass(kw_only=True)
class LinearAdjustmentType:
    """
    A slope and intercept may be applied to scale or shift the value of the
    parameter in the dynamic value.

    The default of slope=1 and intercept=0 results in no change to the value.
    """

    slope: float = field(
        default=1.0,
        metadata={
            "type": "Attribute",
        },
    )
    intercept: float = field(
        default=0.0,
        metadata={
            "type": "Attribute",
        },
    )


class MathOperatorsType(Enum):
    """
    Mathematical operators used in the math operation.

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


@dataclass(kw_only=True)
class MessageRefType:
    """
    Holds a reference to a message.

    Attributes:
        message_ref: name of message
    """

    message_ref: str = field(
        metadata={
            "name": "messageRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )


@dataclass(kw_only=True)
class NoteSetType:
    """
    Contains an unordered collection of Notes.

    Usage is user defined. See NoteType.

    Attributes:
        note: Contains a program defined technical note regarding this document.
    """

    note: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Note",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


class Pcmtype(Enum):
    NRZL = "NRZL"
    NRZM = "NRZM"
    NRZS = "NRZS"
    BI_PHASE_L = "BiPhaseL"
    BI_PHASE_M = "BiPhaseM"
    BI_PHASE_S = "BiPhaseS"


@dataclass(kw_only=True)
class ParameterRefType:
    """
    A reference to a Parameter.

    Uses Unix-like naming across the SpaceSystem Tree (e.g.,
    SimpleSat/Bus/EPDS/BatteryOne/Voltage). To reference an individual member of an
    array use the zero based bracket notation commonly used in languages like C,
    C++, and Java.
    """

    parameter_ref: str = field(
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
        }
    )


class ParityFormType(Enum):
    EVEN = "Even"
    ODD = "Odd"


@dataclass(kw_only=True)
class PhysicalAddressType:
    """
    Describe the physical address(s) that this parameter is collected from.

    Examples of physical addresses include a memory location on the spacecraft or a
    location on a data collection bus, with the source identified with a descriptive
    name for the region of memory, such as RAM, Flash, EEPROM, and other
    possibilities that can be adapted for program specific usage.

    Attributes:
        sub_address: A sub-address may be used to further specify the location if
            it fractionally occupies the address.  Additional possibilities exist
            for separating partitions of memory or other address based storage
            mechanisms.  This specification does not specify spacecraft specific
            hardware properties, so usage of addressing information is largely
            program and platform specific.
        source_name: A descriptive name for the location, such as a memory type,
            where this address is located.
        source_address: The address within the memory location.  This
            specification does not specify program and hardware specific
            attributes, such as address size and address region starting
            location.  These are part of the spacecraft hardware properties.
    """

    sub_address: None | PhysicalAddressType = field(
        default=None,
        metadata={
            "name": "SubAddress",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    source_name: None | str = field(
        default=None,
        metadata={
            "name": "sourceName",
            "type": "Attribute",
        },
    )
    source_address: None | str = field(
        default=None,
        metadata={
            "name": "sourceAddress",
            "type": "Attribute",
        },
    )


class RadixType(Enum):
    """
    Specifies the number base.
    """

    DECIMAL = "Decimal"
    HEXADECIMAL = "Hexadecimal"
    OCTAL = "Octal"
    BINARY = "Binary"


class RangeFormType(Enum):
    """
    Defines inside and outside enumerated terms, where the term outside means the
    range is (-inf, minimum) and (maximum, inf) -- that is a range where acceptable
    values must be less than the minimum and greater than the maximum, and the term
    inside means the range is (minimum, maximum) -- that is acceptable values are
    between the minimum and maximum (either the min or max may be inclusive or
    exclusive).
    """

    OUTSIDE = "outside"
    INSIDE = "inside"


class ReferenceLocationType(Enum):
    """
    The location may be relative to the start of the container (containerStart),
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


class ReferencePointType(Enum):
    START = "start"
    END = "end"


@dataclass(kw_only=True)
class ServiceRefType:
    """
    A reference to a Service.
    """

    service_ref: str = field(
        metadata={
            "name": "serviceRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )


@dataclass(kw_only=True)
class SplinePointType:
    """
    A spline, or piecewise defined function, is a set on points from which a curve
    may be drawn to interpolate raw to calibrated values.

    Attributes:
        order: The order of a SplineCalibrator refers to the interpolation
            function.  Order 0 is a flat line from the defined point (inclusive)
            to the next point (exclusive).  Order 1 is linear interpolation
            between two points.  Order 2 is quadratic fit and requires at least 3
            points (unusual case).  This order is generally not needed, but may
            be used to override the interpolation order for this point.
        raw: The raw encoded value.
        calibrated: The engineering/calibrated value associated with the raw
            value for this point.
    """

    order: int = field(
        default=1,
        metadata={
            "type": "Attribute",
            "min_inclusive": 0,
        },
    )
    raw: float = field(
        metadata={
            "type": "Attribute",
        }
    )
    calibrated: float = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class StreamRefType:
    """
    Holds a reference to a stream.

    Attributes:
        stream_ref: name of reference stream
    """

    stream_ref: str = field(
        metadata={
            "name": "streamRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )


class StringEncodingType(Enum):
    """
    Defines string encodings.

    US-ASCII (7-bit), ISO-8859-1 (8-bit Extended ASCII), Windows-1252 (8-bit
    Extended ASCII), UTF-8 (Unicode), UTF-16 (Unicode with Byte Order Mark),
    UTF-16LE (Unicode Little Endian), UTF-16BE (Unicode Big Endian). See
    StringDataEncodingType.

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


@dataclass(kw_only=True)
class SyncPatternType:
    """
    The pattern of bits used to look for frame synchronization.

    Attributes:
        pattern: CCSDS ASM for non-turbocoded frames = 1acffc1d
        bit_location_from_start_of_container:
        mask:
        mask_length_in_bits: truncate the mask from the left
        pattern_length_in_bits: truncate the pattern from the left
    """

    pattern: bytes = field(
        metadata={
            "type": "Attribute",
            "format": "base16",
        }
    )
    bit_location_from_start_of_container: int = field(
        default=0,
        metadata={
            "name": "bitLocationFromStartOfContainer",
            "type": "Attribute",
        },
    )
    mask: None | bytes = field(
        default=None,
        metadata={
            "type": "Attribute",
            "format": "base16",
        },
    )
    mask_length_in_bits: None | int = field(
        default=None,
        metadata={
            "name": "maskLengthInBits",
            "type": "Attribute",
            "min_inclusive": 1,
        },
    )
    pattern_length_in_bits: int = field(
        metadata={
            "name": "patternLengthInBits",
            "type": "Attribute",
            "min_inclusive": 1,
        }
    )


class SystemTypeType(Enum):
    """
    The type attribute represents what from a space enterprise this SpaceSystem
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


class TelemetryDataSourceType(Enum):
    """
    A telemetered Parameter is one that will have values in telemetry.

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


@dataclass(kw_only=True)
class TermType:
    """
    A term in a polynomial expression.

    Attributes:
        coefficient: The coefficient in a single term of a polynomial expression.
        exponent: The exponent in a single term of a polynomial expression.
            Should negative exponents be required, use a Math Calibrator style of
            definition for this type.
    """

    coefficient: float = field(
        metadata={
            "type": "Attribute",
        }
    )
    exponent: int = field(
        metadata={
            "type": "Attribute",
            "min_inclusive": 0,
        }
    )


class TimeAssociationUnitType(Enum):
    """
    Time units the time association decimal value is in.
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


class TimeUnitsType(Enum):
    """
    Base time unit of measure.

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


class TimeWindowIsRelativeToType(Enum):
    COMMAND_RELEASE = "commandRelease"
    TIME_LAST_VERIFIER_PASSED = "timeLastVerifierPassed"


class UnitFormType(Enum):
    """
    Defines enumerated values to categorize a unit associated with a telemetered
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


class ValidationStatusType(Enum):
    UNKNOWN = "Unknown"
    WORKING = "Working"
    DRAFT = "Draft"
    TEST = "Test"
    VALIDATED = "Validated"
    RELEASED = "Released"
    WITHDRAWN = "Withdrawn"


@dataclass(kw_only=True)
class ValueEnumerationType:
    """
    Describe a value and an associated string label, see EnumerationListType.

    Attributes:
        value: Numeric raw/uncalibrated value to associate with a string
            enumeration label.
        max_value: If max value is given, the label maps to a range where value
            is less than or equal to maxValue. The range is inclusive.
        label: String enumeration label to apply to this value definition in the
            enumeration.
        short_description: An optional additional string description can be
            specified for this enumeration label to provide extended information
            if desired.
    """

    value: int = field(
        metadata={
            "type": "Attribute",
        }
    )
    max_value: None | int = field(
        default=None,
        metadata={
            "name": "maxValue",
            "type": "Attribute",
        },
    )
    label: str = field(
        metadata={
            "type": "Attribute",
        }
    )
    short_description: None | str = field(
        default=None,
        metadata={
            "name": "shortDescription",
            "type": "Attribute",
        },
    )


class VerifierEnumerationType(Enum):
    """
    An enumerated list of verifier types.
    """

    RELEASE = "release"
    TRANSFERRED_TO_RANGE = "transferredToRange"
    SENT_FROM_RANGE = "sentFromRange"
    RECEIVED = "received"
    ACCEPTED = "accepted"
    QUEUED = "queued"
    EXECUTING = "executing"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass(kw_only=True)
class AliasSetType:
    """
    Contains an unordered collection of Alias elements to describe alternate names
    or IDs for this named item.

    Attributes:
        alias: An alternate name, ID number, and sometimes flight software
            variable name in the code for this item.
    """

    alias: list[AliasType] = field(
        default_factory=list,
        metadata={
            "name": "Alias",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class AncillaryDataSetType:
    """
    Describe an unordered collection of ancillary data.

    AncillaryData elements capture platform/program/implementation specific data
    about the parent element object that is non-standard and would not fit into the
    schema. See AncillaryDataType.

    Attributes:
        ancillary_data: Optional list of AncillaryData elements associated with
            this item.
    """

    ancillary_data: list[AncillaryDataType] = field(
        default_factory=list,
        metadata={
            "name": "AncillaryData",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class ArgumentAssignmentListType:
    """
    Argument Assignments specialize a MetaCommand or BlockMetaCommand when
    inheriting from another MetaCommand.

    General argument values can be restricted to specific values to further
    specialize the MetaCommand. Use it to "narrow" a MetaCommand from its base
    MetaCommand by specifying values of arguments for example, a power command may
    be narrowed to a "power on" command by assigning the value of an argument to
    "on". See ArgumentAssignmentType and MetaCommandType.

    Attributes:
        argument_assignment: Specialize this command definition when inheriting
            from a more general MetaCommand by restricting the specific values of
            otherwise general arguments.
    """

    argument_assignment: list[ArgumentAssignmentType] = field(
        default_factory=list,
        metadata={
            "name": "ArgumentAssignment",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class ArgumentRestrictionListType:
    """
    Defines a list of argument values that restrict a constraint from being realized
    in the commanding lifecycle.

    Attributes:
        argument_restriction: Specifies an argument value that causes this
            constraint to be realized.
    """

    argument_restriction: list[ArgumentAssignmentType] = field(
        default_factory=list,
        metadata={
            "name": "ArgumentRestriction",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class Crctype:
    """
    Cyclic Redundancy Check (CRC) definition.

    The polynomial coefficients for the CRC are defined as a truncated hex value.
    The coefficient for the nth bit of an n-bit CRC will always be 1 and is not
    represented in the truncated hex value. For example, the truncated hex value of
    CRC-32 (width=32 bits) used in the Ethernet specification is 0x04C11DB7, where
    each non-zero bit of the truncated hex represents a coefficient of 1 in the
    polynomial and the bit position represents the exponent. There may also be an
    initial remainder "InitRemainder" and a final XOR "FinalXOR" to fully specify
    the CRC. reflectData and reflectRemainder may also be specified to reverse the
    bit order in the incoming data and/or the result.

    Attributes:
        polynomial: The polynomial that represents the calculation in hexadecimal
            form (described at CRCType annotation).
        init_remainder: A hexadecimal digit string specifying the initial value
            to set in the shift register before computing the CRC.
        final_xor: A hexadecimal digit string specifying the value to be added to
            the final shift register value before output.
        width: The width is the number of bits in the shift register, which is
            not necessarily the number of bits of the parameter holding the
            value.
        reflect_data: Endianness of the input data, true=little, false=big.
        reflect_remainder: Endianness of the output data, true=little, false=big.
        direction: The direction to perform the CRC calculation.
        bits_from_reference: An offset of non-zero may be specified to skip some
            bits against the reference position in the reference attribute.
        reference: The bits involved in the calculation may start at the
            beginning or the end of the container.
        parameter_ref: Reference to the parameter that contains the value of the
            CRC based on this container.  This attribute is optional because not
            all implementations verify (telemetry) or create (telecommand) error
            control fields using the XTCE definition.
    """

    class Meta:
        name = "CRCType"

    polynomial: bytes = field(
        metadata={
            "name": "Polynomial",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "format": "base16",
        }
    )
    init_remainder: None | bytes = field(
        default=None,
        metadata={
            "name": "InitRemainder",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "format": "base16",
        },
    )
    final_xor: None | bytes = field(
        default=None,
        metadata={
            "name": "FinalXOR",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "format": "base16",
        },
    )
    width: int = field(
        metadata={
            "type": "Attribute",
            "min_inclusive": 1,
        }
    )
    reflect_data: bool = field(
        default=False,
        metadata={
            "name": "reflectData",
            "type": "Attribute",
        },
    )
    reflect_remainder: bool = field(
        default=False,
        metadata={
            "name": "reflectRemainder",
            "type": "Attribute",
        },
    )
    direction: BitOrderType = field(
        default=BitOrderType.MOST_SIGNIFICANT_BIT_FIRST,
        metadata={
            "type": "Attribute",
        },
    )
    bits_from_reference: int = field(
        default=0,
        metadata={
            "name": "bitsFromReference",
            "type": "Attribute",
            "min_inclusive": 0,
        },
    )
    reference: ReferencePointType = field(
        default=ReferencePointType.START,
        metadata={
            "type": "Attribute",
        },
    )
    parameter_ref: None | str = field(
        default=None,
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
        },
    )


@dataclass(kw_only=True)
class CheckWindowType:
    """
    Used by CommandVerifiers to limit the time allocated to check for the
    verification.

    See CheckWindowAlgorithmsType.
    """

    time_to_start_checking: None | XmlDuration = field(
        default=None,
        metadata={
            "name": "timeToStartChecking",
            "type": "Attribute",
        },
    )
    time_to_stop_checking: XmlDuration = field(
        metadata={
            "name": "timeToStopChecking",
            "type": "Attribute",
        }
    )
    time_window_is_relative_to: TimeWindowIsRelativeToType = field(
        default=TimeWindowIsRelativeToType.TIME_LAST_VERIFIER_PASSED,
        metadata={
            "name": "timeWindowIsRelativeTo",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ContainerRefSetType:
    container_ref: list[ContainerRefType] = field(
        default_factory=list,
        metadata={
            "name": "ContainerRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class EnumerationAlarmLevelType:
    """
    Describe an alarm level and its enumeration label to trigger from.

    See EnumeratedAlarmType and EnumeratedParameterType.

    Attributes:
        alarm_level: Defines six levels: Normal, Watch, Warning, Distress,
            Critical and Severe. Typical implementations color the "normal" level
            as green, "warning" level as yellow, and "critical" level as red. In
            the case of enumeration alarms, the "normal" is assumed by
            implementations to be any label not otherwise in an alarm state.
        enumeration_label: The enumeration label is the engineering/calibrated
            value for enumerated types.
    """

    alarm_level: ConcernLevelsType = field(
        metadata={
            "name": "alarmLevel",
            "type": "Attribute",
        }
    )
    enumeration_label: str = field(
        metadata={
            "name": "enumerationLabel",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class EnumerationListType:
    enumeration: list[ValueEnumerationType] = field(
        default_factory=list,
        metadata={
            "name": "Enumeration",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class ExternalAlgorithmSetType:
    external_algorithm: list[ExternalAlgorithmType] = field(
        default_factory=list,
        metadata={
            "name": "ExternalAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class FlagType:
    """
    The pattern of bits used to look for frame synchronization.
    """

    flag_size_in_bits: int = field(
        default=6,
        metadata={
            "name": "flagSizeInBits",
            "type": "Attribute",
            "min_inclusive": 1,
        },
    )
    flag_bit_type: FlagBitType = field(
        default=FlagBitType.ONES,
        metadata={
            "name": "flagBitType",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class HeaderType:
    """
    Schema for a Header record.

    A header contains general information about the system or subsystem.

    Attributes:
        author_set: The AuthorSet contains optional contact information for this
            document.
        note_set: The NoteSet contains optional technical information related to
            the content of this document.
        history_set: The HistorySet contains optional evolutionary information
            for data contained in this document.
        version: This attribute contains an optional version descriptor for this
            document.
        date: This attribute contains an optional date to be associated with this
            document.
        classification: This attribute contains optional classification status
            for use by programs for which that is applicable.
        classification_instructions: This attribute contains an optional
            additional instructions attribute to be interpreted by programs that
            use this attribute.
        validation_status: This attribute contains a flag describing the state of
            this document in the evolution of the project using it.
    """

    author_set: None | AuthorSetType = field(
        default=None,
        metadata={
            "name": "AuthorSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    note_set: None | NoteSetType = field(
        default=None,
        metadata={
            "name": "NoteSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    history_set: None | HistorySetType = field(
        default=None,
        metadata={
            "name": "HistorySet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    version: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    date: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    classification: str = field(
        default="NotClassified",
        metadata={
            "type": "Attribute",
        },
    )
    classification_instructions: None | str = field(
        default=None,
        metadata={
            "name": "classificationInstructions",
            "type": "Attribute",
        },
    )
    validation_status: ValidationStatusType = field(
        metadata={
            "name": "validationStatus",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class InterlockType:
    """
    Describe a type of constraint on the next command, rather than this command.

    Interlocks apply only to the next command. An interlock will block successive
    commands until this command has reached a certain stage of verifier. Interlocks
    are scoped to a SpaceSystem basis: they by default apply to the SpaceSystem the
    MetaCommand is defined in but this may be overridden. See MetaCommandType and
    VerifierSetType.

    Attributes:
        scope_to_space_system: The name of a SpaceSystem this Interlock applies
            to.  By default, it only applies to the SpaceSystem that contains
            this MetaCommand.
        verification_to_wait_for: The verification stage of the command that
            releases the interlock, with the default being complete.
        verification_progress_percentage: Only applies when the
            verificationToWaitFor attribute is 'queued' or 'executing'.
        suspendable: A flag that indicates that under special circumstances, this
            Interlock can be suspended.
    """

    scope_to_space_system: None | str = field(
        default=None,
        metadata={
            "name": "scopeToSpaceSystem",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        },
    )
    verification_to_wait_for: VerifierEnumerationType = field(
        default=VerifierEnumerationType.COMPLETE,
        metadata={
            "name": "verificationToWaitFor",
            "type": "Attribute",
        },
    )
    verification_progress_percentage: None | float = field(
        default=None,
        metadata={
            "name": "verificationProgressPercentage",
            "type": "Attribute",
        },
    )
    suspendable: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class MessageRefSetType:
    message_ref: list[MessageRefType] = field(
        default_factory=list,
        metadata={
            "name": "MessageRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class MultiRangeType(FloatRangeType):
    """
    The alarm multi-range element type permits users to define multiple alarm ranges
    in a sequence that goes beyond the more typical "inside" and "outside" range
    definitions.

    It can be thought of as a "barber pole" definition.

    Attributes:
        range_form: A value of outside specifies that the most severe range is
            outside all the other ranges: -severe -critical -distress -warning
            -watch normal +watch +warning +distress +critical +severe.  This
            means each min, max pair are a range: (-inf, min) or (-inf, min], and
            [max, inf) or (max, inf).  However a value of inside "inverts" these
            bands: -normal -watch -warning -distress -critical severe +critical
            +distress +warning +watch, +normal.  This means each min, max pair
            form a range of (min, max) or [min, max) or (min, max] or [min, max].
            The most common form used is "outside" and it is the default.  The
            set notation used defines parenthesis as exclusive and square
            brackets as inclusive.
        level: The level of concern for this alarm definition.
    """

    range_form: RangeFormType = field(
        default=RangeFormType.OUTSIDE,
        metadata={
            "name": "rangeForm",
            "type": "Attribute",
        },
    )
    level: None | ConcernLevelsType = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class NumberFormatType:
    """
    This type describes how a numeric value should be represented in
    engineering/calibrated form.

    The defaults reflect the most common form.

    Attributes:
        number_base: Describes how the engineering/calibrated value of this
            number should be displayed with respect to the radix.  Default is
            base 10.
        minimum_fraction_digits: Describes how the engineering/calibrated value
            of this number should be displayed with respect to the minimum number
            of fractional digits.  The default is 0.
        maximum_fraction_digits: Describes how the engineering/calibrated value
            of this number should be displayed with respect to the maximum or
            upper bound of the number of digits.  There is no default.  No value
            specified should be interpreted as no upper bound such that all
            requires digits are used to fully characterize the value.
        minimum_integer_digits: Describes how the engineering/calibrated value of
            this number should be displayed with respect to the minimum number of
            integer digits.  The default is 1.
        maximum_integer_digits: Describes how the engineering/calibrated value of
            this number should be displayed with respect to the maximum or upper
            bound of the integer digits.  There is no default.  No value
            specified should be interpreted as no upper bound such that all
            requires digits are used to fully characterize the value.
        negative_suffix: Describes how the engineering/calibrated value of this
            number should be displayed with respect to negative values.  This
            attribute specifies the character or characters that should be
            appended to the numeric value to indicate negative values.  The
            default is none.
        positive_suffix: Describes how the engineering/calibrated value of this
            number should be displayed with respect to positive values.  This
            attribute specifies the character or characters that should be
            appended to the numeric value to indicate positive values.  The
            default is none.  Zero is considered to be specific to the
            implementation/platform and is not implied here.
        negative_prefix: Describes how the engineering/calibrated value of this
            number should be displayed with respect to negative values.  This
            attribute specifies the character or characters that should be
            prepended to the numeric value to indicate negative values.  The
            default is a minus character "-".
        positive_prefix: Describes how the engineering/calibrated value of this
            number should be displayed with respect to positive values.  This
            attribute specifies the character or characters that should be
            prepended to the numeric value to indicate positive values.  The
            default is none.  Zero is considered to be specific to the
            implementation/platform and is not implied here.
        show_thousands_grouping: Describes how the engineering/calibrated value
            of this number should be displayed with respect to larger values.
            Groupings by thousand are specific to locale, so the schema only
            specifies whether they will be present and not which character
            separators are used.  The default is false.
        notation: Describes how the engineering/calibrated value of this number
            should be displayed with respect to notation.  Engineering,
            scientific, or traditional decimal notation may be specified.  The
            precise characters used is locale specific for the
            implementation/platform.  The default is "normal" for the traditional
            notation.
    """

    number_base: RadixType = field(
        default=RadixType.DECIMAL,
        metadata={
            "name": "numberBase",
            "type": "Attribute",
        },
    )
    minimum_fraction_digits: int = field(
        default=0,
        metadata={
            "name": "minimumFractionDigits",
            "type": "Attribute",
            "min_inclusive": 0,
        },
    )
    maximum_fraction_digits: None | int = field(
        default=None,
        metadata={
            "name": "maximumFractionDigits",
            "type": "Attribute",
            "min_inclusive": 0,
        },
    )
    minimum_integer_digits: int = field(
        default=1,
        metadata={
            "name": "minimumIntegerDigits",
            "type": "Attribute",
            "min_inclusive": 0,
        },
    )
    maximum_integer_digits: None | int = field(
        default=None,
        metadata={
            "name": "maximumIntegerDigits",
            "type": "Attribute",
            "min_inclusive": 0,
        },
    )
    negative_suffix: str = field(
        default="",
        metadata={
            "name": "negativeSuffix",
            "type": "Attribute",
        },
    )
    positive_suffix: str = field(
        default="",
        metadata={
            "name": "positiveSuffix",
            "type": "Attribute",
        },
    )
    negative_prefix: str = field(
        default="-",
        metadata={
            "name": "negativePrefix",
            "type": "Attribute",
        },
    )
    positive_prefix: str = field(
        default="",
        metadata={
            "name": "positivePrefix",
            "type": "Attribute",
        },
    )
    show_thousands_grouping: bool = field(
        default=False,
        metadata={
            "name": "showThousandsGrouping",
            "type": "Attribute",
        },
    )
    notation: FloatingPointNotationType = field(
        default=FloatingPointNotationType.NORMAL,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class OnContainerUpdateTriggerType(BaseTriggerType):
    """
    Describe a reference to container that triggers an event when the telemetry
    container referred to is updated (processed).

    See TriggerSetType.

    Attributes:
        container_ref: Reference to the Container whose update/receipt triggers
            this algorithm to evaluate.
    """

    container_ref: str = field(
        metadata={
            "name": "containerRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )


@dataclass(kw_only=True)
class OnParameterUpdateTriggerType(BaseTriggerType):
    """
    Describe a reference to parameter that triggers an event when the telemetry
    parameter referred to is updated (processed) with a new value.

    See TriggerSetType.

    Attributes:
        parameter_ref: Reference to the Parameter whose update triggers this
            algorithm to evaluate.
    """

    parameter_ref: str = field(
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
        }
    )


@dataclass(kw_only=True)
class OnPeriodicRateTriggerType(BaseTriggerType):
    """
    Describe a periodic time basis to trigger an event.

    See TriggerSetType.

    Attributes:
        fire_rate_in_seconds: The periodic rate in time in which this algorithm
            is triggered to evaluate.
    """

    fire_rate_in_seconds: float = field(
        metadata={
            "name": "fireRateInSeconds",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class OutputParameterRefType(ParameterRefType):
    """
    Names an output parameter to the algorithm.

    There are two attributes to OutputParm, outputName and parameterName.
    parameterName is a parameter reference name for a parameter that will be updated
    by this algorithm. outputName is an optional "friendly" name for the output
    parameter.
    """

    output_name: None | str = field(
        default=None,
        metadata={
            "name": "outputName",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ParameterInstanceRefType(ParameterRefType):
    """
    A reference to an instance of a Parameter.

    Used when the value of a parameter is required for a calculation or as an index
    value. A positive value for instance is forward in time, a negative value for
    count is backward in time, a 0 value for count means use the current value of
    the parameter or the first value in a container.
    """

    instance: int = field(
        default=0,
        metadata={
            "type": "Attribute",
        },
    )
    use_calibrated_value: bool = field(
        default=True,
        metadata={
            "name": "useCalibratedValue",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ParameterToSuspendAlarmsOnType(ParameterRefType):
    """
    Will suspend all Alarms associated with this Parameter for the given suspense
    time after the given verifier.
    """

    suspense_time: XmlDuration = field(
        metadata={
            "name": "suspenseTime",
            "type": "Attribute",
        }
    )
    verifier_to_trigger_on: VerifierEnumerationType = field(
        default=VerifierEnumerationType.RELEASE,
        metadata={
            "name": "verifierToTriggerOn",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ParameterValueChangeType:
    """
    A parameter change in value or specified delta change in value.
    """

    parameter_ref: ParameterRefType = field(
        metadata={
            "name": "ParameterRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    change: ChangeValueType = field(
        metadata={
            "name": "Change",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class ParityType:
    """
    Describe the parity value.

    See ErrorDetectCorrectType.

    Attributes:
        type_value: The parity form.
        bits_from_reference: An offset of non-zero may be specified to skip some
            bits against the reference position in the reference attribute.
        reference: The bits involved in the calculation may start at the
            beginning or the end of the container.
        parameter_ref: Reference to the parameter that contains the value of the
            parity based on this container.  This attribute is optional because
            not all implementations verify (telemetry) or create (telecommand)
            error control fields using the XTCE definition.
    """

    type_value: ParityFormType = field(
        metadata={
            "name": "type",
            "type": "Attribute",
        }
    )
    bits_from_reference: int = field(
        default=0,
        metadata={
            "name": "bitsFromReference",
            "type": "Attribute",
            "min_inclusive": 0,
        },
    )
    reference: ReferencePointType = field(
        default=ReferencePointType.START,
        metadata={
            "type": "Attribute",
        },
    )
    parameter_ref: None | str = field(
        default=None,
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
        },
    )


@dataclass(kw_only=True)
class PhysicalAddressSetType:
    """
    One or more physical addresses may be associated with each Parameter.

    Examples of physical addresses include a location on the spacecraft or a
    location on a data collection bus.

    Attributes:
        physical_address: Contains the address (e.g., channel information)
            required to process the spacecraft telemetry streams. May be an
            onboard  id, a mux address, or a physical location. Contains the
            address (channel information) required to process the spacecraft
            telemetry streams
    """

    physical_address: list[PhysicalAddressType] = field(
        default_factory=list,
        metadata={
            "name": "PhysicalAddress",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class RateInStreamType:
    """
    Define the expected appearance (rate) of a container in a stream where the rate
    is defined on either a perSecond or perContainer update basis.

    Many programs and platforms have variable reporting rates for containers and
    these can be commanded. As a result, this element is only useful to some users
    and generally does not affect the processing of the received containers
    themselves. See ContainerType.

    Attributes:
        basis: The measurement unit basis for the minimum and maximum appearance
            count values.
        minimum_value: The minimum rate for the specified basis for which this
            container should appear in the stream.
        maximum_value: The maximum rate for the specified basis for which this
            container should appear in the stream.
    """

    basis: BasisType = field(
        default=BasisType.PER_SECOND,
        metadata={
            "type": "Attribute",
        },
    )
    minimum_value: None | float = field(
        default=None,
        metadata={
            "name": "minimumValue",
            "type": "Attribute",
        },
    )
    maximum_value: None | float = field(
        default=None,
        metadata={
            "name": "maximumValue",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class SignificanceType:
    """
    Significance provides some cautionary information about the potential
    consequence of each MetaCommand.

    Attributes:
        space_system_at_risk: If none is supplied, then the current SpaceSystem
            is assumed to be the one at risk by the issuance of this command
        reason_for_warning:
        consequence_level:
    """

    space_system_at_risk: None | str = field(
        default=None,
        metadata={
            "name": "spaceSystemAtRisk",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        },
    )
    reason_for_warning: None | str = field(
        default=None,
        metadata={
            "name": "reasonForWarning",
            "type": "Attribute",
        },
    )
    consequence_level: ConsequenceLevelType = field(
        default=ConsequenceLevelType.NORMAL,
        metadata={
            "name": "consequenceLevel",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class SizeInBitsType:
    """
    Attributes:
        fixed: This is the simplest case of a string data type where the encoding
            size of the string does not change.
        termination_char: The termination character that represents the end of
            the string contents.  For C and most strings, this is null (00),
            which is the default.
        leading_size: In some string implementations, the size of the string
            contents (not the memory allocation size) is determined by a leading
            numeric value.  This is sometimes referred to as Pascal strings.  If
            a LeadingSize is specified, then the TerminationChar element does not
            have a functional meaning.
    """

    fixed: SizeInBitsType.Fixed = field(
        metadata={
            "name": "Fixed",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    termination_char: None | bytes = field(
        default=None,
        metadata={
            "name": "TerminationChar",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "format": "base16",
        },
    )
    leading_size: None | LeadingSizeType = field(
        default=None,
        metadata={
            "name": "LeadingSize",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )

    @dataclass(kw_only=True)
    class Fixed:
        """
        Attributes:
            fixed_value: Size in bits of this string data type for both the
                memory allocation in the implementing software and also the size
                in bits for this parameter when it appears in a container.
        """

        fixed_value: int = field(
            metadata={
                "name": "FixedValue",
                "type": "Element",
                "namespace": "http://www.omg.org/spec/XTCE/20250214",
                "min_inclusive": 1,
            }
        )


@dataclass(kw_only=True)
class StringAlarmLevelType:
    """
    Describe a string alarm condition based on matching a regular expression.

    The level and regular expression are described. The specific implementation of
    the regular expression syntax is not specified in the schema at this time. See
    StringAlarmListType.
    """

    alarm_level: ConcernLevelsType = field(
        metadata={
            "name": "alarmLevel",
            "type": "Attribute",
        }
    )
    match_pattern: str = field(
        metadata={
            "name": "matchPattern",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class UnitType:
    """
    Describe the exponent, factor, form, and description for a unit.

    The unit itself is in element Unit in UnitSet. See UnitSetType. The attributes
    are optional because different programs use this element in different ways,
    depending on vendor support.

    Attributes:
        power: Optional attribute used in conjunction with the "factor" attribute
            where some programs choose to specify the unit definition with these
            machine processable algebraic features.  For example, a unit text of
            "meters" may have a "power" attribute of 2, resulting "meters
            squared" as the actual unit.  This is not commonly used.  The most
            common method for "meters squared" is to use the text content of the
            Unit element in a form like "m^2".
        factor: Optional attribute used in conjunction with the "power" attribute
            where some programs choose to specify the unit definition with these
            machine processable algebraic features.  For example, a unit text of
            "meters" may have a "factor" attribute of 2, resulting "2 times
            meters" as the actual unit.  This is not commonly used.  The most
            common method for "2 times meters" is to use the text content of the
            Unit element in a form like "2*m".
        description: A description of the unit, which may be for expanded human
            readability or for specification of the nature/property of the unit.
            For example, meters per second squared is of a nature/property of
            acceleration.
        form: The default value "calibrated" is most common practice to specify
            units at the engineering/calibrated value, it is possible to specify
            an additional Unit element for the raw/uncalibrated value.
        content:
    """

    power: float = field(
        default=1.0,
        metadata={
            "type": "Attribute",
        },
    )
    factor: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        },
    )
    description: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    form: UnitFormType = field(
        default=UnitFormType.CALIBRATED,
        metadata={
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass(kw_only=True)
class ValidFloatRangeSetType:
    """
    Numerical ranges that define the universe of valid values for this argument.

    A single range is the most common, although it is possible to define multiple
    ranges when the valid values are not contiguous.

    Attributes:
        valid_range: A valid range constrains the whole set of possible values
            that could be encoded by the data type to a more "valid" or
            "reasonable" set of values.  This should be treated as a boundary
            check in an implementation to validate the input or output value.
            Typically, only 1 range is used.  In cases where multiple ranges are
            used, then the value is valid when it is valid in any of the provided
            ranges.  Implementations may also use these ranges to enhance user
            interface displays and other visualization widgets as appropriate for
            the type.
        valid_range_applies_to_calibrated: By default and general recommendation,
            the valid range is specified in engineering/calibrated values,
            although this can be adjusted.
    """

    valid_range: list[FloatRangeType] = field(
        default_factory=list,
        metadata={
            "name": "ValidRange",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )
    valid_range_applies_to_calibrated: bool = field(
        default=True,
        metadata={
            "name": "validRangeAppliesToCalibrated",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ValidIntegerRangeSetType:
    """
    Numerical ranges that define the universe of valid values for this argument.

    A single range is the most common, although it is possible to define multiple
    ranges when the valid values are not contiguous.

    Attributes:
        valid_range: A valid range constrains the whole set of possible values
            that could be encoded by the data type to a more "valid" or
            "reasonable" set of values.  This should be treated as a boundary
            check in an implementation to validate the input or output value.
            Typically, only 1 range is used.  In cases where multiple ranges are
            used, then the value is valid when it is valid in any of the provided
            ranges.  Implementations may also use these ranges to enhance user
            interface displays and other visualization widgets as appropriate for
            the type.
        valid_range_applies_to_calibrated: By default and general recommendation,
            the valid range is specified in engineering/calibrated values,
            although this can be adjusted.
    """

    valid_range: list[IntegerRangeType] = field(
        default_factory=list,
        metadata={
            "name": "ValidRange",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )
    valid_range_applies_to_calibrated: bool = field(
        default=True,
        metadata={
            "name": "validRangeAppliesToCalibrated",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Xortype:
    """
    Describe an exclusive or (XOR) checksum definition.

    See ErrorDetectCorrectType.

    Attributes:
        bits_from_reference: An offset of non-zero may be specified to skip some
            bits against the reference position in the reference attribute.
        reference: The bits involved in the calculation may start at the
            beginning or the end of the container.
        parameter_ref: Reference to the parameter that contains the value of this
            computed XOR based on this container.  This attribute is optional
            because not all implementations verify (telemetry) or create
            (telecommand) error control fields using the XTCE definition.
    """

    class Meta:
        name = "XORType"

    bits_from_reference: int = field(
        default=0,
        metadata={
            "name": "bitsFromReference",
            "type": "Attribute",
            "min_inclusive": 0,
        },
    )
    reference: ReferencePointType = field(
        default=ReferencePointType.START,
        metadata={
            "type": "Attribute",
        },
    )
    parameter_ref: None | str = field(
        default=None,
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
        },
    )


@dataclass(kw_only=True)
class ArgumentComparisonCheckType(BaseComparisonType):
    """
    Identical to ComparisonCheckType but supports argument instance references.

    Attributes:
        parameter_instance_ref: Left hand side parameter instance.
        argument_instance_ref: Left hand side argument instance.
        comparison_operator: Comparison operator.
        value: Specify as: integer data type using xs:integer, float data type
            using xs:double, string data type using xs:string, boolean data type
            using xs:boolean, binary data type using xs:hexBinary, enum data type
            using label name, relative time data type using xs:duration, absolute
            time data type using xs:dateTime.  Values must not exceed the
            characteristics for the data type or this is a validation error.
            Takes precedence over an initial value given in the data type. Values
            are calibrated unless there is an option to override it.
    """

    parameter_instance_ref: list[ParameterInstanceRefType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterInstanceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "max_occurs": 2,
        },
    )
    argument_instance_ref: list[ArgumentInstanceRefType] = field(
        default_factory=list,
        metadata={
            "name": "ArgumentInstanceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "max_occurs": 2,
        },
    )
    comparison_operator: ComparisonOperatorsType = field(
        metadata={
            "name": "ComparisonOperator",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    value: None | str = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class ArgumentComparisonType:
    """
    Identical to ComparisonType but supports argument instance references.

    Attributes:
        parameter_instance_ref: This parameter instance is being compared to the
            value in the parent element using the comparison defined there also.
        argument_instance_ref: This argument instance is being compared to the
            value in the parent element using the comparison defined there also.
        comparison_operator: Comparison operator to use with equality being the
            common default.
        value: Specify as: integer data type using xs:integer, float data type
            using xs:double, string data type using xs:string, boolean data type
            using xs:boolean, binary data type using xs:hexBinary, enum data type
            using label name, relative time data type using xs:duration, absolute
            time data type using xs:dateTime.  Values must not exceed the
            characteristics for the data type or this is a validation error.
            Takes precedence over an initial value given in the data type. Values
            are calibrated unless there is an option to override it.
    """

    parameter_instance_ref: None | ParameterInstanceRefType = field(
        default=None,
        metadata={
            "name": "ParameterInstanceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    argument_instance_ref: None | ArgumentInstanceRefType = field(
        default=None,
        metadata={
            "name": "ArgumentInstanceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    comparison_operator: ComparisonOperatorsType = field(
        default=ComparisonOperatorsType.EQUALS_SIGN_EQUALS_SIGN,
        metadata={
            "name": "comparisonOperator",
            "type": "Attribute",
        },
    )
    value: str = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class ArgumentDynamicValueType:
    """
    Identical to DynamicValueType but supports argument instance references.

    Attributes:
        argument_instance_ref: Retrieve the value by referencing the value of an
            Argument.
        parameter_instance_ref: Retrieve the value by referencing the value of a
            Parameter.
        linear_adjustment: A slope and intercept may be applied to scale or shift
            the value selected from the argument or parameter.
    """

    argument_instance_ref: None | ArgumentInstanceRefType = field(
        default=None,
        metadata={
            "name": "ArgumentInstanceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    parameter_instance_ref: None | ParameterInstanceRefType = field(
        default=None,
        metadata={
            "name": "ParameterInstanceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    linear_adjustment: None | LinearAdjustmentType = field(
        default=None,
        metadata={
            "name": "LinearAdjustment",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class ArgumentMathOperationType:
    """
    Describe a value to set to a destination Parameter after completion of a
    commanding lifecycle step.

    Attributes:
        value_operand: Use a constant in the calculation.
        this_parameter_operand: Use the value of the target parameter in the
            calculation. It is the calibrated/engineering value only.  If the raw
            value is needed, specify it explicitly using
            ParameterInstanceRefOperand. Note this element has no content.
        operator: All operators utilize operands on the top values in the stack
            and leaving the result on the top of the stack.  Ternary operators
            utilize the top three operands on the stack, binary operators utilize
            the top two operands on the stack, and unary operators use the top
            operand on the stack.
        parameter_instance_ref_operand: This element is used to reference the
            last received/assigned value of any Parameter in this math operation.
        argument_instance_ref_operand: This element is used to reference a value
            of any Argument from this command instance in this math operation.
    """

    value_operand: list[str] = field(
        default_factory=list,
        metadata={
            "name": "ValueOperand",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    this_parameter_operand: list[str] = field(
        default_factory=list,
        metadata={
            "name": "ThisParameterOperand",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    operator: list[MathOperatorsType] = field(
        default_factory=list,
        metadata={
            "name": "Operator",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    parameter_instance_ref_operand: list[ParameterInstanceRefType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterInstanceRefOperand",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    argument_instance_ref_operand: list[ArgumentInstanceRefType] = field(
        default_factory=list,
        metadata={
            "name": "ArgumentInstanceRefOperand",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class BaseAlarmType:
    """
    Supplies an optional non-reference-able name and short description for alarms.

    Also includes an optional ancillary data for any special local flags, note that
    these may not necessarily transfer to another recipient of an instance document.

    Attributes:
        ancillary_data_set:
        name: The alarm definition may be named.
        short_description: An optional brief description of this alarm
            definition.
    """

    ancillary_data_set: None | AncillaryDataSetType = field(
        default=None,
        metadata={
            "name": "AncillaryDataSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    short_description: None | str = field(
        default=None,
        metadata={
            "name": "shortDescription",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class BaseCalibratorType:
    """
    Supplies an optional non-reference-able name and short description for
    calibrators.

    Also includes an optional ancillary data for any special local flags, note that
    these may not necessarily transfer to another recipient of an instance document.

    Attributes:
        ancillary_data_set: Optional additional ancillary information for this
            calibrator/algorithm
        name: Optional name for this calibrator/algorithm
        short_description: Optional description for this calibrator/algorithm
    """

    ancillary_data_set: None | AncillaryDataSetType = field(
        default=None,
        metadata={
            "name": "AncillaryDataSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    short_description: None | str = field(
        default=None,
        metadata={
            "name": "shortDescription",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class BaseMetaCommandType:
    """
    When specified, a BaseMetaCommand element identifies that this MetaCommand
    inherits (extends) another MetaCommand.

    It's required ArgumentAssignmentList narrows or this command from the parent.
    This is typically used when specializing a generic MetaCommand to a specific
    MetaCommand. See MetaCommandType.

    Attributes:
        argument_assignment_list: Argument Assignments specialize a MetaCommand
            or BlockMetaCommand when inheriting from another MetaCommand.
            General argument values can be restricted to specific values to
            further specialize the MetaCommand.
        meta_command_ref: Reference to the MetaCommand definition that this
            MetaCommand extends.
    """

    argument_assignment_list: None | ArgumentAssignmentListType = field(
        default=None,
        metadata={
            "name": "ArgumentAssignmentList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    meta_command_ref: str = field(
        metadata={
            "name": "metaCommandRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )


@dataclass(kw_only=True)
class ComparisonCheckType(BaseComparisonType):
    """
    Describe the comparison between the instance (value) of a parameter against
    either a specified value or another parameter instance.

    Attributes:
        parameter_instance_ref: Left hand side parameter instance.
        comparison_operator: Comparison operator.
        value: Right hand side value.  Specify as: integer data type using
            xs:integer, float data type using xs:double, string data type using
            xs:string, boolean data type using xs:boolean, binary data type using
            xs:hexBinary, enum data type using label name, relative time data
            type using xs:duration, absolute time data type using xs:dateTime.
            Values must not exceed the characteristics for the data type or this
            is a validation error. Takes precedence over an initial value given
            in the data type. Values are calibrated unless there is an option to
            override it.
    """

    parameter_instance_ref: list[ParameterInstanceRefType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterInstanceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
            "max_occurs": 2,
        },
    )
    comparison_operator: ComparisonOperatorsType = field(
        metadata={
            "name": "ComparisonOperator",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    value: None | str = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class ComparisonType(ParameterInstanceRefType):
    """
    A simple ParameterInstanceRef to value comparison.

    The string supplied in the value attribute needs to be converted to a type
    matching the Parameter being compared to. For integer types it is base 10 form.
    Floating point types may be specified in normal (100.0) or scientific (1.0e2)
    form. The value is truncated to use the least significant bits that match the
    bit size of the Parameter being compared to.

    Attributes:
        comparison_operator: Operator to use for the comparison with the common
            equality operator as the default.
        value: Specify value as a string compliant with the XML schema (xs) type
            specified for each XTCE type: integer=xs:integer; float=xs:double;
            string=xs:string; boolean=xs:boolean; binary=xs:hexBinary;
            enum=xs:string from EnumerationList; relative time= xs:duration;
            absolute time=xs:dateTime.  Supplied value must be within the
            ValidRange specified for the type.
    """

    comparison_operator: ComparisonOperatorsType = field(
        default=ComparisonOperatorsType.EQUALS_SIGN_EQUALS_SIGN,
        metadata={
            "name": "comparisonOperator",
            "type": "Attribute",
        },
    )
    value: str = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class DescriptionType:
    """
    Defines an abstract schema type used as basis for NameDescriptionType and
    OptionalNameDescriptionType, includes an attribute for a short description and
    an element for a longer unbounded description.

    This type also provides alias set and ancillary data set See AliasSetType and
    AncillaryDataSetType.

    Attributes:
        long_description: Optional long form description to be used for
            explanatory descriptions of this item and may include HTML markup
            using CDATA.  Long Descriptions are of unbounded length.
        alias_set: Used to contain an alias (alternate) name or ID for this item.
            See AliasSetType for additional explanation.
        ancillary_data_set: Use for any non-standard data associated with this
            named item.  See AncillaryDataSetType for additional explanation.
        short_description: Optional short description to be used for explanation
            of this item.  It is recommended that the short description be kept
            under 80 characters in length.
    """

    long_description: None | str = field(
        default=None,
        metadata={
            "name": "LongDescription",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    alias_set: None | AliasSetType = field(
        default=None,
        metadata={
            "name": "AliasSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    ancillary_data_set: None | AncillaryDataSetType = field(
        default=None,
        metadata={
            "name": "AncillaryDataSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    short_description: None | str = field(
        default=None,
        metadata={
            "name": "shortDescription",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class DynamicValueType:
    """
    Uses a parameter instance to obtain the value.

    The parameter value may be optionally adjusted by a Linear function or use a
    series of boolean expressions to lookup the value. Anything more complex and a
    DynamicValue with a CustomAlgorithm may be used.

    Attributes:
        parameter_instance_ref: Retrieve the value by referencing the value of a
            Parameter.
        linear_adjustment: A slope and intercept may be applied to scale or shift
            the value selected from the argument or parameter.
    """

    parameter_instance_ref: ParameterInstanceRefType = field(
        metadata={
            "name": "ParameterInstanceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    linear_adjustment: None | LinearAdjustmentType = field(
        default=None,
        metadata={
            "name": "LinearAdjustment",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class EnumerationAlarmListType:
    """
    Attributes:
        enumeration_alarm: Describe an alarm state for an enumeration label where
            the label is engineer/calibrated value. Note that labels may
            represent multiple raw/uncalbrated values.
    """

    enumeration_alarm: list[EnumerationAlarmLevelType] = field(
        default_factory=list,
        metadata={
            "name": "EnumerationAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class InputParameterInstanceRefType(ParameterInstanceRefType):
    """
    Names an input parameter to the algorithm.

    There are two attributes to InputParm, inputName and parameterName.
    parameterName is a parameter reference name for a parameter that will be used in
    this algorithm. inputName is an optional "friendly" name for the input
    parameter.
    """

    input_name: None | str = field(
        default=None,
        metadata={
            "name": "inputName",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class MetaCommandStepType:
    """
    Describe a MetaCommand step, consisting MetaCommand reference and argument list.

    See MetaCommandStepListType and NameReferenceType.
    """

    argument_assignment_list: None | ArgumentAssignmentListType = field(
        default=None,
        metadata={
            "name": "ArgumentAssignmentList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    meta_command_ref: str = field(
        metadata={
            "name": "metaCommandRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )


@dataclass(kw_only=True)
class OutputSetType:
    output_parameter_ref: list[OutputParameterRefType] = field(
        default_factory=list,
        metadata={
            "name": "OutputParameterRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class ParametersToSuspendAlarmsOnSetType:
    """
    Sometimes it is necessary to suspend alarms - particularly 'change' alarms for
    commands that will change the value of a Parameter.
    """

    parameter_to_suspend_alarms_on: list[ParameterToSuspendAlarmsOnType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterToSuspendAlarmsOn",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class RateInStreamWithStreamNameType(RateInStreamType):
    """
    Define the expected appearance (rate) of a container in a named stream where the
    rate is defined on either a perSecond or perContainer update basis.

    Many programs and platforms have variable reporting rates for containers and
    these can be commanded. As a result, this element is only useful to some users
    and generally does not affect the processing of the received containers
    themselves. See ContainerType and RateInStreamType.

    Attributes:
        stream_ref: Reference to a named stream for which this rate specification
            applies.
    """

    stream_ref: str = field(
        metadata={
            "name": "streamRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )


@dataclass(kw_only=True)
class ReferenceTimeType:
    """
    Most time values are relative to another time e.g. seconds are relative to
    minutes, minutes are relative to hours.

    This type is used to describe this relationship starting with the least
    significant time Parameter to and progressing to the most significant time
    parameter.

    Attributes:
        offset_from:
        epoch: Epochs may be specified as an xs date where time is implied to be
            00:00:00, xs dateTime, or string enumeration of common epochs.  The
            enumerations are TAI (used by CCSDS and others), J2000, UNIX (also
            known as POSIX), and GPS.
    """

    offset_from: None | ParameterInstanceRefType = field(
        default=None,
        metadata={
            "name": "OffsetFrom",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    epoch: None | XmlDate | XmlDateTime | EpochTimeEnumsType = field(
        default=None,
        metadata={
            "name": "Epoch",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class StringAlarmListType:
    """
    Describe an ordered collection of string alarms, where duplicates are valid.

    Evaluate the alarms in list order. The first to evaluate to true takes
    precedence. See StringAlarmLevelType.
    """

    string_alarm: list[StringAlarmLevelType] = field(
        default_factory=list,
        metadata={
            "name": "StringAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class TimeAssociationType(ParameterInstanceRefType):
    """
    Describes a time association consisting of an instance of an absolute time
    parameter (parameterRef) and this entry.

    Because telemetry parameter instances are oftentimes "time-tagged" with a timing
    signal either provided on the ground or on the space system. This data element
    allows one to specify which of possibly many AbsoluteTimeParameters to use to
    "time-tag" parameter instances with. See AbsoluteTimeParameterType.

    Attributes:
        interpolate_time: If true, then the current value of the AbsoluteTime
            will be projected to current time.  In other words, if the value of
            the AbsoluteTime parameter was set 10 seconds ago, then 10 seconds
            will be added to its value before associating this time with the
            parameter.
        offset: The offset is used to supply a relative time offset from the time
            association and to this parameter
        unit: Specify the units the offset is in, the default is seconds.
    """

    interpolate_time: bool = field(
        default=True,
        metadata={
            "name": "interpolateTime",
            "type": "Attribute",
        },
    )
    offset: None | float = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    unit: TimeAssociationUnitType = field(
        default=TimeAssociationUnitType.SECONDS,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ToStringType:
    """
    Attributes:
        number_format: This element describes how a numeric value should be
            represented in engineering/calibrated form.  The defaults reflect the
            most common form.
    """

    number_format: NumberFormatType = field(
        metadata={
            "name": "NumberFormat",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class TriggerSetType:
    """
    A trigger is used to initiate the processing of some algorithm.

    A trigger may be based on an update of a Parameter, receipt of a Container, or
    on a time basis. Triggers may also have a maximum rate that limits how often the
    trigger can be invoked.

    Attributes:
        on_parameter_update_trigger: This element instructs the trigger to invoke
            the algorithm evaluation when a Parameter update is received.
        on_container_update_trigger: This element instructs the trigger to invoke
            the algorithm evaluation when a Container is received.
        on_periodic_rate_trigger: This element instructs the trigger to invoke
            the algorithm evaluation using a timer.
        name: Triggers may optionally be named.
        trigger_rate: This attribute is a maximum rate that constrains how
            quickly this trigger may evaluate the algorithm to avoid flooding the
            implementation.  The default is once per second.  Setting to 0
            results in no maximum.
    """

    on_parameter_update_trigger: list[OnParameterUpdateTriggerType] = field(
        default_factory=list,
        metadata={
            "name": "OnParameterUpdateTrigger",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    on_container_update_trigger: list[OnContainerUpdateTriggerType] = field(
        default_factory=list,
        metadata={
            "name": "OnContainerUpdateTrigger",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    on_periodic_rate_trigger: list[OnPeriodicRateTriggerType] = field(
        default_factory=list,
        metadata={
            "name": "OnPeriodicRateTrigger",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    trigger_rate: int = field(
        default=1,
        metadata={
            "name": "triggerRate",
            "type": "Attribute",
            "min_inclusive": 0,
        },
    )


@dataclass(kw_only=True)
class UnitSetType:
    """
    Describe an ordered collection of units that form a unit-expression.

    Units may be described for both calibrated/engineering values and also
    potentially uncalibrated/raw values. See UnitType.

    Attributes:
        unit: Describe the exponent, factor, form, and description for a unit.
            The attributes are optional because different programs use this
            element in different ways, depending on vendor support.
    """

    unit: list[UnitType] = field(
        default_factory=list,
        metadata={
            "name": "Unit",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class AndedConditionsType(BaseConditionsType):
    """
    Describe two or more conditions that are logically anded together.

    Conditions may be a mix of Condition and ORedCondition. See ORedConditionType
    and BooleanExpressionType.

    Attributes:
        condition: Condition elements describe a test similar to the Comparison
            element except that the parameters used have additional flexibility
            for the compare.
        ored_conditions: This element describes tests similar to the
            ComparisonList element except that the parameters used are more
            flexible and the and/or for multiple checks can be specified.
    """

    class Meta:
        name = "ANDedConditionsType"

    condition: list[ComparisonCheckType] = field(
        default_factory=list,
        metadata={
            "name": "Condition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 2,
        },
    )
    ored_conditions: list[OredConditionsType] = field(
        default_factory=list,
        metadata={
            "name": "ORedConditions",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 2,
        },
    )


@dataclass(kw_only=True)
class AlarmMultiRangesType(BaseAlarmType):
    """
    Describe any number of alarm ranges, each with its own level (normal, warning,
    watch, distress, critical, severe) and range form (inside -- (min,max),
    [min,max), (min, max], [min, max], or outside -- (-inf, min) or (-inf,min] and
    [max, +inf) or (max,+inf).

    Ranges may overlap, be disjoint and so forth. Ranges within the value spectrum
    non-specified are non-normal. The most severe range level of value within the
    ranges is the level of the alarm. Range values are in calibrated engineering
    units. See FloatRangeType.

    Attributes:
        range: Describe any number of alarm ranges, each with its own level
            (normal, warning, watch, distress, critical, severe) and range form
            (inside -- (min,max),[min,max), (min, max], [min, max], or outside --
            (-inf, min) or (-inf,min] and [max, +inf) or (max,+inf).. Ranges may
            overlap, be disjoint and so forth. Ranges within the value spectrum
            non-specified are non-normal. The most severe range level of value
            within the ranges is the level of the alarm. Range values are in
            calibrated engineering units. See FloatRangeType.
    """

    range: list[MultiRangeType] = field(
        default_factory=list,
        metadata={
            "name": "Range",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class AlarmRangesType(BaseAlarmType):
    """
    Describe up to six ranges where either less severe ranges are a subset of more
    severe ranges (outside), or more severe ranges are a subset of less severe
    ranges (inside).

    In both forms, the undefined least severe range is normal. Range values are in
    calibrated engineering units. See FloatRangeType.

    Attributes:
        watch_range: A range of least concern. Considered to be below the most
            commonly used Warning level.
        warning_range: A range of concern that represents the most commonly used
            minimum concern level for many software applications.
        distress_range: A range of concern in between the most commonly used
            Warning and Critical levels.
        critical_range: A range of concern that represents the most commonly used
            maximum concern level for many software applications.
        severe_range: A range of highest concern. Considered to be above the most
            commonly used Critical level.
        range_form: A value of outside specifies that the most severe range is
            outside all the other ranges: -severe -critical -distress -warning
            -watch normal +watch +warning +distress +critical +severe.  This
            means each min, max pair are a range: (-inf, min) or (-inf, min], and
            [max, inf) or (max, inf).  However a value of inside "inverts" these
            bands: -normal -watch -warning -distress -critical severe +critical
            +distress +warning +watch, +normal.  This means each min, max pair
            form a range of (min, max) or [min, max) or (min, max] or [min, max].
            The most common form used is "outside" and it is the default.  The
            set notation used defines parenthesis as exclusive and square
            brackets as inclusive.
    """

    watch_range: None | FloatRangeType = field(
        default=None,
        metadata={
            "name": "WatchRange",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    warning_range: None | FloatRangeType = field(
        default=None,
        metadata={
            "name": "WarningRange",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    distress_range: None | FloatRangeType = field(
        default=None,
        metadata={
            "name": "DistressRange",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    critical_range: None | FloatRangeType = field(
        default=None,
        metadata={
            "name": "CriticalRange",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    severe_range: None | FloatRangeType = field(
        default=None,
        metadata={
            "name": "SevereRange",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    range_form: RangeFormType = field(
        default=RangeFormType.OUTSIDE,
        metadata={
            "name": "rangeForm",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArgumentAndedConditionsType(BaseConditionsType):
    """
    Identical to ANDedConditionsType but supports argument instance references.

    Attributes:
        condition: Condition elements describe a test similar to the Comparison
            element except that the arguments/parameters used have additional
            flexibility for the compare.
        ored_conditions: This element describes tests similar to the
            ComparisonList element except that the arguments/parameters used are
            more flexible and the and/or for multiple checks can be specified.
    """

    class Meta:
        name = "ArgumentANDedConditionsType"

    condition: list[ArgumentComparisonCheckType] = field(
        default_factory=list,
        metadata={
            "name": "Condition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 2,
        },
    )
    ored_conditions: list[ArgumentOredConditionsType] = field(
        default_factory=list,
        metadata={
            "name": "ORedConditions",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 2,
        },
    )


@dataclass(kw_only=True)
class ArgumentComparisonListType:
    """
    Identical to ComparisonListType but supports argument instance references.

    Attributes:
        comparison: List of Comparison elements must all be true for the
            comparison to evaluate to true.
    """

    comparison: list[ArgumentComparisonType] = field(
        default_factory=list,
        metadata={
            "name": "Comparison",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class ArgumentInputSetType:
    """
    Identical to InputSetType but supports argument instance references.

    Attributes:
        input_parameter_instance_ref: Reference a parameter to serve as an input
            to the algorithm.
        input_argument_instance_ref: Reference an argument to serve as an input
            to the algorithm.
        constant: Supply a local constant name and value to input to this
            algorithm.
    """

    input_parameter_instance_ref: list[InputParameterInstanceRefType] = field(
        default_factory=list,
        metadata={
            "name": "InputParameterInstanceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    input_argument_instance_ref: list[ArgumentInstanceRefType] = field(
        default_factory=list,
        metadata={
            "name": "InputArgumentInstanceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    constant: list[ConstantType] = field(
        default_factory=list,
        metadata={
            "name": "Constant",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class ComparisonListType:
    """
    All comparisons must be true.

    Attributes:
        comparison: List of Comparison elements must all be true for the
            comparison to evaluate to true.
    """

    comparison: list[ComparisonType] = field(
        default_factory=list,
        metadata={
            "name": "Comparison",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class InputSetType:
    """
    Attributes:
        input_parameter_instance_ref: Reference a parameter to serve as an input
            to the algorithm.
        constant: Supply a local constant name and value to input to this
            algorithm.
    """

    input_parameter_instance_ref: list[InputParameterInstanceRefType] = field(
        default_factory=list,
        metadata={
            "name": "InputParameterInstanceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    constant: list[ConstantType] = field(
        default_factory=list,
        metadata={
            "name": "Constant",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class MathOperationCalibratorType(BaseCalibratorType):
    """
    Describe a mathematical function for calibration where the mathematical function
    is defined using the MathOperationType.

    Attributes:
        value_operand: Use a constant in the calculation.
        this_parameter_operand: Use the value of this parameter in the
            calculation. It is the calibrator's value only.  If the raw value is
            needed, specify it explicitly using ParameterInstanceRefOperand. Note
            this element has no content.
        operator: All operators utilize operands on the top values in the stack
            and leaving the result on the top of the stack.  Ternary operators
            utilize the top three operands on the stack, binary operators utilize
            the top two operands on the stack, and unary operators use the top
            operand on the stack.
        parameter_instance_ref_operand: This element is used to reference the
            last received/assigned value of any Parameter in this math operation.
    """

    value_operand: list[str] = field(
        default_factory=list,
        metadata={
            "name": "ValueOperand",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    this_parameter_operand: list[str] = field(
        default_factory=list,
        metadata={
            "name": "ThisParameterOperand",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    operator: list[MathOperatorsType] = field(
        default_factory=list,
        metadata={
            "name": "Operator",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    parameter_instance_ref_operand: list[ParameterInstanceRefType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterInstanceRefOperand",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class MetaCommandStepListType:
    """
    Describe the list of MetaCommand definitions that form the block command.

    Contains an ordered list of MetaCommandSteps where each step is a MetaCommand
    with associated arguments, duplicates are valid. See BlockMetaCommandType.

    Attributes:
        meta_command_step: A MetaCommand with specific specified argument values
            to include in the BlockMetaCommand.
    """

    meta_command_step: list[MetaCommandStepType] = field(
        default_factory=list,
        metadata={
            "name": "MetaCommandStep",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class NameDescriptionType(DescriptionType):
    """
    Defines a base schema type definition used by many other schema types throughout
    schema.

    Use it to describe a name with optional descriptions, aliases, and ancillary
    data. See NameType, LongDescriptionType, ShortDescriptionType, AliasSetType and
    AncillaryDataSetType.

    Attributes:
        name: The name of this defined item.  See NameType for restriction
            information.
    """

    name: str = field(
        metadata={
            "type": "Attribute",
            "pattern": r"[^.\[\]:/ \t]+",
        }
    )


@dataclass(kw_only=True)
class OptionalNameDescriptionType(DescriptionType):
    """
    The type definition used by most elements that have an optional name with
    optional descriptions.

    Attributes:
        name: Optional name of this defined item.  See NameType for restriction
            information.
    """

    name: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"[^.\[\]:/ \t]+",
        },
    )


@dataclass(kw_only=True)
class ParameterToSetType(ParameterRefType):
    """
    Sets a Parameter to a new value (either from a derivation or explicitly) after
    the command has been verified (all verifications have passed).

    Attributes:
        derivation: Specify a simple algorithm to use to set the target Parameter
            value.  See ArgumentMathOperationType.
        new_value: Specify value as a string compliant with the XML schema (xs)
            type specified for each XTCE type: integer=xs:integer;
            float=xs:double; string=xs:string; boolean=xs:boolean;
            binary=xs:hexBinary; enum=xs:string from EnumerationList; relative
            time= xs:duration; absolute time=xs:dateTime.  Supplied value must be
            within the ValidRange specified for the Parameter and appropriate for
            the type.
        set_on_verification: This attribute provides more specific control over
            when the Parameter value is set.  By default, it is when the command
            have all verifications complete.  See VerifierEnumerationType.
    """

    derivation: None | ArgumentMathOperationType = field(
        default=None,
        metadata={
            "name": "Derivation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    new_value: None | str = field(
        default=None,
        metadata={
            "name": "NewValue",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    set_on_verification: VerifierEnumerationType = field(
        default=VerifierEnumerationType.COMPLETE,
        metadata={
            "name": "setOnVerification",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class PercentCompleteType:
    """
    Describe a percentage complete that is fixed from 0 to 100, or as value from a
    parameter.

    See ExecutionVerifierType.

    Attributes:
        fixed_value: 0 to 100 percent
        dynamic_value: Uses a parameter instance to obtain the value. The
            parameter value may be optionally adjusted by a Linear function or
            use a series of boolean expressions to lookup the value. Anything
            more complex and a DynamicValue with a CustomAlgorithm may be used.
    """

    fixed_value: None | float = field(
        default=None,
        metadata={
            "name": "FixedValue",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_inclusive": 0.0,
            "max_inclusive": 100.0,
        },
    )
    dynamic_value: None | DynamicValueType = field(
        default=None,
        metadata={
            "name": "DynamicValue",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class PolynomialCalibratorType(BaseCalibratorType):
    """
    Describe a polynomial equation for calibration.

    This is a calibration type where a curve in a raw vs calibrated plane is
    described using a set of polynomial coefficients. Raw values are converted to
    calibrated values by finding a position on the curve corresponding to the raw
    value. The first coefficient belongs with the X^0 term, the next coefficient
    belongs to the X^1 term and so on. See CalibratorType.

    Attributes:
        term: A single term in the polynomial function.
    """

    term: list[TermType] = field(
        default_factory=list,
        metadata={
            "name": "Term",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class RateInStreamSetType:
    rate_in_stream: list[RateInStreamWithStreamNameType] = field(
        default_factory=list,
        metadata={
            "name": "RateInStream",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class SplineCalibratorType(BaseCalibratorType):
    """
    Describe a spline function for calibration using a set of at least 2 points.

    Raw values are converted to calibrated values by finding a position on the line
    corresponding to the raw value. The line may be interpolated and/or extrapolated
    as needed. The interpolation order may be specified for all the points and
    overridden on individual points. The algorithm triggers on the input parameter.
    See CalibratorType.

    Attributes:
        spline_point: Describes a single point of the spline or piecewise
            function.
        order: The interpolation order to apply to the overall spline function.
            Order 0 is no slope between the points (flat).  Order 1 is linear
            interpolation.  Order 2 would be quadratic and in this special case,
            3 points would be required, etc.
        extrapolate: Extrapolation allows the closest outside point and the
            associated interpolation to extend outside of the range of the points
            in the spline function.
    """

    spline_point: list[SplinePointType] = field(
        default_factory=list,
        metadata={
            "name": "SplinePoint",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 2,
        },
    )
    order: int = field(
        default=1,
        metadata={
            "type": "Attribute",
            "min_inclusive": 0,
        },
    )
    extrapolate: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArgumentOredConditionsType(BaseConditionsType):
    """
    Identical to ORedConditionsType but supports argument instance references.

    Attributes:
        condition: Condition elements describe a test similar to the Comparison
            element except that the arguments/parameters used have additional
            flexibility for the compare.
        anded_conditions: This element describes tests similar to the
            ComparisonList element except that the arguments/parameters used are
            more flexible and the and/or for multiple checks can be specified.
    """

    class Meta:
        name = "ArgumentORedConditionsType"

    condition: list[ArgumentComparisonCheckType] = field(
        default_factory=list,
        metadata={
            "name": "Condition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 2,
        },
    )
    anded_conditions: list[ArgumentAndedConditionsType] = field(
        default_factory=list,
        metadata={
            "name": "ANDedConditions",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 2,
        },
    )


@dataclass(kw_only=True)
class ArgumentType(NameDescriptionType):
    """
    An Argument has a name and can take on values with the underlying value type
    described by the ArgumentTypeRef.

    Describe the properties of a command argument referring to a data type (argument
    type). The bulk of properties associated with a command argument are in its
    argument type. The initial value specified here, overrides the initial value in
    the argument type. See BaseDataType, BaseTimeDataType and NameReferenceType.

    Attributes:
        argument_type_ref: Specify the reference to the argument type from the
            ArgumentTypeSet area using the path reference rules, either local to
            this SpaceSystem, relative, or absolute.
        initial_value: Specify as: integer data type using xs:integer, float data
            type using xs:double, string data type using xs:string, boolean data
            type using xs:boolean, binary data type using xs:hexBinary, enum data
            type using label name, relative time data type using xs:duration,
            absolute time data type using xs:dateTime, arrays using JSON syntax
            (e.g. '[1, 3, 4]', and aggregates using JSON syntax '{"member1": 1,
            "member2": "foo"}' ). Values must not exceed the characteristics for
            the data type or this is a validation error. Takes precedence over an
            initial value given in the data type. Values are calibrated unless
            there is an option to override it.
    """

    argument_type_ref: str = field(
        metadata={
            "name": "argumentTypeRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )
    initial_value: None | str = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArrayDataTypeType(NameDescriptionType):
    """
    A base schema type for describing an array data type.

    The number of and size of each dimension is defined in its two child types. See
    NameReferenceType, ArrayArgumentType and ArrayParameterType.

    Attributes:
        array_type_ref: Reference to the data type that represents the type of
            the elements for this array.
        initial_value: Initial values for the individual elements of the array
            may be provided here at the type definition using JSON style array
            notation (e.g. [1, 2, 3]).  It may be multi-dimension, in which case
            the sequence matches the sequence of the Dimension elements in the
            DimensionList.  When provided here, the initialValue attributes in
            the type definition specified in attribute arrayTypeRef are ignored.
    """

    array_type_ref: str = field(
        metadata={
            "name": "arrayTypeRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )
    initial_value: None | str = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class BlockMetaCommandType(NameDescriptionType):
    """
    Describe an ordered grouping of MetaCommands into a list, duplicates are valid.

    The block contains argument values fully specified. See MetaCommandStepListType.

    Attributes:
        meta_command_step_list: List of the MetaCommands to include in this
            BlockMetaCommand.
    """

    meta_command_step_list: MetaCommandStepListType = field(
        metadata={
            "name": "MetaCommandStepList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class CalibratorType(BaseCalibratorType):
    """
    Describe a calibrator to transform a source data type raw/uncalibrated value
    (e.g. an integer count from a spacecraft) to an engineering unit/calibrated
    value for users (e.g. a float).

    Attributes:
        spline_calibrator: Describes a calibrator in the form of a piecewise
            defined function
        polynomial_calibrator: Describes a calibrator in the form of a polynomial
            function
        math_operation_calibrator: Describes a calibrator in the form of a
            user/program/implementation defined function
    """

    spline_calibrator: None | SplineCalibratorType = field(
        default=None,
        metadata={
            "name": "SplineCalibrator",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    polynomial_calibrator: None | PolynomialCalibratorType = field(
        default=None,
        metadata={
            "name": "PolynomialCalibrator",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    math_operation_calibrator: None | MathOperationCalibratorType = field(
        default=None,
        metadata={
            "name": "MathOperationCalibrator",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class ChangeAlarmRangesType(AlarmRangesType):
    """
    Describe an alarm when the parameter value's rate-of-change is either too fast
    or too slow.

    The change may be with respect to time (the default) or with respect to samples
    (delta alarms). Use the changeType attribute to select the type: changePerSecond
    (time) or changePerSample (delta). The change may also be ether relative (as a
    percentage change) or absolute as set by the changeBasis attribute. (Delta
    alarms are typically absolute but percentage is conceivable). The alarm also
    requires the spanOfInterest in both samples and seconds to have passed before it
    is to trigger. For time based rate of change alarms, the time specified in
    spanOfInterestInSeconds is used to calculate the change. For sample based rate
    of change alarms, the change is calculated over the number of samples specified
    in spanOfInterestInSamples. A typical delta alarm would set:
    changeType=changePerSample, changeBasis=absoluteChange,
    spanOfInterestInSamples=1. A typical time based version would set:
    changeType=changePerSecond, changeBasis=percentageChange, and
    spaceOfInterestInSeconds=1. To set the ranges use maxInclusive, the following
    definition applies: | Normal.maxInclusive | &lt;= | Watch.maxInclusive | &lt;= |
    Warning.maxInclusive | &lt;= | Distress.maxInclusive | &lt;= |
    Critical.maxInclusive | &lt;= | Severe.maxInclusive |. And it is further assumed
    the absolute value of each range and sampled value it taken to evaluate the
    alarm. See NumericAlarmType.
    """

    change_type: ChangeSpanType = field(
        default=ChangeSpanType.CHANGE_PER_SECOND,
        metadata={
            "name": "changeType",
            "type": "Attribute",
        },
    )
    change_basis: ChangeBasisType = field(
        default=ChangeBasisType.ABSOLUTE_CHANGE,
        metadata={
            "name": "changeBasis",
            "type": "Attribute",
        },
    )
    span_of_interest_in_samples: int = field(
        default=1,
        metadata={
            "name": "spanOfInterestInSamples",
            "type": "Attribute",
            "min_inclusive": 1,
        },
    )
    span_of_interest_in_seconds: float = field(
        default=0.0,
        metadata={
            "name": "spanOfInterestInSeconds",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class MathOperationType(MathOperationCalibratorType):
    """
    Postfix (aka Reverse Polish Notation (RPN)) notation is used to describe
    mathmatical equations.

    It uses a stack where operands (either fixed values or ParameterInstances) are
    pushed onto the stack from first to last in the XML. As the operators are
    specified, each pops off operands as it evaluates them, and pushes the result
    back onto the stack. In this case postfix is used to avoid having to specify
    parenthesis. To convert from infix to postfix, use Dijkstra's "shunting yard"
    algorithm.
    """


@dataclass(kw_only=True)
class MemberType(NameDescriptionType):
    """
    Describe a member field in an AggregateDataType.

    Each member has a name and a type reference to a data type for the aggregate
    member name. If this aggregate is a Parameter aggregate, then the typeRef is a
    parameter type reference. If this aggregate is an Argument aggregate, then the
    typeRef is an argument type reference. References to an array data type is
    currently not supported. Circular references are not allowed. See
    MemberListType. AggregateParameterType and AggregateArgumentType.

    Attributes:
        type_ref:
        initial_value: Used to set the initial calibrated values of Parameters
            and Arguments.  Will overwrite an initial value defined for the
            ParameterType or ArgumentType definition elements.  For integer types
            it is base 10 form.  Floating point types may be specified in normal
            (100.0) or scientific (1.0e2) form.  Time types are specified using
            the ISO 8601 formats described for XTCE time data types.  Initial
            values for string types, may include C language style (\\n, \\t, \\",
            \\\\, etc.) escape sequences.
    """

    type_ref: str = field(
        metadata={
            "name": "typeRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )
    initial_value: None | str = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class OredConditionsType(BaseConditionsType):
    """
    Describe two or more conditions that are logically ored together.

    Conditions may be a mix of Condition and ANDedCondition. See ORedConditionType
    and BooleanExpressionType.

    Attributes:
        condition: Condition elements describe a test similar to the Comparison
            element except that the parameters used have additional flexibility
            for the compare.
        anded_conditions: This element describes tests similar to the
            ComparisonList element except that the parameters used are more
            flexible and the and/or for multiple checks can be specified.
    """

    class Meta:
        name = "ORedConditionsType"

    condition: list[ComparisonCheckType] = field(
        default_factory=list,
        metadata={
            "name": "Condition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 2,
        },
    )
    anded_conditions: list[AndedConditionsType] = field(
        default_factory=list,
        metadata={
            "name": "ANDedConditions",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 2,
        },
    )


@dataclass(kw_only=True)
class PcmstreamType(NameDescriptionType):
    """
    A PCM Stream Type is the high level definition for all Pulse Code Modulated
    (PCM) (i.e., binary) streams.
    """

    class Meta:
        name = "PCMStreamType"

    bit_rate_in_bps: None | float = field(
        default=None,
        metadata={
            "name": "bitRateInBPS",
            "type": "Attribute",
        },
    )
    pcm_type: Pcmtype = field(
        default=Pcmtype.NRZL,
        metadata={
            "name": "pcmType",
            "type": "Attribute",
        },
    )
    inverted: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ParameterToSetListType:
    """
    Parameters that are set with a new value after the command has been sent.

    Appended to the Base Command list.
    """

    parameter_to_set: list[ParameterToSetType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterToSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class ServiceType(NameDescriptionType):
    """
    Holds a set of services, logical groups of containers OR messages (not both).
    """

    message_ref_set: None | MessageRefSetType = field(
        default=None,
        metadata={
            "name": "MessageRefSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    container_ref_set: None | ContainerRefSetType = field(
        default=None,
        metadata={
            "name": "ContainerRefSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class SimpleAlgorithmType(NameDescriptionType):
    """
    The simplest form of algorithm, a SimpleAlgorithmType contains an area for a
    free-form pseudo code description of the algorithm plus a Set of references to
    external algorithms.

    External algorithms are usually unique to a ground system type. Multiple
    external algorithms are possible because XTCE documents may be used across
    multiple ground systems.
    """

    algorithm_text: None | AlgorithmTextType = field(
        default=None,
        metadata={
            "name": "AlgorithmText",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    external_algorithm_set: None | ExternalAlgorithmSetType = field(
        default=None,
        metadata={
            "name": "ExternalAlgorithmSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class TimeAlarmRangesType(AlarmRangesType):
    """
    Attributes:
        time_units: Time units, with the default being in seconds.
    """

    time_units: TimeUnitsType = field(
        default=TimeUnitsType.SECONDS,
        metadata={
            "name": "timeUnits",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArgumentBooleanExpressionType:
    """
    Identical to BooleanExpressionType but supports argument instance references.

    Attributes:
        condition: Condition elements describe a test similar to the Comparison
            element except that the arguments/parameters used have additional
            flexibility.
        anded_conditions: This element describes tests similar to the
            ComparisonList element except that the arguments/parameters used are
            more flexible.
        ored_conditions: This element describes tests similar to the
            ComparisonList element except that the arguments/parameters used are
            more flexible.
    """

    condition: None | ArgumentComparisonCheckType = field(
        default=None,
        metadata={
            "name": "Condition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    anded_conditions: None | ArgumentAndedConditionsType = field(
        default=None,
        metadata={
            "name": "ANDedConditions",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    ored_conditions: None | ArgumentOredConditionsType = field(
        default=None,
        metadata={
            "name": "ORedConditions",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class ArgumentInputAlgorithmType(SimpleAlgorithmType):
    """
    Identical to InputAlgorithmType but supports argument instance references.

    Attributes:
        input_set: The InputSet describes the list of arguments and/or parameters
            that should be made available as input arguments to the algorithm.
    """

    input_set: None | ArgumentInputSetType = field(
        default=None,
        metadata={
            "name": "InputSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class ArgumentListType:
    """
    Defines a list of Arguments for a command definition.

    Attributes:
        argument: Defines an Argument for a command definition.  Arguments are
            local to the MetaCommand, BlockMetaCommand, and those that inherit
            from the definition.
    """

    argument: list[ArgumentType] = field(
        default_factory=list,
        metadata={
            "name": "Argument",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class BooleanExpressionType:
    """
    Holds an arbitrarily complex boolean expression.

    Attributes:
        condition: Condition elements describe a test similar to the Comparison
            element except that the parameters used have additional flexibility.
        anded_conditions: This element describes tests similar to the
            ComparisonList element except that the parameters used are more
            flexible.
        ored_conditions: This element describes tests similar to the
            ComparisonList element except that the parameters used are more
            flexible.
    """

    condition: None | ComparisonCheckType = field(
        default=None,
        metadata={
            "name": "Condition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    anded_conditions: None | AndedConditionsType = field(
        default=None,
        metadata={
            "name": "ANDedConditions",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    ored_conditions: None | OredConditionsType = field(
        default=None,
        metadata={
            "name": "ORedConditions",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class FrameStreamType(PcmstreamType):
    """
    The top level type definition for all data streams that are frame based.

    Attributes:
        container_ref: This Container (usually abstract) is the container that is
            in the fixed frame stream.  Normally, this is a general container
            type from which many specific containers are inherited.
        service_ref:
        stream_ref: This is a reference to a connecting stream - say a custom
            stream.
    """

    container_ref: None | ContainerRefType = field(
        default=None,
        metadata={
            "name": "ContainerRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    service_ref: None | ServiceRefType = field(
        default=None,
        metadata={
            "name": "ServiceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    stream_ref: None | StreamRefType = field(
        default=None,
        metadata={
            "name": "StreamRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class InputAlgorithmType(SimpleAlgorithmType):
    """
    A set of labeled inputs is added to the SimpleAlgorithmType.

    Attributes:
        input_set: The InputSet describes the list of parameters that should be
            made available as input arguments to the algorithm.
    """

    input_set: None | InputSetType = field(
        default=None,
        metadata={
            "name": "InputSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class MemberListType:
    """
    Order is important only if the name of the AggregateParameter or Aggregate
    Argument is directly referenced in SequenceContainers.

    In this case the members are assued to be added sequentially (in the order
    listed here) into the Container.
    """

    member: list[MemberType] = field(
        default_factory=list,
        metadata={
            "name": "Member",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class ServiceSetType:
    """
    A service is a logical grouping of container and/or messages.
    """

    service: list[ServiceType] = field(
        default_factory=list,
        metadata={
            "name": "Service",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class TriggeredMathOperationType(MathOperationType):
    trigger_set: TriggerSetType = field(
        metadata={
            "name": "TriggerSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    output_parameter_ref: str = field(
        metadata={
            "name": "outputParameterRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
        }
    )


@dataclass(kw_only=True)
class AggregateDataType(NameDescriptionType):
    """
    A base schema type for describing a complex data type analogous to a C-struct.

    Each field of the data type is called a Member. Each Member is part of the
    MemberList which forms the list of items to be placed under this data type's
    name. The MemberList defines a data block and block's size is defined by the
    DataEncodings of each Member's type reference. The data members are ordered and
    contiguous in the MemberList element (packed). Each member may be addressed by
    the dot syntax similar to C such as P.voltage if P is the referring parameter
    and voltage is of a member of P's aggregate type. See MemberType,
    MemberListType, DataEncodingType, NameReferenceType, AggregateParameterType and
    AggregateArgumentType.

    Attributes:
        member_list: Ordered list of the members of the aggregate/structure.
            Members are contiguous.
        initial_value: Initial values for the individual members of the
            aggregate/structure may be provided here at the type definition using
            JSON style notation (e.g. '{ "member1": 2, "member2": "foo" }').
            When Member elements provide initialValue attributes, they take
            precedence over these since these are at the type definition level
            and the Member element acts like a Parameter element.  These may also
            recurse into members that are also aggregates.
    """

    member_list: MemberListType = field(
        metadata={
            "name": "MemberList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    initial_value: None | str = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArgumentMatchCriteriaType:
    """
    Identical to MatchCriteriaType but supports argument instance references.

    Attributes:
        comparison: A simple comparison check involving a single test of an
            argument or parameter value.
        comparison_list: A series of simple comparison checks with an implicit
            'and' in that they all must be true for the overall condition to be
            true.
        boolean_expression: An arbitrarily complex boolean expression that has
            additional flexibility on the terms beyond the Comparison and
            ComparisonList elements.
        custom_algorithm: An escape to an externally defined algorithm.
    """

    comparison: None | ArgumentComparisonType = field(
        default=None,
        metadata={
            "name": "Comparison",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    comparison_list: None | ArgumentComparisonListType = field(
        default=None,
        metadata={
            "name": "ComparisonList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    boolean_expression: None | ArgumentBooleanExpressionType = field(
        default=None,
        metadata={
            "name": "BooleanExpression",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    custom_algorithm: None | ArgumentInputAlgorithmType = field(
        default=None,
        metadata={
            "name": "CustomAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class AutoInvertType:
    """
    After searching for the frame sync marker for some number of bits, it may be
    desirable to invert the incoming data, and then look for frame sync.

    In some cases this will require an external algorithm.
    """

    invert_algorithm: None | InputAlgorithmType = field(
        default=None,
        metadata={
            "name": "InvertAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    bad_frames_to_auto_invert: int = field(
        default=1024,
        metadata={
            "name": "badFramesToAutoInvert",
            "type": "Attribute",
            "min_inclusive": 1,
        },
    )


@dataclass(kw_only=True)
class CheckWindowAlgorithmsType:
    """
    Used by CommandVerifiers to limit the time allocated to check for the
    verification.

    See CommandVerifierType.
    """

    start_check: InputAlgorithmType = field(
        metadata={
            "name": "StartCheck",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    stop_time: InputAlgorithmType = field(
        metadata={
            "name": "StopTime",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class ChecksumType:
    """
    Describe checksum or hash function definiton.

    See ErrorDetectCorrectType.

    Attributes:
        input_algorithm: Provided to account for an algorithm not otherwise
            listed by enumeration.  Assumed to return the computed checksum.
        bits_from_reference: An offset of non-zero may be specified to skip some
            bits against the reference position in the reference attribute.
        reference: The bits involved in the calculation may start at the
            beginning or the end of the container.
        name: Qualified list of named common checksum algorithms. If custom is
            chosen, InputAlgorithm must be set.
        hash_size_in_bits: The hashing algorithm may use a larger internal bucket
            size than the emitted value size in bits captured by the parameterRef
            attribute.
        parameter_ref: Reference to the parameter that contains the value of this
            computed checksum or hash based on this container.  This attribute is
            optional because not all implementations verify (telemetry) or create
            (telecommand) error control fields using the XTCE definition.
    """

    input_algorithm: None | InputAlgorithmType = field(
        default=None,
        metadata={
            "name": "InputAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    bits_from_reference: int = field(
        default=0,
        metadata={
            "name": "bitsFromReference",
            "type": "Attribute",
            "min_inclusive": 0,
        },
    )
    reference: ReferencePointType = field(
        default=ReferencePointType.START,
        metadata={
            "type": "Attribute",
        },
    )
    name: ChecksumTypeName = field(
        metadata={
            "type": "Attribute",
        }
    )
    hash_size_in_bits: None | int = field(
        default=None,
        metadata={
            "name": "hashSizeInBits",
            "type": "Attribute",
            "min_inclusive": 1,
        },
    )
    parameter_ref: None | str = field(
        default=None,
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
        },
    )


@dataclass(kw_only=True)
class CustomAlarmType(BaseAlarmType):
    """
    Describe a custom, algorithmic alarm condition.

    The algorithm is assumed to return a boolean value: true or false. See
    AlarmType.

    Attributes:
        input_algorithm: Algorithm returns a boolean.
    """

    input_algorithm: InputAlgorithmType = field(
        metadata={
            "name": "InputAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class InputOutputAlgorithmType(InputAlgorithmType):
    """
    A set of labeled outputs are added to the SimpleInputAlgorithmType.
    """

    output_set: None | OutputSetType = field(
        default=None,
        metadata={
            "name": "OutputSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    thread: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class MatchCriteriaType:
    """
    Contains either a simple Comparison, a ComparisonList, an arbitrarily complex
    BooleanExpression or an escape to an externally defined algorithm.

    Attributes:
        comparison: A simple comparison check involving a single test of a
            parameter value.
        comparison_list: A series of simple comparison checks with an implicit
            'and' in that they all must be true for the overall condition to be
            true.
        boolean_expression: An arbitrarily complex boolean expression that has
            additional flexibility on the terms beyond the Comparison and
            ComparisonList elements.
        custom_algorithm: An escape to an externally defined algorithm.
    """

    comparison: None | ComparisonType = field(
        default=None,
        metadata={
            "name": "Comparison",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    comparison_list: None | ComparisonListType = field(
        default=None,
        metadata={
            "name": "ComparisonList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    boolean_expression: None | BooleanExpressionType = field(
        default=None,
        metadata={
            "name": "BooleanExpression",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    custom_algorithm: None | InputAlgorithmType = field(
        default=None,
        metadata={
            "name": "CustomAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class MathAlgorithmType(NameDescriptionType):
    """
    Describe a postfix (Reverse Polish Notation (RPN)) notation based mathmatical
    equations.

    See MathOperationType.

    Attributes:
        math_operation: The contents of the Math Operation as an algorithm
            definition in RPN.  See TriggeredMathOperationType.
    """

    math_operation: TriggeredMathOperationType = field(
        metadata={
            "name": "MathOperation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class AggregateArgumentType(AggregateDataType):
    """
    Describe a complex data type analogous to a C-struct.

    Each field of the data type is called a Member. Each Member is part of the
    MemberList which forms the list of items to be placed under this data type's
    name. The MemberList defines a data block and block's size is defined by the
    DataEncodings of each Member's type reference. The data members are ordered and
    contiguous in the MemberList element (packed). Each member may be addressed by
    the dot syntax similar to C such as P.voltage if P is the referring parameter
    and voltage is of a member of P's aggregate type. See MemberType,
    MemberListType, DataEncodingType, NameReferenceType, and AggregateDataType.
    """


@dataclass(kw_only=True)
class AggregateParameterType(AggregateDataType):
    """
    Describe a complex data type analogous to a C-struct.

    Each field of the data type is called a Member. Each Member is part of the
    MemberList which forms the list of items to be placed under this data type's
    name. The MemberList defines a data block and block's size is defined by the
    DataEncodings of each Member's type reference. The data members are ordered and
    contiguous in the MemberList element (packed). Each member may be addressed by
    the dot syntax similar to C such as P.voltage if P is the referring parameter
    and voltage is of a member of P's aggregate type. See MemberType,
    MemberListType, DataEncodingType, NameReferenceType, and AggregateDataType.
    """


@dataclass(kw_only=True)
class AlarmConditionsType:
    """
    Describe up to six levels: Normal, Watch, Warning, Distress, Critical, and
    Severe of conditions the alarm will trigger when true.

    The types are conditions available are a single comparison, a comparison list, a
    discrete lookup list, and custom algorithm. See MatchCriteriaType.

    Attributes:
        watch_alarm: An alarm state of least concern.  Considered to be below the
            most commonly used Warning level.
        warning_alarm: An alarm state of concern that represents the most
            commonly used minimum concern level for many software applications.
        distress_alarm: An alarm state of concern in between the most commonly
            used Warning and Critical levels.
        critical_alarm: An alarm state of concern that represents the most
            commonly used maximum concern level for many software applications.
        severe_alarm: An alarm state of highest concern.  Considered to be above
            the most commonly used Critical level.
    """

    watch_alarm: None | MatchCriteriaType = field(
        default=None,
        metadata={
            "name": "WatchAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    warning_alarm: None | MatchCriteriaType = field(
        default=None,
        metadata={
            "name": "WarningAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    distress_alarm: None | MatchCriteriaType = field(
        default=None,
        metadata={
            "name": "DistressAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    critical_alarm: None | MatchCriteriaType = field(
        default=None,
        metadata={
            "name": "CriticalAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    severe_alarm: None | MatchCriteriaType = field(
        default=None,
        metadata={
            "name": "SevereAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class ArgumentDiscreteLookupType(ArgumentMatchCriteriaType):
    """
    Identical to ArgumentDiscreteLookupType but supports argument instance
    references.

    Attributes:
        value: Value to use when the lookup conditions are true.
    """

    value: int = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class CommandVerifierType(OptionalNameDescriptionType):
    """
    A command verifier is used to check that the command has been successfully
    executed.

    Command Verifiers may be either a Custom Algorithm or a Boolean Check or the
    presence of a Container for a relative change in the value of a Parameter. The
    CheckWindow is a time period where the verification must test true to pass.

    Attributes:
        comparison_list: Verification is a list of comparisons.
        container_ref: Verification is a new instance of the referenced
            container. For example, sending a command to download memory then
            receiving a packet with the memory download would be verified upon
            receipt of the packet.
        parameter_value_change: Verification is a telemetry parameter value
            change on the ground.  For example, a command counter.
        custom_algorithm: Verification is outside the scope of regular command
            and telemetry processing.
        boolean_expression: Verification is a boolean expression of conditions.
        comparison: Verification is a single comparison.
        check_window: Define a time window for checking for verification.
        check_window_algorithms: Define a time window algorithmically for
            verification.
        argument_restriction_list: Optional list of argument values that manifest
            this post-transmission validation parameter value check.  When not
            present, this check applies to all instances of the command.
    """

    comparison_list: None | ComparisonListType = field(
        default=None,
        metadata={
            "name": "ComparisonList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    container_ref: None | ContainerRefType = field(
        default=None,
        metadata={
            "name": "ContainerRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    parameter_value_change: None | ParameterValueChangeType = field(
        default=None,
        metadata={
            "name": "ParameterValueChange",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    custom_algorithm: None | InputAlgorithmType = field(
        default=None,
        metadata={
            "name": "CustomAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    boolean_expression: None | BooleanExpressionType = field(
        default=None,
        metadata={
            "name": "BooleanExpression",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    comparison: None | ComparisonType = field(
        default=None,
        metadata={
            "name": "Comparison",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    check_window: None | CheckWindowType = field(
        default=None,
        metadata={
            "name": "CheckWindow",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    check_window_algorithms: None | CheckWindowAlgorithmsType = field(
        default=None,
        metadata={
            "name": "CheckWindowAlgorithms",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    argument_restriction_list: None | ArgumentAssignmentListType = field(
        default=None,
        metadata={
            "name": "ArgumentRestrictionList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class ContextMatchType(MatchCriteriaType):
    """
    A MatchCriteriaType used for Context selection.

    It is possible that no match evaluates to true, which results in the default
    element being used. It is also possible that a match can have an empty context
    change, in which case the default is replaced with nothing.
    """


@dataclass(kw_only=True)
class CustomStreamType(PcmstreamType):
    """
    A stream type where some level of custom processing (e.g. convolutional,
    encryption, compression) is performed.

    Has a reference to external algorithms for encoding and decoding algorithms.

    Attributes:
        encoding_algorithm:
        decoding_algorithm: Algorithm outputs may be used to set decoding quality
            parameters.
        encoded_stream_ref:
        decoded_stream_ref:
    """

    encoding_algorithm: InputAlgorithmType = field(
        metadata={
            "name": "EncodingAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    decoding_algorithm: InputOutputAlgorithmType = field(
        metadata={
            "name": "DecodingAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    encoded_stream_ref: str = field(
        metadata={
            "name": "encodedStreamRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )
    decoded_stream_ref: str = field(
        metadata={
            "name": "decodedStreamRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )


@dataclass(kw_only=True)
class DiscreteLookupType(MatchCriteriaType):
    """
    Describe a discrete value lookup and the value associated when the lookup
    evaluates to true.

    Attributes:
        value: Value to use when the lookup conditions are true.
    """

    value: int = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class ErrorDetectCorrectType:
    """
    Describe CRC, Checksum, Parity, or XOR for error detection and correction
    algorithm calculation.

    See CRCType, ChecksumType, ParityType, and XORType.

    Attributes:
        checksum: Describe checksum or hash function applied to all or part of
            this container definition.
        crc: Describe a Cyclic Redundancy Check (CRC) algorithm applied to all or
            part of this container definition.
        xor: Describe an "exclusive or" (XOR) checksum applied to all or part of
            this container definition.
        parity: Describe a parity applied to all or part of this container
            definition.
    """

    checksum: list[ChecksumType] = field(
        default_factory=list,
        metadata={
            "name": "Checksum",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    crc: list[Crctype] = field(
        default_factory=list,
        metadata={
            "name": "CRC",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    xor: list[Xortype] = field(
        default_factory=list,
        metadata={
            "name": "XOR",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    parity: list[ParityType] = field(
        default_factory=list,
        metadata={
            "name": "Parity",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class InputOutputTriggerAlgorithmType(InputOutputAlgorithmType):
    """
    Input output algorithm is extended with a set of labeled triggers.

    See InputOutputAlgorithmType.

    Attributes:
        trigger_set:
        trigger_container: First telemetry container from which the output
            parameter should be calculated.
        priority: Algorithm processing priority. If more than one algorithm is
            triggered by the same container, the lowest priority algorithm should
            be calculated first.
    """

    trigger_set: None | TriggerSetType = field(
        default=None,
        metadata={
            "name": "TriggerSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    trigger_container: None | str = field(
        default=None,
        metadata={
            "name": "triggerContainer",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        },
    )
    priority: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class MessageType(NameDescriptionType):
    """
    Attributes:
        match_criteria:
        container_ref: The ContainerRef should point to ROOT container that will
            describe an entire packet/minor frame or chunk of telemetry.
    """

    match_criteria: MatchCriteriaType = field(
        metadata={
            "name": "MatchCriteria",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    container_ref: ContainerRefType = field(
        metadata={
            "name": "ContainerRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class ParameterPropertiesType:
    """
    Describes extended properties/attributes of Parameter definitions.

    Attributes:
        system_name: Optional.  Normally used when the database is built in a
            flat, non-hierarchical format.
        validity_condition: Optional condition that must be true for this
            Parameter to be valid.
        physical_address_set: When present, this set of elements describes
            physical address location(s) of the parameter where it is stored.
            Typically this is on the data source, although that is not
            constrained by this schema.
        time_association: This time will override any Default value for
            TimeAssociation.
        data_source: This attribute describes the nature of the source entity for
            which this parameter receives a value.  Implementations assign
            different attributes/properties internally to a parameter based on
            the anticipated data source.
        read_only: A Parameter marked as 'readOnly' true is non-settable by users
            and applications/services that do not represent the data source
            itself.  Note that a slight conceptual overlap exists here between
            the 'dataSource' attribute and this attribute when the data source is
            'constant'.  For a constant data source, then 'readOnly' should be
            'true'.  Application implementations may choose to implicitly enforce
            this.  Some implementations have both concepts of a Parameter that is
            settable or non-settable and a Constant in different parts of their
            internal data model.
        persistence: A Parameter marked to persist should retain the latest value
            through resets/restarts to the extent that is possible or defined in
            the implementation.  The net effect is that the initial/default value
            on a Parameter is only seen once or when the system has a reset to
            revert to initial/default values.
    """

    system_name: None | str = field(
        default=None,
        metadata={
            "name": "SystemName",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    validity_condition: None | MatchCriteriaType = field(
        default=None,
        metadata={
            "name": "ValidityCondition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    physical_address_set: None | PhysicalAddressSetType = field(
        default=None,
        metadata={
            "name": "PhysicalAddressSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    time_association: None | TimeAssociationType = field(
        default=None,
        metadata={
            "name": "TimeAssociation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    data_source: None | TelemetryDataSourceType = field(
        default=None,
        metadata={
            "name": "dataSource",
            "type": "Attribute",
        },
    )
    read_only: bool = field(
        default=False,
        metadata={
            "name": "readOnly",
            "type": "Attribute",
        },
    )
    persistence: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class RestrictionCriteriaType(MatchCriteriaType):
    """
    Define one or more conditions (constraints) for container inheritance.

    A container is instantiable if its constraints are true. Constraint conditions
    may be a comparison, a list of comparisons, a boolean expression, or a graph of
    containers that are instantiable (if all containers are instantiable the
    condition is true). See BaseContainerType, ComparisonType, ComparisonListType,
    BooleanExpressionType and NextContainerType.

    Attributes:
        next_container: Reference to the named container that must follow this
            container in the stream sequence.
    """

    next_container: None | ContainerRefType = field(
        default=None,
        metadata={
            "name": "NextContainer",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class SyncStrategyType:
    """
    A Sync Strategy specifies the strategy on how to find frames within a stream of
    PCM data.

    The sync strategy is based upon a state machine that begins in the 'Search'
    state until the first sync marker is found. Then it goes into the 'Verify' state
    until a specified number of successive good sync markers are found. Then, the
    state machine goes into the 'Lock' state, in the 'Lock' state frames are
    considered good. Should a sync marker be missed in the 'Lock' state, the state
    machine will transition into the 'Check' state, if the next sync marker is where
    it's expected within a specified number of frames, then the state machine will
    transition back to the 'Lock' state, it not it will transition back to 'Search'.

    Attributes:
        auto_invert:
        verify_to_lock_good_frames:
        check_to_lock_good_frames:
        max_bit_errors_in_sync_pattern: Maximum number of bit errors in the sync
            pattern (marker).
    """

    auto_invert: None | AutoInvertType = field(
        default=None,
        metadata={
            "name": "AutoInvert",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    verify_to_lock_good_frames: int = field(
        default=4,
        metadata={
            "name": "verifyToLockGoodFrames",
            "type": "Attribute",
            "min_inclusive": 0,
        },
    )
    check_to_lock_good_frames: int = field(
        default=1,
        metadata={
            "name": "checkToLockGoodFrames",
            "type": "Attribute",
            "min_inclusive": 0,
        },
    )
    max_bit_errors_in_sync_pattern: int = field(
        default=0,
        metadata={
            "name": "maxBitErrorsInSyncPattern",
            "type": "Attribute",
            "min_inclusive": 0,
        },
    )


@dataclass(kw_only=True)
class TransmissionConstraintType(MatchCriteriaType):
    """
    A CommandTransmission constraint is used to check that the command can be run in
    the current operating mode and may block the transmission of the command if the
    constraint condition is true.

    Attributes:
        argument_restriction_list: Optional list of argument values that manifest
            this pre-transmission constraint parameter value check.
        time_out: Pause during timeOut, fail when the timeout passes
        suspendable: Indicates whether the constraints for a Command may be
            suspended.
    """

    argument_restriction_list: None | ArgumentAssignmentListType = field(
        default=None,
        metadata={
            "name": "ArgumentRestrictionList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    time_out: None | XmlDuration = field(
        default=None,
        metadata={
            "name": "timeOut",
            "type": "Attribute",
        },
    )
    suspendable: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class AcceptedVerifierType(CommandVerifierType):
    """
    A verifier that means the destination has accepted the command.
    """


@dataclass(kw_only=True)
class AlarmType(BaseAlarmType):
    """
    Defines a base schema type used to build up the other data type specific alarm
    types.

    The definition includes a count to go into alarm (minViolations - the counts to
    go out of alarm is the same), a condition style alarm and a custom alarm. See
    AlarmConditionType, CustomAlgorithmType, BinaryAlarmConditionType,
    BooleanAlarmType, BinaryContextAlarmType, EnumerationAlarmType,
    NumericAlarmType, StringAlarmType, TimeAlarmType, TimeAlarmConditionType.

    Attributes:
        alarm_conditions: A MatchCriteria may be specified for each of the 5
            alarm levels. Each level is optional and the alarm should be the
            highest level to test true.
        custom_alarm: An escape for ridiculously complex alarm conditions. Will
            trigger on changes to the containing Parameter.
        min_violations: The number of successive instances that meet the alarm
            conditions for the alarm to trigger. The default is 1.
        min_conformance: Optionally specify the number of successive instances
            that do not meet the alarm conditions to leave the alarm state. If
            this attribute is not specified, it is treated as being equal to
            minViolations (symmetric).
        disabled: The initial state of this alarm definition as delivered.  When
            true, this leaves the alarm definition empty for the parameter and
            also short circuits the remaining context matches and the default so
            no alarm is active on the parameter.
    """

    alarm_conditions: None | AlarmConditionsType = field(
        default=None,
        metadata={
            "name": "AlarmConditions",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    custom_alarm: None | CustomAlarmType = field(
        default=None,
        metadata={
            "name": "CustomAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    min_violations: int = field(
        default=1,
        metadata={
            "name": "minViolations",
            "type": "Attribute",
            "min_inclusive": 1,
        },
    )
    min_conformance: int = field(
        default=1,
        metadata={
            "name": "minConformance",
            "type": "Attribute",
            "min_inclusive": 1,
        },
    )
    disabled: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class AlgorithmSetType:
    """
    An unordered collection of algorithms.
    """

    custom_algorithm: list[InputOutputTriggerAlgorithmType] = field(
        default_factory=list,
        metadata={
            "name": "CustomAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    math_algorithm: list[MathAlgorithmType] = field(
        default_factory=list,
        metadata={
            "name": "MathAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class ArgumentDiscreteLookupListType:
    """
    Identical to DiscreteLookupListType but supports argument instance references.

    Attributes:
        discrete_lookup: Describe a lookup condition set using discrete values
            from arguments and/or parameters.
        default_value: In the event that no lookup condition evaluates to true,
            then this value will be used.
    """

    discrete_lookup: list[ArgumentDiscreteLookupType] = field(
        default_factory=list,
        metadata={
            "name": "DiscreteLookup",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )
    default_value: int = field(
        metadata={
            "name": "defaultValue",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class BaseContainerType:
    """
    Describe a child/parent container inheritance relationship.

    Describe constraints with RestrictionCriteria, conditions that must be true for
    this container to be an extension of the parent container. A constraint can be
    used to convey the identifying features of the telemetry format such as the
    CCSDS application id or minor-frame id. See RestrictionCriteriaType and
    SequenceContainerType.

    Attributes:
        restriction_criteria: Contains the conditions that must evaluate to true
            in order for this container to be an extension of the parent
            container.
        container_ref: Reference to the container that this container extends.
    """

    restriction_criteria: None | RestrictionCriteriaType = field(
        default=None,
        metadata={
            "name": "RestrictionCriteria",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    container_ref: str = field(
        metadata={
            "name": "containerRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )


@dataclass(kw_only=True)
class CompleteVerifierType(CommandVerifierType):
    """
    A possible set of verifiers that all must be true for the command be considered
    completed.

    Consider that some may not participate due to argument value restriction, if
    that element is used.
    """

    return_parm_ref: None | ParameterRefType = field(
        default=None,
        metadata={
            "name": "ReturnParmRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class ContextCalibratorType:
    """
    Context calibrations are applied when the ContextMatch is true.

    Context calibrators overide Default calibrators.
    """

    context_match: ContextMatchType = field(
        metadata={
            "name": "ContextMatch",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    calibrator: CalibratorType = field(
        metadata={
            "name": "Calibrator",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class ContextSignificanceType:
    """
    Describe a significance level for a MetaCommand definition where the
    significance level depends on matching a context value.

    See ContextMatchType and SignificanceType.

    Attributes:
        context_match: Describe the context matching value and source that will
            enable the Significance listed in the Significance element.
        significance: Describe the signficance of this MetaCommand definition.
            See SignificanceType.
    """

    context_match: ContextMatchType = field(
        metadata={
            "name": "ContextMatch",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    significance: SignificanceType = field(
        metadata={
            "name": "Significance",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class DataEncodingType:
    """
    Describes how a particular piece of data is sent or received from some
    non-native, off-platform device. (e.g. a spacecraft).

    Attributes:
        error_detect_correct: DEPRECATED: Use the ErrorDetectCorrect element in
            the container elements instead.
        bit_order: Describes the bit ordering of the encoded value.
        byte_order: Describes the endianness of the encoded value.
    """

    error_detect_correct: None | ErrorDetectCorrectType = field(
        default=None,
        metadata={
            "name": "ErrorDetectCorrect",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    bit_order: BitOrderType = field(
        default=BitOrderType.MOST_SIGNIFICANT_BIT_FIRST,
        metadata={
            "name": "bitOrder",
            "type": "Attribute",
        },
    )
    byte_order: ByteOrderCommonType | str = field(
        default=ByteOrderCommonType.MOST_SIGNIFICANT_BYTE_FIRST,
        metadata={
            "name": "byteOrder",
            "type": "Attribute",
            "pattern": r"(0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15)(,(0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15))*",
        },
    )


@dataclass(kw_only=True)
class DiscreteLookupListType:
    """
    Describe an ordered table of integer values and associated conditions, forming a
    lookup table.

    The list may have duplicates. The table is evaluated from first to last, the
    first condition to be true returns the value associated with it. See
    DiscreteLookupType.

    Attributes:
        discrete_lookup: Describe a lookup condition set using discrete values
            from parameters.
        default_value: In the event that no lookup condition evaluates to true,
            then this value will be used.
    """

    discrete_lookup: list[DiscreteLookupType] = field(
        default_factory=list,
        metadata={
            "name": "DiscreteLookup",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )
    default_value: int = field(
        metadata={
            "name": "defaultValue",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class ExecutionVerifierType(CommandVerifierType):
    """
    A verifier that indicates that the command is being executed.

    An optional Element indicates how far along the command has progressed either as
    a fixed value or an (possibly scaled) ParameterInstance value.
    """

    percent_complete: None | PercentCompleteType = field(
        default=None,
        metadata={
            "name": "PercentComplete",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class FailedVerifierType(CommandVerifierType):
    """
    When true, indicates that the command failed. timeToWait is how long to wait for
    the FailedVerifier to test true.
    """

    return_parm_ref: None | ParameterRefType = field(
        default=None,
        metadata={
            "name": "ReturnParmRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class FixedFrameSyncStrategyType(SyncStrategyType):
    """
    Describe a sync pattern and an optional reference to an algorithm used to invert
    the stream if the frame sync pattern is not found.

    See FixedFrameStreamType.

    Attributes:
        sync_pattern: The pattern of bits used to look for frame synchronization.
            See SyncPatternType.
    """

    sync_pattern: SyncPatternType = field(
        metadata={
            "name": "SyncPattern",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class MessageSetType(OptionalNameDescriptionType):
    message: list[MessageType] = field(
        default_factory=list,
        metadata={
            "name": "Message",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class ParameterType(NameDescriptionType):
    """
    Describe the properties of a telemetry parameter, including its data type
    (parameter type).

    The bulk of properties associated with a telemetry parameter are in its
    parameter type. The initial value specified here, overrides the initial value in
    the parameter type. A parameter may be local, in which case its parameter type
    would have no data encodings. Ideally such a definition would also set data
    source in parameter properties to "local" but the syntax does not enforce this.
    See BaseDataType, BaseTimeDataType, and NameReferenceType.

    Attributes:
        parameter_properties: Specify additional properties for this Parameter
            used by the implementation of tailor the behavior and attributes of
            the Parameter.  When not specified, the defaults on the
            ParameterProperties element attributes are assumed.
        parameter_type_ref: Specify the reference to the parameter type from the
            ParameterTypeSet area using the path reference rules, either local to
            this SpaceSystem, relative, or absolute.
        initial_value: Specify as: integer data type using xs:integer, float data
            type using xs:double, string data type using xs:string, boolean data
            type using xs:boolean, binary data type using xs:hexBinary, enum data
            type using label name, relative time data type using xs:duration,
            absolute time data type using xs:dateTime, arrays using JSON syntax
            (e.g. '[1, 3, 4]', and aggregates using JSON syntax '{"member1": 1,
            "member2": "foo"}' ). Values must not exceed the characteristics for
            the data type or this is a validation error. Takes precedence over an
            initial value given in the data type. Values are calibrated unless
            there is an option to override it.
    """

    parameter_properties: None | ParameterPropertiesType = field(
        default=None,
        metadata={
            "name": "ParameterProperties",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    parameter_type_ref: str = field(
        metadata={
            "name": "parameterTypeRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )
    initial_value: None | str = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class QueuedVerifierType(CommandVerifierType):
    """
    A verifer that means the command is scheduled for execution by the destination.
    """


@dataclass(kw_only=True)
class ReceivedVerifierType(CommandVerifierType):
    """
    A verifier that simply means the destination has received the command.
    """


@dataclass(kw_only=True)
class SentFromRangeVerifierType(CommandVerifierType):
    """
    Sent from range means the command has been transmitted to the spacecraft by the
    network that connects the ground system to the spacecraft.

    Typically, this verifier would come from something other than the spacecraft,
    such as a modem or front end processor.
    """


@dataclass(kw_only=True)
class TransferredToRangeVerifierType(CommandVerifierType):
    """
    Transferred to range means the command has been received to the network that
    connects the ground system to the spacecraft.

    Typically, this verifier would come from something other than the spacecraft,
    such as a modem or front end processor.
    """


@dataclass(kw_only=True)
class TransmissionConstraintListType:
    """
    Appended to the TramsmissionConstraint List of the base command.

    Constraints are checked in order.

    Attributes:
        transmission_constraint: A constraint that potentially blocks
            transmission of this command based on parameter values for all
            instances or optionally limited to only when specified argument
            values are used in the command.
    """

    transmission_constraint: list[TransmissionConstraintType] = field(
        default_factory=list,
        metadata={
            "name": "TransmissionConstraint",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class VariableFrameSyncStrategyType(SyncStrategyType):
    flag: FlagType = field(
        metadata={
            "name": "Flag",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class ArgumentIntegerValueType:
    """
    Identical to IntegerValueType but supports argument instance references.

    Attributes:
        fixed_value: Use a fixed integer value.
        dynamic_value: Determine the value by interrogating an instance of an
            argument or parameter.
        discrete_lookup_list: Determine the value by interrogating an instance of
            an argument or parameter and selecting a specified value based on
            tests of the value of that argument or parameter.
    """

    fixed_value: None | int = field(
        default=None,
        metadata={
            "name": "FixedValue",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    dynamic_value: None | ArgumentDynamicValueType = field(
        default=None,
        metadata={
            "name": "DynamicValue",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    discrete_lookup_list: None | ArgumentDiscreteLookupListType = field(
        default=None,
        metadata={
            "name": "DiscreteLookupList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class ArgumentVariableStringType:
    """
    Identical to VariableStringType but supports argument instance references.

    Attributes:
        dynamic_value: Determine the container size in bits by interrogating an
            instance of a parameter or argument.
        discrete_lookup_list: Determine the container size in bits by
            interrogating an instance of a parameter or argument and selecting a
            specified value based on tests of the value of that parameter or
            argument.
        leading_size: In some string implementations, the size of the string
            contents (not the memory allocation size) is determined by a leading
            numeric value.  This is sometimes referred to as Pascal strings.  If
            a LeadingSize is specified, then the TerminationChar element does not
            have a functional meaning.
        termination_char: The termination character that represents the end of
            the string contents.  For C and most strings, this is null (00),
            which is the default.
        max_size_in_bits: The upper bound of the size of this string data type so
            that the implementation can reserve/allocate enough memory to capture
            all reported instances of the string.
    """

    dynamic_value: None | ArgumentDynamicValueType = field(
        default=None,
        metadata={
            "name": "DynamicValue",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    discrete_lookup_list: None | ArgumentDiscreteLookupListType = field(
        default=None,
        metadata={
            "name": "DiscreteLookupList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    leading_size: None | LeadingSizeType = field(
        default=None,
        metadata={
            "name": "LeadingSize",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    termination_char: None | bytes = field(
        default=None,
        metadata={
            "name": "TerminationChar",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "format": "base16",
        },
    )
    max_size_in_bits: int = field(
        metadata={
            "name": "maxSizeInBits",
            "type": "Attribute",
            "min_inclusive": 1,
        }
    )


@dataclass(kw_only=True)
class BinaryAlarmType(AlarmType):
    """
    Describe alarm conditions specific to the binary data type, extends the basic
    AlarmType.
    """


@dataclass(kw_only=True)
class BooleanAlarmType(AlarmType):
    """
    Alarm conditions for Boolean types.
    """


@dataclass(kw_only=True)
class ContextCalibratorListType:
    """
    Describe an ordered list of calibrators with a context match.

    Useful when different calibrations must be used depending on a matching value.
    The first context that matches determines which calibrator to use. See
    IntegerDataEncodingType and FloatDataEncodingType.

    Attributes:
        context_calibrator: Describe a calibrator that depends on a matching
            value using a ContextMatch.  When the context matches for the
            calibrator, the default calibrator is overridden, if it exists.
    """

    context_calibrator: list[ContextCalibratorType] = field(
        default_factory=list,
        metadata={
            "name": "ContextCalibrator",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class ContextSignificanceListType:
    """
    Describe an ordered list of ContextSignificance elements where the significance
    on the first context match to test true is used as the significance of the
    MetaCommand.

    If there is a DefaultSignificance, it is overrideen by the matching context. See
    ContextSignificantType and MetaCommandType.

    Attributes:
        context_significance: A Context contains a different significance
            definition and a context match.  The match takes precedence over any
            default significance when the first in the overall list evaluates to
            true.
    """

    context_significance: list[ContextSignificanceType] = field(
        default_factory=list,
        metadata={
            "name": "ContextSignificance",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class EnumerationAlarmType(AlarmType):
    """
    Describe alarm conditions specific to the enumeration data type, extends the
    basic AlarmType with an EnumerationAlarmList.

    The alarms are described using the label (engineering/calibrated value) of the
    enumerated parameter. Enumeration labels may represent several raw/uncalibrated
    values, so as a result, a single alarm definition here may represent multiple
    raw values in the enumerated parameter. It is not necessary to define an alarm
    for raw/uncalibrated values that do not map to an enumeration. Implementations
    should implicitly define this as an alarm case, of which the manifestation of
    that is program/implementation specific. See EnumeratedParameterType.

    Attributes:
        enumeration_alarm_list: List of alarm state definitions for this
            enumerated type.
        default_alarm_level: Alarm state name for when no enumeration alarms
            evaluate to true. This defaults to "normal", which is almost always
            the case. Setting it to another alarm state permits a form of
            "inverted logic" where the alarm list can specify the normal states
            instead of the alarm states.
    """

    enumeration_alarm_list: None | EnumerationAlarmListType = field(
        default=None,
        metadata={
            "name": "EnumerationAlarmList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    default_alarm_level: ConcernLevelsType = field(
        default=ConcernLevelsType.NORMAL,
        metadata={
            "name": "defaultAlarmLevel",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class FixedFrameStreamType(FrameStreamType):
    """
    For streams that contain a series of frames with a fixed frame length where the
    frames are found by looking for a marker in the data.

    This marker is sometimes called the frame sync pattern and sometimes the
    Asynchronous Sync Marker (ASM). This marker need not be contiguous although it
    usually is.

    Attributes:
        sync_strategy:
        sync_aperture_in_bits: Allowed slip (in bits) in either direction for the
            sync pattern
        frame_length_in_bits:
    """

    sync_strategy: FixedFrameSyncStrategyType = field(
        metadata={
            "name": "SyncStrategy",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    sync_aperture_in_bits: int = field(
        default=0,
        metadata={
            "name": "syncApertureInBits",
            "type": "Attribute",
            "min_inclusive": 0,
        },
    )
    frame_length_in_bits: int = field(
        metadata={
            "name": "frameLengthInBits",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class IntegerValueType:
    """
    Contains an Integer value; value may be provided directly or via the value in a
    parameter.

    Attributes:
        fixed_value: Use a fixed integer value.
        dynamic_value: Determine the value by interrogating an instance of a
            parameter.
        discrete_lookup_list: Determine the value by interrogating an instance of
            a parameter and selecting a specified value based on tests of the
            value of that parameter.
    """

    fixed_value: None | int = field(
        default=None,
        metadata={
            "name": "FixedValue",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    dynamic_value: None | DynamicValueType = field(
        default=None,
        metadata={
            "name": "DynamicValue",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    discrete_lookup_list: None | DiscreteLookupListType = field(
        default=None,
        metadata={
            "name": "DiscreteLookupList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class NumericAlarmType(AlarmType):
    """
    Describe alarm conditions specific to the numeric data types, extends the basic
    AlarmType with StaticAlarmRanges and ChangeAlarmRanges.

    See FloatParameterType and IntegerParameterType.

    Attributes:
        static_alarm_ranges: StaticAlarmRanges are used to trigger alarms when
            the parameter value passes some threshold value.
        change_alarm_ranges: ChangeAlarmRanges are used to trigger alarms when
            the parameter value changes by a rate or quantity from a reference.
        alarm_multi_ranges: Similar to but more lenient form of
            StaticAlarmRanges.
    """

    static_alarm_ranges: None | AlarmRangesType = field(
        default=None,
        metadata={
            "name": "StaticAlarmRanges",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    change_alarm_ranges: None | ChangeAlarmRangesType = field(
        default=None,
        metadata={
            "name": "ChangeAlarmRanges",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    alarm_multi_ranges: None | AlarmMultiRangesType = field(
        default=None,
        metadata={
            "name": "AlarmMultiRanges",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class ParameterSetType:
    """
    Describe an unordered collection of parameters where duplicates defined by the
    Parameter name attribute are invalid.

    The ParameterSet exists in both the TelemetryMetaData and the CommandMetaData
    element so that each may be built independently but from a single namespace. See
    TelemetryMetaDataType and CommandMetaDataType.

    Attributes:
        parameter: Defines a named and typed Parameter.
        parameter_ref: Used to include a Parameter defined in another sub-system
            in this sub-system.
    """

    parameter: list[ParameterType] = field(
        default_factory=list,
        metadata={
            "name": "Parameter",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    parameter_ref: list[ParameterRefType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class StringAlarmType(AlarmType):
    """
    Describe alarms specific to the string data type, extends the basic AlarmType,
    while adding a StringAlarmList and defaultAlarmLevel attribute.

    The string alarm list is evaluated in list order. See ConcernsLevelsType and
    StringAlarmListType.
    """

    string_alarm_list: None | StringAlarmListType = field(
        default=None,
        metadata={
            "name": "StringAlarmList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    default_alarm_level: ConcernLevelsType = field(
        default=ConcernLevelsType.NORMAL,
        metadata={
            "name": "defaultAlarmLevel",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class TimeAlarmType(AlarmType):
    """
    Alarms associated with time data types.

    Attributes:
        static_alarm_ranges: StaticAlarmRanges are used to trigger alarms when
            the parameter value passes some threshold value
        change_per_second_alarm_ranges: ChangePerSecondAlarmRanges are used to
            trigger alarms when the parameter value's rate-of-change passes some
            threshold value.  An alarm condition that triggers when the value
            changes too fast (or too slow)
    """

    static_alarm_ranges: None | TimeAlarmRangesType = field(
        default=None,
        metadata={
            "name": "StaticAlarmRanges",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    change_per_second_alarm_ranges: None | TimeAlarmRangesType = field(
        default=None,
        metadata={
            "name": "ChangePerSecondAlarmRanges",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class VariableFrameStreamType(FrameStreamType):
    """
    For streams that contain a series of frames with a variable frame length where
    the frames are found by looking for a series of one's or zero's (usually one's).

    The series is called the flag. in the PCM stream that are usually made to be
    illegal in the PCM stream by zero or one bit insertion.
    """

    sync_strategy: VariableFrameSyncStrategyType = field(
        metadata={
            "name": "SyncStrategy",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class VariableStringType:
    """
    Describe a variable string whose length may change between samples.

    Attributes:
        dynamic_value: Determine the container size in bits by interrogating an
            instance of a parameter.
        discrete_lookup_list: Determine the container size in bits by
            interrogating an instance of a parameter and selecting a specified
            value based on tests of the value of that parameter.
        leading_size: In some string implementations, the size of the string
            contents (not the memory allocation size) is determined by a leading
            numeric value.  This is sometimes referred to as Pascal strings.  If
            a LeadingSize is specified, then the TerminationChar element does not
            have a functional meaning.
        termination_char: The termination character that represents the end of
            the string contents.  For C and most strings, this is null (00),
            which is the default.
        max_size_in_bits: The upper bound of the size of this string data type so
            that the implementation can reserve/allocate enough memory to capture
            all reported instances of the string.
    """

    dynamic_value: None | DynamicValueType = field(
        default=None,
        metadata={
            "name": "DynamicValue",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    discrete_lookup_list: None | DiscreteLookupListType = field(
        default=None,
        metadata={
            "name": "DiscreteLookupList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    leading_size: None | LeadingSizeType = field(
        default=None,
        metadata={
            "name": "LeadingSize",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    termination_char: None | bytes = field(
        default=None,
        metadata={
            "name": "TerminationChar",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "format": "base16",
        },
    )
    max_size_in_bits: int = field(
        metadata={
            "name": "maxSizeInBits",
            "type": "Attribute",
            "min_inclusive": 1,
        }
    )


@dataclass(kw_only=True)
class VerifierSetType:
    """
    Describe a collection of unordered verifiers.

    A command verifier is a conditional check on the telemetry from a SpaceSystem
    that that provides positive indication on the processing state of a command.
    There are eight different verifiers each associated with different states in
    command processing: TransferredToRange, TransferredFromRange, Received,
    Accepted, Queued, Execution, Complete, and Failed. There may be multiple
    "complete" and "execution" verifiers. If the MetaCommand is part of an
    inheritance relation (BaseMetaCommand), the "complete" and "execution" verifier
    sets are appended to any defined in the parent MetaCommand. All others will
    override a verifier defined in a BaseMetaCommand. Duplicate verifiers in the
    list of CompleteVerifiers and ExecutionVerifiers before and after appending to
    the verifiers in BaseMetaCommand should be avoided. See MetaCommandType and
    BaseMetaCommandType for additional information.

    Attributes:
        transferred_to_range_verifier: Transferred to range means the command has
            been received to the network that connects the ground system to the
            spacecraft.  Typically, this verifier would come from something other
            than the spacecraft, such as a modem or front end processor.
        sent_from_range_verifier: Sent from range means the command has been
            transmitted to the spacecraft by the network that connects the ground
            system to the spacecraft.  Typically, this verifier would come from
            something other than the spacecraft, such as a modem or front end
            processor.
        received_verifier: A verifier that simply means the destination has
            received the command.
        accepted_verifier: A verifier that means the destination has accepted the
            command.
        queued_verifier: A verifer that means the command is scheduled for
            execution by the destination.
        execution_verifier: A verifier that indicates that the command is being
            executed.  An optional Element indicates how far along the command
            has progressed either as a fixed value or an (possibly scaled)
            ParameterInstance value.
        complete_verifier: A possible set of verifiers that all must be true for
            the command be considered completed.  Consider that some may not
            participate due to argument value restriction, if that element is
            used.
        failed_verifier: When true, indicates that the command failed.
            timeToWait is how long to wait for the FailedVerifier to test true.
    """

    transferred_to_range_verifier: None | TransferredToRangeVerifierType = field(
        default=None,
        metadata={
            "name": "TransferredToRangeVerifier",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    sent_from_range_verifier: None | SentFromRangeVerifierType = field(
        default=None,
        metadata={
            "name": "SentFromRangeVerifier",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    received_verifier: None | ReceivedVerifierType = field(
        default=None,
        metadata={
            "name": "ReceivedVerifier",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    accepted_verifier: None | AcceptedVerifierType = field(
        default=None,
        metadata={
            "name": "AcceptedVerifier",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    queued_verifier: None | QueuedVerifierType = field(
        default=None,
        metadata={
            "name": "QueuedVerifier",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    execution_verifier: list[ExecutionVerifierType] = field(
        default_factory=list,
        metadata={
            "name": "ExecutionVerifier",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    complete_verifier: list[CompleteVerifierType] = field(
        default_factory=list,
        metadata={
            "name": "CompleteVerifier",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    failed_verifier: None | FailedVerifierType = field(
        default=None,
        metadata={
            "name": "FailedVerifier",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class ArgumentBinaryDataEncodingType(DataEncodingType):
    """
    Identical to BinaryDataEncodingType but supports argument instance references.

    Attributes:
        size_in_bits: Number of bits this value occupies on the stream being
            encoded/decoded.
        from_binary_transform_algorithm: Used to convert binary data to an
            application data type
        to_binary_transform_algorithm: Used to convert binary data from an
            application data type to binary data
    """

    size_in_bits: ArgumentIntegerValueType = field(
        metadata={
            "name": "SizeInBits",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    from_binary_transform_algorithm: None | ArgumentInputAlgorithmType = field(
        default=None,
        metadata={
            "name": "FromBinaryTransformAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    to_binary_transform_algorithm: None | ArgumentInputAlgorithmType = field(
        default=None,
        metadata={
            "name": "ToBinaryTransformAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class ArgumentDimensionType:
    """
    Identical to DimensionType but supports argument instance references.

    Attributes:
        starting_index: zero based index
        ending_index:
    """

    starting_index: ArgumentIntegerValueType = field(
        metadata={
            "name": "StartingIndex",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    ending_index: ArgumentIntegerValueType = field(
        metadata={
            "name": "EndingIndex",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class ArgumentLocationInContainerInBitsType(ArgumentIntegerValueType):
    """
    Identical to LocationInContainerInBitsType but supports argument instance
    references.
    """

    reference_location: ReferenceLocationType = field(
        default=ReferenceLocationType.PREVIOUS_ENTRY,
        metadata={
            "name": "referenceLocation",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArgumentRepeatType:
    """
    Identical to RepeatType but supports argument instance references.

    Attributes:
        count: Value (either fixed or dynamic) that contains the count of
            repeated structures.
        offset:
    """

    count: ArgumentIntegerValueType = field(
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    offset: None | ArgumentIntegerValueType = field(
        default=None,
        metadata={
            "name": "Offset",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class ArgumentStringDataEncodingType(DataEncodingType):
    """
    Identical to StringDataEncodingType but supports argument instance references.

    Attributes:
        size_in_bits: Static length strings do not change in overall length
            between samples.   They may terminate before the end of their buffer
            using a terminating character, or by various lookups, or
            calculations.  But they have a maximum fixed size, and the data
            itself is always within that maximum size.
        variable: Variable length strings are those where the space occupied in a
            container can vary.  If the string has variable content but occupies
            the same amount of space when encoded should use the SizeInBits
            element.  Specification of a variable length string needs to consider
            that the implementation needs to allocate space to store the string.
            Specify the maximum possible length of the string data type for
            memory purposes and also specify the bit size of the string to use in
            containers with the dynamic elements.
        encoding: The character set encoding of this string data type.
    """

    size_in_bits: None | SizeInBitsType = field(
        default=None,
        metadata={
            "name": "SizeInBits",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    variable: None | ArgumentVariableStringType = field(
        default=None,
        metadata={
            "name": "Variable",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    encoding: StringEncodingType = field(
        default=StringEncodingType.UTF_8,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class BinaryContextAlarmType(BinaryAlarmType):
    context_match: ContextMatchType = field(
        metadata={
            "name": "ContextMatch",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class BinaryDataEncodingType(DataEncodingType):
    """
    Describe binary data that is unmolested in the decoding/encoding or cannot be
    represented in any of the other data encoding formats.

    Optionally use the FromBinaryTransformAlgorithm and ToBinaryTransformAlgorithm
    element to describe the transformation process. See InputAlgorithmType for the
    transformation structure.

    Attributes:
        size_in_bits: Number of bits this value occupies on the stream being
            encoded/decoded.
        from_binary_transform_algorithm: Used to convert binary data to an
            application data type
        to_binary_transform_algorithm: Used to convert binary data from an
            application data type to binary data
    """

    size_in_bits: IntegerValueType = field(
        metadata={
            "name": "SizeInBits",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    from_binary_transform_algorithm: None | InputAlgorithmType = field(
        default=None,
        metadata={
            "name": "FromBinaryTransformAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    to_binary_transform_algorithm: None | InputAlgorithmType = field(
        default=None,
        metadata={
            "name": "ToBinaryTransformAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class BooleanContextAlarmType(BooleanAlarmType):
    context_match: ContextMatchType = field(
        metadata={
            "name": "ContextMatch",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class ContainerBinaryDataEncodingType:
    """
    Describe container binary data that is unmolested in the decoding/encoding or
    cannot be represented in any of the other data encoding formats.

    Optionally use the FromBinaryTransformAlgorithm and ToBinaryTransformAlgorithm
    element to describe the transformation process. See InputAlgorithmType for the
    transformation structure.

    Attributes:
        error_detect_correct: Describes the optional inclusion of an error
            detection and/or correction algorithm used with this container.
        size_in_bits: Number of bits this container occupies on the stream being
            encoded/decoded.  This is only needed to "force" the bit length of
            the container to be a fixed value.  In most cases, the entry list
            would define the size of the container.
        from_binary_transform_algorithm: Used to convert binary data to an
            application data type.
        to_binary_transform_algorithm: Used to convert binary data from an
            application data type to binary data.
    """

    error_detect_correct: None | ErrorDetectCorrectType = field(
        default=None,
        metadata={
            "name": "ErrorDetectCorrect",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    size_in_bits: None | IntegerValueType = field(
        default=None,
        metadata={
            "name": "SizeInBits",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    from_binary_transform_algorithm: None | InputAlgorithmType = field(
        default=None,
        metadata={
            "name": "FromBinaryTransformAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    to_binary_transform_algorithm: None | InputAlgorithmType = field(
        default=None,
        metadata={
            "name": "ToBinaryTransformAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class DimensionType:
    """
    For partial entries of an array, the starting and ending index for each
    dimension, OR the Size must be specified.

    Indexes are zero based.

    Attributes:
        starting_index: zero based index
        ending_index:
    """

    starting_index: IntegerValueType = field(
        metadata={
            "name": "StartingIndex",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    ending_index: IntegerValueType = field(
        metadata={
            "name": "EndingIndex",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class EnumerationContextAlarmType(EnumerationAlarmType):
    """
    Describe a context that when true the alarm condition may be evaluated.

    See ContextMatchType and EnumerationAlarmType.

    Attributes:
        context_match: Describe a context in terms of a parameter and value that
            when true enables the context alarm definition.
    """

    context_match: ContextMatchType = field(
        metadata={
            "name": "ContextMatch",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class FloatDataEncodingType(DataEncodingType):
    """
    For common encodings of floating point data.

    Attributes:
        default_calibrator: Calibrator to be applied to the raw uncalibrated
            value to arrive at the engineering/calibrated value when no Context
            Calibrators are provided or evaluate to true, based on their
            MatchCriteria.
        context_calibrator_list: Calibrator to be applied to the raw uncalibrated
            value to arrive at the engineering/calibrated value when a
            MatchCriteria evaluates to true.  The first in the list to match
            takes precedence.
        encoding: Specifies real/decimal numeric value to raw encoding method,
            with the default being "IEEE754_1985".
        size_in_bits: Number of bits to use for the float raw encoding method,
            with 32 being the default.  Not every number of bits is valid for
            each encoding method.
        change_threshold: A changeThreshold may optionally be specified to inform
            systems of the minimum change in value that is significant.  This is
            used by some systems to limit the telemetry processing and/or
            recording requirements. If the value is unspecified or zero, any
            change is significant.
    """

    default_calibrator: None | CalibratorType = field(
        default=None,
        metadata={
            "name": "DefaultCalibrator",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    context_calibrator_list: None | ContextCalibratorListType = field(
        default=None,
        metadata={
            "name": "ContextCalibratorList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    encoding: FloatEncodingType = field(
        default=FloatEncodingType.IEEE754_1985,
        metadata={
            "type": "Attribute",
        },
    )
    size_in_bits: FloatEncodingSizeInBitsType = field(
        default=FloatEncodingSizeInBitsType.VALUE_32,
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
        },
    )
    change_threshold: None | float = field(
        default=None,
        metadata={
            "name": "changeThreshold",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class IntegerDataEncodingType(DataEncodingType):
    """
    For all major encodings of integer data.

    Attributes:
        default_calibrator: Calibrator to be applied to the raw uncalibrated
            value to arrive at the engineering/calibrated value when no Context
            Calibrators are provided or evaluate to true, based on their
            MatchCriteria.
        context_calibrator_list: Calibrator to be applied to the raw uncalibrated
            value to arrive at the engineering/calibrated value when a
            MatchCriteria evaluates to true.  The first in the list to match
            takes precedence.
        encoding: Specifies integer numeric value to raw encoding method, with
            the default being "unsigned".
        size_in_bits: Number of bits to use for the raw encoding, with 8 being
            the default.
        change_threshold: A changeThreshold may optionally be specified to inform
            systems of the minimum change in value that is significant.  This is
            used by some systems to limit the telemetry processing and/or
            recording requirements, such as for an analog-to-digital converter
            that dithers in the least significant bit. If the value    is
            unspecified or zero, any change is significant.
    """

    default_calibrator: None | CalibratorType = field(
        default=None,
        metadata={
            "name": "DefaultCalibrator",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    context_calibrator_list: None | ContextCalibratorListType = field(
        default=None,
        metadata={
            "name": "ContextCalibratorList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    encoding: IntegerEncodingType = field(
        default=IntegerEncodingType.UNSIGNED,
        metadata={
            "type": "Attribute",
        },
    )
    size_in_bits: int = field(
        default=8,
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
            "min_inclusive": 1,
        },
    )
    change_threshold: None | int = field(
        default=None,
        metadata={
            "name": "changeThreshold",
            "type": "Attribute",
            "min_inclusive": 0,
        },
    )


@dataclass(kw_only=True)
class LocationInContainerInBitsType(IntegerValueType):
    """
    Describe the absolute or relative bit location of an entry in a container.

    The "referenceLocation" attribute specifies the starting bit anchor. If no
    referenceLocation value is given, the entry is assumed to begin at the first bit
    position after the previous entry. Each container starts at bit 0, thus
    "containerStart" is an offset from 0. Negative container start bits are before
    the container and are implementation dependent - these should be flagged as
    likely errors. "containerEnd" is given as a positive offset from the end of the
    container, thus a container end of 0 is exactly at the end of the container.
    Negative container end addresses are after the container and are implementation
    dependent - these should be flagged as likely errors. Positive "previouEntry"
    values are offsets from the previous entry - zero (0) is the default which means
    it follows contiguously from the last occupied bit of the previous entry. A
    value of one means it is offset 1-bit from the previous entry, and a value of
    negative 1 (-1) means it overlaps the previous entry by one bit, and so forth.
    The "nextEntry" attribute value is proposed for deprecation and should be
    avoided. See SequenceEntryType.

    Attributes:
        reference_location: Defines the relative reference used to interpret the
            start bit position.  The default is 0 bits from the end of the
            previousEntry, which makes the entry contiguous.
    """

    reference_location: ReferenceLocationType = field(
        default=ReferenceLocationType.PREVIOUS_ENTRY,
        metadata={
            "name": "referenceLocation",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class NumericContextAlarmType(NumericAlarmType):
    """
    Describe a parameter dependent context, that when evaluates to true, enables the
    use of this alarm definition.

    See ContextMatchType and NumericAlarmType.

    Attributes:
        context_match: Contains the evaluation criteria for a parameter dependent
            test, that when evaluates to true, enables this alarm definition.
    """

    context_match: ContextMatchType = field(
        metadata={
            "name": "ContextMatch",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class RepeatType:
    """
    Contains elements that describe how an Entry is identically repeated.

    This includes a Count of the number of appearances and an optional Offset in
    bits that may occur between appearances. A Count of 1 indicates no repetition.
    The Offset default is 0 when not specified.

    Attributes:
        count: Value (either fixed or dynamic) that contains the count of
            appearances for an Entry. The value must be positive where 1 is the
            same as not specifying a RepeatEntry element at all.
        offset: Value (either fixed or dynamic) that contains an optional offset
            in bits between repeats of the Entry. The default is 0, which is
            contiguous. The value must be 0 or positive. Empty offset after the
            last repeat count is not implicitly reserved, so the parent EntryList
            should consider if these are occupied bits when placing the next
            Entry.
    """

    count: IntegerValueType = field(
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    offset: None | IntegerValueType = field(
        default=None,
        metadata={
            "name": "Offset",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class StreamSetType:
    """
    Contains an unordered set of Streams.
    """

    fixed_frame_stream: list[FixedFrameStreamType] = field(
        default_factory=list,
        metadata={
            "name": "FixedFrameStream",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    variable_frame_stream: list[VariableFrameStreamType] = field(
        default_factory=list,
        metadata={
            "name": "VariableFrameStream",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    custom_stream: list[CustomStreamType] = field(
        default_factory=list,
        metadata={
            "name": "CustomStream",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class StringContextAlarmType(StringAlarmType):
    """
    Describe a context that when true the alarm may be evaluated.

    See ContextMatchType and StringAlarmType.
    """

    context_match: ContextMatchType = field(
        metadata={
            "name": "ContextMatch",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class StringDataEncodingType(DataEncodingType):
    """
    Describe common encodings of string data: UTF-8 and UTF-16.

    See StringDataType.

    Attributes:
        size_in_bits: Static length strings do not change in overall length
            between samples.   They may terminate before the end of their buffer
            using a terminating character, or by various lookups, or
            calculations.  But they have a maximum fixed size, and the data
            itself is always within that maximum size.
        variable: Variable length strings are those where the space occupied in a
            container can vary.  If the string has variable content but occupies
            the same amount of space when encoded should use the SizeInBits
            element.  Specification of a variable length string needs to consider
            that the implementation needs to allocate space to store the string.
            Specify the maximum possible length of the string data type for
            memory purposes and also specify the bit size of the string to use in
            containers with the dynamic elements.
        encoding: The character set encoding of this string data type.
    """

    size_in_bits: None | SizeInBitsType = field(
        default=None,
        metadata={
            "name": "SizeInBits",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    variable: None | VariableStringType = field(
        default=None,
        metadata={
            "name": "Variable",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    encoding: StringEncodingType = field(
        default=StringEncodingType.UTF_8,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class TimeContextAlarmType(TimeAlarmType):
    """
    Context alarms are applied when the ContextMatch is true.

    Context alarms override Default alarms.
    """

    context_match: ContextMatchType = field(
        metadata={
            "name": "ContextMatch",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class ArgumentBaseDataType(NameDescriptionType):
    """
    Identical to BaseDataType but supports argument instance references.

    Attributes:
        unit_set: When appropriate, describe the units of measure that are
            represented by this argument value.
        binary_data_encoding: Binary encoding is typically a "pass through" raw
            encoding form where one of the more common encodings is not required
            for the argument.  A custom transformation capability is available if
            needed.
        float_data_encoding: Float encoding is a common encoding where the raw
            binary is in a form that gets interpreted as a decimal numeric value.
        integer_data_encoding: Integer encoding is a common encoding where the
            raw binary is in a form that gets interpreted as an integral value,
            either signed or unsigned.
        string_data_encoding: String encoding is a common encoding where the raw
            binary is in a form that gets interpreted as a character sequence.
        base_type: Used to derive one Data Type from another - will inherit all
            the attributes from the baseType any of which may be redefined in
            this type definition.
    """

    unit_set: None | UnitSetType = field(
        default=None,
        metadata={
            "name": "UnitSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    binary_data_encoding: None | ArgumentBinaryDataEncodingType = field(
        default=None,
        metadata={
            "name": "BinaryDataEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    float_data_encoding: None | FloatDataEncodingType = field(
        default=None,
        metadata={
            "name": "FloatDataEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    integer_data_encoding: None | IntegerDataEncodingType = field(
        default=None,
        metadata={
            "name": "IntegerDataEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    string_data_encoding: None | ArgumentStringDataEncodingType = field(
        default=None,
        metadata={
            "name": "StringDataEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    base_type: None | str = field(
        default=None,
        metadata={
            "name": "baseType",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        },
    )


@dataclass(kw_only=True)
class ArgumentDimensionListType:
    """
    Identical to DimensionListType but supports argument instance references.
    """

    dimension: list[ArgumentDimensionType] = field(
        default_factory=list,
        metadata={
            "name": "Dimension",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class ArgumentSequenceEntryType:
    """
    Identical to a SequenceEntryType but supports argument instance references.

    Attributes:
        location_in_container_in_bits: The start bit 0 position for each
            container is local to the container, but does include space occupied
            by inherited containers.  When a container is "included", as opposed
            to inherited, then the interpreting implementation takes into account
            the start bit position of the referring container when finally
            assembling the start bits for the post-processed entry content.  The
            default start bit for any entry is 0 bits from the previous entry,
            making the content contiguous when this element is not used.
        repeat_entry: May be used when this entry repeats itself in the sequence
            container.  When an entry repeats, it effectively specifies that the
            same entry is reported more than once in the container and has the
            same physical meaning.  This should not be construed to be equivalent
            to arrays.
        include_condition: This entry will only be included in the sequence when
            this condition is true, otherwise it is always included.  When the
            include condition evaluates to false, it is as if the entry does not
            exist such that any start bit interpretations cannot take into
            account the space that would have been occupied if this included
            condition were true.
        ancillary_data_set: Ancillary data associated with this entry.
        short_description: Optional short description for this entry element.
    """

    location_in_container_in_bits: None | ArgumentLocationInContainerInBitsType = field(
        default=None,
        metadata={
            "name": "LocationInContainerInBits",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    repeat_entry: None | ArgumentRepeatType = field(
        default=None,
        metadata={
            "name": "RepeatEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    include_condition: None | ArgumentMatchCriteriaType = field(
        default=None,
        metadata={
            "name": "IncludeCondition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    ancillary_data_set: None | AncillaryDataSetType = field(
        default=None,
        metadata={
            "name": "AncillaryDataSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    short_description: None | str = field(
        default=None,
        metadata={
            "name": "shortDescription",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class BaseDataType(NameDescriptionType):
    """
    An abstract schema type used by within the schema to derive the other
    simple/primitive engineering form data types: BooleanDataType, BinaryDataType,
    StringDataType, EnumeratedDataType, FloatDataType and IntegerDataType.

    The encoding elements are optional because they describe the raw wire encoded
    form of the data type. Encoding is only necessary when the type is telemetered
    in some form. Local variables and derived typically do not require encoding.

    Attributes:
        unit_set: When appropriate, describe the units of measure that are
            represented by this parameter value.
        binary_data_encoding: Binary encoding is typically a "pass through" raw
            encoding form where one of the more common encodings is not required
            for the parameter.  A custom transformation capability is available
            if needed.
        float_data_encoding: Float encoding is a common encoding where the raw
            binary is in a form that gets interpreted as a decimal numeric value.
        integer_data_encoding: Integer encoding is a common encoding where the
            raw binary is in a form that gets interpreted as an integral value,
            either signed or unsigned.
        string_data_encoding: String encoding is a common encoding where the raw
            binary is in a form that gets interpreted as a character sequence.
        base_type: Used to derive one Data Type from another - will inherit all
            the attributes from the baseType any of which may be redefined in
            this type definition.
    """

    unit_set: None | UnitSetType = field(
        default=None,
        metadata={
            "name": "UnitSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    binary_data_encoding: None | BinaryDataEncodingType = field(
        default=None,
        metadata={
            "name": "BinaryDataEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    float_data_encoding: None | FloatDataEncodingType = field(
        default=None,
        metadata={
            "name": "FloatDataEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    integer_data_encoding: None | IntegerDataEncodingType = field(
        default=None,
        metadata={
            "name": "IntegerDataEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    string_data_encoding: None | StringDataEncodingType = field(
        default=None,
        metadata={
            "name": "StringDataEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    base_type: None | str = field(
        default=None,
        metadata={
            "name": "baseType",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        },
    )


@dataclass(kw_only=True)
class BinaryContextAlarmListType:
    """
    Describe an ordered collection of context binary alarms, duplicates are valid.

    Process the contexts in list order. See BinaryContextAlarmType.

    Attributes:
        context_alarm: A Context contains a new alarm definition and a context
            match.  The match takes precedence over any default alarm when the
            first in the overall list evaluates to true.  It is also possible the
            alarm definition is empty, in which case the context means no alarm
            defined when the match is true.
    """

    context_alarm: list[BinaryContextAlarmType] = field(
        default_factory=list,
        metadata={
            "name": "ContextAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class BooleanContextAlarmListType:
    """
    Describe an ordered collection of context boolean alarms, duplicates are valid.

    Process the contexts in list order. See BooleanContextAlarmType.

    Attributes:
        context_alarm: A Context contains a new alarm definition and a context
            match.  The match takes precedence over any default alarm when the
            first in the overall list evaluates to true.  It is also possible the
            alarm definition is empty, in which case the context means no alarm
            defined when the match is true.
    """

    context_alarm: list[BooleanContextAlarmType] = field(
        default_factory=list,
        metadata={
            "name": "ContextAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class ContainerType(NameDescriptionType):
    """
    An abstract block of data; used as the base type for more specific container
    types.

    Attributes:
        default_rate_in_stream:
        rate_in_stream_set:
        binary_encoding: May be used to indicate error detection and correction,
            change byte order,  provide the size (when it can't be derived), or
            perform some custom processing.
    """

    default_rate_in_stream: None | RateInStreamType = field(
        default=None,
        metadata={
            "name": "DefaultRateInStream",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    rate_in_stream_set: None | RateInStreamSetType = field(
        default=None,
        metadata={
            "name": "RateInStreamSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    binary_encoding: None | ContainerBinaryDataEncodingType = field(
        default=None,
        metadata={
            "name": "BinaryEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class DimensionListType:
    """
    Where the Dimension list is in this form: Array[1stDim][2ndDim][lastDim].

    The last dimension is assumed to be the least significant - that is this
    dimension will cycle through its combination before the next to last dimension
    changes. The order MUST ascend or the array will need to be broken out entry by
    entry.
    """

    dimension: list[DimensionType] = field(
        default_factory=list,
        metadata={
            "name": "Dimension",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class EncodingType:
    """
    Describe the data encoding for a time data type.

    It includes the units and other attributes scale and offset. Use scale and
    offset to describe a y=mx+b relationship (where m is the slope/scale and b is
    the intercept/offset) to make adjustments to the encoded time value so that it
    matches the time units. For binary encoded time use transform algorithms to
    convert time data formats that are too difficult to describe in XTCE. See
    AbsoluteTimeDataType and RelativeTimeDataType.

    Attributes:
        binary_data_encoding: Binary encoding is typically a "pass through" raw
            encoding form where one of the more common encodings is not required
            for the parameter.  A custom transformation capability is available
            if needed.
        float_data_encoding: Float encoding is a common encoding where the raw
            binary is in a form that gets interpreted as a decimal numeric value.
        integer_data_encoding: Integer encoding is a common encoding where the
            raw binary is in a form that gets interpreted as an integral value,
            either signed or unsigned.
        string_data_encoding: String encoding is a common encoding where the raw
            binary is in a form that gets interpreted as a character sequence.
        units: Time units, with the default being in seconds.
        scale: Linear slope used as a shorter form of specifying a calibrator to
            convert between the raw value and the engineering units.
        offset: Linear intercept used as a shorter form of specifying a
            calibrator to convert between the raw value and the engineering
            units.
    """

    binary_data_encoding: None | BinaryDataEncodingType = field(
        default=None,
        metadata={
            "name": "BinaryDataEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    float_data_encoding: None | FloatDataEncodingType = field(
        default=None,
        metadata={
            "name": "FloatDataEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    integer_data_encoding: None | IntegerDataEncodingType = field(
        default=None,
        metadata={
            "name": "IntegerDataEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    string_data_encoding: None | StringDataEncodingType = field(
        default=None,
        metadata={
            "name": "StringDataEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    units: TimeUnitsType = field(
        default=TimeUnitsType.SECONDS,
        metadata={
            "type": "Attribute",
        },
    )
    scale: float = field(
        default=1.0,
        metadata={
            "type": "Attribute",
        },
    )
    offset: float = field(
        default=0.0,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class EnumerationContextAlarmListType:
    """
    Describe an ordered collection of context enumeration alarms, duplicates are
    valid.

    Process the contexts in list order. See EnumerationContextAlarmType.

    Attributes:
        context_alarm: A Context contains a new alarm definition and a context
            match.  The match takes precedence over any default alarm when the
            first in the overall list evaluates to true.  It is also possible the
            alarm definition is empty, in which case the context means no alarm
            defined when the match is true.
    """

    context_alarm: list[EnumerationContextAlarmType] = field(
        default_factory=list,
        metadata={
            "name": "ContextAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class NumericContextAlarmListType:
    """
    An ordered collection of numeric alarms associated with a context.

    A context is an alarm definition on a parameter which is valid only in the case
    of a test on the value of other parameters. Process the contexts in list order.
    Used by both FloatParameterType and IntegerParameterType. See
    NumericContextAlarmType.

    Attributes:
        context_alarm: A Context contains a new alarm definition and a context
            match.  The match takes precedence over any default alarm when the
            first in the overall list evaluates to true.  It is also possible the
            alarm definition is empty, in which case the context means no alarm
            defined when the match is true.
    """

    context_alarm: list[NumericContextAlarmType] = field(
        default_factory=list,
        metadata={
            "name": "ContextAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class SequenceEntryType:
    """
    Defines an abstract schema type used to create other entry types.

    Describe an entry's location in the container (See
    LocationInContainerInBitsType). The location may be fixed or dynamic, absolute
    or relative. Entries may be included depending on the value of a condition (See
    IncludeConditionType), and entries may also repeat (see RepeatEntryType). The
    entry's IncludeCondition resolves to true, it is fully-resolved when its size is
    computable after RepeatEntry has been accounted for and then offset by
    LocationInContainer. See EntryListType, IncludeConditionType, RepeatEntryType
    and LocationInContainerInBitsType.

    Attributes:
        location_in_container_in_bits: The start bit 0 position for each
            container is local to the container, but does include space occupied
            by inherited containers.  When a container is "included", as opposed
            to inherited, then the interpreting implementation takes into account
            the start bit position of the referring container when finally
            assembling the start bits for the post-processed entry content.  The
            default start bit for any entry is 0 bits from the previous entry,
            making the content contiguous when this element is not used.
        repeat_entry: May be used when this entry repeats itself in the sequence
            container.  When an entry repeats, it effectively specifies that the
            same entry is reported more than once in the container and has the
            same physical meaning.  This should not be construed to be equivalent
            to arrays.
        include_condition: This entry will only be included in the sequence when
            this condition is true, otherwise it is always included.  When the
            include condition evaluates to false, it is as if the entry does not
            exist such that any start bit interpretations cannot take into
            account the space that would have been occupied if this included
            condition were true.
        time_association: Optional timing information associated with this entry.
        ancillary_data_set: Optional ancillary data associated with this element.
        short_description: Optional short description for this entry element.
    """

    location_in_container_in_bits: None | LocationInContainerInBitsType = field(
        default=None,
        metadata={
            "name": "LocationInContainerInBits",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    repeat_entry: None | RepeatType = field(
        default=None,
        metadata={
            "name": "RepeatEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    include_condition: None | MatchCriteriaType = field(
        default=None,
        metadata={
            "name": "IncludeCondition",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    time_association: None | TimeAssociationType = field(
        default=None,
        metadata={
            "name": "TimeAssociation",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    ancillary_data_set: None | AncillaryDataSetType = field(
        default=None,
        metadata={
            "name": "AncillaryDataSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    short_description: None | str = field(
        default=None,
        metadata={
            "name": "shortDescription",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class StringContextAlarmListType:
    """
    Describe an ordered collection of context string alarms, duplicates are valid.

    Process the contexts in list order. See StringContextAlarmType.

    Attributes:
        context_alarm: A Context contains a new alarm definition and a context
            match.  The match takes precedence over any default alarm when the
            first in the overall list evaluates to true.  It is also possible the
            alarm definition is empty, in which case the context means no alarm
            defined when the match is true.
    """

    context_alarm: list[StringContextAlarmType] = field(
        default_factory=list,
        metadata={
            "name": "ContextAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class TimeContextAlarmListType:
    """
    An ordered collection of temporal alarms associated with a context.

    A context is an alarm definition on a parameter which is valid only in the case
    of a test on the value of other parameters. Process the contexts in list order.
    See TimeContextAlarmType.

    Attributes:
        context_alarm: A Context contains a new alarm definition and a context
            match.  The match takes precedence over any default alarm when the
            first in the overall list evaluates to true.  It is also possible the
            alarm definition is empty, in which case the context means no alarm
            defined when the match is true.
    """

    context_alarm: list[TimeContextAlarmType] = field(
        default_factory=list,
        metadata={
            "name": "ContextAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class ArgumentArgumentRefEntryType(ArgumentSequenceEntryType):
    """
    Identical to ArgumentRefEntryType but supports argument instance references.
    """

    argument_ref: str = field(
        metadata={
            "name": "argumentRef",
            "type": "Attribute",
            "pattern": r"([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)",
        }
    )


@dataclass(kw_only=True)
class ArgumentArrayArgumentRefEntryType(ArgumentSequenceEntryType):
    """
    Identical to ArrayParameterRefEntryType but supports argument instance
    references.

    Attributes:
        dimension_list: The dimension here if used for subsetting must be less
            than the ones in the type.  It's not a subset if its the same size.
        argument_ref:
        last_entry_for_this_array_instance:
    """

    dimension_list: None | ArgumentDimensionListType = field(
        default=None,
        metadata={
            "name": "DimensionList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    argument_ref: str = field(
        metadata={
            "name": "argumentRef",
            "type": "Attribute",
            "pattern": r"([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)",
        }
    )
    last_entry_for_this_array_instance: bool = field(
        default=False,
        metadata={
            "name": "lastEntryForThisArrayInstance",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArgumentArrayParameterRefEntryType(ArgumentSequenceEntryType):
    """
    Identical to ArrayParameterRefEntryType but supports argument instance
    references.

    Attributes:
        dimension_list: The dimension here if used for subsetting must be less
            than the ones in the type.  It's not a subset if its the same size.
        parameter_ref:
        last_entry_for_this_array_instance:
    """

    dimension_list: None | DimensionListType = field(
        default=None,
        metadata={
            "name": "DimensionList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    parameter_ref: str = field(
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
        }
    )
    last_entry_for_this_array_instance: bool = field(
        default=False,
        metadata={
            "name": "lastEntryForThisArrayInstance",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArgumentBaseTimeDataType(NameDescriptionType):
    """
    Identical to BaseTimeDataType but supports argument instance references.

    Attributes:
        encoding: Describes how the raw base counts of the time type are
            encoded/decoded.
        reference_time: Describes origin (epoch or reference) of this time type.
        base_type: Extend another absolute or relative time type.
    """

    encoding: None | EncodingType = field(
        default=None,
        metadata={
            "name": "Encoding",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    reference_time: None | ReferenceTimeType = field(
        default=None,
        metadata={
            "name": "ReferenceTime",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    base_type: None | str = field(
        default=None,
        metadata={
            "name": "baseType",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        },
    )


@dataclass(kw_only=True)
class ArgumentBinaryDataType(ArgumentBaseDataType):
    """
    Identical to BinaryDataType but supports argument instance references.

    Attributes:
        initial_value: Default/Initial value is always given in calibrated form.
            Extra bits are truncated from the MSB (leftmost).
    """

    initial_value: None | bytes = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
            "format": "base16",
        },
    )


@dataclass(kw_only=True)
class ArgumentBooleanDataType(ArgumentBaseDataType):
    """
    Identical to BooleanDataType but supports argument instance references.

    Attributes:
        initial_value: Default/Initial value is always given in calibrated form.
        one_string_value: Enumeration string representing the 1 value, with the
            default being 'True'.
        zero_string_value: Enumeration string representing the 0 value, with the
            default being 'False'.
    """

    initial_value: None | str = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )
    one_string_value: str = field(
        default="True",
        metadata={
            "name": "oneStringValue",
            "type": "Attribute",
        },
    )
    zero_string_value: str = field(
        default="False",
        metadata={
            "name": "zeroStringValue",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArgumentContainerRefEntryType(ArgumentSequenceEntryType):
    """
    Identical to ContainerRefEntryType but supports argument instance references.
    """

    container_ref: str = field(
        metadata={
            "name": "containerRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )


@dataclass(kw_only=True)
class ArgumentContainerSegmentRefEntryType(ArgumentSequenceEntryType):
    """
    Identical to ContainerSegmentRefEntryType but supports argument instance
    references.
    """

    container_ref: str = field(
        metadata={
            "name": "containerRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )
    order: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_inclusive": 1,
        },
    )
    size_in_bits: int = field(
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
            "min_inclusive": 1,
        }
    )


@dataclass(kw_only=True)
class ArgumentEnumeratedDataType(ArgumentBaseDataType):
    """
    Identical to EnumeratedDataType but supports argument instance references.

    Attributes:
        enumeration_list: Unordered list of label/value pairs where values cannot
            be duplicated.
        initial_value: Default/Initial value is always given in calibrated form.
            Use the label, it must be in the enumeration list to be valid.
    """

    enumeration_list: EnumerationListType = field(
        metadata={
            "name": "EnumerationList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    initial_value: None | str = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArgumentFixedValueEntryType(ArgumentSequenceEntryType):
    """
    Identical to FixedValueEntryType but supports argument instance references.

    Attributes:
        name: An optional name for the fixed/constant field in the sequence.
        binary_value: The fixed/constant value that should be encoded into the
            sequence.  This value provided should have sufficient bit length to
            accomodate the size in bits.  If the value is larger, the most
            significant unnecessary bits are dropped.  The value provided should
            be in network byte order for encoding.
        size_in_bits: The number of bits that this fixed/constant value should
            occupy in the sequence.
    """

    name: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    binary_value: bytes = field(
        metadata={
            "name": "binaryValue",
            "type": "Attribute",
            "format": "base16",
        }
    )
    size_in_bits: int = field(
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
            "min_inclusive": 1,
        }
    )


@dataclass(kw_only=True)
class ArgumentFloatDataType(ArgumentBaseDataType):
    """
    Identical to FloatDataType but supports argument instance references.

    Attributes:
        to_string: This element provides the implementation with assistance
            rendering the value as a string for users.
        initial_value: Default/Initial value is always given in calibrated form.
        size_in_bits: Optional hint to the implementation about the size of the
            engineering/calibrated data type to use internally.  Generally this
            can be determined by examination of the space required to capture the
            full range of the encoding, but it is not always clear when
            calibrators are in use.  A tolerant implementation will endeavor to
            always make sufficient size engineering data types to capture the
            entire range of possible values.
    """

    to_string: None | ToStringType = field(
        default=None,
        metadata={
            "name": "ToString",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    initial_value: None | float = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )
    size_in_bits: FloatSizeInBitsType = field(
        default=FloatSizeInBitsType.VALUE_32,
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArgumentIndirectParameterRefEntryType(ArgumentSequenceEntryType):
    """
    Identical to IndirectParameterRefEntryType but supports argument instance
    references.
    """

    parameter_instance: ParameterInstanceRefType = field(
        metadata={
            "name": "ParameterInstance",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    alias_name_space: None | str = field(
        default=None,
        metadata={
            "name": "aliasNameSpace",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArgumentIntegerDataType(ArgumentBaseDataType):
    """
    Identical to IntegerDataType but supports argument instance references.

    Attributes:
        to_string: This element provides the implementation with assistance
            rendering the value as a string for users.
        initial_value: Default/Initial value is always given in calibrated form.
            Specify the value as a base 10 integer.
        size_in_bits: Optional hint to the implementation about the size of the
            engineering/calibrated data type to use internally.  Generally this
            can be determined by examination of the space required to capture the
            full range of the encoding, but it is not always clear when
            calibrators are in use.  A tolerant implementation will endeavor to
            always make sufficient size engineering data types to capture the
            entire range of possible values.
        signed: Flag indicating if the engineering/calibrated data type used
            should support signed representation.  This should not be confused
            with the encoding type for the raw value.  The default is true.
    """

    to_string: None | ToStringType = field(
        default=None,
        metadata={
            "name": "ToString",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    initial_value: None | int = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )
    size_in_bits: int = field(
        default=32,
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
            "min_inclusive": 1,
        },
    )
    signed: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArgumentParameterRefEntryType(ArgumentSequenceEntryType):
    """
    Identical to ParameterRefEntryType but supports argument instance references.
    """

    parameter_ref: str = field(
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
        }
    )


@dataclass(kw_only=True)
class ArgumentParameterSegmentRefEntryType(ArgumentSequenceEntryType):
    """
    Identical to ParameterSegmentRefEntryType but supports argument instance
    references.
    """

    parameter_ref: str = field(
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
        }
    )
    order: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_inclusive": 1,
        },
    )
    size_in_bits: int = field(
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
            "min_inclusive": 1,
        }
    )


@dataclass(kw_only=True)
class ArgumentStreamSegmentEntryType(ArgumentSequenceEntryType):
    """
    Identical to StreamRefEntryType but supports argument instance references.
    """

    stream_ref: str = field(
        metadata={
            "name": "streamRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )
    order: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_inclusive": 1,
        },
    )
    size_in_bits: int = field(
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
            "min_inclusive": 1,
        }
    )


@dataclass(kw_only=True)
class ArgumentStringDataType(ArgumentBaseDataType):
    """
    Identical to StringDataType but supports argument instance references.

    Attributes:
        size_range_in_characters:
        initial_value: Initial values for string types, may include C language
            style (\\n, \\t, \\", \\\\, etc.) escape sequences.
        restriction_pattern: restriction pattern is a regular expression
        character_width: Optional hint to the implementation about the size of
            the engineering/calibrated data type to use internally. Generally
            this can be determined by examination of the encoding information for
            the string, but it is not always clear, so this attribute allows the
            extra hint when needed. A tolerant implementation will endeavor to
            always make sufficient size engineering data types to capture the
            entire range of possible characters.
    """

    size_range_in_characters: None | IntegerRangeType = field(
        default=None,
        metadata={
            "name": "SizeRangeInCharacters",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    initial_value: None | str = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )
    restriction_pattern: None | str = field(
        default=None,
        metadata={
            "name": "restrictionPattern",
            "type": "Attribute",
        },
    )
    character_width: None | CharacterWidthType = field(
        default=None,
        metadata={
            "name": "characterWidth",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArrayArgumentType(ArrayDataTypeType):
    """
    Describe an array argument type.

    The size and number of dimension are described here. See
    ArrayParameterRefEntryType, NameReferenceType and ArrayDataType.

    Attributes:
        dimension_list: Describe the dimensions of this array.
    """

    dimension_list: ArgumentDimensionListType = field(
        metadata={
            "name": "DimensionList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class ArrayParameterRefEntryType(SequenceEntryType):
    """
    Describe an entry that is an array parameter.

    Specify the dimension sizes if you subsetting the array (the number of
    dimensions shall match the number defined in the parameter's type definition),
    otherwise the ones in the ParameterType are assumed. See SequenceEntryType.

    Attributes:
        dimension_list: The dimension here if used for subsetting must be less
            than the ones in the type.  It's not a subset if its the same size.
        parameter_ref:
    """

    dimension_list: None | DimensionListType = field(
        default=None,
        metadata={
            "name": "DimensionList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    parameter_ref: str = field(
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
        }
    )


@dataclass(kw_only=True)
class ArrayParameterType(ArrayDataTypeType):
    """
    Describe an array parameter type.

    The size and number of dimensions are described here. See
    ArrayParameterRefEntryType, NameReferenceType and ArrayDataType.

    Attributes:
        dimension_list: Describe the dimensions of this array.
    """

    dimension_list: DimensionListType = field(
        metadata={
            "name": "DimensionList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )


@dataclass(kw_only=True)
class BaseTimeDataType(NameDescriptionType):
    """
    An abstract schema type used within the schema to derive other time based data
    types: RelativeTimeDataType and AbsoluteTimeDataType.

    An absolute time data type is a telemetered source/destination data type. A data
    encoding must be set. An optional epoch may be set. Time types are an exception
    to other primitives because, if the time data type is not telemetered, it still
    must have a data encoding set. See DataEncodingType, AbsoluteTimeDataType and
    RelativeTimeDataType.

    Attributes:
        encoding: Describes how the raw base counts of the time type are
            encoded/decoded.
        reference_time: Describes origin (epoch or reference) of this time type.
        base_type: Extend another absolute or relative time type.
    """

    encoding: None | EncodingType = field(
        default=None,
        metadata={
            "name": "Encoding",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    reference_time: None | ReferenceTimeType = field(
        default=None,
        metadata={
            "name": "ReferenceTime",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    base_type: None | str = field(
        default=None,
        metadata={
            "name": "baseType",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        },
    )


@dataclass(kw_only=True)
class BinaryDataType(BaseDataType):
    """
    A base schema type for describing a binary data engineering/calibrated type
    (often called "blob type").

    The binary data may be of fixed or variable length, and has an optional encoding
    and decoding algorithm that may be defined to transform the data between space
    and ground. See BaseDataType, BinaryParameterType and BinaryArgumentType.

    Attributes:
        initial_value: Default/Initial value is always given in calibrated form.
            Extra bits are truncated from the MSB (leftmost).
    """

    initial_value: None | bytes = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
            "format": "base16",
        },
    )


@dataclass(kw_only=True)
class BooleanDataType(BaseDataType):
    """
    A base schema type for describing a boolean data type which has two values only:
    "True" (1) or "False" (0).

    The values one and zero may be mapped to a specific string using the attributes
    oneStringValue and zeroStringValue. This type is a simplified form of the
    EnumeratedDataType. See BaseDataType, BooleanParameterType and
    BooleanArgumentType.

    Attributes:
        initial_value: Default/Initial value is always given in calibrated form.
        one_string_value: Enumeration string representing the 1 value, with the
            default being 'True'.
        zero_string_value: Enumeration string representing the 0 value, with the
            default being 'False'.
    """

    initial_value: None | str = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )
    one_string_value: str = field(
        default="True",
        metadata={
            "name": "oneStringValue",
            "type": "Attribute",
        },
    )
    zero_string_value: str = field(
        default="False",
        metadata={
            "name": "zeroStringValue",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ContainerRefEntryType(SequenceEntryType):
    """
    An entry that is simply a reference to another container.
    """

    container_ref: str = field(
        metadata={
            "name": "containerRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )


@dataclass(kw_only=True)
class ContainerSegmentRefEntryType(SequenceEntryType):
    """
    An entry that is only a portion of a container indicating that the entire
    container must be assembled from other container segments.

    It is assumed that container segments happen sequentially in time, that is the
    first part of a container is first, however (and there's always a however), if
    this is not the case the order of this container segment may be supplied with
    the order attribute where the first segment order="0". Each instance of a
    container cannot overlap in the overall sequence with another instance.
    """

    container_ref: str = field(
        metadata={
            "name": "containerRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )
    order: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_inclusive": 1,
        },
    )
    size_in_bits: int = field(
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
            "min_inclusive": 1,
        }
    )


@dataclass(kw_only=True)
class EnumeratedDataType(BaseDataType):
    """
    Describes an enumerated parameter type.

    The enumeration list consists of label/value pairs. See EnumerationListType,
    EnumeratedParameterType and EnumeratedArgumentType.

    Attributes:
        enumeration_list: Unordered list of label/value pairs where values cannot
            be duplicated.
        initial_value: Default/Initial value is always given in calibrated form.
            Use the label, it must be in the enumeration list to be valid.
    """

    enumeration_list: EnumerationListType = field(
        metadata={
            "name": "EnumerationList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    initial_value: None | str = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class FloatDataType(BaseDataType):
    """
    A base schema type for describing a floating point engineering/calibrated data
    type.

    Several encodings are supported. Calibrated integer to float relationships
    should be described with this data type. Use the data encoding to define
    calibrators. Joins integer as one of the numerics. See BaseDataType,
    FloatParameterType and FloatArgumentType.

    Attributes:
        to_string: This element provides the implementation with assistance
            rendering the value as a string for users.
        valid_range: The ValidRange defines the span of valid values for this
            data type.  This is a subset within the data type itself.  For
            example, an IEEE754 encoded float has almost a universal of possible
            values.  However, the known possible valid range may only span -180.0
            to +180.0, due to the physics of the measurement.  So, the valid
            range provides additional boundary/constraint information beyond that
            of the data encoding in the range of possible values that are
            meaningful to this parameter.  The valid range is not to be construed
            as an alarm definition and is not affected by any alarm definitions,
            instead violations of the valid range make a parameter value
            "unreasonable", as opposed to reasonable to be reported.  The exact
            effect of this state which should be of concern is implementation
            dependent.
        initial_value: Initial value is always given in calibrated form
        size_in_bits: Optional hint to the implementation about the size of the
            engineering/calibrated data type to use internally.  Generally this
            can be determined by examination of the space required to capture the
            full range of the encoding, but it is not always clear when
            calibrators are in use.  A tolerant implementation will endeavor to
            always make sufficient size engineering data types to capture the
            entire range of possible values.
    """

    to_string: None | ToStringType = field(
        default=None,
        metadata={
            "name": "ToString",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    valid_range: None | FloatDataType.ValidRange = field(
        default=None,
        metadata={
            "name": "ValidRange",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    initial_value: None | float = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )
    size_in_bits: FloatSizeInBitsType = field(
        default=FloatSizeInBitsType.VALUE_32,
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
        },
    )

    @dataclass(kw_only=True)
    class ValidRange(FloatRangeType):
        """
        Attributes:
            valid_range_applies_to_calibrated: By default and general
                recommendation, the valid range is specified in
                engineering/calibrated values, although this can be adjusted.
        """

        valid_range_applies_to_calibrated: bool = field(
            default=True,
            metadata={
                "name": "validRangeAppliesToCalibrated",
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class IndirectParameterRefEntryType(SequenceEntryType):
    """
    An entry whose name is given by the value of a ParamameterInstance.

    This entry may be used to implement dwell telemetry streams. The value of the
    parameter in ParameterInstance must use either the name of the Parameter or its
    alias. If it's an alias name, the alias namespace is supplied as an attribute.
    """

    parameter_instance: ParameterInstanceRefType = field(
        metadata={
            "name": "ParameterInstance",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    alias_name_space: None | str = field(
        default=None,
        metadata={
            "name": "aliasNameSpace",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class IntegerDataType(BaseDataType):
    """
    Describe an integer engineering/calibrated data type.

    Several encodings are supported. See BaseDataType, IntegerParameterType and
    IntegerArgumentType.

    Attributes:
        to_string: This element provides the implementation with assistance
            rendering the value as a string for users.
        valid_range: The ValidRange defines the span of valid values for this
            data type.  This is a subset within the data type itself.  For
            example, a 16 bit unsigned integer has possible values from 0 to
            65535.  However, the known possible valid range may only span 0 to
            999, due to the physics of the measurement.  So, the valid range
            provides additional boundary/constraint information beyond that of
            the data encoding in the range of possible values that are meaningful
            to this parameter.  The valid range is not to be construed as an
            alarm definition and is not affected by any alarm definitions,
            instead violations of the valid range make a parameter value
            "unreasonable", as opposed to reasonable to be reported.  The exact
            effect of this state which should be of concern is implementation
            dependent.
        initial_value: Default/Initial value is always given in calibrated form.
            Specify the value as a base 10 integer.
        size_in_bits: Optional hint to the implementation about the size of the
            engineering/calibrated data type to use internally.  Generally this
            can be determined by examination of the space required to capture the
            full range of the encoding, but it is not always clear when
            calibrators are in use.  A tolerant implementation will endeavor to
            always make sufficient size engineering data types to capture the
            entire range of possible values.
        signed: Flag indicating if the engineering/calibrated data type used
            should support signed representation.  This should not be confused
            with the encoding type for the raw value.  The default is true.
    """

    to_string: None | ToStringType = field(
        default=None,
        metadata={
            "name": "ToString",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    valid_range: None | IntegerDataType.ValidRange = field(
        default=None,
        metadata={
            "name": "ValidRange",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    initial_value: None | int = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )
    size_in_bits: int = field(
        default=32,
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
            "min_inclusive": 1,
        },
    )
    signed: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass(kw_only=True)
    class ValidRange(IntegerRangeType):
        """
        Attributes:
            valid_range_applies_to_calibrated: By default and general
                recommendation, the valid range is specified in
                engineering/calibrated values, although this can be adjusted.
        """

        valid_range_applies_to_calibrated: bool = field(
            default=True,
            metadata={
                "name": "validRangeAppliesToCalibrated",
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class ParameterRefEntryType(SequenceEntryType):
    """
    An entry that is a single Parameter.
    """

    parameter_ref: str = field(
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
        }
    )


@dataclass(kw_only=True)
class ParameterSegmentRefEntryType(SequenceEntryType):
    """
    An entry that is only a portion of a parameter value indicating that the entire
    parameter value must be assembled from other parameter segments.

    It is assumed that parameter segments happen sequentially in time, that is the
    first part if a telemetry parameter first, however (and there's always a
    however), if this is not the case the order of this parameter segment may be
    supplied with the order attribute where the first segment order="0".
    """

    parameter_ref: str = field(
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
        }
    )
    order: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_inclusive": 1,
        },
    )
    size_in_bits: int = field(
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
            "min_inclusive": 1,
        }
    )


@dataclass(kw_only=True)
class StreamSegmentEntryType(SequenceEntryType):
    """
    An entry that is a portion of a stream (streams are by definition, assumed
    continuous) It is assumed that stream segments happen sequentially in time, that
    is the first part if a steam first, however, if this is not the case the order
    of the stream segments may be supplied with the order attribute where the first
    segment order="0".
    """

    stream_ref: str = field(
        metadata={
            "name": "streamRef",
            "type": "Attribute",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        }
    )
    order: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_inclusive": 1,
        },
    )
    size_in_bits: int = field(
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
            "min_inclusive": 1,
        }
    )


@dataclass(kw_only=True)
class StringDataType(BaseDataType):
    """
    Defines a base schema type for StringParameterType and StringArgumentType,
    adding initial value, restriction pattern, character width, and size range in
    characters.

    The initial value if set is the initial value of all instances of the child
    types. The restriction pattern is a regular expression enforcing the string
    value to this pattern. The character width is on the local data type side. And
    the size range in character restricts the character set. For telemetered values,
    if the restriction pattern of size range in character is not met, the item is
    invalid. See BaseDataType, StringParameterType, StringArgumentType,
    CharacterWidthType and IntegerRangeType.

    Attributes:
        size_range_in_characters: The size in bits may be greater than or equal
            to minInclusive.  It may be less than or equal to maxInclusive.  They
            both may be set indicating a closed range.
        initial_value: Initial values for string types, may include C language
            style (\\n, \\t, \\", \\\\, etc.) escape sequences.
        restriction_pattern: restriction pattern is a regular expression
        character_width: Optional hint to the implementation about the size of
            the engineering/calibrated data type to use internally. Generally
            this can be determined by examination of the encoding information for
            the string, but it is not always clear, so this attribute allows the
            extra hint when needed. A tolerant implementation will endeavor to
            always make sufficient size engineering data types to capture the
            entire range of possible characters.
    """

    size_range_in_characters: None | IntegerRangeType = field(
        default=None,
        metadata={
            "name": "SizeRangeInCharacters",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    initial_value: None | str = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )
    restriction_pattern: None | str = field(
        default=None,
        metadata={
            "name": "restrictionPattern",
            "type": "Attribute",
        },
    )
    character_width: None | CharacterWidthType = field(
        default=None,
        metadata={
            "name": "characterWidth",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class AbsoluteTimeDataType(BaseTimeDataType):
    """
    A base schema type for describing an absolute time data type.

    Contains an absolute (to a known epoch) time. Use the [ISO 8601] extended format
    CCYY-MM-DDThh:mm:ss where "CC" represents the century, "YY" the year, "MM" the
    month and "DD" the day, preceded by an optional leading "-" sign to indicate a
    negative number. If the sign is omitted, "+" is assumed. The letter "T" is the
    date/time separator and "hh", "mm", "ss" represent hour, minute and second
    respectively. Additional digits can be used to increase the precision of
    fractional seconds if desired i.e. the format ss.ss... with any number of digits
    after the decimal point is supported. See AbsoluteTimeParameterType and
    AbsoluteTimeArgumentType. See AbsouteTimeParameterType, AbsoluteTimeArgumentType
    and BaseTimeDataType.

    Attributes:
        initial_value: Default/Initial value is always given in calibrated form.
    """

    initial_value: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArgumentAbsoluteTimeDataType(ArgumentBaseTimeDataType):
    """
    A base schema type for describing an absolute time data type.

    Contains an absolute (to a known epoch) time. Use the [ISO 8601] extended format
    CCYY-MM-DDThh:mm:ss where "CC" represents the century, "YY" the year, "MM" the
    month and "DD" the day, preceded by an optional leading "-" sign to indicate a
    negative number. If the sign is omitted, "+" is assumed. The letter "T" is the
    date/time separator and "hh", "mm", "ss" represent hour, minute and second
    respectively. Additional digits can be used to increase the precision of
    fractional seconds if desired i.e. the format ss.ss... with any number of digits
    after the decimal point is supported. See AbsoluteTimeParameterType and
    AbsoluteTimeArgumentType. See AbsouteTimeParameterType, AbsoluteTimeArgumentType
    and BaseTimeDataType.

    Attributes:
        initial_value: Default/Initial value is always given in calibrated form.
    """

    initial_value: None | XmlDateTime = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ArgumentRelativeTimeDataType(ArgumentBaseTimeDataType):
    """
    Used to contain a relative time value.

    Used to describe a relative time. Normally used for time offsets. A Relative
    time is expressed as PnYn MnDTnH nMnS, where nY represents the number of years,
    nM the number of months, nD the number of days, 'T' is the date/time separator,
    nH the number of hours, nM the number of minutes and nS the number of seconds.
    The number of seconds can include decimal digits to arbitrary precision. For
    example, to indicate a duration of 1 year, 2 months, 3 days, 10 hours, and 30
    minutes, one would write: P1Y2M3DT10H30M. One could also indicate a duration of
    minus 120 days as: -P120D. An extension of Schema duration type.
    """

    initial_value: None | XmlDuration = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class BinaryArgumentType(ArgumentBinaryDataType):
    """
    Defines a binary engineering/calibrated argument type (often called "blob
    type").

    The binary data may be of fixed or variable length, and has an optional encoding
    and decoding algorithm that may be defined to transform the data between space
    and ground. See BinaryDataEncodingType, IntegerValueType, InputAlgorithmType,
    and BinaryDataType.
    """


@dataclass(kw_only=True)
class BinaryParameterType(BinaryDataType):
    """
    Describe a binary engineering/calibrated parameter type (sometimes called a
    "blob type").

    It may be of fixed or variable length, and has an optional encoding and decoding
    algorithm that may be defined to transform the data between space and ground.
    See BinaryDataEncodingType, IntegerValueType, InputAlgorithmType and
    BinaryDataType.

    Attributes:
        default_alarm: Optionally describe an alarm monitoring specification that
            is effective whenever a contextual alarm definition does not take
            precedence.
        context_alarm_list: Optionally describe one or more alarm monitoring
            specifications that are effective whenever a contextual match
            definition evaluates to true.  The first match that evaluates to true
            takes precedence.
    """

    default_alarm: None | BinaryAlarmType = field(
        default=None,
        metadata={
            "name": "DefaultAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    context_alarm_list: None | BinaryContextAlarmListType = field(
        default=None,
        metadata={
            "name": "ContextAlarmList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class BooleanArgumentType(ArgumentBooleanDataType):
    """
    Defines a boolean argument type which has two values only: "True" (1) or "False"
    (0).

    The values one and zero may be mapped to a specific string using the attributes
    oneStringValue and zeroStringValue. This type is a simplified form of the
    EnumeratedDataType. See IntegerDataEncoding and BooleanDataType.
    """


@dataclass(kw_only=True)
class BooleanParameterType(BooleanDataType):
    """
    Describe a boolean parameter type which has two values only: "True" (1) or
    "False" (0).

    The values one and zero may be mapped to a specific string using the attributes
    oneStringValue and zeroStringValue. This type is a simplified form of the
    EnumeratedDataType. See IntegerDataEncoding and BooleanDataType.

    Attributes:
        default_alarm: Optionally describe an alarm monitoring specification that
            is effective whenever a contextual alarm definition does not take
            precedence.
        context_alarm_list: Optionally describe one or more alarm monitoring
            specifications that are effective whenever a contextual match
            definition evaluates to true.  The first match that evaluates to true
            takes precedence.
    """

    default_alarm: None | BooleanAlarmType = field(
        default=None,
        metadata={
            "name": "DefaultAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    context_alarm_list: None | BooleanContextAlarmListType = field(
        default=None,
        metadata={
            "name": "ContextAlarmList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class CommandContainerEntryListType:
    """
    Describe an entry list for a CommandContainer which is associated with a
    MetaCommand.

    The entry list for a MetaCommand CommandContainer element operates in a similar
    fashion as the entry list element for a SequenceContainer element. It adds fixed
    value and argument entries to the entry list not present in sequence containers.
    See MetaCommandType, CommandContainerType and EntryListType.

    Attributes:
        parameter_ref_entry: Specify a Parameter to be a part of this container
            layout definition.
        parameter_segment_ref_entry: Specify a portion of a Parameter to be a
            part of this container layout definition.  This is used when the
            Parameter is reported in fractional parts in the container before
            being fully updated.
        container_ref_entry: Specify the content of another Container to be a
            part of this container layout definition.
        container_segment_ref_entry: Specify a portion of another Container to be
            a part of this container layout definition.
        stream_segment_entry: Specify a portion of a Stream to be a part of this
            container layout definition.
        indirect_parameter_ref_entry: Specify a previous (not last reported)
            value of a Parmeter to be a part of this container layout definition.
        array_parameter_ref_entry: Specify an Array Type Parameter to be a part
            of this container layout definition when the Container does not
            populate the entire space of the Array contents.  If the entire space
            of the Array is populated, a tolerant implementation will accept
            ParameterRefEntry also.
        argument_ref_entry: Specify an Argument to be a part of this container
            layout definition.
        array_argument_ref_entry: Specify an Array Type Argument to be a part of
            this container layout definition when the Container does not populate
            the entire space of the Array contents.  If the entire space of the
            Array is populated, a tolerant implementation will accept
            ArgumentRefEntry also.
        fixed_value_entry: Specify an immutable value to be a part of this
            container layout definition.
    """

    parameter_ref_entry: list[ArgumentParameterRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    parameter_segment_ref_entry: list[ArgumentParameterSegmentRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterSegmentRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    container_ref_entry: list[ArgumentContainerRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ContainerRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    container_segment_ref_entry: list[ArgumentContainerSegmentRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ContainerSegmentRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    stream_segment_entry: list[ArgumentStreamSegmentEntryType] = field(
        default_factory=list,
        metadata={
            "name": "StreamSegmentEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    indirect_parameter_ref_entry: list[ArgumentIndirectParameterRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "IndirectParameterRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    array_parameter_ref_entry: list[ArgumentArrayParameterRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ArrayParameterRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    argument_ref_entry: list[ArgumentArgumentRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ArgumentRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    array_argument_ref_entry: list[ArgumentArrayArgumentRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ArrayArgumentRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    fixed_value_entry: list[ArgumentFixedValueEntryType] = field(
        default_factory=list,
        metadata={
            "name": "FixedValueEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class EntryListType:
    """
    Contains an ordered list of Entries.

    Used in Sequence Container.

    Attributes:
        parameter_ref_entry: Specify a Parameter to be a part of this container
            layout definition.
        parameter_segment_ref_entry: Specify a portion of a Parameter to be a
            part of this container layout definition.  This is used when the
            Parameter is reported in fractional parts in the container before
            being fully updated.
        container_ref_entry: Specify the content of another Container to be a
            part of this container layout definition.
        container_segment_ref_entry: Specify a portion of another Container to be
            a part of this container layout definition.
        stream_segment_entry: Specify a portion of a Stream to be a part of this
            container layout definition.
        indirect_parameter_ref_entry: Specify a previous (not last reported)
            value of a Parmeter to be a part of this container layout definition.
        array_parameter_ref_entry: Specify an Array Type Parameter to be a part
            of this container layout definition when the Container does not
            populate the entire space of the Array contents.  If the entire space
            of the Array is populated, a tolerant implementation will accept
            ParameterRefEntry also.
    """

    parameter_ref_entry: list[ParameterRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    parameter_segment_ref_entry: list[ParameterSegmentRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterSegmentRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    container_ref_entry: list[ContainerRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ContainerRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    container_segment_ref_entry: list[ContainerSegmentRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ContainerSegmentRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    stream_segment_entry: list[StreamSegmentEntryType] = field(
        default_factory=list,
        metadata={
            "name": "StreamSegmentEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    indirect_parameter_ref_entry: list[IndirectParameterRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "IndirectParameterRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    array_parameter_ref_entry: list[ArrayParameterRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ArrayParameterRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class EnumeratedArgumentType(ArgumentEnumeratedDataType):
    """
    Describes an enumerated argument type.

    The enumeration list consists of label/value pairs. See EnumerationListType,
    IntegerDataEncodingType and EnumeratedDataType.
    """


@dataclass(kw_only=True)
class EnumeratedParameterType(EnumeratedDataType):
    """
    Describe an enumerated parameter type.

    The enumeration list consists of label/value pairs. See EnumerationListType,
    IntegerDataEncodingType and EnumeratedDataType.

    Attributes:
        default_alarm: Describe labels for this parameter that should be in an
            alarm state.  The default definition applies when there are no
            context alarm definitions or all the context alarm definitions
            evaluate to false in their matching criteria.
        context_alarm_list: Describe labels for this parameter that should be in
            an alarm state when another parameter and value combination evaluates
            to true using the described matching criteria.
    """

    default_alarm: None | EnumerationAlarmType = field(
        default=None,
        metadata={
            "name": "DefaultAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    context_alarm_list: None | EnumerationContextAlarmListType = field(
        default=None,
        metadata={
            "name": "ContextAlarmList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class FloatArgumentType(ArgumentFloatDataType):
    """
    Describe a floating point argument type.

    Several encodings are supported. Calibrated integer to float relationships
    should be described with this data type. Use the data encoding to define
    calibrators. Joins integer as one of the numerics. See FloatDataEncodingType,
    IntegerDataEncodingType and FloatDataType.

    Attributes:
        valid_range_set: Provides additional platform/program specific ranging
            information.
    """

    valid_range_set: None | ValidFloatRangeSetType = field(
        default=None,
        metadata={
            "name": "ValidRangeSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class FloatParameterType(FloatDataType):
    """
    Describe a floating point parameter type.

    Several encodings are supported. Calibrated integer to float relationships
    should be described with this data type. Use the data encoding to define
    calibrators. Joins integer as one of the numerics. See FloatDataEncodingType,
    IntegerDataEncodingType and FloatDataType.

    Attributes:
        default_alarm: Default alarm definitions are those which do not adjust
            definition logic based on the value of other parameters.  Other
            parameters may participate in the determination of an alarm condition
            for this parameter, but the definition logic of the alarm on this
            parameter is constant.  If the alarming logic on this parameter
            changes based on the value of other parameters, then it is a
            ContextAlarm and belongs in the ContextAlarmList element.
        context_alarm_list: Context alarm definitions are those which adjust the
            definition logic for this parameter based on the value of other
            parameters.  A context which evaluates to being in effect, based on
            the testing of another parameter, takes precedence over the default
            alarms in the DefaultAlarm element.  If the no context alarm
            evaluates to being in effect, based on the testing of another
            parameter, then the default alarm definitions from the DefaultAlarm
            element will remain in effect.  If multiple contexts evaluate to
            being in effect, then the first one that appears will take
            precedence.
    """

    default_alarm: None | NumericAlarmType = field(
        default=None,
        metadata={
            "name": "DefaultAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    context_alarm_list: None | NumericContextAlarmListType = field(
        default=None,
        metadata={
            "name": "ContextAlarmList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class IntegerArgumentType(ArgumentIntegerDataType):
    """
    Describes an integer argument type.

    Several encodings supported. Calibrated integer to integer relationships should
    be described with this data type. Use the integer data encoding to define
    calibrators. Joins float as one of the numerics. See IntegerDataEncoding and
    IntegerDataType.

    Attributes:
        valid_range_set: Provides additional platform/program specific ranging
            information.
    """

    valid_range_set: None | ValidIntegerRangeSetType = field(
        default=None,
        metadata={
            "name": "ValidRangeSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class IntegerParameterType(IntegerDataType):
    """
    Describe an integer parameter type.

    Several are supported. Calibrated integer to integer relationships should be
    described with this data type. Use the integer data encoding to define
    calibrators. Joins float as one of the numerics. See IntegerDataEncoding and
    IntegerDataType.

    Attributes:
        default_alarm: Default alarm definitions are those which do not adjust
            definition logic based on the value of other parameters. Other
            parameters may participate in the determination of an alarm condition
            for this parameter, but the definition logic of the alarm on this
            parameter is constant. If the alarming logic on this parameter
            changes based on the value of other parameters, then it is a
            ContextAlarm and belongs in the ContextAlarmList element.
        context_alarm_list: Context alarm definitions are those which adjust the
            definition logic for this parameter based on the value of other
            parameters. A context which evaluates to being in effect, based on
            the testing of another parameter, takes precedence over the default
            alarms in the DefaultAlarm element. If the no context alarm evaluates
            to being in effect, based on the testing of another parameter, then
            the default alarm definitions from the DefaultAlarm element will
            remain in effect. If multiple contexts evaluate to being in effect,
            then the first one that appears will take precedence.
    """

    default_alarm: None | NumericAlarmType = field(
        default=None,
        metadata={
            "name": "DefaultAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    context_alarm_list: None | NumericContextAlarmListType = field(
        default=None,
        metadata={
            "name": "ContextAlarmList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class RelativeTimeDataType(BaseTimeDataType):
    """
    Used to contain a relative time value.

    Used to describe a relative time. Normally used for time offsets. A Relative
    time is expressed as PnYn MnDTnH nMnS, where nY represents the number of years,
    nM the number of months, nD the number of days, 'T' is the date/time separator,
    nH the number of hours, nM the number of minutes and nS the number of seconds.
    The number of seconds can include decimal digits to arbitrary precision. For
    example, to indicate a duration of 1 year, 2 months, 3 days, 10 hours, and 30
    minutes, one would write: P1Y2M3DT10H30M. One could also indicate a duration of
    minus 120 days as: -P120D. An extension of Schema duration type.
    """

    initial_value: None | XmlDuration = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class StringArgumentType(ArgumentStringDataType):
    """
    Describes a string parameter type.

    Three forms are supported: fixed length, variable length and variable length
    using a prefix. See StringDataEncodingType and StringDataType.
    """


@dataclass(kw_only=True)
class StringParameterType(StringDataType):
    """
    Describes a string parameter type.

    Three forms are supported: fixed length, variable length and variable length
    using a prefix. See StringDataEncodingType and StringDataType.

    Attributes:
        default_alarm: Default alarm definitions are those which do not adjust
            definition logic based on the value of other parameters.  Other
            parameters may participate in the determination of an alarm condition
            for this parameter, but the definition logic of the alarm on this
            parameter is constant.  If the alarming logic on this parameter
            changes based on the value of other parameters, then it is a
            ContextAlarm and belongs in the ContextAlarmList element.
        context_alarm_list: Context alarm definitions are those which adjust the
            definition logic for this parameter based on the value of other
            parameters.  A context which evaluates to being in effect, based on
            the testing of another parameter, takes precedence over the default
            alarms in the DefaultAlarm element.  If the no context alarm
            evaluates to being in effect, based on the testing of another
            parameter, then the default alarm definitions from the DefaultAlarm
            element will remain in effect.  If multiple contexts evaluate to
            being in effect, then the first one that appears will take
            precedence.
    """

    default_alarm: None | StringAlarmType = field(
        default=None,
        metadata={
            "name": "DefaultAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    context_alarm_list: None | StringContextAlarmListType = field(
        default=None,
        metadata={
            "name": "ContextAlarmList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class AbsoluteTimeArgumentType(ArgumentAbsoluteTimeDataType):
    """
    Describe an absolute time argument type relative to a known epoch (such as TAI).

    The string representation of this time should use the [ISO 8601] extended format
    CCYY-MM-DDThh:mm:ss where "CC" represents the century, "YY" the year, "MM" the
    month and "DD" the day, preceded by an optional leading "-" sign to indicate a
    negative number. If the sign is omitted, "+" is assumed. The letter "T" is the
    date/time separator and "hh", "mm", "ss" represent hour, minute and second
    respectively. Additional digits can be used to increase the precision of
    fractional seconds if desired i.e. the format ss.ss... with any number of digits
    after the decimal point is supported. See TAIType, IntegerDataEncoding and
    AbsoluteTimeDataType.
    """


@dataclass(kw_only=True)
class AbsoluteTimeParameterType(AbsoluteTimeDataType):
    """
    Describe an absolute time parameter type relative to a known epoch (such as
    TAI).

    The string representation of this time should use the [ISO 8601] extended format
    CCYY-MM-DDThh:mm:ss where "CC" represents the century, "YY" the year, "MM" the
    month and "DD" the day, preceded by an optional leading "-" sign to indicate a
    negative number. If the sign is omitted, "+" is assumed. The letter "T" is the
    date/time separator and "hh", "mm", "ss" represent hour, minute and second
    respectively. Additional digits can be used to increase the precision of
    fractional seconds if desired i.e. the format ss.ss... with any number of digits
    after the decimal point is supported. See TAIType, IntegerDataEncoding and
    AbsoluteTimeDataType.
    """


@dataclass(kw_only=True)
class CommandContainerType(ContainerType):
    """
    Describe a MetaCommand command container.

    The command container may contain arguments, parameters, other basic containers,
    and fixed values. Arguments are supplied by the user of a commanding
    application; parameters are supplied by the controlling system. Parameters and
    arguments map source data types to encodings. See MetaCommandType.

    Attributes:
        entry_list: List of item entries to pack/encode into this container
            definition.
        base_container: When a MetaCommand inherits/extends another MetaCommand,
            this references the CommandContainer from the BaseMetaCommand.
    """

    entry_list: CommandContainerEntryListType = field(
        metadata={
            "name": "EntryList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    base_container: None | BaseContainerType = field(
        default=None,
        metadata={
            "name": "BaseContainer",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class RelativeTimeArgumentType(ArgumentRelativeTimeDataType):
    """
    Describes a relative time argument type.

    Relative time parameters are time offsets (e.g. 10 second, 1.24 milliseconds,
    etc.) See IntegerDataEncodingType, FloatDataEncoding and RelativeTimeDataType.
    """


@dataclass(kw_only=True)
class RelativeTimeParameterType(RelativeTimeDataType):
    """
    Describes a relative time parameter type.

    Relative time parameters are time offsets (e.g. 10 second, 1.24 milliseconds,
    etc.) See IntegerDataEncodingType, FloatDataEncoding and RelativeTimeDataType.

    Attributes:
        default_alarm: Default alarm definitions are those which do not adjust
            definition logic based on the value of other parameters.  Other
            parameters may participate in the determination of an alarm condition
            for this parameter, but the definition logic of the alarm on this
            parameter is constant.  If the alarming logic on this parameter
            changes based on the value of other parameters, then it is a
            ContextAlarm and belongs in the ContextAlarmList element.
        context_alarm_list: Context alarm definitions are those which adjust the
            definition logic for this parameter based on the value of other
            parameters.  A context which evaluates to being in effect, based on
            the testing of another parameter, takes precedence over the default
            alarms in the DefaultAlarm element.  If the no context alarm
            evaluates to being in effect, based on the testing of another
            parameter, then the default alarm definitions from the DefaultAlarm
            element will remain in effect.  If multiple contexts evaluate to
            being in effect, then the first one that appears will take
            precedence.
    """

    default_alarm: None | TimeAlarmType = field(
        default=None,
        metadata={
            "name": "DefaultAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    context_alarm_list: None | TimeContextAlarmListType = field(
        default=None,
        metadata={
            "name": "ContextAlarmList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class SequenceContainerType(ContainerType):
    """
    Describes the binary layout/packing of data and also related properties,
    including an entry list of parameters, parameter segments, array parameters,
    stream segments, containers, and container segments.

    Sequence containers may extend other sequence containers (see
    BaseContainerType). The parent container's entries are placed before the entries
    in the child container forming one entry list. An inheritance chain may be
    formed using this mechanism, but only one entry list is being created. Sequence
    containers may be marked as "abstract", when this occurs an instance of it
    cannot itself be created. The idle pattern is part of any unallocated space in
    the container. See EntryListType.

    Attributes:
        entry_list: List of item entries to pack/encode into this container
            definition.
        base_container: Optional inheritance for this container from another
            named container.
        abstract: Abstract container definitions that are not instantiated,
            rather only used as bases to inherit from to create specialized
            container definitions.
        idle_pattern: The idle pattern is part of any unallocated space in the
            container.  This is uncommon.
    """

    entry_list: EntryListType = field(
        metadata={
            "name": "EntryList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        }
    )
    base_container: None | BaseContainerType = field(
        default=None,
        metadata={
            "name": "BaseContainer",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    abstract: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    idle_pattern: int | str = field(
        default=0,
        metadata={
            "name": "idlePattern",
            "type": "Attribute",
            "pattern": r"0[xX][0-9a-fA-F]+",
        },
    )


@dataclass(kw_only=True)
class ArgumentTypeSetType:
    """
    Describe an unordered collection of argument type definitions.

    These types named for the engineering/calibrated type of the argument. See
    BaseDataType and BaseTimeDataType.

    Attributes:
        string_argument_type: Describe an argument type that has an
            engineering/calibrated value in the form of a character string.
        enumerated_argument_type: Describe an argument type that has an
            engineering/calibrated value in the form of an enumeration.
        integer_argument_type: Describe an argument type that has an
            engineering/calibrated value in the form of an integer.
        binary_argument_type: Describe an argument type that has an
            engineering/calibrated value in the form of a binary (usually hex
            represented).
        float_argument_type: Describe an argument type that has an
            engineering/calibrated value in the form of a decimal.
        boolean_argument_type: Describe an argument type that has an
            engineering/calibrated value in the form of a boolean enumeration.
        relative_time_argument_type: Describe an argument type that has an
            engineering/calibrated value in the form of a duration in time.
        absolute_time_argument_type: Describe an argument type that has an
            engineering/calibrated value in the form of an instant in time.
        array_argument_type: Describe an argument type that has an
            engineering/calibrated value in the form of an array of a primitive
            type.
        aggregate_argument_type: Describe an argument type that has an
            engineering/calibrated value in the form of a structure of arguments
            of other types.
    """

    string_argument_type: list[StringArgumentType] = field(
        default_factory=list,
        metadata={
            "name": "StringArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    enumerated_argument_type: list[EnumeratedArgumentType] = field(
        default_factory=list,
        metadata={
            "name": "EnumeratedArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    integer_argument_type: list[IntegerArgumentType] = field(
        default_factory=list,
        metadata={
            "name": "IntegerArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    binary_argument_type: list[BinaryArgumentType] = field(
        default_factory=list,
        metadata={
            "name": "BinaryArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    float_argument_type: list[FloatArgumentType] = field(
        default_factory=list,
        metadata={
            "name": "FloatArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    boolean_argument_type: list[BooleanArgumentType] = field(
        default_factory=list,
        metadata={
            "name": "BooleanArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    relative_time_argument_type: list[RelativeTimeArgumentType] = field(
        default_factory=list,
        metadata={
            "name": "RelativeTimeArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    absolute_time_argument_type: list[AbsoluteTimeArgumentType] = field(
        default_factory=list,
        metadata={
            "name": "AbsoluteTimeArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    array_argument_type: list[ArrayArgumentType] = field(
        default_factory=list,
        metadata={
            "name": "ArrayArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    aggregate_argument_type: list[AggregateArgumentType] = field(
        default_factory=list,
        metadata={
            "name": "AggregateArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class CommandContainerSetType:
    """
    Contains an unordered Set of Command Containers.
    """

    command_container: list[SequenceContainerType] = field(
        default_factory=list,
        metadata={
            "name": "CommandContainer",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class ContainerSetType:
    """
    Unordered Set of Containers.

    Attributes:
        sequence_container: SequenceContainers define sequences of parameters or
            other containers.
    """

    sequence_container: list[SequenceContainerType] = field(
        default_factory=list,
        metadata={
            "name": "SequenceContainer",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class MetaCommandType(NameDescriptionType):
    """
    Describe a command which consists of an abstract portion (MetaCommand) and an
    optional packaging portion (MetaCommand CommandContainer).

    An argument list is provided. MetaCommand may extend other MetaCommands and
    their CommandContainer may extend other CommandContainer or SequenceContainers.
    A MetaCommand's CommandContainer is private except as referred to in
    BaseMetaCommand (they are not visible to other containers and cannot be used in
    an entry list). MetaCommands may also define various other behavioral aspects of
    a command such as command verifiers. See CommandContainerType, ArgumentListType,
    BaseMetaCommandType and BaseContainerType.

    Attributes:
        base_meta_command: Optional inheritance for this MetaCommand from another
            named MetaCommand.
        system_name: Optional.  Normally used when the database is built in a
            flat, non-hierarchical format.  May be used by implementations to
            group MetaCommands together.
        argument_list: Many commands have one or more options.  These are called
            command arguments.  Command arguments may be of any of the standard
            data types.  MetaCommand arguments are local to the MetaCommand, but
            may be referenced in inherited MetaCommand definitions, generally to
            apply Argument Assignments to the values.
        command_container: Tells how to package/encode this command definition in
            binary form.
        transmission_constraint_list: List of constraints to check when sending
            this command.
        default_significance: Some Command and Control Systems may require
            special user access or confirmations before transmitting commands
            with certain levels.  The level is inherited from the Base
            MetaCommand.
        context_significance_list: Some Command and Control Systems may require
            special user access or confirmations before transmitting commands
            with certain levels.  In addition to the default, Significance can be
            defined in contexts where it changes based on the values of
            parameters.
        interlock: An Interlock is a type of Constraint, but not on Command
            instances of this MetaCommand; Interlocks apply instead to the next
            command.  An Interlock will block successive commands until this
            command has reached a certain stage (through verifications).
            Interlocks are scoped to a SpaceSystem basis.
        verifier_set: Functional list of conditions/changes to check after
            sending this command to determine success or failure.
        parameter_to_set_list: List of parameters to set new values upon
            completion of sending this command.
        parameters_to_suspend_alarms_on_set: List of parameters to suspend alarm
            processing/detection upon completion of sending this command.
        abstract: Abstract MetaCommand definitions that are not instantiated,
            rather only used as bases to inherit from to create specialized
            command definitions.
    """

    base_meta_command: None | BaseMetaCommandType = field(
        default=None,
        metadata={
            "name": "BaseMetaCommand",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    system_name: None | str = field(
        default=None,
        metadata={
            "name": "SystemName",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    argument_list: None | ArgumentListType = field(
        default=None,
        metadata={
            "name": "ArgumentList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    command_container: None | CommandContainerType = field(
        default=None,
        metadata={
            "name": "CommandContainer",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    transmission_constraint_list: None | TransmissionConstraintListType = field(
        default=None,
        metadata={
            "name": "TransmissionConstraintList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    default_significance: None | SignificanceType = field(
        default=None,
        metadata={
            "name": "DefaultSignificance",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    context_significance_list: None | ContextSignificanceListType = field(
        default=None,
        metadata={
            "name": "ContextSignificanceList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    interlock: None | InterlockType = field(
        default=None,
        metadata={
            "name": "Interlock",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    verifier_set: None | VerifierSetType = field(
        default=None,
        metadata={
            "name": "VerifierSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    parameter_to_set_list: None | ParameterToSetListType = field(
        default=None,
        metadata={
            "name": "ParameterToSetList",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    parameters_to_suspend_alarms_on_set: None | ParametersToSuspendAlarmsOnSetType = (
        field(
            default=None,
            metadata={
                "name": "ParametersToSuspendAlarmsOnSet",
                "type": "Element",
                "namespace": "http://www.omg.org/spec/XTCE/20250214",
            },
        )
    )
    abstract: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ParameterTypeSetType:
    """
    Describe an unordered collection of parameter type definitions.

    These types named for the engineering/calibrated type of the parameter. See
    BaseDataType and BaseTimeDataType.

    Attributes:
        string_parameter_type: Describe a parameter type that has an
            engineering/calibrated value in the form of a character string.
        enumerated_parameter_type: Describe a parameter type that has an
            engineering/calibrated value in the form of an enumeration.
        integer_parameter_type: Describe a parameter type that has an
            engineering/calibrated value in the form of an integer.
        binary_parameter_type: Describe a parameter type that has an
            engineering/calibrated value in the form of a binary (usually hex
            represented).
        float_parameter_type: Describe a parameter type that has an
            engineering/calibrated value in the form of a decimal.
        boolean_parameter_type: Describe a parameter type that has an
            engineering/calibrated value in the form of a boolean enumeration.
        relative_time_parameter_type: Describe a parameter type that has an
            engineering/calibrated value in the form of a duration in time.
        absolute_time_parameter_type: Describe a parameter type that has an
            engineering/calibrated value in the form of an instant in time.
        array_parameter_type: Describe a parameter type that has an
            engineering/calibrated value in the form of an array of a primitive
            type.
        aggregate_parameter_type: Describe a parameter type that has an
            engineering/calibrated value in the form of a structure of parameters
            of other types.
    """

    string_parameter_type: list[StringParameterType] = field(
        default_factory=list,
        metadata={
            "name": "StringParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    enumerated_parameter_type: list[EnumeratedParameterType] = field(
        default_factory=list,
        metadata={
            "name": "EnumeratedParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    integer_parameter_type: list[IntegerParameterType] = field(
        default_factory=list,
        metadata={
            "name": "IntegerParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    binary_parameter_type: list[BinaryParameterType] = field(
        default_factory=list,
        metadata={
            "name": "BinaryParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    float_parameter_type: list[FloatParameterType] = field(
        default_factory=list,
        metadata={
            "name": "FloatParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    boolean_parameter_type: list[BooleanParameterType] = field(
        default_factory=list,
        metadata={
            "name": "BooleanParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    relative_time_parameter_type: list[RelativeTimeParameterType] = field(
        default_factory=list,
        metadata={
            "name": "RelativeTimeParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    absolute_time_parameter_type: list[AbsoluteTimeParameterType] = field(
        default_factory=list,
        metadata={
            "name": "AbsoluteTimeParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    array_parameter_type: list[ArrayParameterType] = field(
        default_factory=list,
        metadata={
            "name": "ArrayParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    aggregate_parameter_type: list[AggregateParameterType] = field(
        default_factory=list,
        metadata={
            "name": "AggregateParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class MetaCommandSetType:
    """
    Describes an unordered collection of command definitions.

    Duplicates are invalid based on the name attribute of MetaCommand and
    BlockMetaCommand. See MetaCommandType and BlockMetaCommandType.

    Attributes:
        meta_command: All atomic commands to be sent on this mission are listed
            here.  In addition this area has verification and validation
            information.
        meta_command_ref: Used to include a MetaCommand defined in another sub-
            system in this sub-system.
        block_meta_command: Used to define a command that includes more than one
            atomic MetaCommand definition.
    """

    meta_command: list[MetaCommandType] = field(
        default_factory=list,
        metadata={
            "name": "MetaCommand",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    meta_command_ref: list[str] = field(
        default_factory=list,
        metadata={
            "name": "MetaCommandRef",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "pattern": r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
        },
    )
    block_meta_command: list[BlockMetaCommandType] = field(
        default_factory=list,
        metadata={
            "name": "BlockMetaCommand",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class TelemetryMetaDataType:
    """
    All the data about telemetry is contained in TelemetryMetaData.

    Attributes:
        parameter_type_set: A list of parameter types
        parameter_set: A list of Parameters for this Space System.
        container_set: Holds the list of all potential container definitions for
            telemetry. Containers may parts of packets or TDM, and then groups of
            the containers, and then an entire entity -- such as a packet.  In
            order to maximize re-used for duplication, the pieces may defined
            once here, and then assembled as needed into larger structures, also
            here.
        message_set: Messages are an alternative method of uniquely identifying
            containers within a Service.  A message provides a test in the form
            of MatchCriteria to match to a container.  A simple example might be:
            [When minorframeID=21, the message is the 21st minorframe container.
            The collection of messages to search thru will be bound by a Service.
        stream_set:
        algorithm_set:
    """

    parameter_type_set: None | ParameterTypeSetType = field(
        default=None,
        metadata={
            "name": "ParameterTypeSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    parameter_set: None | ParameterSetType = field(
        default=None,
        metadata={
            "name": "ParameterSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    container_set: None | ContainerSetType = field(
        default=None,
        metadata={
            "name": "ContainerSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    message_set: None | MessageSetType = field(
        default=None,
        metadata={
            "name": "MessageSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    stream_set: None | StreamSetType = field(
        default=None,
        metadata={
            "name": "StreamSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    algorithm_set: None | AlgorithmSetType = field(
        default=None,
        metadata={
            "name": "AlgorithmSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class CommandMetaDataType:
    """
    Describe command related metadata.

    Items defined in this area may refer to items defined in TelemetryMetaData. See
    TelemetryMetaDataType.

    Attributes:
        parameter_type_set: A list of parameter types.
        parameter_set: Parameters referenced by MetaCommands.  This Parameter Set
            is located here so that MetaCommand data can be built independently
            of TelemetryMetaData.
        argument_type_set: A list of argument types.  MetaCommand definitions can
            contain arguments and parameters.  Arguments are user provided to the
            specific command definition.  Parameters are
            provided/calculated/determined by the software creating the command
            instance.  As a result, arguments contain separate type information.
            In some cases, arguments have different descriptive characteristics.
        meta_command_set: A list of command definitions with their arguments,
            parameters, and container encoding descriptions.
        command_container_set: Similar to the ContainerSet for telemetry, the
            CommandContainerSet contains containers that can be referenced/shared
            by MetaCommand definitions.
        stream_set: Contains an unordered set of Streams.
        algorithm_set: Contains an unordered set of Algorithms.
    """

    parameter_type_set: None | ParameterTypeSetType = field(
        default=None,
        metadata={
            "name": "ParameterTypeSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    parameter_set: None | ParameterSetType = field(
        default=None,
        metadata={
            "name": "ParameterSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    argument_type_set: None | ArgumentTypeSetType = field(
        default=None,
        metadata={
            "name": "ArgumentTypeSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    meta_command_set: None | MetaCommandSetType = field(
        default=None,
        metadata={
            "name": "MetaCommandSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    command_container_set: None | CommandContainerSetType = field(
        default=None,
        metadata={
            "name": "CommandContainerSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    stream_set: None | StreamSetType = field(
        default=None,
        metadata={
            "name": "StreamSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    algorithm_set: None | AlgorithmSetType = field(
        default=None,
        metadata={
            "name": "AlgorithmSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )


@dataclass(kw_only=True)
class SpaceSystemType(NameDescriptionType):
    """
    SpaceSystem is a collection of SpaceSystem(s) including space assets, ground
    assets, multi-satellite systems and sub-systems.

    A SpaceSystem is the root element for the set of data necessary to monitor and
    command an arbitrary space device - this includes the binary decomposition the
    data streams going into and out of a device.

    Attributes:
        header: The Header element contains optional descriptive information
            about this SpaceSystem or the document as a whole when specified at
            the root SpaceSystem.
        telemetry_meta_data: This element contains descriptions of the telemetry
            created on the space asset/device and sent to other data consumers.
        command_meta_data: This element contains descriptions of the commands and
            their associated constraints and verifications that can be sent to
            the space asset/device.
        service_set:
        space_system: Additional SpaceSystem elements may be used like namespaces
            to segregate portions of the space asset/device into convenient
            groupings or may be used to specialize a product line generic
            SpaceSystem to a specific asset instance.
        system_type: Type of the space system.  Represents what from a space
            enterprise this SpaceSystem element represents.  See the individual
            enumeration descriptions in SystemTypeType.
        asset_type: Broad name for the type of asset, such as spacecraft,
            aircraft, device, or any other that makes sense for the system.
        operational_status: Optional descriptive attribute for document owner
            convenience.
        base:
    """

    header: None | HeaderType = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    telemetry_meta_data: None | TelemetryMetaDataType = field(
        default=None,
        metadata={
            "name": "TelemetryMetaData",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    command_meta_data: None | CommandMetaDataType = field(
        default=None,
        metadata={
            "name": "CommandMetaData",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    service_set: None | ServiceSetType = field(
        default=None,
        metadata={
            "name": "ServiceSet",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
        },
    )
    space_system: list[SpaceSystem] = field(
        default_factory=list,
        metadata={
            "name": "SpaceSystem",
            "type": "Element",
            "namespace": "http://www.omg.org/spec/XTCE/20250214",
            "nillable": True,
        },
    )
    system_type: SystemTypeType = field(
        default=SystemTypeType.UNKNOWN,
        metadata={
            "name": "systemType",
            "type": "Attribute",
        },
    )
    asset_type: str = field(
        default="unknown",
        metadata={
            "name": "assetType",
            "type": "Attribute",
        },
    )
    operational_status: None | str = field(
        default=None,
        metadata={
            "name": "operationalStatus",
            "type": "Attribute",
        },
    )
    base: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass(kw_only=True)
class SpaceSystem(SpaceSystemType):
    """
    The top-level SpaceSystem is the root element for the set of metadata necessary
    to monitor and command a space device, such as a satellite.

    A SpaceSystem defines a namespace. Metadata areas include: packets/minor frames
    layout, telemetry, calibration, alarm, algorithms, streams and commands. A
    SpaceSystem may have child SpaceSystems, forming a SpaceSystem tree. See
    SpaceSystemType.
    """

    class Meta:
        nillable = True
        namespace = "http://www.omg.org/spec/XTCE/20250214"
