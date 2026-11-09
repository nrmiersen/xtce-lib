# Exceptions

Raised when converting between XTCE versions. `DowngradePolicy` controls how features that the target version cannot represent are handled. See [XTCE version compatibility](../xtce-version-compatibility.md) for examples and policy details.

```python
from xtce_lib import DowngradePolicy, XtceDowngradeError, XtceUnsupportedError
```

::: xtce_lib.exceptions
    options:
      show_root_heading: false
      show_root_toc_entry: false
      merge_init_into_class: false
