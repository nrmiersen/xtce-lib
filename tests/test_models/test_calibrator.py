"""Test calibrator models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from xtce_lib import (
    DowngradePolicy,
    XtceDowngradeError,
    XtcePath,
    XtceUnsupportedError,
    XtceVersion,
    xtce,
)
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

SUPPORTED_MATH_OPERATION_VERSIONS = [
    XtceVersion.V1_1,
    XtceVersion.V1_2,
    XtceVersion.V1_3,
]
SUPPORTED_BASE_CALIBRATOR_VERSIONS = [XtceVersion.V1_2, XtceVersion.V1_3]
SUPPORTED_CALIBRATOR_VERSIONS = [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3]


def _make_ancillary_data() -> xtce.AncillaryData:
    """Build a reusable ancillary data element for calibrator tests."""
    return xtce.AncillaryData(
        name="ContainerSize",
        value="123 bytes",
        mime_type="text/plain",
        href="http://example.com/data",
    )


def _make_comparison(ref: str = "/TestSystem/ParameterA") -> xtce.Comparison:
    """Build a reusable comparison for context match tests."""
    return xtce.Comparison(
        ref=XtcePath(ref),
        instance=0,
        use_calibrated_value=True,
        comparison_operator=xtce.ComparisonOperator.EQ,
        value=1,
    )


def _make_context_match() -> xtce.ContextMatch:
    """Build a reusable context match for context calibrator tests."""
    return xtce.ContextMatch(criteria=_make_comparison())


def _make_rpn_operation() -> list[
    xtce.ValueOperand
    | xtce.ThisParameterOperand
    | xtce.MathOperator
    | xtce.ParameterInstanceRef
]:
    """Build a valid RPN operation sequence exercising every operand kind."""
    return [
        xtce.ValueOperand(value=1.0),
        xtce.ValueOperand(value=2.0),
        xtce.MathOperator.ADD,
        xtce.ThisParameterOperand(),
        xtce.MathOperator.MULTIPLY,
        xtce.ParameterInstanceRef(
            ref=XtcePath("/TestSystem/ParameterA"),
            instance=0,
            use_calibrated_value=True,
        ),
        xtce.MathOperator.SUBTRACT,
    ]


class TestValueOperand:
    """Test ValueOperand model."""

    def test_accepts_float_value(self) -> None:
        """A plain float should be accepted as-is."""
        model = xtce.ValueOperand(value=3.14)

        assert model.value == 3.14

    @pytest.mark.parametrize("value", ["1e9", "3.14", "-2", "10"])
    def test_accepts_numeric_string_value(self, value: str) -> None:
        """Numeric strings, including scientific notation, should be accepted."""
        model = xtce.ValueOperand(value=value)

        assert model.value == value

    def test_rejects_non_numeric_string_value(self) -> None:
        """Non-numeric strings should raise a validation error."""
        with pytest.raises(ValidationError):
            xtce.ValueOperand(value="not-a-number")


class TestThisParameterOperand:
    """Test ThisParameterOperand model."""

    def test_constructs_with_no_fields(self) -> None:
        """ThisParameterOperand should construct without any fields."""
        model = xtce.ThisParameterOperand()

        assert isinstance(model, xtce.ThisParameterOperand)


class TestMathOperationCalibrator:
    """Test MathOperationCalibrator model."""

    def test_accepts_empty_operation(self) -> None:
        """An empty operation sequence should be valid."""
        model = xtce.MathOperationCalibrator()

        assert model.operation == []

    def test_accepts_valid_rpn_sequence(self) -> None:
        """A well-formed RPN sequence should be accepted."""
        model = xtce.MathOperationCalibrator(operation=_make_rpn_operation())

        assert len(model.operation) == 7

    def test_rejects_stack_underflow(self) -> None:
        """An operator without enough operands should raise a validation error."""
        with pytest.raises(ValidationError) as exc_info:
            xtce.MathOperationCalibrator(
                operation=[xtce.ValueOperand(value=1.0), xtce.MathOperator.ADD]
            )

        assert "RPN stack underflow" in str(exc_info.value)

    def test_rejects_leftover_stack_depth(self) -> None:
        """A sequence that doesn't reduce to a single value should be rejected."""
        with pytest.raises(ValidationError) as exc_info:
            xtce.MathOperationCalibrator(
                operation=[xtce.ValueOperand(value=1.0), xtce.ValueOperand(value=2.0)]
            )

        assert "invalid RPN sequence" in str(exc_info.value)

    def test_round_trip_operands_only_v1_1(self) -> None:
        """Round-trip a basic operand sequence through XTCE 1.1.

        XTCE 1.1 stores ValueOperand as a native float, so a float-valued operand
        round-trips exactly.

        """
        original = xtce.MathOperationCalibrator(operation=_make_rpn_operation())

        round_tripped = xtce.MathOperationCalibrator.from_xsdata(
            original.to_xsdata(XtceVersion.V1_1), XtceVersion.V1_1
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_BASE_CALIBRATOR_VERSIONS)
    def test_round_trip_operands_only_v1_2_and_v1_3(self, version: XtceVersion) -> None:
        """Round-trip a basic operand sequence through XTCE 1.2 and 1.3.

        XTCE 1.2+ stores ValueOperand as a string, so a string-valued operand is used
        here to round-trip exactly.

        """
        original = xtce.MathOperationCalibrator(
            operation=[
                xtce.ValueOperand(value="1"),
                xtce.ValueOperand(value="2"),
                xtce.MathOperator.ADD,
                xtce.ThisParameterOperand(),
                xtce.MathOperator.MULTIPLY,
                xtce.ParameterInstanceRef(
                    ref=XtcePath("/TestSystem/ParameterA"),
                    instance=0,
                    use_calibrated_value=True,
                ),
                xtce.MathOperator.SUBTRACT,
            ]
        )

        round_tripped = xtce.MathOperationCalibrator.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_BASE_CALIBRATOR_VERSIONS)
    def test_round_trip_with_name_and_ancillary_data(
        self, version: XtceVersion
    ) -> None:
        """Round-trip name, short_description and ancillary_data on 1.2+."""
        original = xtce.MathOperationCalibrator(
            name="MyCalibrator",
            short_description="A description",
            ancillary_data=[_make_ancillary_data()],
            operation=[xtce.ValueOperand(value="1")],
        )

        round_tripped = xtce.MathOperationCalibrator.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_to_v1_1_strict_rejects_name(self) -> None:
        """Exporting a name to XTCE 1.1 should raise in strict mode."""
        model = xtce.MathOperationCalibrator(
            name="MyCalibrator", operation=[xtce.ValueOperand(value=1.0)]
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.STRICT)

    def test_to_v1_1_ignore_drops_name(self) -> None:
        """Exporting a name to XTCE 1.1 should succeed under IGNORE policy."""
        model = xtce.MathOperationCalibrator(
            name="MyCalibrator", operation=[xtce.ValueOperand(value=1.0)]
        )

        xsdata_obj = model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.IGNORE)

        assert isinstance(xsdata_obj, xtce_1_1.MathOperationType)

    def test_to_v1_2_preserves_numeric_string_value_operand(self) -> None:
        """Numeric string value operands should be preserved verbatim in 1.2."""
        model = xtce.MathOperationCalibrator(operation=[xtce.ValueOperand(value="1e9")])

        xsdata_obj = model._to_v1_2()

        assert isinstance(
            xsdata_obj.choice[0], xtce_1_2.MathOperationCalibratorType.ValueOperand
        )
        assert xsdata_obj.choice[0].value == "1e9"

    def test_to_v1_3_preserves_numeric_string_value_operand(self) -> None:
        """Numeric string value operands should be preserved verbatim in 1.3."""
        model = xtce.MathOperationCalibrator(operation=[xtce.ValueOperand(value="1e9")])

        xsdata_obj = model._to_v1_3()

        assert isinstance(
            xsdata_obj.choice[0], xtce_1_3.MathOperationCalibratorType.ValueOperand
        )
        assert xsdata_obj.choice[0].value == "1e9"

    def test_to_v1_1_converts_numeric_string_value_operand_to_float(self) -> None:
        """Numeric string value operands should be converted to float for 1.1."""
        model = xtce.MathOperationCalibrator(operation=[xtce.ValueOperand(value="1e9")])

        xsdata_obj = model._to_v1_1()

        assert xsdata_obj.choice[0] == 1e9
        assert isinstance(xsdata_obj.choice[0], float)

    def test_from_v1_2_keeps_numeric_string_literal(self) -> None:
        """Importing from 1.2 should preserve the raw numeric string."""
        raw_obj = xtce_1_2.MathOperationCalibratorType(
            choice=[xtce_1_2.MathOperationCalibratorType.ValueOperand(value="1e9")]
        )

        model = xtce.MathOperationCalibrator._from_v1_2(raw_obj)

        assert model.operation[0] == xtce.ValueOperand(value="1e9")

    def test_from_v1_1_keeps_float_operand(self) -> None:
        """Importing from 1.1 should produce a float-valued ValueOperand."""
        raw_obj = xtce_1_1.MathOperationType(choice=[1e9])

        model = xtce.MathOperationCalibrator._from_v1_1(raw_obj)

        assert model.operation[0] == xtce.ValueOperand(value=1e9)


class TestArgumentMathOperation:
    """Test ArgumentMathOperation model."""

    def test_accepts_valid_rpn_sequence_with_argument_ref(self) -> None:
        """A valid RPN sequence including an ArgumentInstanceRef should be accepted."""
        model = xtce.ArgumentMathOperation(
            operation=[
                xtce.ValueOperand(value=1.0),
                xtce.ArgumentInstanceRef(ref="ArgumentA"),
                xtce.MathOperator.ADD,
            ]
        )

        assert len(model.operation) == 3

    def test_rejects_stack_underflow(self) -> None:
        """An operator without enough operands should raise a validation error."""
        with pytest.raises(ValidationError) as exc_info:
            xtce.ArgumentMathOperation(
                operation=[xtce.ValueOperand(value=1.0), xtce.MathOperator.ADD]
            )

        assert "RPN stack underflow" in str(exc_info.value)

    def test_from_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 import is unsupported for ArgumentMathOperation."""
        with pytest.raises(XtceUnsupportedError):
            xtce.ArgumentMathOperation.from_xsdata(object(), XtceVersion.V1_1)

    def test_from_v1_2_is_unsupported(self) -> None:
        """XTCE 1.2 import is unsupported for ArgumentMathOperation."""
        with pytest.raises(XtceUnsupportedError):
            xtce.ArgumentMathOperation.from_xsdata(object(), XtceVersion.V1_2)

    def test_to_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 export is unsupported for ArgumentMathOperation."""
        model = xtce.ArgumentMathOperation(operation=[xtce.ValueOperand(value=1.0)])

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)

    def test_to_v1_2_is_unsupported(self) -> None:
        """XTCE 1.2 export is unsupported for ArgumentMathOperation."""
        model = xtce.ArgumentMathOperation(operation=[xtce.ValueOperand(value=1.0)])

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_2)

    def test_round_trip_v1_3(self) -> None:
        """Round-trip an operation with all operand kinds through XTCE 1.3.

        XTCE 1.3 stores ValueOperand as a string, so string-valued operands are used
        here to round-trip exactly.

        """
        original = xtce.ArgumentMathOperation(
            operation=[
                xtce.ValueOperand(value="1"),
                xtce.ValueOperand(value="2"),
                xtce.MathOperator.ADD,
                xtce.ThisParameterOperand(),
                xtce.MathOperator.MULTIPLY,
                xtce.ParameterInstanceRef(
                    ref=XtcePath("/TestSystem/ParameterA"),
                    instance=0,
                    use_calibrated_value=True,
                ),
                xtce.MathOperator.SUBTRACT,
                xtce.ArgumentInstanceRef(ref="ArgumentA", use_calibrated_value=False),
                xtce.MathOperator.ADD,
            ]
        )

        round_tripped = xtce.ArgumentMathOperation.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original


class TestSplinePoint:
    """Test SplinePoint model."""

    def test_accepts_fields(self) -> None:
        """SplinePoint should accept order, raw and calibrated values."""
        model = xtce.SplinePoint(order=2, raw=1.0, calibrated=2.0)

        assert model.order == 2
        assert model.raw == 1.0
        assert model.calibrated == 2.0

    def test_defaults_order_to_one(self) -> None:
        """The order field should default to 1."""
        model = xtce.SplinePoint(raw=1.0, calibrated=2.0)

        assert model.order == 1

    @pytest.mark.parametrize("version", SUPPORTED_CALIBRATOR_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a spline point through each supported version."""
        original = xtce.SplinePoint(order=0, raw=1.5, calibrated=2.5)

        round_tripped = xtce.SplinePoint.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestSplineCalibrator:
    """Test SplineCalibrator model."""

    def test_rejects_fewer_than_two_spline_points(self) -> None:
        """At least two spline points are required when explicitly provided."""
        with pytest.raises(ValidationError):
            xtce.SplineCalibrator(
                spline_points=[xtce.SplinePoint(raw=1.0, calibrated=2.0)]
            )

    def test_accepts_two_spline_points(self) -> None:
        """Two spline points should be accepted."""
        model = xtce.SplineCalibrator(
            spline_points=[
                xtce.SplinePoint(raw=1.0, calibrated=2.0),
                xtce.SplinePoint(raw=3.0, calibrated=4.0),
            ]
        )

        assert len(model.spline_points) == 2

    @pytest.mark.parametrize("version", SUPPORTED_CALIBRATOR_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a spline calibrator through each supported version."""
        original = xtce.SplineCalibrator(
            spline_points=[
                xtce.SplinePoint(raw=1.0, calibrated=2.0),
                xtce.SplinePoint(raw=3.0, calibrated=4.0),
            ],
            order=2,
            extrapolate=True,
        )

        round_tripped = xtce.SplineCalibrator.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_BASE_CALIBRATOR_VERSIONS)
    def test_round_trip_with_name_and_ancillary_data(
        self, version: XtceVersion
    ) -> None:
        """Round-trip name, short_description and ancillary_data on 1.2+."""
        original = xtce.SplineCalibrator(
            name="MySpline",
            short_description="A description",
            ancillary_data=[_make_ancillary_data()],
            spline_points=[
                xtce.SplinePoint(raw=1.0, calibrated=2.0),
                xtce.SplinePoint(raw=3.0, calibrated=4.0),
            ],
        )

        round_tripped = xtce.SplineCalibrator.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_to_v1_1_strict_rejects_name(self) -> None:
        """Exporting a name to XTCE 1.1 should raise in strict mode."""
        model = xtce.SplineCalibrator(
            name="MySpline",
            spline_points=[
                xtce.SplinePoint(raw=1.0, calibrated=2.0),
                xtce.SplinePoint(raw=3.0, calibrated=4.0),
            ],
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.STRICT)

    def test_to_v1_1_ignore_drops_name(self) -> None:
        """Exporting a name to XTCE 1.1 should succeed under IGNORE policy."""
        model = xtce.SplineCalibrator(
            name="MySpline",
            spline_points=[
                xtce.SplinePoint(raw=1.0, calibrated=2.0),
                xtce.SplinePoint(raw=3.0, calibrated=4.0),
            ],
        )

        xsdata_obj = model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.IGNORE)

        assert isinstance(xsdata_obj, xtce_1_1.CalibratorType.SplineCalibrator)


class TestTerm:
    """Test Term model."""

    def test_accepts_fields(self) -> None:
        """Term should accept coefficient and exponent."""
        model = xtce.Term(coefficient=2.0, exponent=3)

        assert model.coefficient == 2.0
        assert model.exponent == 3

    def test_rejects_negative_exponent(self) -> None:
        """Negative exponents should be rejected."""
        with pytest.raises(ValidationError):
            xtce.Term(coefficient=1.0, exponent=-1)

    @pytest.mark.parametrize("version", SUPPORTED_CALIBRATOR_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a term through each supported version."""
        original = xtce.Term(coefficient=2.5, exponent=2)

        round_tripped = xtce.Term.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original


class TestPolynomialCalibrator:
    """Test PolynomialCalibrator model."""

    def test_accepts_empty_terms_by_default(self) -> None:
        """The terms field should default to an empty list."""
        model = xtce.PolynomialCalibrator()

        assert model.terms == []

    @pytest.mark.parametrize("version", SUPPORTED_CALIBRATOR_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a polynomial calibrator through each supported version."""
        original = xtce.PolynomialCalibrator(
            terms=[
                xtce.Term(coefficient=1.0, exponent=0),
                xtce.Term(coefficient=2.0, exponent=1),
            ]
        )

        round_tripped = xtce.PolynomialCalibrator.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_BASE_CALIBRATOR_VERSIONS)
    def test_round_trip_with_name_and_ancillary_data(
        self, version: XtceVersion
    ) -> None:
        """Round-trip name, short_description and ancillary_data on 1.2+."""
        original = xtce.PolynomialCalibrator(
            name="MyPolynomial",
            short_description="A description",
            ancillary_data=[_make_ancillary_data()],
            terms=[xtce.Term(coefficient=1.0, exponent=0)],
        )

        round_tripped = xtce.PolynomialCalibrator.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_to_v1_1_strict_rejects_ancillary_data(self) -> None:
        """Exporting ancillary_data to XTCE 1.1 should raise in strict mode."""
        model = xtce.PolynomialCalibrator(
            ancillary_data=[_make_ancillary_data()],
            terms=[xtce.Term(coefficient=1.0, exponent=0)],
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.STRICT)

    def test_to_v1_1_ignore_drops_ancillary_data(self) -> None:
        """Exporting ancillary_data to XTCE 1.1 should succeed under IGNORE policy."""
        model = xtce.PolynomialCalibrator(
            ancillary_data=[_make_ancillary_data()],
            terms=[xtce.Term(coefficient=1.0, exponent=0)],
        )

        xsdata_obj = model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.IGNORE)

        assert isinstance(xsdata_obj, xtce_1_1.PolynomialType)


class TestCalibrator:
    """Test Calibrator model."""

    @pytest.mark.parametrize(
        "calibrator_type",
        [
            xtce.SplineCalibrator(
                spline_points=[
                    xtce.SplinePoint(raw=1.0, calibrated=2.0),
                    xtce.SplinePoint(raw=3.0, calibrated=4.0),
                ]
            ),
            xtce.PolynomialCalibrator(terms=[xtce.Term(coefficient=1.0, exponent=0)]),
            xtce.MathOperationCalibrator(operation=[xtce.ThisParameterOperand()]),
        ],
        ids=["spline", "polynomial", "math_operation"],
    )
    @pytest.mark.parametrize("version", SUPPORTED_CALIBRATOR_VERSIONS)
    def test_round_trip_for_each_calibrator_type(
        self,
        calibrator_type: (
            xtce.SplineCalibrator
            | xtce.PolynomialCalibrator
            | xtce.MathOperationCalibrator
        ),
        version: XtceVersion,
    ) -> None:
        """Round-trip a Calibrator wrapping each calibrator_type variant."""
        original = xtce.Calibrator(calibrator_type=calibrator_type)

        round_tripped = xtce.Calibrator.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_v1_1_preserves_long_description_and_aliases(self) -> None:
        """XTCE 1.1 natively supports long_description and aliases."""
        original = xtce.Calibrator(
            long_description="A long description",
            aliases=[xtce.Alias(namespace="Bus", alias="BatteryVoltage")],
            calibrator_type=xtce.PolynomialCalibrator(
                terms=[xtce.Term(coefficient=1.0, exponent=0)]
            ),
        )

        round_tripped = xtce.Calibrator.from_xsdata(
            original.to_xsdata(XtceVersion.V1_1), XtceVersion.V1_1
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_BASE_CALIBRATOR_VERSIONS)
    def test_downgrade_strict_rejects_long_description(
        self, version: XtceVersion
    ) -> None:
        """Exporting long_description to 1.2+ should raise in strict mode."""
        model = xtce.Calibrator(
            long_description="A long description",
            calibrator_type=xtce.PolynomialCalibrator(
                terms=[xtce.Term(coefficient=1.0, exponent=0)]
            ),
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(version, DowngradePolicy.STRICT)

    @pytest.mark.parametrize("version", SUPPORTED_BASE_CALIBRATOR_VERSIONS)
    def test_downgrade_strict_rejects_aliases(self, version: XtceVersion) -> None:
        """Exporting aliases to 1.2+ should raise in strict mode."""
        model = xtce.Calibrator(
            aliases=[xtce.Alias(namespace="Bus", alias="BatteryVoltage")],
            calibrator_type=xtce.PolynomialCalibrator(
                terms=[xtce.Term(coefficient=1.0, exponent=0)]
            ),
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(version, DowngradePolicy.STRICT)

    @pytest.mark.parametrize("version", SUPPORTED_BASE_CALIBRATOR_VERSIONS)
    def test_downgrade_ignore_drops_long_description_and_aliases(
        self, version: XtceVersion
    ) -> None:
        """Exporting long_description/aliases to 1.2+ should succeed under IGNORE."""
        model = xtce.Calibrator(
            long_description="A long description",
            aliases=[xtce.Alias(namespace="Bus", alias="BatteryVoltage")],
            calibrator_type=xtce.PolynomialCalibrator(
                terms=[xtce.Term(coefficient=1.0, exponent=0)]
            ),
        )

        xsdata_obj = model.to_xsdata(version, DowngradePolicy.IGNORE)

        assert xsdata_obj.name == model.name


class TestContextCalibrator:
    """Test ContextCalibrator model."""

    @pytest.mark.parametrize("version", SUPPORTED_BASE_CALIBRATOR_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a context calibrator through XTCE 1.2 and 1.3."""
        original = xtce.ContextCalibrator(
            context_match=_make_context_match(),
            calibrator=xtce.Calibrator(
                calibrator_type=xtce.PolynomialCalibrator(
                    terms=[xtce.Term(coefficient=1.0, exponent=0)]
                )
            ),
        )

        round_tripped = xtce.ContextCalibrator.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestLinearAdjustment:
    """Test LinearAdjustment model."""

    def test_defaults(self) -> None:
        """Default slope should be 1.0 and intercept 0.0."""
        model = xtce.LinearAdjustment()

        assert model.slope == 1.0
        assert model.intercept == 0.0

    def test_accepts_fields(self) -> None:
        """LinearAdjustment should accept custom slope and intercept."""
        model = xtce.LinearAdjustment(slope=2.5, intercept=-1.0)

        assert model.slope == 2.5
        assert model.intercept == -1.0

    @pytest.mark.parametrize("version", SUPPORTED_CALIBRATOR_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a linear adjustment through XTCE 1.2 and 1.3."""
        original = xtce.LinearAdjustment(slope=2.0, intercept=1.5)

        round_tripped = xtce.LinearAdjustment.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_from_v1_2_falls_back_to_default_slope_when_falsy(self) -> None:
        """A falsy slope from XTCE 1.2 should default to 1.0."""
        raw_obj = xtce_1_2.LinearAdjustmentType(slope=0.0, intercept=1.0)

        model = xtce.LinearAdjustment._from_v1_2(raw_obj)

        assert model.slope == 1.0
        assert model.intercept == 1.0


class TestMathOperation:
    """Test MathOperation model (base class for triggered math operations)."""

    def test_inherits_rpn_validation(self) -> None:
        """MathOperation should enforce the same RPN validation as its parent."""
        with pytest.raises(ValidationError):
            xtce.MathOperation(
                operation=[xtce.ValueOperand(value=1.0), xtce.MathOperator.ADD]
            )

    def test_accepts_valid_operation(self) -> None:
        """MathOperation should accept a valid RPN operation sequence."""
        model = xtce.MathOperation(operation=[xtce.ValueOperand(value=1.0)])

        assert model.operation == [xtce.ValueOperand(value=1.0)]
