"""Range models."""

from typing import Any, Self, assert_never

from pydantic import Field, model_validator

from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy, XtceUnsupportedError
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from ._util import coerce_optional_int, unwrap
from .enum import ConcernLevel, RangeForm


class IntegerRange(XtceBaseModel):
    """A range of integer numbers."""

    min_inclusive: int | str | None = Field(default=None)
    """The minimum value of the range, including itself.

    Hex, octal, and binary literals are accepted as strings for XTCE 1.1 compatibility,
    but will be coerced to integers for all future versions.

    """

    max_inclusive: int | str | None = Field(default=None)
    """The maximum value of the range, including itself.

    Hex, octal, and binary literals are accepted as strings for XTCE 1.1 compatibility,
    but will be coerced to integers for all future versions.

    """

    @model_validator(mode="after")
    def validate_range(self) -> "IntegerRange":
        """Validate that the minimum value is less than or equal to the maximum
        value.
        """
        min_val = coerce_optional_int(self.min_inclusive)
        max_val = coerce_optional_int(self.max_inclusive)

        if min_val is None and max_val is None:
            raise ValueError(
                "at least one of min_inclusive or max_inclusive must be set"
            )

        if min_val is not None and max_val is not None:
            if min_val > max_val:
                raise ValueError(
                    f"minimum value ({min_val}) cannot be greater than maximum "
                    f"value ({max_val})"
                )

        return self

    @classmethod
    def _from_v1_1(cls: type[Self], integer_range: xtce_1_1.IntegerRangeType) -> Self:
        return cls(
            min_inclusive=coerce_optional_int(integer_range.min_inclusive),
            max_inclusive=coerce_optional_int(integer_range.max_inclusive),
        )

    @classmethod
    def _from_v1_2(cls: type[Self], integer_range: xtce_1_2.IntegerRangeType) -> Self:
        return cls(
            min_inclusive=integer_range.min_inclusive,
            max_inclusive=integer_range.max_inclusive,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], integer_range: xtce_1_3.IntegerRangeType) -> Self:
        return cls(
            min_inclusive=integer_range.min_inclusive,
            max_inclusive=integer_range.max_inclusive,
        )

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create a IntegerRange from an xsdata-generated
        IntegerRangeType object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                return cls._from_v1_1(raw_obj)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.IntegerRangeType:
        return xtce_1_1.IntegerRangeType(
            min_inclusive=self.min_inclusive, max_inclusive=self.max_inclusive
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.IntegerRangeType:
        return xtce_1_2.IntegerRangeType(
            min_inclusive=coerce_optional_int(self.min_inclusive),
            max_inclusive=coerce_optional_int(self.max_inclusive),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.IntegerRangeType:
        return xtce_1_3.IntegerRangeType(
            min_inclusive=coerce_optional_int(self.min_inclusive),
            max_inclusive=coerce_optional_int(self.max_inclusive),
        )

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> (
        xtce_1_1.IntegerRangeType
        | xtce_1_2.IntegerRangeType
        | xtce_1_3.IntegerRangeType
    ):
        """Convert this IntegerRange to an xsdata-generated IntegerRangeType object of
        the specified version.
        """
        match version:
            case XtceVersion.V1_1:
                return self._to_v1_1(policy)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)


class ValidIntegerRange(IntegerRange):
    """A range of integer numbers.

    Contains an optional flag to indicate whether the range applies to calibrated
    values.

    """

    applies_to_calibrated: bool = Field(default=True)
    """Whether this valid range applies to calibrated values.

    If False, it applies to raw values.

    """

    @classmethod
    def _from_v1_2(
        cls: type[Self], integer_range: xtce_1_2.IntegerDataType.ValidRange
    ) -> Self:
        return cls(
            min_inclusive=integer_range.min_inclusive,
            max_inclusive=integer_range.max_inclusive,
            applies_to_calibrated=integer_range.valid_range_applies_to_calibrated,
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], integer_range: xtce_1_3.IntegerDataType.ValidRange
    ) -> Self:
        return cls(
            min_inclusive=integer_range.min_inclusive,
            max_inclusive=integer_range.max_inclusive,
            applies_to_calibrated=integer_range.valid_range_applies_to_calibrated,
        )

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create a ValidIntegerRange from an xsdata-generated
        IntegerDataType.ValidRange object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, cls.__name__)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.IntegerDataType.ValidRange:
        return xtce_1_2.IntegerDataType.ValidRange(
            min_inclusive=coerce_optional_int(self.min_inclusive),
            max_inclusive=coerce_optional_int(self.max_inclusive),
            valid_range_applies_to_calibrated=self.applies_to_calibrated,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.IntegerDataType.ValidRange:
        return xtce_1_3.IntegerDataType.ValidRange(
            min_inclusive=coerce_optional_int(self.min_inclusive),
            max_inclusive=coerce_optional_int(self.max_inclusive),
            valid_range_applies_to_calibrated=self.applies_to_calibrated,
        )

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.IntegerDataType.ValidRange | xtce_1_3.IntegerDataType.ValidRange:
        """Convert this ValidIntegerRange to an xsdata-generated
        IntegerDataType.ValidRange object of the specified version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, self.__class__.__name__)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)


class ValidIntegerRanges(XtceBaseModel):
    """A collection of valid integer ranges.

    A single range is the most common, but multiple ranges can be used to specify non-
    contiguous valid values.

    """

    valid_ranges: list[IntegerRange] = Field(default_factory=list, min_length=1)
    """Defines one or more valid ranges.

    Multiple ranges can be used to specify non- contiguous valid values. Typically, only
    one range is used. In cases where multiple ranges are used, then the value is valid
    when it is valid in any of the provided ranges.

    """

    applies_to_calibrated: bool = Field(default=True)
    """Whether these valid ranges apply to calibrated values.

    If False, they apply to raw values.

    """

    @classmethod
    def _from_v1_2(
        cls: type[Self], integer_range: xtce_1_2.ValidIntegerRangeSetType
    ) -> Self:
        return cls(
            valid_ranges=[
                IntegerRange._from_v1_2(range) for range in integer_range.valid_range
            ],
            applies_to_calibrated=integer_range.valid_range_applies_to_calibrated,
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], integer_range: xtce_1_3.ValidIntegerRangeSetType
    ) -> Self:
        return cls(
            valid_ranges=[
                IntegerRange._from_v1_3(range) for range in integer_range.valid_range
            ],
            applies_to_calibrated=integer_range.valid_range_applies_to_calibrated,
        )

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create a ValidIntegerRanges from an xsdata-generated
        ValidIntegerRangeSetType object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, cls.__name__)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ValidIntegerRangeSetType:
        return xtce_1_2.ValidIntegerRangeSetType(
            valid_range=[range._to_v1_2(policy) for range in self.valid_ranges],
            valid_range_applies_to_calibrated=self.applies_to_calibrated,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ValidIntegerRangeSetType:
        return xtce_1_3.ValidIntegerRangeSetType(
            valid_range=[range._to_v1_3(policy) for range in self.valid_ranges],
            valid_range_applies_to_calibrated=self.applies_to_calibrated,
        )

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ValidIntegerRangeSetType | xtce_1_3.ValidIntegerRangeSetType:
        """Convert this ValidIntegerRanges to an xsdata-generated
        ValidIntegerRangeSetType object of the specified version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, self.__class__.__name__)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)


class FloatRange(XtceBaseModel):
    """A range of floating-point numbers.

    Options for both inclusive and exclusive minimum and maximum values are provided,
    but only one of the minimum options and one of the maximum options can be used at a
    time.

    """

    min_inclusive: float | None = Field(default=None)
    """The minimum value of the range, including itself."""

    min_exclusive: float | None = Field(default=None)
    """The minimum value of the range, excluding itself."""

    max_inclusive: float | None = Field(default=None)
    """The maximum value of the range, including itself."""

    max_exclusive: float | None = Field(default=None)
    """The maximum value of the range, excluding itself."""

    @model_validator(mode="after")
    def validate_range(self) -> "FloatRange":
        """Validate that the minimum value is less than or equal to the maximum value,
        and that only one of the minimum options and one of the maximum options are used
        at a time.
        """
        if self.min_inclusive is not None and self.min_exclusive is not None:
            raise ValueError("only one of min_inclusive and min_exclusive can be set")

        if self.max_inclusive is not None and self.max_exclusive is not None:
            raise ValueError("only one of max_inclusive and max_exclusive can be set")

        effective_min = (
            self.min_inclusive if self.min_inclusive is not None else self.min_exclusive
        )
        effective_max = (
            self.max_inclusive if self.max_inclusive is not None else self.max_exclusive
        )

        if effective_min is None and effective_max is None:
            raise ValueError(
                "at least one of the minimum or maximum values must be set"
            )

        if (
            effective_min is not None
            and effective_max is not None
            and effective_min > effective_max
        ):
            raise ValueError(
                f"minimum value ({effective_min}) cannot be greater than maximum "
                f"value ({effective_max})"
            )

        return self

    @classmethod
    def _from_v1_1(cls: type[Self], float_range: xtce_1_1.FloatRangeType) -> Self:
        return cls(
            min_inclusive=float_range.min_inclusive,
            min_exclusive=float_range.min_exclusive,
            max_inclusive=float_range.max_inclusive,
            max_exclusive=float_range.max_exclusive,
        )

    @classmethod
    def _from_v1_2(cls: type[Self], float_range: xtce_1_2.FloatRangeType) -> Self:
        return cls(
            min_inclusive=float_range.min_inclusive,
            min_exclusive=float_range.min_exclusive,
            max_inclusive=float_range.max_inclusive,
            max_exclusive=float_range.max_exclusive,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], float_range: xtce_1_3.FloatRangeType) -> Self:
        return cls(
            min_inclusive=float_range.min_inclusive,
            min_exclusive=float_range.min_exclusive,
            max_inclusive=float_range.max_inclusive,
            max_exclusive=float_range.max_exclusive,
        )

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create a FloatRange from an xsdata-generated FloatRangeType
        object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                return cls._from_v1_1(raw_obj)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.FloatRangeType:
        return xtce_1_1.FloatRangeType(
            min_inclusive=self.min_inclusive,
            min_exclusive=self.min_exclusive,
            max_inclusive=self.max_inclusive,
            max_exclusive=self.max_exclusive,
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.FloatRangeType:
        return xtce_1_2.FloatRangeType(
            min_inclusive=self.min_inclusive,
            min_exclusive=self.min_exclusive,
            max_inclusive=self.max_inclusive,
            max_exclusive=self.max_exclusive,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.FloatRangeType:
        return xtce_1_3.FloatRangeType(
            min_inclusive=self.min_inclusive,
            min_exclusive=self.min_exclusive,
            max_inclusive=self.max_inclusive,
            max_exclusive=self.max_exclusive,
        )

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.FloatRangeType | xtce_1_2.FloatRangeType | xtce_1_3.FloatRangeType:
        """Convert this FloatRange to an xsdata-generated FloatRangeType object of the
        specified version.
        """
        match version:
            case XtceVersion.V1_1:
                return self._to_v1_1(policy)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)


class ValidFloatRange(FloatRange):
    """A range of floating-point numbers.

    Contains an optional flag to indicate whether the range applies to calibrated
    values.

    """

    applies_to_calibrated: bool = Field(default=True)

    @classmethod
    def _from_v1_2(
        cls: type[Self], float_range: xtce_1_2.FloatDataType.ValidRange
    ) -> Self:
        return cls(
            min_inclusive=float_range.min_inclusive,
            min_exclusive=float_range.min_exclusive,
            max_inclusive=float_range.max_inclusive,
            max_exclusive=float_range.max_exclusive,
            applies_to_calibrated=float_range.valid_range_applies_to_calibrated,
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], float_range: xtce_1_3.FloatDataType.ValidRange
    ) -> Self:
        return cls(
            min_inclusive=float_range.min_inclusive,
            min_exclusive=float_range.min_exclusive,
            max_inclusive=float_range.max_inclusive,
            max_exclusive=float_range.max_exclusive,
            applies_to_calibrated=float_range.valid_range_applies_to_calibrated,
        )

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create a ValidFloatRange from an xsdata-generated
        FloatDataType.ValidRange object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, cls.__name__)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.FloatDataType.ValidRange:
        return xtce_1_2.FloatDataType.ValidRange(
            min_inclusive=self.min_inclusive,
            min_exclusive=self.min_exclusive,
            max_inclusive=self.max_inclusive,
            max_exclusive=self.max_exclusive,
            valid_range_applies_to_calibrated=self.applies_to_calibrated,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.FloatDataType.ValidRange:
        return xtce_1_3.FloatDataType.ValidRange(
            min_inclusive=self.min_inclusive,
            min_exclusive=self.min_exclusive,
            max_inclusive=self.max_inclusive,
            max_exclusive=self.max_exclusive,
            valid_range_applies_to_calibrated=self.applies_to_calibrated,
        )

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.FloatDataType.ValidRange | xtce_1_3.FloatDataType.ValidRange:
        """Convert this ValidFloatRange to an xsdata-generated FloatDataType.ValidRange
        object of the specified version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, self.__class__.__name__)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)


class ValidFloatRanges(XtceBaseModel):
    """A collection of valid float ranges.

    A single range is the most common, but multiple ranges can be used to specify non-
    contiguous valid values.

    """

    valid_ranges: list[FloatRange] = Field(default_factory=list, min_length=1)
    """Defines one or more valid ranges.

    Multiple ranges can be used to specify non- contiguous valid values. Typically, only
    one range is used. In cases where multiple ranges are used, then the value is valid
    when it is valid in any of the provided ranges.

    """

    applies_to_calibrated: bool = Field(default=True)
    """Whether these valid ranges apply to calibrated values.

    If False, they apply to raw values.

    """

    @classmethod
    def _from_v1_2(
        cls: type[Self], float_range: xtce_1_2.ValidFloatRangeSetType
    ) -> Self:
        return cls(
            valid_ranges=[
                FloatRange._from_v1_2(range) for range in float_range.valid_range
            ],
            applies_to_calibrated=float_range.valid_range_applies_to_calibrated,
        )

    @classmethod
    def _from_v1_3(
        cls: type[Self], float_range: xtce_1_3.ValidFloatRangeSetType
    ) -> Self:
        return cls(
            valid_ranges=[
                FloatRange._from_v1_3(range) for range in float_range.valid_range
            ],
            applies_to_calibrated=float_range.valid_range_applies_to_calibrated,
        )

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create a ValidFloatRanges from an xsdata-generated
        ValidFloatRangeSetType object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, cls.__name__)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ValidFloatRangeSetType:
        return xtce_1_2.ValidFloatRangeSetType(
            valid_range=[range._to_v1_2(policy) for range in self.valid_ranges],
            valid_range_applies_to_calibrated=self.applies_to_calibrated,
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.ValidFloatRangeSetType:
        return xtce_1_3.ValidFloatRangeSetType(
            valid_range=[range._to_v1_3(policy) for range in self.valid_ranges],
            valid_range_applies_to_calibrated=self.applies_to_calibrated,
        )

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.ValidFloatRangeSetType | xtce_1_3.ValidFloatRangeSetType:
        """Convert this ValidFloatRanges to an xsdata-generated ValidFloatRangeSetType
        object of the specified version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, self.__class__.__name__)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)


class MultiRange(FloatRange):
    """An entry in a multi-range alarm definition.

    This allows for alarm ranges that go beyond the typical "inside" and "outside" range
    definitions.

    """

    range_form: RangeForm = Field(default=RangeForm.OUTSIDE)
    """The form of the range.

    A value of `OUTSIDE` specifies that the most severe range is outside all the other
    ranges:

        -severe -critical -distress -warning -watch
        normal
        +watch +warning +distress +critical +severe

    This means each min, max pair are a range: (-inf, min) or (-inf, min], and [max, inf) or (max, inf). However a value of `INSIDE` "inverts" these bands:

        -normal -watch -warning -distress -critical
        severe
        +critical +distress +warning +watch +normal

    This means each min, max pair form a range of (min, max) or [min, max) or (min, max] or [min, max]. The most common form used is "outside" and it is the default. The set notation used defines parenthesis as exclusive and square brackets as inclusive.

    """

    level: ConcernLevel = Field(...)
    """The concern level of this alarm range."""

    @classmethod
    def _from_v1_2(cls: type[Self], multi_range: xtce_1_2.MultiRangeType) -> Self:
        return cls(
            min_inclusive=multi_range.min_inclusive,
            min_exclusive=multi_range.min_exclusive,
            max_inclusive=multi_range.max_inclusive,
            max_exclusive=multi_range.max_exclusive,
            range_form=RangeForm(multi_range.range_form.value),
            level=ConcernLevel(unwrap(multi_range.level).value),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], multi_range: xtce_1_3.MultiRangeType) -> Self:
        return cls(
            min_inclusive=multi_range.min_inclusive,
            min_exclusive=multi_range.min_exclusive,
            max_inclusive=multi_range.max_inclusive,
            max_exclusive=multi_range.max_exclusive,
            range_form=RangeForm(multi_range.range_form.value),
            level=ConcernLevel(unwrap(multi_range.level).value),
        )

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create a MultiRange from an xsdata-generated MultiRange
        object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, cls.__name__)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.MultiRangeType:
        return xtce_1_2.MultiRangeType(
            min_inclusive=self.min_inclusive,
            min_exclusive=self.min_exclusive,
            max_inclusive=self.max_inclusive,
            max_exclusive=self.max_exclusive,
            range_form=xtce_1_2.RangeFormType(self.range_form),
            level=xtce_1_2.ConcernLevelsType(self.level),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.MultiRangeType:
        return xtce_1_3.MultiRangeType(
            min_inclusive=self.min_inclusive,
            min_exclusive=self.min_exclusive,
            max_inclusive=self.max_inclusive,
            max_exclusive=self.max_exclusive,
            range_form=xtce_1_3.RangeFormType(self.range_form),
            level=xtce_1_3.ConcernLevelsType(self.level),
        )

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.MultiRangeType | xtce_1_3.MultiRangeType:
        """Convert this MultiRange to an xsdata-generated MultiRangeType object of the
        specified version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, self.__class__.__name__)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)
