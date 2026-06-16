"""XTCE version information."""

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class XtceVersionInfo:
    """Metadata for a specific XTCE version."""

    version: str
    namespace: str
    module_name: str
    xsd_name: str


class XtceVersion(Enum):
    """Supported XTCE schema versions."""

    V1_1 = XtceVersionInfo(
        version="1.1",
        namespace="http://www.omg.org/space/xtce",
        module_name="xtce_1_1",
        xsd_name="dtc-06-11-06.xsd",
    )
    V1_2 = XtceVersionInfo(
        version="1.2",
        namespace="http://www.omg.org/spec/XTCE/20180204",
        module_name="xtce_1_2",
        xsd_name="dtc-18-02-04.xsd",
    )
    V1_3 = XtceVersionInfo(
        version="1.3",
        namespace="http://www.omg.org/spec/XTCE/20250214",
        module_name="xtce_1_3",
        xsd_name="dtc-25-02-18.xsd",
    )

    @classmethod
    def from_namespace(cls, namespace: str) -> "XtceVersion":
        """Get the XtceVersion enum member from a namespace URI."""
        for ext_version in cls:
            if ext_version.value.namespace == namespace:
                return ext_version
        raise ValueError(f"Unsupported XTCE namespace: {namespace}")
