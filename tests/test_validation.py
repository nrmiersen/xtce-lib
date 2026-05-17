"""Test validation."""

import xtce_lib as xtce

TEST_FILE = "/home/nrmiersen/xtce-generation/xtce_files/CONKSAT-1-XTCE.xml"
f = xtce.XtceFile(TEST_FILE)
validation_result = f.validate()
if not validation_result.is_valid:
    for error in validation_result.errors:
        print(f"Line {error.line}: {error.message}")
