# Unified XTCE Model

The unified model is a superset of the contents of XTCE versions 1.1, 1.2 and 1.3. Start with `SpaceSystem` and its metadata, then browse the model reference by domain using the navigation.

```python
from xtce_lib import xtce
```

Version badges show which XTCE versions a model can be converted to directly. Green indicates the model can be converted to that target version. Red indicates that conversion raises `XtceUnsupportedError`. Some fields or nested models may have additional restrictions. See [XTCE version compatibility](../xtce-version-compatibility.md) for export options and errors.

## Model Reference

- [Parameters](xtce/parameters.md): telemetry parameters and their properties.
- [Commands and Arguments](xtce/commands.md) and [Command Verification](xtce/verification.md): command definitions and verification.
- [Containers](xtce/containers.md): telemetry and command container entries.
- [Data Types](xtce/data-types.md) and [Data Encodings](xtce/encodings.md): value types and their binary representations.
- [Calibration](xtce/calibration.md) and [Alarms](xtce/alarms.md): conversions and alarm definitions.
- [Conditions and Ranges](xtce/conditions.md): matching, comparisons and valid values.
- [Algorithms and Triggers](xtce/algorithms.md): calculations and execution triggers.
- [Streams and Messages](xtce/streams.md): streams, framing and messages.
- [References and Time](xtce/references.md): references and time associations.
- [Common Utilities](xtce/common.md): shared utilities.
- [Enumerations](xtce/enums.md): values used throughout the model.

## Space System and Metadata

::: xtce_lib.xtce
    options:
      show_root_heading: false
      show_root_toc_entry: false
      members_order: source
      members:
        - SpaceSystem
        - Header
        - TelemetryMetadata
        - CommandMetadata
        - Service
        - MessageRef
        - Alias
        - AncillaryData
