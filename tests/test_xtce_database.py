"""Unit tests for XtceDatabase."""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from xtce_lib import (
    DowngradePolicy,
    XtceDatabase,
    XtceDowngradeError,
    XtceFile,
    XtcePath,
    XtceVersion,
    xtce,
)


def _make_sample_database() -> XtceDatabase:
    """Create a sample XtceDatabase with telemetry and command metadata."""
    db = XtceDatabase(name="Sat1")
    db.short_description = "Sat1 short description"
    db.long_description = "Sat1 long description"
    db.aliases = [xtce.Alias(namespace="Ground", alias="Satellite-1")]
    db.ancillary_data = [xtce.AncillaryData(name="Source", value="Test")]
    db.header = xtce.Header(
        version="1.0",
        authors=["Flight Dynamics Team"],
        notes=["Test DB Note"],
        history=["Initial release"],
        date="2026-08-29",
        classification="Unclassified",
        validation_status=xtce.ValidationStatus.WORKING,
    )

    # Telemetry metadata
    param_type = xtce.IntegerParameter(name="VoltageType", encoding_type=None)
    param = xtce.Parameter(
        name="BatteryVoltage", parameter_type_ref=XtcePath("VoltageType")
    )
    container = xtce.SequenceContainer(
        name="HkContainer",
        entries=[xtce.ParameterRefEntry(parameter_ref=XtcePath("BatteryVoltage"))],
    )
    msg = xtce.Message(
        name="HkMessage",
        match_criteria=xtce.MatchCriteria(
            criteria=xtce.Comparison(
                ref=XtcePath("BatteryVoltage"),
                comparison_operator=xtce.ComparisonOperator.EQ,
                value=1,
            )
        ),
        container_ref=xtce.ContainerRef(ref=XtcePath("HkContainer")),
    )
    msg_set = xtce.MessageSet(name="HkMessageSet", messages=[msg])

    db.telemetry_metadata = xtce.TelemetryMetadata(
        parameter_types=[param_type],
        parameters=[param],
        containers=[container],
        message_set=msg_set,
    )

    # Command metadata
    arg_type = xtce.IntegerArgument(name="PowerLevelType", encoding_type=None)
    cmd = xtce.MetaCommand(
        name="SetPower",
        arguments=[
            xtce.Argument(name="Level", argument_type_ref=XtcePath("PowerLevelType"))
        ],
    )
    block_cmd = xtce.BlockMetaCommand(
        name="PowerSequence",
        meta_command_steps=[
            xtce.MetaCommandStep(meta_command_ref=XtcePath("SetPower"))
        ],
    )

    db.command_metadata = xtce.CommandMetadata(
        argument_types=[arg_type],
        meta_commands=[cmd, block_cmd, xtce.MetaCommandRef(name=XtcePath("SetPower"))],
    )

    # Service
    db.services = [
        xtce.Service(
            name="HkService",
            refs=[xtce.ContainerRef(ref=XtcePath("HkContainer"))],
        )
    ]

    # Child SpaceSystem
    child = xtce.SpaceSystem(name="SubsystemA")
    child.telemetry_metadata = xtce.TelemetryMetadata(
        parameter_types=[xtce.FloatParameter(name="TempType", encoding_type=None)],
        parameters=[
            xtce.Parameter(name="SensorTemp", parameter_type_ref=XtcePath("TempType"))
        ],
    )
    db.space_systems = [child]

    return db


class TestXtceDatabase:
    """Unit tests for the XtceDatabase class."""

    def test_init_and_name_property(self) -> None:
        """Test constructor and name property getters/setters."""
        db = XtceDatabase(name="MySystem")
        assert db.name == "MySystem"
        assert db.root_system.name == "MySystem"

        db.name = "NewSystemName"
        assert db.name == "NewSystemName"
        assert db.root_system.name == "NewSystemName"

    def test_init_rejects_invalid_name(self) -> None:
        """Constructor validates name."""
        with pytest.raises(ValidationError):
            XtceDatabase(name="")  # type: ignore[arg-type]

    def test_from_space_system(self) -> None:
        """Test from_space_system factory method."""
        ss = xtce.SpaceSystem(name="ExistingSystem")
        db = XtceDatabase.from_space_system(ss)
        assert db.name == "ExistingSystem"
        assert db.root_system is ss

    def test_root_system_properties_passthrough(self) -> None:
        """Test that properties on XtceDatabase correctly proxy to the root SpaceSystem."""
        db = XtceDatabase(name="ProxyTest")

        # short_description / long_description
        assert db.short_description is None
        db.short_description = "Short desc"
        assert db.short_description == "Short desc"
        assert db.root_system.short_description == "Short desc"

        assert db.long_description is None
        db.long_description = "Long desc"
        assert db.long_description == "Long desc"
        assert db.root_system.long_description == "Long desc"

        # aliases
        assert db.aliases == []
        aliases = [xtce.Alias(namespace="Ground", alias="A1")]
        db.aliases = aliases
        assert db.aliases == aliases
        assert db.root_system.aliases == aliases

        # ancillary_data
        assert db.ancillary_data == []
        ancillary = [xtce.AncillaryData(name="key", value="val")]
        db.ancillary_data = ancillary
        assert db.ancillary_data == ancillary
        assert db.root_system.ancillary_data == ancillary

        # header
        assert db.header is None
        header = xtce.Header(version="2.0")
        db.header = header
        assert db.header == header
        assert db.root_system.header == header

        # telemetry_metadata
        assert db.telemetry_metadata is None
        tlm = xtce.TelemetryMetadata()
        db.telemetry_metadata = tlm
        assert db.telemetry_metadata == tlm
        assert db.root_system.telemetry_metadata == tlm

        # command_metadata
        assert db.command_metadata is None
        cmd = xtce.CommandMetadata()
        db.command_metadata = cmd
        assert db.command_metadata == cmd
        assert db.root_system.command_metadata == cmd

        # services
        assert db.services == []
        services = [xtce.Service(name="S1")]
        db.services = services
        assert db.services == services
        assert db.root_system.services == services

        # space_systems
        assert db.space_systems == []
        children = [xtce.SpaceSystem(name="Child1")]
        db.space_systems = children
        assert db.space_systems == children
        assert db.root_system.space_systems == children

        # system_type
        assert db.system_type == xtce.SystemType.UNKNOWN
        db.system_type = xtce.SystemType.ASSET
        assert db.system_type == xtce.SystemType.ASSET
        assert db.root_system.system_type == xtce.SystemType.ASSET

        # asset_type
        assert db.asset_type == "unknown"
        db.asset_type = "satellite"
        assert db.asset_type == "satellite"
        assert db.root_system.asset_type == "satellite"

        # operational_status
        assert db.operational_status is None
        db.operational_status = "active"
        assert db.operational_status == "active"
        assert db.root_system.operational_status == "active"

        # base
        assert db.base is None
        db.base = "http://example.com"
        assert db.base == "http://example.com"
        assert db.root_system.base == "http://example.com"

    def test_registry_indexing_and_rebuild(self) -> None:
        """Test registry indexing of root and child elements."""
        db = _make_sample_database()

        registry = db.registry
        assert registry is not None

        # Check root SpaceSystem is indexed
        assert registry.get_by_path(XtcePath("/Sat1")) is db.root_system

        # Check telemetry items
        assert registry.get_by_path(XtcePath("/Sat1/VoltageType")).name == "VoltageType"
        assert (
            registry.get_by_path(XtcePath("/Sat1/BatteryVoltage")).name
            == "BatteryVoltage"
        )
        assert registry.get_by_path(XtcePath("/Sat1/HkContainer")).name == "HkContainer"
        assert registry.get_by_path(XtcePath("/Sat1/HkMessage")).name == "HkMessage"

        # Check command items
        assert (
            registry.get_by_path(XtcePath("/Sat1/PowerLevelType")).name
            == "PowerLevelType"
        )
        assert registry.get_by_path(XtcePath("/Sat1/SetPower")).name == "SetPower"
        assert (
            registry.get_by_path(XtcePath("/Sat1/PowerSequence")).name
            == "PowerSequence"
        )

        # Check child space system and its items
        assert registry.get_by_path(XtcePath("/Sat1/SubsystemA")).name == "SubsystemA"
        assert (
            registry.get_by_path(XtcePath("/Sat1/SubsystemA/TempType")).name
            == "TempType"
        )
        assert (
            registry.get_by_path(XtcePath("/Sat1/SubsystemA/SensorTemp")).name
            == "SensorTemp"
        )

        # Rebuild registry after adding a new parameter
        db.telemetry_metadata.parameters.append(  # type: ignore[reportOptionalMemberAccess]
            xtce.Parameter(
                name="SolarArrayCurrent", parameter_type_ref=XtcePath("VoltageType")
            )
        )
        db.rebuild_registry()

        assert (
            db.registry.get_by_path(XtcePath("/Sat1/SolarArrayCurrent")).name
            == "SolarArrayCurrent"
        )

    def test_validate_returns_report(self) -> None:
        """Test validate returns a ValidationReport."""
        db = _make_sample_database()
        report = db.validate()
        assert report.title == "Semantic Validation"
        assert report.is_valid

    @pytest.mark.parametrize(
        "version", [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3]
    )
    def test_to_file_round_trip(self, tmp_path: Path, version: XtceVersion) -> None:
        """Test to_file writes a valid XML file that can be read back by XtceFile."""
        db = _make_sample_database()

        out_file = tmp_path / f"test_output_{version.name}.xml"
        xtce_file = db.to_file(
            out_file,
            xtce_version=version,
            downgrade_policy=DowngradePolicy.IGNORE,
        )

        assert isinstance(xtce_file, XtceFile)
        assert out_file.exists()
        assert out_file.stat().st_size > 0

        # Parse back through XtceFile
        read_db = xtce_file.database
        assert read_db.name == db.name
        assert read_db.root_system.name == db.root_system.name

    def test_to_file_downgrade_strict_raises(self, tmp_path: Path) -> None:
        """Test to_file raises XtceDowngradeError under STRICT policy when v1.3 fields are used with v1.1."""
        db = XtceDatabase(name="StrictTest")
        db.system_type = xtce.SystemType.ASSET

        out_file = tmp_path / "strict_fail.xml"
        with pytest.raises(XtceDowngradeError):
            db.to_file(
                out_file,
                xtce_version=XtceVersion.V1_1,
                downgrade_policy=DowngradePolicy.STRICT,
            )
