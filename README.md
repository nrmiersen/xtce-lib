# xtce-lib
Library of XTCE tools.

# Development

## Generate models with xsdata
```sh
uv run xsdata generate <xsd-path> --package <model-path> --config .xsdata.xml
```

XTCE 1.1
```sh
uv run xsdata generate src/xtce_lib/xsd/dtc-06-11-06.xsd --package xtce_lib.generated.xtce_1_1.models --config .xsdata.xml
```

XTCE 1.2
```sh
uv run xsdata generate src/xtce_lib/xsd/dtc-18-02-04.xsd --package xtce_lib.generated.xtce_1_2.models --config .xsdata.xml
```

XTCE 1.3
```sh
uv run xsdata generate src/xtce_lib/xsd/dtc-25-02-18.xsd --package xtce_lib.generated.xtce_1_3.models --config .xsdata.xml
```
