"""Test SpaceSystem models."""

from __future__ import annotations

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


def _message_ref() -> XtcePath:
    return XtcePath("/TestSystem/MessageA")


class TestHeader:
    """Test Header model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal/default Header across all versions."""
        original = xtce.Header()

        round_tripped = xtce.Header.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_full(self, version: XtceVersion) -> None:
        """Round-trip full Header across all versions."""
        original = xtce.Header(
            authors=["Alice", "Bob"],
            notes=["Note 1", "Note 2"],
            history=["v1.0 initial", "v1.1 patch"],
            version="1.1.0",
            date="2026-08-29",
            classification="Unclassified",
            classification_instructions="None",
            validation_status=xtce.ValidationStatus.WORKING,
        )

        round_tripped = xtce.Header.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original


class TestMessageRef:
    """Test MessageRef model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip(self, version: XtceVersion) -> None:
        """Round-trip MessageRef across all versions."""
        original = xtce.MessageRef(ref=_message_ref())

        round_tripped = xtce.MessageRef.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_string_representation(self) -> None:
        """MessageRef string representation."""
        ref = xtce.MessageRef(ref=XtcePath("/Sys/Msg"))
        assert str(ref.ref) == "/Sys/Msg"

    def test_invalid_ref(self) -> None:
        """MessageRef rejects invalid path patterns."""
        with pytest.raises(ValidationError):
            xtce.MessageRef(ref=XtcePath(""))


class TestService:
    """Test Service model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal Service."""
        original = xtce.Service(name="TelemetryService")

        round_tripped = xtce.Service.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_message_refs(self, version: XtceVersion) -> None:
        """Round-trip Service with MessageRefs."""
        original = xtce.Service(
            name="MessageService",
            refs=[
                xtce.MessageRef(ref=XtcePath("/TestSystem/Msg1")),
                xtce.MessageRef(ref=XtcePath("/TestSystem/Msg2")),
            ],
        )

        round_tripped = xtce.Service.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_container_refs(self, version: XtceVersion) -> None:
        """Round-trip Service with ContainerRefs."""
        original = xtce.Service(
            name="ContainerService",
            refs=[
                xtce.ContainerRef(ref=XtcePath("/TestSystem/Container1")),
                xtce.ContainerRef(ref=XtcePath("/TestSystem/Container2")),
            ],
        )

        round_tripped = xtce.Service.from_xsdata(original.to_xsdata(version), version)

        assert round_tripped == original


class TestSpaceSystem:
    """Test SpaceSystem model."""

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_minimal(self, version: XtceVersion) -> None:
        """Round-trip minimal SpaceSystem."""
        original = xtce.SpaceSystem(name="Sat1")

        round_tripped = xtce.SpaceSystem.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_hierarchy_and_services(self, version: XtceVersion) -> None:
        """Round-trip SpaceSystem with header, services, and nested subsystem."""
        original = xtce.SpaceSystem(
            name="Satellite",
            header=xtce.Header(
                version="1.0",
                authors=["Flight Dynamics"],
            ),
            services=[
                xtce.Service(
                    name="HkService",
                    refs=[xtce.ContainerRef(ref=XtcePath("HkContainer"))],
                )
            ],
            space_systems=[
                xtce.SpaceSystem(
                    name="PowerSubsystem",
                    header=xtce.Header(version="0.1"),
                )
            ],
            operational_status="operational",
        )

        round_tripped = xtce.SpaceSystem.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", ALL_VERSIONS)
    def test_round_trip_with_metadata(self, version: XtceVersion) -> None:
        """Round-trip SpaceSystem with telemetry and command metadata."""
        original = xtce.SpaceSystem(
            name="Satellite",
            telemetry_metadata=xtce.TelemetryMetadata(
                parameter_types=[
                    xtce.IntegerParameter(name="VoltageType", encoding_type=None)
                ],
                parameters=[
                    xtce.Parameter(
                        name="BatteryVoltage",
                        parameter_type_ref=XtcePath("VoltageType"),
                    )
                ],
            ),
            command_metadata=xtce.CommandMetadata(
                meta_commands=[xtce.MetaCommand(name="RebootCommand")]
            ),
        )

        round_tripped = xtce.SpaceSystem.from_xsdata(
            original.to_xsdata(version), version
        )

        assert round_tripped == original

    def test_round_trip_v1_3_attributes(self) -> None:
        """Round-trip XTCE 1.3-specific attributes."""
        original = xtce.SpaceSystem(
            name="Sat1",
            system_type=xtce.SystemType.ASSET,
            asset_type="spacecraft",
            base="http://example.com/xtce",
        )

        round_tripped = xtce.SpaceSystem.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3), XtceVersion.V1_3
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", [XtceVersion.V1_1, XtceVersion.V1_2])
    def test_downgrade_policy_v1_3_attributes(self, version: XtceVersion) -> None:
        """Test v1.1 and v1.2 reject v1.3 attributes under STRICT."""
        ss = xtce.SpaceSystem(
            name="Sat1",
            system_type=xtce.SystemType.ASSET,
            asset_type="spacecraft",
            base="http://example.com/xtce",
        )

        with pytest.raises(XtceDowngradeError):
            ss.to_xsdata(version, policy=DowngradePolicy.STRICT)

        exported = ss.to_xsdata(version, policy=DowngradePolicy.IGNORE)
        assert exported.name == "Sat1"
