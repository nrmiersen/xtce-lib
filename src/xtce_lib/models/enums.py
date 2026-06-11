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
