"""Defines the XTCE registry class, which manages a mapping of XTCE paths to objects."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from xtce_lib.common.xtce_path import XtcePath

if TYPE_CHECKING:
    from xtce_lib.xtce._type_aliases import ReferenceableXtceObject

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class ResolvedReference:
    """Represents a resolved XTCE reference."""

    path: XtcePath
    target: ReferenceableXtceObject


class XtceRegistry:
    """A registry for managing XTCE definitions by their full absolute paths."""

    def __init__(self):
        """Initialize an empty registry."""
        self._definitions: dict[XtcePath, ReferenceableXtceObject] = {}
        self._object_paths: dict[int, XtcePath] = {}

    def register(self, path: XtcePath, xtce_obj: ReferenceableXtceObject) -> None:
        """Register an XTCE object with its full absolute path."""
        if not path.is_absolute():
            raise ValueError(f"cannot register non-absolute path '{path}'")

        if path in self._definitions:
            log.warning("Overwriting definition for '%s'", path)

        self._definitions[path] = xtce_obj
        self._object_paths[id(xtce_obj)] = path

        log.debug(
            f"Registered [{path}] -> {type(xtce_obj).__name__}"
            f"{'(' + xtce_obj.name + ')' if xtce_obj.name else ''}"
        )

    def get_by_path(self, path: XtcePath) -> ReferenceableXtceObject:
        """Retrieve an XTCE object by its absolute path."""
        if not path.is_absolute():
            raise ValueError(f"cannot get object from non-absolute path '{path}'")

        xtce_obj = self._definitions.get(path)
        if xtce_obj is None:
            raise KeyError(f"no object registered at path '{path}'")
        return xtce_obj

    def get_path(self, xtce_obj: ReferenceableXtceObject) -> XtcePath:
        """Retrieve the absolute path of an XTCE object."""
        path = self._object_paths.get(id(xtce_obj))
        if path is None:
            raise KeyError(
                f"object not registered: {type(xtce_obj).__name__} "
                f"({hex(id(xtce_obj))})"
            )
        return path

    def resolve(self, path: XtcePath, scope: XtcePath) -> ResolvedReference:
        """Resolve a reference path relative to a given scope."""
        if path.is_absolute():
            # Absolute paths ignore the scope
            xtce_obj = self._definitions.get(path)
            if xtce_obj is not None:
                return ResolvedReference(path, xtce_obj)
            raise KeyError(f"failed to resolve absolute path '{path}'")

        if not scope.is_absolute():
            raise ValueError(f"scope must be absolute, got '{scope}'")

        current_scope = scope
        while True:
            candidate_path = (current_scope / path).resolve()

            target = self._definitions.get(candidate_path)
            if target is not None:
                return ResolvedReference(path=candidate_path, target=target)

            # Can't find the path in any scope
            if current_scope == XtcePath("/"):
                break

            # Doesn't exist in the current scope, move up to the parent scope
            current_scope = current_scope.parent

        raise KeyError(f"failed to resolve reference '{path}' from scope '{scope}'")
