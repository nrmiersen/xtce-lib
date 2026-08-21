"""Model type aliases intended for internal use."""

from typing import Annotated

from pydantic import StringConstraints

XtceHexString = Annotated[str, StringConstraints(pattern=r"^0[xX][0-9a-fA-F]+$")]
XtceHexOrInt = int | XtceHexString
