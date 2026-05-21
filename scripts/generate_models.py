"""Generate XTCE models from XSD files with xsdata."""

import subprocess
import sys
from pathlib import Path

XTCE_VERSIONS = {
    "1_1": "dtc-06-11-06.xsd",
    "1_2": "dtc-18-02-04.xsd",
    "1_3": "dtc-25-02-18.xsd",
}


def main() -> None:
    """Generate XTCE models for all supported versions."""
    project_root = Path(__file__).resolve().parent.parent
    src_dir = project_root / "src"
    config_path = project_root / ".xsdata.xml"

    for version, xsd_name in XTCE_VERSIONS.items():
        xsd_path = src_dir / "xtce_lib" / "xsd" / xsd_name
        package_name = f"xtce_lib.generated.xtce_{version}.models"

        print(f"\n[{version}] Generating models from {xsd_name}...")

        command = [
            "uv",
            "run",
            "xsdata",
            "generate",
            str(xsd_path),
            "--package",
            package_name,
            "--config",
            str(config_path),
        ]

        try:
            subprocess.run(command, cwd=src_dir, check=True)
            print(f"[{version}] Successfully generated {package_name}")
        except subprocess.CalledProcessError as e:
            print(
                f"\n[ERROR] Failed to generate models for XTCE {version}: {e}",
                file=sys.stderr,
            )
            sys.exit(1)


if __name__ == "__main__":
    main()
