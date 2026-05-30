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
