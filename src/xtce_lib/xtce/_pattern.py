"""Regex pattern constants."""

# xtce:NameReferenceNoPathType
NAME_REF_NO_PATH = r"[^.\[\]:/ \t]+"

# xtce:ExpandedNameReferenceNoPathType
EXPD_NAME_REF_NO_PATH = (
    r"([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)"
)

# xtce:NameReferenceWithPathType
NAME_REF_W_PATH = r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"

# xtce:ExpandedNameReferenceWithPathType
EXPD_NAME_REF_W_PATH = r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*"
