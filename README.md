# xtce-lib

[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Development Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://img.shields.io/badge/status-alpha-orange.svg)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Package Manager](https://img.shields.io/badge/package%20manager-uv-blueviolet.svg)](https://docs.astral.sh/uv/)

`xtce-lib` is a Python library for creating, reading, validating, and converting XTCE databases.

**Alpha software:** the API is not stable yet and may change in future releases.

## Supported Versions

`xtce-lib` currently supports XTCE versions [`1.1`](https://www.omg.org/spec/XTCE/1.1/), [`1.2`](https://www.omg.org/spec/XTCE/1.2/), and [`1.3`](https://www.omg.org/spec/XTCE/1.3/).

## Installation

From PyPI:
```bash
pip install xtce-lib==0.1.0a5
```

## Documentation

See the [website](https://xtce-lib.readthedocs.io/en/latest/).

## Development Roadmap
- [x] Write a class to represent XTCE object paths (`XtcePath`)
- [x] Generate Python representations of the XML schemas with `xsdata`
- [x] Write a class to represent an XTCE file (`XtceFile`)
- [x] Write a class to represent the unified XTCE model (`XtceDatabase`)
- [x] Scaffold the structure of the unified XTCE model
- [x] Implement all base subclasses in the unified model, including translation methods
- [x] Refactor translation methods for inherited classes
- [x] Implement unified model serialization and deserialization
- [x] Release alpha
- [ ] Update models (better docstrings and better validation)
  - [ ] Algorithm models
  - [ ] Array models
  - [ ] Calibrator models
  - [ ] Common models
  - [ ] Condition models
  - [ ] Range models
  - [ ] Reference models
  - [ ] Stream models
  - [ ] Time models
  - [ ] Trigger models
  - [ ] Verifier models
  - [ ] Alarm models
  - [ ] Codec models
  - [ ] Datatype models
  - [ ] Argument models
  - [ ] Container models
  - [ ] Command models
  - [ ] Parameter models
  - [ ] Telemetry models
  - [ ] Space system
  - [ ] Enum models
- [ ] Fix the many things I messed up in the alpha
- [ ] Fix unit tests
- [ ] Implement full model semantic validation
- [ ] Write end-to-end tests for generating and parsing XTCE files
- [ ] Write documentation
  - [ ] Add examples to all applicable model Fields
  - [x] Automate API documentation generation

## Disclaimer
This project is an independent open-source implementation and is not affiliated with, endorsed by, or sponsored by the Object Management Group (OMG). XTCE is a specification developed by OMG. All trademarks are the property of their respective owners.
