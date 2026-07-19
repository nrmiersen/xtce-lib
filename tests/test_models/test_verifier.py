"""Test verifier models."""

import datetime

import pytest
from pydantic import ValidationError

from xtce_lib import (
    XtceDowngradeError,
    XtcePath,
    XtceUnsupportedError,
    XtceVersion,
    xtce,
)
from xtce_lib.generated import xtce_1_2, xtce_1_3


def make_parameter_ref() -> xtce.ParameterRef:
    """Build a reusable parameter reference for verifier tests."""
    return xtce.ParameterRef(ref=XtcePath("/SimpleSat/Bus/Voltage"))


def make_parameter_value_change() -> xtce.ParameterValueChange:
    """Build a reusable parameter value change verifier payload."""
    return xtce.ParameterValueChange(ref=make_parameter_ref(), change=1.5)


def make_check_window() -> xtce.CheckWindow:
    """Build a reusable check window."""
    return xtce.CheckWindow(
        start_time=datetime.timedelta(seconds=2),
        stop_time=datetime.timedelta(seconds=15),
        is_relative_to=xtce.TimeWindowIsRelativeTo.COMMAND_RELEASE,
    )


def make_dynamic_percent_complete() -> xtce.DynamicValue:
    """Build a DynamicValue for execution percent completion."""
    return xtce.DynamicValue(
        instance=xtce.ParameterInstanceRef(
            ref=XtcePath("/SimpleSat/Bus/PercentComplete"),
            instance=0,
            use_calibrated_value=True,
        )
    )


def make_argument_assignment() -> xtce.ArgumentAssignment:
    """Build a reusable argument restriction assignment."""
    return xtce.ArgumentAssignment(name="Mode", value="SCIENCE")


class TestParameterValueChange:
    """Test ParameterValueChange model."""

    @pytest.mark.parametrize(
        "version",
        [XtceVersion.V1_2, XtceVersion.V1_3],
    )
    def test_round_trip_through_xsdata_preserves_fields(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve parameter value change fields."""
        original = make_parameter_value_change()

        round_tripped = xtce.ParameterValueChange.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    def test_from_xsdata_rejects_v1_1(self) -> None:
        """v1.1 does not support ParameterValueChange."""
        with pytest.raises(XtceUnsupportedError):
            xtce.ParameterValueChange.from_xsdata(object(), XtceVersion.V1_1)

    def test_to_xsdata_rejects_v1_1(self) -> None:
        """v1.1 export should fail for ParameterValueChange."""
        model = make_parameter_value_change()

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)


class TestCheckWindow:
    """Test CheckWindow model."""

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_2, xtce_1_2.CheckWindowType),
            (XtceVersion.V1_3, xtce_1_3.CheckWindowType),
        ],
    )
    def test_to_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should return the expected versioned CheckWindowType."""
        model = make_check_window()

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.time_to_start_checking is not None
        assert raw_obj.time_to_stop_checking is not None

    @pytest.mark.parametrize("version", [XtceVersion.V1_2, XtceVersion.V1_3])
    def test_round_trip_through_xsdata_preserves_fields(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve check window fields."""
        original = make_check_window()

        round_tripped = xtce.CheckWindow.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", [XtceVersion.V1_2, XtceVersion.V1_3])
    def test_round_trip_preserves_none_start_time(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve optional start_time=None."""
        original = xtce.CheckWindow(stop_time=datetime.timedelta(seconds=10))

        round_tripped = xtce.CheckWindow.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    def test_to_xsdata_rejects_v1_1(self) -> None:
        """v1.1 export should fail for CheckWindow."""
        model = make_check_window()

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)


class TestCheckWindowAlgorithms:
    """Test CheckWindowAlgorithms model."""

    def test_accepts_fields(self) -> None:
        """CheckWindowAlgorithms should accept start and stop InputAlgorithm values."""
        model = xtce.CheckWindowAlgorithms(
            start_time=xtce.InputAlgorithm(name="StartAlgorithm"),
            stop_time=xtce.InputAlgorithm(name="StopAlgorithm"),
        )

        assert isinstance(model.start_time, xtce.InputAlgorithm)
        assert isinstance(model.stop_time, xtce.InputAlgorithm)


@pytest.mark.parametrize(
    "verifier_cls",
    [
        xtce.TransferredToRangeVerifier,
        xtce.SentFromRangeVerifier,
        xtce.ReceivedVerifier,
        xtce.AcceptedVerifier,
        xtce.QueuedVerifier,
    ],
)
class TestSimpleCommandVerifierTypes:
    """Test simple command verifier subclasses."""

    def test_accepts_required_fields(self, verifier_cls: type) -> None:
        """Each verifier type should accept the shared base fields."""
        model = verifier_cls(
            name="Verifier",
            verifier=make_parameter_value_change(),
            check_window=make_check_window(),
        )

        assert model.name == "Verifier"
        assert isinstance(model.verifier, xtce.ParameterValueChange)
        assert isinstance(model.check_window, xtce.CheckWindow)

    @pytest.mark.parametrize(
        "version",
        [XtceVersion.V1_2, XtceVersion.V1_3],
    )
    def test_round_trip_through_xsdata_preserves_fields(
        self,
        verifier_cls: type[xtce.CommandVerifier],
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve shared verifier fields."""
        original = verifier_cls(
            name="Verifier",
            short_description="Short",
            verifier=make_parameter_value_change(),
            check_window=make_check_window(),
        )

        round_tripped = verifier_cls.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    def test_to_xsdata_v1_2_rejects_argument_restrictions(
        self, verifier_cls: type[xtce.CommandVerifier]
    ) -> None:
        """XTCE 1.2 should reject argument restrictions because that field is v1.3 only."""
        model = verifier_cls(
            name="Verifier",
            verifier=make_parameter_value_change(),
            check_window=make_check_window(),
            argument_restrictions=[make_argument_assignment()],
        )

        with pytest.raises(XtceDowngradeError):
            model.to_xsdata(XtceVersion.V1_2)


class TestExecutionVerifier:
    """Test ExecutionVerifier model."""

    def test_accepts_percent_complete_float(self) -> None:
        """ExecutionVerifier should accept percent_complete as a float."""
        model = xtce.ExecutionVerifier(
            name="ExecVerifier",
            verifier=make_parameter_value_change(),
            check_window=make_check_window(),
            percent_complete=12.5,
        )

        assert model.percent_complete == 12.5

    def test_rejects_out_of_range_percent_complete(self) -> None:
        """percent_complete must remain within [0, 100]."""
        with pytest.raises(ValidationError):
            xtce.ExecutionVerifier(
                name="ExecVerifier",
                verifier=make_parameter_value_change(),
                check_window=make_check_window(),
                percent_complete=101.0,
            )

    @pytest.mark.parametrize("version", [XtceVersion.V1_2, XtceVersion.V1_3])
    def test_round_trip_with_float_percent_complete(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve numeric percent completion."""
        original = xtce.ExecutionVerifier(
            name="ExecVerifier",
            verifier=make_parameter_value_change(),
            check_window=make_check_window(),
            percent_complete=88.0,
        )

        round_tripped = xtce.ExecutionVerifier.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", [XtceVersion.V1_2, XtceVersion.V1_3])
    def test_round_trip_with_dynamic_percent_complete(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve DynamicValue percent completion."""
        original = xtce.ExecutionVerifier(
            name="ExecVerifier",
            verifier=make_parameter_value_change(),
            check_window=make_check_window(),
            percent_complete=make_dynamic_percent_complete(),
        )

        round_tripped = xtce.ExecutionVerifier.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original


@pytest.mark.parametrize(
    "verifier_cls",
    [xtce.CompleteVerifier, xtce.FailedVerifier],
)
class TestReturnParameterVerifiers:
    """Test CompleteVerifier and FailedVerifier models."""

    def test_accepts_optional_return_parameter_ref(self, verifier_cls: type) -> None:
        """Return-parameter verifiers should accept return_parm_ref values."""
        model = verifier_cls(
            name="Verifier",
            verifier=make_parameter_value_change(),
            check_window=make_check_window(),
            return_parm_ref=make_parameter_ref(),
        )

        assert model.return_parm_ref is not None
        assert model.return_parm_ref.ref == "/SimpleSat/Bus/Voltage"

    @pytest.mark.parametrize("version", [XtceVersion.V1_2, XtceVersion.V1_3])
    def test_round_trip_preserves_return_parameter_ref(
        self,
        verifier_cls: type,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve optional return_parm_ref."""
        original = verifier_cls(
            name="Verifier",
            verifier=make_parameter_value_change(),
            check_window=make_check_window(),
            return_parm_ref=make_parameter_ref(),
        )

        round_tripped = verifier_cls.from_xsdata(  # type: ignore[attr-defined]
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original


class TestVerifierSet:
    """Test VerifierSet model."""

    def test_accepts_all_verifier_categories(self) -> None:
        """VerifierSet should allow all optional/singular and repeated verifier fields."""
        model = xtce.VerifierSet(
            transferred_to_range_verifier=xtce.TransferredToRangeVerifier(
                name="Transferred",
                verifier=make_parameter_value_change(),
                check_window=make_check_window(),
            ),
            sent_from_range_verifier=xtce.SentFromRangeVerifier(
                name="Sent",
                verifier=make_parameter_value_change(),
                check_window=make_check_window(),
            ),
            received_verifier=xtce.ReceivedVerifier(
                name="Received",
                verifier=make_parameter_value_change(),
                check_window=make_check_window(),
            ),
            accepted_verifier=xtce.AcceptedVerifier(
                name="Accepted",
                verifier=make_parameter_value_change(),
                check_window=make_check_window(),
            ),
            queued_verifier=xtce.QueuedVerifier(
                name="Queued",
                verifier=make_parameter_value_change(),
                check_window=make_check_window(),
            ),
            execution_verifiers=[
                xtce.ExecutionVerifier(
                    name="Executing",
                    verifier=make_parameter_value_change(),
                    check_window=make_check_window(),
                    percent_complete=50.0,
                )
            ],
            complete_verifiers=[
                xtce.CompleteVerifier(
                    name="Complete",
                    verifier=make_parameter_value_change(),
                    check_window=make_check_window(),
                    return_parm_ref=make_parameter_ref(),
                )
            ],
            failed_verifier=xtce.FailedVerifier(
                name="Failed",
                verifier=make_parameter_value_change(),
                check_window=make_check_window(),
                return_parm_ref=make_parameter_ref(),
            ),
        )

        assert model.transferred_to_range_verifier is not None
        assert model.sent_from_range_verifier is not None
        assert model.received_verifier is not None
        assert model.accepted_verifier is not None
        assert model.queued_verifier is not None
        assert len(model.execution_verifiers) == 1
        assert len(model.complete_verifiers) == 1
        assert model.failed_verifier is not None

    @pytest.mark.parametrize(
        ("version", "expected_type"),
        [
            (XtceVersion.V1_2, xtce_1_2.VerifierSetType),
            (XtceVersion.V1_3, xtce_1_3.VerifierSetType),
        ],
    )
    def test_to_xsdata_for_supported_versions(
        self,
        version: XtceVersion,
        expected_type: type,
    ) -> None:
        """to_xsdata should produce the correct versioned VerifierSetType."""
        model = xtce.VerifierSet(
            received_verifier=xtce.ReceivedVerifier(
                name="Received",
                verifier=make_parameter_value_change(),
                check_window=make_check_window(),
            ),
            execution_verifiers=[
                xtce.ExecutionVerifier(
                    name="Executing",
                    verifier=make_parameter_value_change(),
                    check_window=make_check_window(),
                    percent_complete=25.0,
                )
            ],
        )

        raw_obj = model.to_xsdata(version)

        assert isinstance(raw_obj, expected_type)
        assert raw_obj.received_verifier is not None
        assert len(raw_obj.execution_verifier) == 1

    @pytest.mark.parametrize("version", [XtceVersion.V1_2, XtceVersion.V1_3])
    def test_round_trip_through_xsdata_preserves_all_fields(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip conversion should preserve populated verifier-set fields."""
        original = xtce.VerifierSet(
            transferred_to_range_verifier=xtce.TransferredToRangeVerifier(
                name="Transferred",
                verifier=make_parameter_value_change(),
                check_window=make_check_window(),
            ),
            sent_from_range_verifier=xtce.SentFromRangeVerifier(
                name="Sent",
                verifier=make_parameter_value_change(),
                check_window=make_check_window(),
            ),
            received_verifier=xtce.ReceivedVerifier(
                name="Received",
                verifier=make_parameter_value_change(),
                check_window=make_check_window(),
            ),
            accepted_verifier=xtce.AcceptedVerifier(
                name="Accepted",
                verifier=make_parameter_value_change(),
                check_window=make_check_window(),
            ),
            queued_verifier=xtce.QueuedVerifier(
                name="Queued",
                verifier=make_parameter_value_change(),
                check_window=make_check_window(),
            ),
            execution_verifiers=[
                xtce.ExecutionVerifier(
                    name="Executing",
                    verifier=make_parameter_value_change(),
                    check_window=make_check_window(),
                    percent_complete=66.0,
                )
            ],
            complete_verifiers=[
                xtce.CompleteVerifier(
                    name="Complete",
                    verifier=make_parameter_value_change(),
                    check_window=make_check_window(),
                    return_parm_ref=make_parameter_ref(),
                )
            ],
            failed_verifier=xtce.FailedVerifier(
                name="Failed",
                verifier=make_parameter_value_change(),
                check_window=make_check_window(),
                return_parm_ref=make_parameter_ref(),
            ),
        )

        round_tripped = xtce.VerifierSet.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    def test_from_xsdata_v1_3_accepts_empty_optional_fields(self) -> None:
        """Import should handle a v1.3 verifier set where all optional fields are empty."""
        raw_obj = xtce_1_3.VerifierSetType()

        model = xtce.VerifierSet.from_xsdata(raw_obj, XtceVersion.V1_3)

        assert model.transferred_to_range_verifier is None
        assert model.sent_from_range_verifier is None
        assert model.received_verifier is None
        assert model.accepted_verifier is None
        assert model.queued_verifier is None
        assert model.execution_verifiers == []
        assert model.complete_verifiers == []
        assert model.failed_verifier is None

    def test_to_xsdata_rejects_v1_1(self) -> None:
        """v1.1 export should fail for VerifierSet."""
        model = xtce.VerifierSet()

        with pytest.raises(XtceUnsupportedError):
            model.to_xsdata(XtceVersion.V1_1)
