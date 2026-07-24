"""Test algorithm models."""

from __future__ import annotations

import datetime

import pytest

from xtce_lib import (
    DowngradePolicy,
    XtceDowngradeError,
    XtcePath,
    XtceUnsupportedError,
    XtceVersion,
    xtce,
)

SUPPORTED_ALL_VERSIONS = [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3]
SUPPORTED_BASE_VERSIONS = [XtceVersion.V1_2, XtceVersion.V1_3]


def _make_input_parameter_ref(
    ref: str = "/TestSystem/ParameterA",
) -> xtce.InputParameterInstanceRef:
    """Build a reusable input parameter instance reference."""
    return xtce.InputParameterInstanceRef(
        ref=XtcePath(ref),
        instance=0,
        use_calibrated_value=True,
        input_name="InParam",
    )


def _make_constant() -> xtce.Constant:
    """Build a reusable constant for algorithm input tests."""
    return xtce.Constant(constant_name="MyConstant", value=42)


def _make_trigger_set() -> xtce.TriggerSet:
    """Build a reusable trigger set."""
    return xtce.TriggerSet(
        triggers=[
            xtce.OnParameterUpdateTrigger(ref=XtcePath("/TestSystem/ParameterA")),
            xtce.OnPeriodicRateTrigger(fire_rate_sec=1.0),
        ],
        trigger_rate=2,
    )


def _make_output_parameter_ref(
    ref: str = "/TestSystem/ParameterB",
) -> xtce.OutputParameterRef:
    """Build a reusable output parameter reference."""
    return xtce.OutputParameterRef(ref=XtcePath(ref), output_name="OutParam")


class TestConstant:
    """Test Constant model."""

    @pytest.mark.parametrize(
        "value",
        [42, 3.14, "hello", True, b"\xde\xad\xbe\xef"],
        ids=["int", "float", "str", "bool", "bytes"],
    )
    def test_accepts_various_value_types(
        self, value: int | float | str | bool | bytes
    ) -> None:
        """Constant should accept all XtceValue variants."""
        model = xtce.Constant(constant_name="C1", value=value)

        assert model.value == value

    @pytest.mark.parametrize(
        "value",
        [42, 3.14, "hello", True, b"\xde\xad\xbe\xef"],
        ids=["int", "float", "str", "bool", "bytes"],
    )
    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip(
        self, value: int | float | str | bool | bytes, version: XtceVersion
    ) -> None:
        """Round-trip a constant through each supported version."""
        original = xtce.Constant(constant_name="C1", value=value)

        round_tripped = xtce.Constant.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    def test_round_trip_timedelta(self) -> None:
        """A timedelta value should round-trip through XTCE duration encoding."""
        original = xtce.Constant(
            constant_name="C1", value=datetime.timedelta(seconds=5)
        )

        round_tripped = xtce.Constant.from_xsdata(
            original.to_xsdata(XtceVersion.V1_2), XtceVersion.V1_2
        )

        assert round_tripped == original


class TestAlgorithmText:
    """Test AlgorithmText model."""

    def test_defaults(self) -> None:
        """Defaults should be an empty text and 'pseudo' language."""
        model = xtce.AlgorithmText()

        assert model.text == ""
        assert model.language == "pseudo"

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip algorithm text through each supported version."""
        original = xtce.AlgorithmText(text="return x + 1;", language="python")

        round_tripped = xtce.AlgorithmText.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestExternalAlgorithm:
    """Test ExternalAlgorithm model."""

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip an external algorithm through each supported version."""
        original = xtce.ExternalAlgorithm(
            implementation_name="OpenC3", algorithm_location="/opt/algos/foo.so"
        )

        round_tripped = xtce.ExternalAlgorithm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestInputAlgorithm:
    """Test InputAlgorithm model."""

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip a minimal input algorithm through each supported version."""
        original = xtce.InputAlgorithm(name="MyAlgorithm")

        round_tripped = xtce.InputAlgorithm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip_full(self, version: XtceVersion) -> None:
        """Round-trip a fully populated input algorithm through each version."""
        original = xtce.InputAlgorithm(
            name="MyAlgorithm",
            short_description="A short description",
            algorithm_text=xtce.AlgorithmText(text="1 + 1", language="python"),
            external_algorithms=[
                xtce.ExternalAlgorithm(
                    implementation_name="OpenC3",
                    algorithm_location="/opt/algos/foo.so",
                )
            ],
            inputs=[_make_input_parameter_ref(), _make_constant()],
        )

        round_tripped = xtce.InputAlgorithm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_BASE_VERSIONS)
    def test_round_trip_with_long_description_and_aliases(
        self, version: XtceVersion
    ) -> None:
        """Round-trip long_description and aliases on 1.2+."""
        original = xtce.InputAlgorithm(
            name="MyAlgorithm",
            long_description="A long description",
            aliases=[xtce.Alias(namespace="Bus", alias="MyAlgorithm")],
        )

        round_tripped = xtce.InputAlgorithm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestArgumentInputAlgorithm:
    """Test ArgumentInputAlgorithm model."""

    def test_from_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 import is unsupported for ArgumentInputAlgorithm."""
        with pytest.raises(XtceUnsupportedError):
            xtce.ArgumentInputAlgorithm.from_xsdata(object(), XtceVersion.V1_1)

    def test_to_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 export is unsupported for ArgumentInputAlgorithm."""
        model = xtce.ArgumentInputAlgorithm(name="MyAlgorithm")

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)

    def test_round_trip_v1_2_with_parameter_and_argument_inputs(self) -> None:
        """Round-trip inputs restricted to parameter/argument refs through 1.2."""
        original = xtce.ArgumentInputAlgorithm(
            name="MyAlgorithm",
            inputs=[
                _make_input_parameter_ref(),
                xtce.ArgumentInstanceRef(ref="ArgumentA"),
            ],
        )

        round_tripped = xtce.ArgumentInputAlgorithm.from_xsdata(
            original.to_xsdata(XtceVersion.V1_2), XtceVersion.V1_2
        )

        assert round_tripped == original

    def test_v1_2_strict_rejects_constant_input(self) -> None:
        """A Constant input cannot be represented in XTCE 1.2 and should raise."""
        model = xtce.ArgumentInputAlgorithm(
            name="MyAlgorithm", inputs=[_make_constant()]
        )

        with pytest.raises((XtceDowngradeError, TypeError)):
            model.to_xsdata(XtceVersion.V1_2, DowngradePolicy.STRICT)

    def test_round_trip_v1_3_with_all_input_kinds(self) -> None:
        """Round-trip inputs of every kind through XTCE 1.3."""
        original = xtce.ArgumentInputAlgorithm(
            name="MyAlgorithm",
            inputs=[
                _make_input_parameter_ref(),
                xtce.ArgumentInstanceRef(ref="ArgumentA"),
                _make_constant(),
            ],
        )

        round_tripped = xtce.ArgumentInputAlgorithm.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original


class TestTriggeredMathOperation:
    """Test TriggeredMathOperation model."""

    def test_round_trip_v1_1(self) -> None:
        """Round-trip a triggered math operation through XTCE 1.1.

        XTCE 1.1 stores ValueOperand as a native float.

        """
        original = xtce.TriggeredMathOperation(
            operation=[xtce.ValueOperand(value=1.0)],
            trigger_set=_make_trigger_set(),
            output_parameter_ref=XtcePath("/TestSystem/ParameterB"),
        )

        round_tripped = xtce.TriggeredMathOperation.from_xsdata(
            original.to_xsdata(XtceVersion.V1_1), XtceVersion.V1_1
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_BASE_VERSIONS)
    def test_round_trip_v1_2_and_v1_3(self, version: XtceVersion) -> None:
        """Round-trip a triggered math operation through XTCE 1.2 and 1.3.

        XTCE 1.2+ stores ValueOperand as a string.

        """
        original = xtce.TriggeredMathOperation(
            name="MyMathOp",
            short_description="A description",
            operation=[
                xtce.ValueOperand(value="1"),
                xtce.ThisParameterOperand(),
                xtce.MathOperator.ADD,
            ],
            trigger_set=_make_trigger_set(),
            output_parameter_ref=XtcePath("/TestSystem/ParameterB"),
        )

        round_tripped = xtce.TriggeredMathOperation.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_to_v1_1_strict_rejects_name(self) -> None:
        """Exporting a name to XTCE 1.1 should raise in strict mode."""
        model = xtce.TriggeredMathOperation(
            name="MyMathOp",
            operation=[xtce.ValueOperand(value=1.0)],
            trigger_set=_make_trigger_set(),
            output_parameter_ref=XtcePath("/TestSystem/ParameterB"),
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_1, DowngradePolicy.STRICT)


class TestMathAlgorithm:
    """Test MathAlgorithm model."""

    @pytest.mark.parametrize("version", SUPPORTED_BASE_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a math algorithm through XTCE 1.2 and 1.3.

        Uses a string ValueOperand since these versions store it as a string.

        """
        original = xtce.MathAlgorithm(
            name="MyMathAlgorithm",
            math_operation=xtce.TriggeredMathOperation(
                operation=[xtce.ValueOperand(value="1")],
                trigger_set=_make_trigger_set(),
                output_parameter_ref=XtcePath("/TestSystem/ParameterB"),
            ),
        )

        round_tripped = xtce.MathAlgorithm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_round_trip_v1_1(self) -> None:
        """Round-trip a math algorithm through XTCE 1.1 using a float operand."""
        original = xtce.MathAlgorithm(
            name="MyMathAlgorithm",
            math_operation=xtce.TriggeredMathOperation(
                operation=[xtce.ValueOperand(value=1.0)],
                trigger_set=_make_trigger_set(),
                output_parameter_ref=XtcePath("/TestSystem/ParameterB"),
            ),
        )

        round_tripped = xtce.MathAlgorithm.from_xsdata(
            original.to_xsdata(XtceVersion.V1_1), XtceVersion.V1_1
        )

        assert round_tripped == original


class TestInputOutputAlgorithm:
    """Test InputOutputAlgorithm model."""

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip an input/output algorithm through each supported version."""
        original = xtce.InputOutputAlgorithm(
            name="MyAlgorithm",
            inputs=[_make_input_parameter_ref()],
            outputs=[_make_output_parameter_ref()],
            thread=True,
        )

        round_tripped = xtce.InputOutputAlgorithm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip_thread_false(self, version: XtceVersion) -> None:
        """A False thread flag should also round-trip correctly."""
        original = xtce.InputOutputAlgorithm(name="MyAlgorithm", thread=False)

        round_tripped = xtce.InputOutputAlgorithm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestInputOutputTriggerAlgorithm:
    """Test InputOutputTriggerAlgorithm model."""

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip a triggered input/output algorithm through each version."""
        original = xtce.InputOutputTriggerAlgorithm(
            name="MyAlgorithm",
            inputs=[_make_input_parameter_ref()],
            outputs=[_make_output_parameter_ref()],
            thread=True,
            triggers=_make_trigger_set(),
            trigger_container=XtcePath("/TestSystem/TestContainer"),
            priority=3,
        )

        round_tripped = xtce.InputOutputTriggerAlgorithm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_ALL_VERSIONS)
    def test_round_trip_without_triggers(self, version: XtceVersion) -> None:
        """A model with no triggers/trigger_container/priority should round-trip."""
        original = xtce.InputOutputTriggerAlgorithm(name="MyAlgorithm")

        round_tripped = xtce.InputOutputTriggerAlgorithm.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestChecksum:
    """Test Checksum model."""

    def test_from_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 import is unsupported for Checksum."""
        with pytest.raises(XtceUnsupportedError):
            xtce.Checksum.from_xsdata(object(), XtceVersion.V1_1)

    def test_to_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 export is unsupported for Checksum."""
        model = xtce.Checksum(name=xtce.ChecksumType.SUM8)

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)

    def test_round_trip_v1_2_without_parameter_ref(self) -> None:
        """Round-trip a checksum through XTCE 1.2 (no parameter_ref support)."""
        original = xtce.Checksum(
            name=xtce.ChecksumType.FLETCHER16,
            bits_from_reference=8,
            reference=xtce.ReferencePoint.END,
            hash_size_bits=16,
        )

        round_tripped = xtce.Checksum.from_xsdata(
            original.to_xsdata(XtceVersion.V1_2), XtceVersion.V1_2
        )

        assert round_tripped == original

    def test_to_v1_2_strict_rejects_parameter_ref(self) -> None:
        """Exporting parameter_ref to XTCE 1.2 should raise in strict mode."""
        model = xtce.Checksum(
            name=xtce.ChecksumType.SUM8,
            parameter_ref=XtcePath("/TestSystem/ParameterA"),
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_2, DowngradePolicy.STRICT)

    def test_round_trip_v1_3_with_parameter_ref(self) -> None:
        """Round-trip a checksum with parameter_ref through XTCE 1.3."""
        original = xtce.Checksum(
            name=xtce.ChecksumType.CUSTOM,
            input_algorithm=xtce.InputAlgorithm(name="MyChecksumAlgorithm"),
            parameter_ref=XtcePath("/TestSystem/ParameterA"),
        )

        round_tripped = xtce.Checksum.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original

    def test_round_trip_v1_3_without_parameter_ref(self) -> None:
        """A checksum with no parameter_ref should not serialize as the string 'None'."""
        original = xtce.Checksum(name=xtce.ChecksumType.SUM8)

        xsdata_obj = original.to_xsdata(XtceVersion.V1_3)

        assert xsdata_obj.parameter_ref is None

        round_tripped = xtce.Checksum.from_xsdata(xsdata_obj, XtceVersion.V1_3)

        assert round_tripped == original


class TestCRC:
    """Test CRC model."""

    def test_from_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 import is unsupported for CRC."""
        with pytest.raises(XtceUnsupportedError):
            xtce.CRC.from_xsdata(object(), XtceVersion.V1_1)

    def test_to_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 export is unsupported for CRC."""
        model = xtce.CRC(polynomial=b"\x07", width=8)

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)

    def test_round_trip_v1_2(self) -> None:
        """Round-trip a CRC through XTCE 1.2 (no direction support)."""
        original = xtce.CRC(
            polynomial=b"\x07",
            init_remainder=b"\xff",
            final_xor=b"\xff",
            width=8,
            reflect_data=True,
            reflect_remainder=True,
            bits_from_reference=4,
            reference=xtce.ReferencePoint.END,
        )

        round_tripped = xtce.CRC.from_xsdata(
            original.to_xsdata(XtceVersion.V1_2), XtceVersion.V1_2
        )

        assert round_tripped == original

    def test_to_v1_2_strict_rejects_non_default_direction(self) -> None:
        """Exporting a non-default direction to XTCE 1.2 should raise in strict mode."""
        model = xtce.CRC(
            polynomial=b"\x07",
            width=8,
            direction=xtce.BitOrder.LEAST_SIGNIFICANT_BIT_FIRST,
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_2, DowngradePolicy.STRICT)

    def test_round_trip_v1_3_with_direction_and_parameter_ref(self) -> None:
        """Round-trip a CRC with direction and parameter_ref through XTCE 1.3."""
        original = xtce.CRC(
            polynomial=b"\x07",
            width=8,
            direction=xtce.BitOrder.LEAST_SIGNIFICANT_BIT_FIRST,
        )

        round_tripped = xtce.CRC.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original


class TestXOR:
    """Test XOR model."""

    def test_from_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 import is unsupported for XOR."""
        with pytest.raises(XtceUnsupportedError):
            xtce.XOR.from_xsdata(object(), XtceVersion.V1_1)

    def test_from_v1_2_is_unsupported(self) -> None:
        """XTCE 1.2 import is unsupported for XOR."""
        with pytest.raises(XtceUnsupportedError):
            xtce.XOR.from_xsdata(object(), XtceVersion.V1_2)

    def test_to_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 export is unsupported for XOR."""
        model = xtce.XOR()

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)

    def test_to_v1_2_is_unsupported(self) -> None:
        """XTCE 1.2 export is unsupported for XOR."""
        model = xtce.XOR()

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_2)

    def test_round_trip_v1_3_with_parameter_ref(self) -> None:
        """Round-trip an XOR with a parameter_ref through XTCE 1.3."""
        original = xtce.XOR(
            bits_from_reference=4,
            reference=xtce.ReferencePoint.END,
            parameter_ref=XtcePath("/TestSystem/ParameterA"),
        )

        round_tripped = xtce.XOR.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original

    def test_round_trip_v1_3_without_parameter_ref(self) -> None:
        """An XOR with no parameter_ref should not serialize as the string 'None'."""
        original = xtce.XOR()

        xsdata_obj = original.to_xsdata(XtceVersion.V1_3)

        assert xsdata_obj.parameter_ref is None

        round_tripped = xtce.XOR.from_xsdata(xsdata_obj, XtceVersion.V1_3)

        assert round_tripped == original


class TestParity:
    """Test Parity model."""

    def test_from_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 import is unsupported for Parity."""
        with pytest.raises(XtceUnsupportedError):
            xtce.Parity.from_xsdata(object(), XtceVersion.V1_1)

    def test_to_v1_1_is_unsupported(self) -> None:
        """XTCE 1.1 export is unsupported for Parity."""
        model = xtce.Parity(parity_form=xtce.ParityForm.EVEN)

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)

    def test_round_trip_v1_2_without_parameter_ref(self) -> None:
        """Round-trip a parity through XTCE 1.2 (no parameter_ref support)."""
        original = xtce.Parity(
            parity_form=xtce.ParityForm.ODD,
            bits_from_reference=2,
            reference=xtce.ReferencePoint.END,
        )

        round_tripped = xtce.Parity.from_xsdata(
            original.to_xsdata(XtceVersion.V1_2), XtceVersion.V1_2
        )

        assert round_tripped == original

    def test_round_trip_v1_3_with_parameter_ref(self) -> None:
        """Round-trip a parity with a parameter_ref through XTCE 1.3."""
        original = xtce.Parity(
            parity_form=xtce.ParityForm.EVEN,
            parameter_ref=XtcePath("/TestSystem/ParameterA"),
        )

        round_tripped = xtce.Parity.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original

    def test_round_trip_v1_3_without_parameter_ref(self) -> None:
        """A parity with no parameter_ref should not serialize as the string 'None'."""
        original = xtce.Parity(parity_form=xtce.ParityForm.EVEN)

        xsdata_obj = original.to_xsdata(XtceVersion.V1_3)

        assert xsdata_obj.parameter_ref is None

        round_tripped = xtce.Parity.from_xsdata(xsdata_obj, XtceVersion.V1_3)

        assert round_tripped == original
