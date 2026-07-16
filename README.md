# xtce-lib

[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Development Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://img.shields.io/badge/status-alpha-orange.svg)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Package Manager](https://img.shields.io/badge/package%20manager-uv-blueviolet.svg)](https://docs.astral.sh/uv/)

`xtce-lib` provides Python tools for working with XTCE databases.

It focuses on three pieces of functionality:

- A unified, Pythonic XTCE model that flattens version-specific XML structure into a cleaner API.
- XTCE file parsing and schema validation for XTCE 1.1, 1.2, and 1.3 documents.
- XTCE path and registry helpers for resolving references inside a database.

**Alpha software:** the API is not stable yet and may change in future releases.

## Supported Versions

`xtce-lib` currently supports XTCE versions [`1.1`](https://www.omg.org/spec/XTCE/1.1/), [`1.2`](https://www.omg.org/spec/XTCE/1.2/), and [`1.3`](https://www.omg.org/spec/XTCE/1.3/).

## Installation

From PyPI:
```bash
pip install xtce-lib
```

## Quick Start

### Create an XTCE model

```python
from xtce_lib import xtce

system = xtce.SpaceSystem(name="CONKSAT1")

system.command_metadata = xtce.CommandMetadata(
    argument_types=[
        xtce.IntegerArgument(
            name="uint32",
            encoding_type=xtce.IntegerDataEncoding(
                encoding=xtce.IntegerEncoding.UNSIGNED,
                size_in_bits=32,
            ),
            signed=False,
        ),
        xtce.FloatArgument(
            name="float32",
            encoding_type=xtce.FloatDataEncoding(
                encoding=xtce.FloatEncoding.IEEE754,
                size_in_bits=32,
            ),
        ),
    ],
)
```

The unified model removes XML-only intermediate nodes, so you can work with the model directly:

```python
for argument in system.command_metadata.argument_types:
    print(argument.name)
```

### Parse an XTCE file

```python
from pathlib import Path
from xtce_lib import XtceDatabase, XtceFile

xtce_file = XtceFile(Path("CONKSAT1-XTCE.xml"))
xtce_database: XtceDatabase = xtce_file.database
```

`XtceFile` can validate the XTCE against the XML schema and parse the XML into the unified `XtceDatabase` model.

### Work with object paths

```python
>>> from xtce_lib import XtcePath
>>> path = XtcePath("/CONKSAT1/BUS[2].BatteryVoltage")
>>> root_path = XtcePath("/CONKSAT1")
>>> path.relative_to(root_path)
XtcePath('BUS[2].BatteryVoltage')
>>> path.contains_array
True
>>> path.contains_aggregate
True
```

`XtcePath` is a pathlib-like helper for XTCE hierarchies, including support for array and aggregate objects.

## Development Roadmap
- [x] Write a class to represent XTCE object paths (`XtcePath`)
- [x] Generate Python representations of the XML schemas with `xsdata`
- [x] Write a class to represent an XTCE file (`XtceFile`)
- [x] Write a class to represent the unified XTCE model (`XtceDatabase`)
- [x] Scaffold the structure of the unified XTCE model
- [ ] Fully implement all subclasses in the unified model, including translation and validation methods
- [ ] Implement unified model serialization and deserialization
- [ ] Implement full model semantic validation
- [ ] Write end-to-end tests for generating and parsing XTCE files
