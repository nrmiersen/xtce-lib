"""Container models."""

from .common import NameDescriptionBase


class ContainerType(NameDescriptionBase):
    pass


class SequenceContainer(ContainerType):
    entries: None
    base_container: None
    abstract: bool
    idle_pattern: None
