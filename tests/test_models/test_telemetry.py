"""Test telemetry models."""

from __future__ import annotations

import pytest

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


def _container_ref() -> XtcePath:
    return XtcePath("/TestSystem/ContainerA")


def _make_comparison(value: object = 21) -> xtce.Comparison:
    """Build a reusable comparison for match criteria."""
    return xtce.Comparison(
        ref=_parameter_ref(),
        instance=0,
        use_calibrated_value=True,
        comparison_operator=xtce.ComparisonOperator.EQ,
        value=value,  # type: ignore[arg-type]
    )


def _make_match_criteria() -> xtce.MatchCriteria:
    """Build a reusable match criteria."""
    return xtce.MatchCriteria(criteria=_make_comparison())


class TestMessage:
    """Test Message model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal Message across all versions."""
        original = xtce.Message(
            name="MinorFrameMessage",
            match_criteria=_make_match_criteria(),
            container_ref=xtce.ContainerRef(ref=_container_ref()),
        )

        round_tripped = xtce.Message.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_descriptions(self, version: XtceVersion) -> None:
        """Round-trip Message with short and long descriptions."""
        original = xtce.Message(
            name="MinorFrameMessage",
            match_criteria=_make_match_criteria(),
            container_ref=xtce.ContainerRef(ref=_container_ref()),
            short_description="Minor frame 21",
            long_description="Packet container when minor frame ID equals 21.",
        )

        round_tripped = xtce.Message.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original


class TestMessageSet:
    """Test MessageSet model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal MessageSet."""
        original = xtce.MessageSet(name="TelemetryMessages")

        round_tripped = xtce.MessageSet.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_messages(self, version: XtceVersion) -> None:
        """Round-trip MessageSet containing messages."""
        original = xtce.MessageSet(
            name="TelemetryMessages",
            messages=[
                xtce.Message(
                    name="Msg1",
                    match_criteria=_make_match_criteria(),
                    container_ref=xtce.ContainerRef(ref=_container_ref()),
                ),
                xtce.Message(
                    name="Msg2",
                    match_criteria=xtce.MatchCriteria(criteria=_make_comparison(42)),
                    container_ref=xtce.ContainerRef(
                        ref=XtcePath("/TestSystem/ContainerB")
                    ),
                ),
            ],
        )

        round_tripped = xtce.MessageSet.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", MODERN_VERSIONS)
    def test_round_trip_with_descriptions_modern(self, version: XtceVersion) -> None:
        """Round-trip MessageSet with descriptions on modern versions."""
        original = xtce.MessageSet(
            name="TelemetryMessages",
            short_description="Set of telemetry messages",
            long_description="Contains all messages for telemetry services.",
            messages=[
                xtce.Message(
                    name="Msg1",
                    match_criteria=_make_match_criteria(),
                    container_ref=xtce.ContainerRef(ref=_container_ref()),
                )
            ],
        )

        round_tripped = xtce.MessageSet.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_v1_1_downgrade_policy_with_descriptions(self) -> None:
        """Test v1.1 rejects short_description under STRICT."""
        original = xtce.MessageSet(
            name="TelemetryMessages",
            short_description="Set of telemetry messages",
        )

        with pytest.raises(XtceDowngradeError):
            original.to_xsdata(XtceVersion.V1_1, policy=DowngradePolicy.STRICT)

        exported = original.to_xsdata(XtceVersion.V1_1, policy=DowngradePolicy.IGNORE)
        assert exported.name == "TelemetryMessages"


class TestTelemetryMetadata:
    """Test TelemetryMetadata model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal TelemetryMetadata."""
        original = xtce.TelemetryMetadata()

        round_tripped = xtce.TelemetryMetadata.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_full(self, version: XtceVersion) -> None:
        """Round-trip TelemetryMetadata with parameter types, parameters, containers, message set."""
        original = xtce.TelemetryMetadata(
            parameter_types=[
                xtce.IntegerParameter(name="VoltageType", encoding_type=None)
            ],
            parameters=[
                xtce.Parameter(
                    name="BatteryVoltage",
                    parameter_type_ref=XtcePath("VoltageType"),
                )
            ],
            containers=[
                xtce.SequenceContainer(
                    name="HkContainer",
                    entries=[xtce.ParameterRefEntry(parameter_ref=_parameter_ref())],
                )
            ],
            message_set=xtce.MessageSet(
                name="HkMessages",
                messages=[
                    xtce.Message(
                        name="HkMsg",
                        match_criteria=_make_match_criteria(),
                        container_ref=xtce.ContainerRef(ref=XtcePath("HkContainer")),
                    )
                ],
            ),
        )

        round_tripped = xtce.TelemetryMetadata.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original
