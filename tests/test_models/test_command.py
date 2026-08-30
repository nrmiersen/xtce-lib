"""Test command models."""

from __future__ import annotations

import datetime

import pytest
from pydantic import ValidationError

from xtce_lib import (
    DowngradePolicy,
    XtceDowngradeError,
    XtcePath,
    XtceVersion,
    xtce,
)

ALL_VERSIONS = [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3]
MODERN_VERSIONS = [XtceVersion.V1_2, XtceVersion.V1_3]


def _parameter_ref() -> XtcePath:
    return XtcePath("/TestSystem/ParameterA")


def _meta_command_ref() -> XtcePath:
    return XtcePath("/TestSystem/BaseCommand")


def _make_comparison(value: object = 1) -> xtce.Comparison:
    """Build a reusable comparison for match criteria."""
    return xtce.Comparison(
        ref=_parameter_ref(),
        instance=1,
        use_calibrated_value=True,
        comparison_operator=xtce.ComparisonOperator.EQ,
        value=value,  # type: ignore[arg-type]
    )


def _make_context_match() -> xtce.ContextMatch:
    """Build a reusable context match."""
    return xtce.ContextMatch(criteria=_make_comparison())


class TestArgument:
    """Test Argument model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal Argument."""
        original = xtce.Argument(
            name="Arg1",
            argument_type_ref=XtcePath("/TestSystem/ArgType"),
        )

        round_tripped = xtce.Argument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    @pytest.mark.parametrize(
        "initial_value",
        [
            42,
            3.14,
            "VAL",
            True,
            b"\xca\xfe",
            datetime.timedelta(seconds=15),
            datetime.datetime(2026, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc),
        ],
    )
    def test_round_trip_initial_values(
        self, version: XtceVersion, initial_value: object
    ) -> None:
        """Round-trip Argument with various scalar initial values."""
        original = xtce.Argument(
            name="ArgWithInit",
            argument_type_ref=XtcePath("/TestSystem/ArgType"),
            initial_value=initial_value,  # type: ignore[arg-type]
        )

        round_tripped = xtce.Argument.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestArgumentAssignment:
    """Test ArgumentAssignment model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    @pytest.mark.parametrize(
        "value",
        [
            100,
            2.5,
            "ON",
            True,
            b"\xca\xfe",
            datetime.timedelta(seconds=30),
            datetime.datetime(2026, 6, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
        ],
    )
    def test_round_trip_values(self, version: XtceVersion, value: object) -> None:
        """Round-trip ArgumentAssignment with various value types."""
        original = xtce.ArgumentAssignment(
            name=XtcePath("ArgName"),
            value=value,  # type: ignore[arg-type]
        )

        round_tripped = xtce.ArgumentAssignment.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestBaseMetaCommand:
    """Test BaseMetaCommand model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal BaseMetaCommand."""
        original = xtce.BaseMetaCommand(
            meta_command_ref=_meta_command_ref(),
        )

        round_tripped = xtce.BaseMetaCommand.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_assignments(self, version: XtceVersion) -> None:
        """Round-trip BaseMetaCommand with argument assignments."""
        original = xtce.BaseMetaCommand(
            meta_command_ref=_meta_command_ref(),
            argument_assignments=[
                xtce.ArgumentAssignment(name=XtcePath("Mode"), value="SAFE"),
                xtce.ArgumentAssignment(name=XtcePath("Retries"), value=3),
            ],
        )

        round_tripped = xtce.BaseMetaCommand.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestTransmissionConstraint:
    """Test TransmissionConstraint model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal TransmissionConstraint."""
        original = xtce.TransmissionConstraint(
            criteria=_make_comparison(),
        )

        round_tripped = xtce.TransmissionConstraint.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_full(self, version: XtceVersion) -> None:
        """Round-trip TransmissionConstraint with timeout and suspendable."""
        original = xtce.TransmissionConstraint(
            criteria=_make_comparison(),
            timeout=datetime.timedelta(seconds=10),
            suspendable=True,
        )

        round_tripped = xtce.TransmissionConstraint.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_round_trip_v1_3_with_argument_restrictions(self) -> None:
        """Round-trip TransmissionConstraint with argument restrictions in v1.3."""
        original = xtce.TransmissionConstraint(
            criteria=_make_comparison(),
            argument_restrictions=[
                xtce.ArgumentAssignment(name=XtcePath("Mode"), value="OPERATIONAL")
            ],
        )

        round_tripped = xtce.TransmissionConstraint.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original

    @pytest.mark.parametrize(
        "version", [XtceVersion.V1_1, XtceVersion.V1_2]
    )
    def test_downgrade_policy_with_argument_restrictions(
        self, version: XtceVersion
    ) -> None:
        """Test v1.1 and v1.2 reject argument_restrictions under STRICT."""
        tc = xtce.TransmissionConstraint(
            criteria=_make_comparison(),
            argument_restrictions=[
                xtce.ArgumentAssignment(name=XtcePath("Mode"), value="OPERATIONAL")
            ],
        )

        with pytest.raises(XtceDowngradeError):
            tc.to_xsdata(version, policy=DowngradePolicy.STRICT)

        exported = tc.to_xsdata(version, policy=DowngradePolicy.IGNORE)
        assert exported is not None


class TestSignificance:
    """Test Significance model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal Significance."""
        original = xtce.Significance()

        round_tripped = xtce.Significance.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_critical(self, version: XtceVersion) -> None:
        """Round-trip Significance with CRITICAL level."""
        original = xtce.Significance(
            space_system_at_risk=XtcePath("/TestSystem"),
            reason_for_warning="Irreversible thruster burn",
            consequence_level=xtce.ConsequenceLevel.CRITICAL,
        )

        round_tripped = xtce.Significance.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", MODERN_VERSIONS)
    def test_round_trip_vital_modern(self, version: XtceVersion) -> None:
        """Round-trip Significance with VITAL level in v1.2/v1.3."""
        original = xtce.Significance(
            consequence_level=xtce.ConsequenceLevel.VITAL,
        )

        round_tripped = xtce.Significance.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_v1_1_downgrade_policy_unsupported_consequence(self) -> None:
        """Test v1.1 rejects unsupported consequence level under STRICT."""
        sig = xtce.Significance(consequence_level=xtce.ConsequenceLevel.VITAL)

        with pytest.raises(XtceDowngradeError):
            sig.to_xsdata(XtceVersion.V1_1, policy=DowngradePolicy.STRICT)

        exported = sig.to_xsdata(XtceVersion.V1_1, policy=DowngradePolicy.IGNORE)
        assert exported is not None


class TestContextSignificance:
    """Test ContextSignificance model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip ContextSignificance."""
        original = xtce.ContextSignificance(
            context_match=_make_context_match(),
            significance=xtce.Significance(
                reason_for_warning="Context warning",
                consequence_level=xtce.ConsequenceLevel.CRITICAL,
            ),
        )

        round_tripped = xtce.ContextSignificance.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestInterlock:
    """Test Interlock model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal Interlock."""
        original = xtce.Interlock()

        round_tripped = xtce.Interlock.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_full(self, version: XtceVersion) -> None:
        """Round-trip full Interlock."""
        original = xtce.Interlock(
            scope_to_space_system=XtcePath("/TestSystem"),
            verification_to_wait_for=xtce.VerifierType.EXECUTING,
            verification_progress_percentage=75.5,
            suspendable=True,
        )

        round_tripped = xtce.Interlock.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestParameterToSet:
    """Test ParameterToSet model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal ParameterToSet."""
        original = xtce.ParameterToSet(
            ref=_parameter_ref(),
        )

        round_tripped = xtce.ParameterToSet.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_new_value(self, version: XtceVersion) -> None:
        """Round-trip ParameterToSet with string new value."""
        original = xtce.ParameterToSet(
            ref=_parameter_ref(),
            derivation_or_new_value="100",
            set_on_verification=xtce.VerifierType.COMPLETE,
        )

        round_tripped = xtce.ParameterToSet.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestParameterToSuspendAlarmsOn:
    """Test ParameterToSuspendAlarmsOn model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip ParameterToSuspendAlarmsOn."""
        original = xtce.ParameterToSuspendAlarmsOn(
            ref=_parameter_ref(),
            suspense_time=datetime.timedelta(seconds=12),
            verifier_to_trigger_on=xtce.VerifierType.ACCEPTED,
        )

        round_tripped = xtce.ParameterToSuspendAlarmsOn.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestMetaCommand:
    """Test MetaCommand model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal MetaCommand."""
        original = xtce.MetaCommand(name="ArmLaser")

        round_tripped = xtce.MetaCommand.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_arguments(self, version: XtceVersion) -> None:
        """Round-trip MetaCommand with arguments."""
        original = xtce.MetaCommand(
            name="SetPower",
            arguments=[
                xtce.Argument(
                    name="Level",
                    argument_type_ref=XtcePath("/TestSystem/PowerLevelType"),
                    initial_value=50,
                )
            ],
            system_name="POWER_SYS",
            abstract=False,
        )

        round_tripped = xtce.MetaCommand.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_constraints_and_significance(
        self, version: XtceVersion
    ) -> None:
        """Round-trip MetaCommand with constraints, significance, interlock, parameters_to_set."""
        original = xtce.MetaCommand(
            name="FireThruster",
            transmission_constraints=[
                xtce.TransmissionConstraint(
                    criteria=_make_comparison(),
                    timeout=datetime.timedelta(seconds=5),
                )
            ],
            default_significance=xtce.Significance(
                consequence_level=xtce.ConsequenceLevel.CRITICAL,
                reason_for_warning="Thruster firing",
            ),
            context_significance=[
                xtce.ContextSignificance(
                    context_match=_make_context_match(),
                    significance=xtce.Significance(
                        consequence_level=xtce.ConsequenceLevel.CRITICAL
                    ),
                )
            ],
            interlock=xtce.Interlock(
                verification_to_wait_for=xtce.VerifierType.COMPLETE,
            ),
            parameters_to_set=[
                xtce.ParameterToSet(
                    ref=_parameter_ref(),
                    derivation_or_new_value="ACTIVE",
                )
            ],
            parameters_to_suspend_alarms_on=[
                xtce.ParameterToSuspendAlarmsOn(
                    ref=_parameter_ref(),
                    suspense_time=datetime.timedelta(seconds=10),
                )
            ],
        )

        round_tripped = xtce.MetaCommand.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_command_container(
        self, version: XtceVersion
    ) -> None:
        """Round-trip MetaCommand with CommandContainer."""
        original = xtce.MetaCommand(
            name="CommandWithContainer",
            command_container=xtce.CommandContainer(
                name="CmdContainer",
                entries=[
                    xtce.ArgumentFixedValueEntry(
                        binary_value=b"\x12\x34", size_in_bits=16
                    )
                ],
            ),
        )

        round_tripped = xtce.MetaCommand.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestMetaCommandRef:
    """Test MetaCommandRef model."""

    def test_string_representation(self) -> None:
        """MetaCommandRef formats name as string."""
        ref = xtce.MetaCommandRef(name=XtcePath("/TestSystem/CommandA"))
        assert str(ref) == "/TestSystem/CommandA"

    def test_rejects_empty_name(self) -> None:
        """MetaCommandRef rejects invalid paths."""
        with pytest.raises(ValidationError):
            xtce.MetaCommandRef(name=XtcePath(""))


class TestMetaCommandStep:
    """Test MetaCommandStep model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip MetaCommandStep with argument assignments."""
        original = xtce.MetaCommandStep(
            meta_command_ref=_meta_command_ref(),
            argument_assignments=[
                xtce.ArgumentAssignment(name=XtcePath("Power"), value=100)
            ],
        )

        round_tripped = xtce.MetaCommandStep.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestBlockMetaCommand:
    """Test BlockMetaCommand model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip BlockMetaCommand with steps."""
        original = xtce.BlockMetaCommand(
            name="DeploySequence",
            meta_command_steps=[
                xtce.MetaCommandStep(
                    meta_command_ref=_meta_command_ref(),
                    argument_assignments=[
                        xtce.ArgumentAssignment(name=XtcePath("Step"), value=1)
                    ],
                ),
                xtce.MetaCommandStep(
                    meta_command_ref=_meta_command_ref(),
                    argument_assignments=[
                        xtce.ArgumentAssignment(name=XtcePath("Step"), value=2)
                    ],
                ),
            ],
        )

        round_tripped = xtce.BlockMetaCommand.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original


class TestCommandMetadata:
    """Test CommandMetadata model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal CommandMetadata."""
        original = xtce.CommandMetadata()

        round_tripped = xtce.CommandMetadata.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_items(self, version: XtceVersion) -> None:
        """Round-trip CommandMetadata with parameter types, parameters, argument types, meta commands."""
        original = xtce.CommandMetadata(
            parameter_types=[
                xtce.IntegerParameter(name="CmdParamType", encoding_type=None)
            ],
            parameters=[
                xtce.Parameter(
                    name="CmdParam",
                    parameter_type_ref=XtcePath("CmdParamType"),
                )
            ],
            argument_types=[
                xtce.IntegerArgument(name="CmdArgType", encoding_type=None)
            ],
            meta_commands=[
                xtce.MetaCommand(name="CommandA"),
                xtce.BlockMetaCommand(
                    name="BlockCmd",
                    meta_command_steps=[
                        xtce.MetaCommandStep(
                            meta_command_ref=XtcePath("CommandA")
                        )
                    ],
                ),
                xtce.MetaCommandRef(name=XtcePath("CommandA")),
            ],
            containers=[
                xtce.SequenceContainer(
                    name="SharedContainer",
                    entries=[
                        xtce.ParameterRefEntry(parameter_ref=_parameter_ref())
                    ],
                ),
            ],
        )

        round_tripped = xtce.CommandMetadata.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original
