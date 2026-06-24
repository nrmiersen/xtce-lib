"""Defines the XtcePath class, a pathlib-like object for handling XTCE SpaceSystem
hierarchies.
"""

import re
from dataclasses import dataclass
from typing import Any

from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

from xtce_lib.xtce._pattern import EXPD_NAME_REF_W_PATH


@dataclass(frozen=True)
class PathNode:
    """Represents a single node in an XTCE path."""

    raw: str
    base: str
    indices: tuple[int, ...] = ()
    member: "PathNode | None" = None

    # Group 1: base name (everything up to first [ or .)
    # Group 2: all brackets combined (e.g., "[0][1]")
    # Group 4: the remainder of the string after the first dot
    _NODE_PATTERN = re.compile(r"^([^\[\.]+)((\[\d+\])*)(?:\.(.+))?$")

    # Extracts individual integers from the bracket string
    _INDEX_PATTERN = re.compile(r"\[(\d+)\]")

    @classmethod
    def from_string(cls, raw_segment: str) -> "PathNode":
        """Parse a raw path segment into a PathNode."""
        if raw_segment in (".", ".."):
            return cls(raw=raw_segment, base=raw_segment)

        match = cls._NODE_PATTERN.match(raw_segment)
        if not match:
            return cls(raw=raw_segment, base=raw_segment)

        base_name = match.group(1)
        brackets_str = match.group(2)
        member_remainder = match.group(4)

        # Parse all indices
        parsed_indices = tuple(
            int(m.group(1)) for m in cls._INDEX_PATTERN.finditer(brackets_str)
        )

        # Parse all aggregate members
        parsed_member = None
        if member_remainder:
            parsed_member = cls.from_string(member_remainder)

        return cls(
            raw=raw_segment,
            base=base_name,
            indices=parsed_indices,
            member=parsed_member,
        )

    @property
    def is_array(self) -> bool:
        """Return True if this node has any array indices."""
        return len(self.indices) > 0

    @property
    def is_aggregate(self) -> bool:
        """Return True if this node has a member (i.e., is an aggregate)."""
        return self.member is not None

    @property
    def contains_array(self) -> bool:
        """Return True if this node or any of its members is an array."""
        if self.is_array:
            return True
        if self.member:
            return self.member.contains_array
        return False

    @property
    def contains_aggregate(self) -> bool:
        """Return True if this node or any of its members is an aggregate."""
        if self.is_aggregate:
            return True
        if self.member:
            return self.member.contains_aggregate
        return False

    def __str__(self) -> str:
        """Return the string representation of this node."""
        return self.raw


class XtcePath:
    """A pathlib-like object specifically for XTCE SpaceSystem hierarchies."""

    def __init__(self, path: "str | XtcePath | PathNode"):
        """Initialize a normalized XTCE path from a string, another XtcePath, or a PathNode.

        Multiple consecutive '/'s are treated as one.
        """
        if isinstance(path, XtcePath):
            self._parts: tuple[PathNode, ...] = path.parts
            self._is_absolute = path.is_absolute()
        elif isinstance(path, PathNode):
            self._is_absolute = False
            self._parts = (path,)
        else:
            self._is_absolute = path.startswith("/")
            clean_path = path.strip("/")
            self._parts: tuple[PathNode, ...] = tuple(
                PathNode.from_string(p) for p in clean_path.split("/") if p
            )

    @staticmethod
    def _to_parts(path: "str | XtcePath | PathNode") -> tuple[PathNode, ...]:
        """Normalize input into path parts."""
        return path.parts if isinstance(path, XtcePath) else XtcePath(path).parts

    @property
    def parts(self) -> tuple[PathNode, ...]:
        """Returns the rigid tuple of path components."""
        return self._parts

    @property
    def name(self) -> str:
        """The final component (e.g., the Command name or Type name)."""
        return str(self._parts[-1]) if self._parts else ""

    @property
    def leaf(self) -> "PathNode | None":
        """The final PathNode component, or None for empty paths."""
        return self._parts[-1] if self._parts else None

    @property
    def parent(self) -> "XtcePath":
        """Returns a new XtcePath representing the parent SpaceSystem (directory)."""
        if not self._parts:
            return XtcePath("/" if self._is_absolute else ".")

        if len(self._parts) == 1:
            return XtcePath("/" if self._is_absolute else ".")

        prefix = "/" if self._is_absolute else ""
        return XtcePath(prefix + "/".join(str(p) for p in self._parts[:-1]))

    @property
    def parents(self) -> tuple["XtcePath", ...]:
        """Returns all ancestors, from closest parent up to root."""
        if not self._parts:
            return ()

        prefix = "/" if self._is_absolute else ""
        ancestors = [
            XtcePath(prefix + "/".join(str(p) for p in self._parts[:i]))
            for i in range(len(self._parts) - 1, 0, -1)
        ]

        terminal = XtcePath("/" if self._is_absolute else ".")
        if not ancestors or ancestors[-1] != terminal:
            ancestors.append(terminal)

        return tuple(ancestors)

    @property
    def is_root(self) -> bool:
        """True if this path has no parent packages."""
        return len(self._parts) <= 1

    def joinpath(self, *other: "str | XtcePath | PathNode") -> "XtcePath":
        """Join one or more path segments and return a new XtcePath."""
        parts = list(self._parts)
        is_absolute = self._is_absolute

        for segment in other:
            segment_path = XtcePath(segment)
            if segment_path.is_absolute():
                parts = list(segment_path.parts)
                is_absolute = True
            else:
                parts.extend(segment_path.parts)

        prefix = "/" if is_absolute else ""
        path_str = prefix + "/".join(str(p) for p in parts)
        if not path_str and not is_absolute:
            path_str = "."
        return XtcePath(path_str)

    def with_name(self, name: str) -> "XtcePath":
        """Return a new path with the final component replaced by name."""
        if not self._parts:
            msg = "XtcePath has no name"
            raise ValueError(msg)

        clean_name = name.strip("/")
        if not clean_name or "/" in clean_name:
            msg = "name must be a single non-empty path segment"
            raise ValueError(msg)

        prefix = "/" if self._is_absolute else ""
        return XtcePath(
            prefix + "/".join(str(p) for p in (*self._parts[:-1], clean_name))
        )

    def is_absolute(self) -> bool:
        """Return True if this path is absolute (i.e., starts with a slash)."""
        return self._is_absolute

    def relative_to(self, other: "str | XtcePath | PathNode") -> "XtcePath":
        """Return this path relative to other, or raise ValueError."""
        base_path = XtcePath(other)
        base_parts = base_path.parts
        if self._is_absolute != base_path.is_absolute():
            msg = f"{self} is not in the subpath of {base_path}"
            raise ValueError(msg)
        if self._parts[: len(base_parts)] != base_parts:
            msg = f"{self} is not in the subpath of {base_path}"
            raise ValueError(msg)
        suffix = "/".join(str(p) for p in self._parts[len(base_parts) :])
        return XtcePath(suffix or ".")

    def is_relative_to(self, other: "str | XtcePath | PathNode") -> bool:
        """Return True if this path is relative to other."""
        base_path = XtcePath(other)
        if self._is_absolute != base_path.is_absolute():
            return False
        base_parts = base_path.parts
        return self._parts[: len(base_parts)] == base_parts

    def normalize(self) -> "XtcePath":
        """Normalize '.' and '..' segments in the path."""
        resolved_parts: list[str] = []

        for part in self._parts:
            if str(part) == "..":
                if resolved_parts and resolved_parts[-1] != "..":
                    resolved_parts.pop()
                    if not resolved_parts and not self._is_absolute:
                        resolved_parts.append("..")
                elif not self._is_absolute:
                    resolved_parts.append(str(part))
                # For absolute paths at root, ".." is ignored
            elif str(part) == ".":
                # Skip current-directory references
                pass
            else:
                resolved_parts.append(str(part))

        prefix = "/" if self._is_absolute else ""
        path_str = prefix + "/".join(resolved_parts)
        if not path_str and not self._is_absolute:
            path_str = "."
        return XtcePath(path_str)

    def __str__(self) -> str:
        """Return the normalized XTCE path string."""
        if self._is_absolute:
            return "/" + "/".join(str(p) for p in self._parts) if self._parts else "/"
        return "/".join(str(p) for p in self._parts) if self._parts else "."

    def __repr__(self) -> str:
        """Return a debug-friendly representation of this path."""
        return f"XtcePath('{self.__str__()}')"

    def __truediv__(self, other: "str | XtcePath | PathNode | None") -> "XtcePath":
        """Support path composition with the / operator."""
        if other is None:
            return self
        return self.joinpath(other)

    def __eq__(self, other: object) -> bool:
        """Return True when two paths normalize to the same components."""
        if isinstance(other, XtcePath):
            return (
                self._parts == other._parts and self._is_absolute == other._is_absolute
            )
        if isinstance(other, str):
            return self == XtcePath(other)
        return False

    def __hash__(self) -> int:
        """Return a hash so XtcePath can be used as dictionary keys."""
        return hash((self._parts, self._is_absolute))

    def __fspath__(self) -> str:
        """Support os.fspath protocol for interoperability."""
        return str(self)

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: Any,
    ) -> core_schema.CoreSchema:
        """Hook for Pydantic to validate and serialize XtcePath values."""

        def validate(value: Any) -> "XtcePath":
            if isinstance(value, XtcePath):
                return value
            if isinstance(value, PathNode):
                return XtcePath(value)
            if isinstance(value, str):
                if not re.compile(EXPD_NAME_REF_W_PATH).fullmatch(value):
                    msg = "XtcePath must be a valid XTCE name reference path"
                    raise ValueError(msg)
                return XtcePath(value)

            msg = "XtcePath must be a string, PathNode, or XtcePath"
            raise ValueError(msg)

        return core_schema.no_info_plain_validator_function(
            validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda value: str(value),
                when_used="always",
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        core_schema_obj: core_schema.CoreSchema,
        handler: Any,
    ) -> JsonSchemaValue:
        """Represent XtcePath as a string with XTCE name-reference constraints."""
        return {
            "type": "string",
            "pattern": EXPD_NAME_REF_W_PATH,
        }
