"""Defines the XtcePath class, a pathlib-like object for handling XTCE SpaceSystem
hierarchies.
"""

import re
from dataclasses import dataclass, field
from typing import Any, Callable

from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


def require_regex(pattern: str) -> Callable[["XtcePath"], "XtcePath"]:
    """Create a validator that requires a path to match a regular expression.

    Args:
        pattern: Regular expression that must match the complete path string.

    Returns:
        A validator that returns matching paths unchanged.

    Raises:
        re.error: If pattern is not a valid regular expression.

    Examples:
        >>> validate = require_regex(r"/[A-Z]+")
        >>> validate(XtcePath("/BUS"))
        XtcePath('/BUS')

    """
    compiled = re.compile(pattern)

    def validator(path: XtcePath) -> XtcePath:
        if not compiled.fullmatch(str(path)):
            raise ValueError(f"XtcePath '{path}' must match pattern: '{pattern}'")
        return path

    return validator


@dataclass(frozen=True)
class PathNode:
    """Represents a single node in an XTCE path."""

    raw: str
    base: str
    indices: tuple[int, ...] = field(default_factory=tuple)
    member: "PathNode | None" = None

    # Group 1: base name (everything up to first [ or .)
    # Group 2: all brackets combined (e.g., "[0][1]")
    # Group 4: the remainder of the string after the first dot
    _NODE_PATTERN = re.compile(r"^([^\[\.]+)((\[\d+\])*)(?:\.(.+))?$")

    # Extracts individual integers from the bracket string
    _INDEX_PATTERN = re.compile(r"\[(\d+)\]")

    @classmethod
    def from_string(cls, raw_segment: str) -> "PathNode":
        """Parse a raw path segment into a PathNode.

        If the raw segment does not match the allowed pattern by XTCE, it will be
        treated as a base name without indices or members.

        Args:
            raw_segment (str): The raw string segment of the XTCE path to parse.

        Returns:
            PathNode: Parsed representation of the segment.

        Examples:
            >>> PathNode.from_string("CONKSAT-1")
            PathNode(raw='CONKSAT-1', base='CONKSAT-1', indices=(), member=None)

            >>> PathNode.from_string("foo[0].bar[1]")
            PathNode(raw='foo[0].bar[1]', base='foo', indices=(0,), member=PathNode(raw='bar[1]', base='bar', indices=(1,), member=None))

            >>> PathNode.from_string("BadNode[[]]")
            PathNode(raw='BadNode[[]]', base='BadNode[[]]', indices=(), member=None)

        """
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
        """Check if this node has any array indices.

        Returns:
            bool: True if this node has any array indices.

        Examples:
            >>> node = PathNode.from_string("foo[0]")
            >>> node.is_array
            True

            >>> node = PathNode.from_string("foo")
            >>> node.is_array
            False

        """
        return len(self.indices) > 0

    @property
    def is_aggregate(self) -> bool:
        """Check if this node has a member (i.e., is an aggregate).

        Returns:
            bool: True if this node has a member.

        Examples:
            >>> node = PathNode.from_string("foo.bar")
            >>> node.is_aggregate
            True

            >>> node = PathNode.from_string("foo")
            >>> node.is_aggregate
            False

        """
        return self.member is not None

    @property
    def contains_array(self) -> bool:
        """Check if this node or a nested member has array indices.

        Returns:
            bool: True if any part of the node contains array indexing.

        Examples:
            >>> PathNode.from_string("foo[0].bar").contains_array
            True
            >>> PathNode.from_string("foo.bar").contains_array
            False

        """
        if self.is_array:
            return True
        if self.member:
            return self.member.contains_array
        return False

    @property
    def contains_aggregate(self) -> bool:
        """Check if this node or a nested member has aggregate access.

        Returns:
            bool: True if any part of the node contains aggregate access.

        Examples:
            >>> PathNode.from_string("foo.bar").contains_aggregate
            True
            >>> PathNode.from_string("foo").contains_aggregate
            False

        """
        if self.is_aggregate:
            return True
        if self.member:
            return self.member.contains_aggregate
        return False

    def __str__(self) -> str:
        """Return the original segment text for this node.

        Returns:
            str: The unmodified segment text.

        """
        return self.raw


class XtcePath:
    """A pathlib-like object specifically for XTCE SpaceSystem hierarchies."""

    def __init__(self, path: "str | XtcePath | PathNode") -> None:
        """Initialize a normalized XTCE path from a string, another XtcePath, or a
        PathNode.

        Multiple consecutive '/'s are treated as one.

        Args:
            path (str | XtcePath | PathNode): The input path to normalize into an
                XtcePath.

        Raises:
            TypeError: If path is not a string, XtcePath, or PathNode.

        Examples:
            >>> XtcePath("foo/bar")
            XtcePath('foo/bar')

        """
        if isinstance(path, XtcePath):
            self._parts: tuple[PathNode, ...] = path.parts
            self._is_absolute = path.is_absolute()
        elif isinstance(path, PathNode):
            self._is_absolute = False
            self._parts = (path,)
        elif isinstance(path, str):
            self._is_absolute = path.startswith("/")
            clean_path = path.strip("/")
            self._parts = tuple(
                PathNode.from_string(part) for part in clean_path.split("/") if part
            )
        else:
            raise TypeError("path must be str, XtcePath, or PathNode")

    @property
    def parts(self) -> tuple[PathNode, ...]:
        """Returns the rigid tuple of path components.

        Returns:
            tuple[PathNode, ...]: Components in path order.

        Examples:
            >>> XtcePath("foo/bar").parts
            (PathNode(raw='foo', base='foo', indices=(), member=None), PathNode(raw='bar', base='bar', indices=(), member=None))

        """
        return self._parts

    @property
    def name(self) -> str:
        """The final component.

        Returns:
            str: Final component, or an empty string when there are no components.

        Examples:
            >>> XtcePath("foo/bar").name
            'bar'

            >>> XtcePath("foo/bar[0]").name
            'bar[0]'

        """
        return str(self._parts[-1]) if self._parts else ""

    @property
    def leaf(self) -> "PathNode | None":
        """The final PathNode component.

        Returns:
            PathNode | None: Final component, or None when there are no components.

        Examples:
            >>> XtcePath("foo/bar").leaf
            PathNode(raw='bar', base='bar', indices=(), member=None)

            >>> XtcePath("foo/bar[0]").leaf
            PathNode(raw='bar[0]', base='bar', indices=(0,), member=None)

        """
        return self._parts[-1] if self._parts else None

    @property
    def parent(self) -> "XtcePath":
        """Returns a new XtcePath representing the parent SpaceSystem.

        Returns:
            XtcePath: Immediate parent, or the root/current-directory path when this
                path has at most one component.

        Examples:
            >>> XtcePath("foo/bar").parent
            XtcePath('foo')

            >>> XtcePath("foo").parent
            XtcePath('.')

            >>> XtcePath("/foo").parent
            XtcePath('/')

        """
        if not self._parts:
            return XtcePath("/" if self._is_absolute else ".")

        if len(self._parts) == 1:
            return XtcePath("/" if self._is_absolute else ".")

        prefix = "/" if self._is_absolute else ""
        return XtcePath(prefix + "/".join(str(p) for p in self._parts[:-1]))

    @property
    def parents(self) -> tuple["XtcePath", ...]:
        """Returns all ancestors, from closest parent up to root.

        Returns:
            tuple[XtcePath, ...]: Ancestors ordered from nearest parent to root.

        Examples:
            >>> XtcePath("foo/bar").parents
            (XtcePath('foo'), XtcePath('.'))

            >>> XtcePath("foo").parents
            (XtcePath('.'),)

            >>> XtcePath("/foo").parents
            (XtcePath('/'),)

        """
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
        """Check whether this path has no parent packages.

        Returns:
            bool: True for paths with at most one component.

        Examples:
            >>> XtcePath("foo/bar").is_root
            False

            >>> XtcePath("foo").is_root
            True

            >>> XtcePath("/foo").is_root
            True

        """
        return len(self._parts) <= 1

    @property
    def contains_array(self) -> bool:
        """Check whether any path component contains array indexing.

        Returns:
            bool: Whether array indexing occurs anywhere in the path.

        Examples:
            >>> XtcePath("/Bus[0]/Temperature").contains_array
            True
            >>> XtcePath("/Bus/Temperature").contains_array
            False

        """
        return any(part.contains_array for part in self._parts)

    @property
    def contains_aggregate(self) -> bool:
        """Check whether any path component contains aggregate member access.

        Returns:
            bool: Whether aggregate access occurs anywhere in the path.

        Examples:
            >>> XtcePath("/Bus/Reading.value").contains_aggregate
            True
            >>> XtcePath("/Bus/Reading").contains_aggregate
            False

        """
        return any(part.contains_aggregate for part in self._parts)

    def joinpath(self, *other: "str | XtcePath | PathNode") -> "XtcePath":
        """Join path segments, replacing the path when a segment is absolute.

        Args:
            *other: String, XtcePath, or PathNode segments to append.

        Returns:
            XtcePath: The composed path.

        Examples:
            >>> XtcePath("/A").joinpath("B", "C")
            XtcePath('/A/B/C')
            >>> XtcePath("/A").joinpath("/B")
            XtcePath('/B')

        """
        parts = list(self._parts)
        is_absolute = self._is_absolute

        for segment in other:
            segment_path = XtcePath(segment)  # Handles input type checking
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
        """Return a copy of this path with its final component replaced.

        Args:
            name: Replacement component, without path separators.

        Returns:
            XtcePath: A path with the same parent and the new final component.

        Raises:
            ValueError: If this path is empty or name is not one non-empty segment.

        Examples:
            >>> XtcePath("/A/B").with_name("C")
            XtcePath('/A/C')

        """
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
        """Check whether this path starts at the absolute root.

        Returns:
            bool: Whether the input path began with a slash.

        Examples:
            >>> XtcePath("/A").is_absolute()
            True
            >>> XtcePath("A").is_absolute()
            False

        """
        return self._is_absolute

    def relative_to(self, other: "str | XtcePath | PathNode") -> "XtcePath":
        """Return the suffix remaining after removing a matching base path.

        Args:
            other: Base path to remove from this path.

        Returns:
            XtcePath: The relative suffix, or ``.`` when both paths are equal.

        Raises:
            ValueError: If the base is not a component-wise prefix or has different
                absolute/relative status.

        Examples:
            >>> XtcePath("/A/B/C").relative_to("/A/B")
            XtcePath('C')

        """
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
        """Check whether another path is a component-wise prefix of this path.

        Args:
            other: Candidate base path.

        Returns:
            bool: Whether the base matches and both paths have the same absolute or
                relative status.

        Examples:
            >>> XtcePath("/A/B").is_relative_to("/A")
            True
            >>> XtcePath("/A/B").is_relative_to("A")
            False

        """
        base_path = XtcePath(other)
        if self._is_absolute != base_path.is_absolute():
            return False
        base_parts = base_path.parts
        return self._parts[: len(base_parts)] == base_parts

    def normalize(self) -> "XtcePath":
        """Resolve current- and parent-directory components lexically.

        Returns:
            XtcePath: A path with redundant ``.`` and resolvable ``..`` components
                removed. Absolute paths do not traverse above root.

        Examples:
            >>> XtcePath("A/./B/../C").normalize()
            XtcePath('A/C')
            >>> XtcePath("/../A").normalize()
            XtcePath('/A')

        """
        resolved_parts: list[str] = []

        for part in self._parts:
            if str(part) == "..":
                if resolved_parts and resolved_parts[-1] != "..":
                    resolved_parts.pop()
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
        """Return the normalized XTCE path string.

        Returns:
            str: Slash-separated path, using ``.`` for an empty relative path and
                ``/`` for an empty absolute path.

        """
        if self._is_absolute:
            return "/" + "/".join(str(p) for p in self._parts) if self._parts else "/"
        return "/".join(str(p) for p in self._parts) if self._parts else "."

    def __repr__(self) -> str:
        """Return a debug representation of this path.

        Returns:
            str: Constructor-style representation containing the normalized path.

        """
        return f"XtcePath('{self.__str__()}')"

    def __truediv__(self, other: "str | XtcePath | PathNode | None") -> "XtcePath":
        """Compose a path with a segment using the ``/`` operator.

        Args:
            other: Segment to join, or None to leave this path unchanged.

        Returns:
            XtcePath: The composed path.

        Examples:
            >>> XtcePath("/A") / "B"
            XtcePath('/A/B')
            >>> XtcePath("/A") / None
            XtcePath('/A')

        """
        if other is None:
            return self
        return self.joinpath(other)

    def __eq__(self, other: object) -> bool:
        """Compare path components and absolute status.

        Args:
            other: Value to compare with this path.

        Returns:
            bool: Whether other is an equal XtcePath or an equivalent path string.

        """
        if isinstance(other, XtcePath):
            return (
                self._parts == other._parts and self._is_absolute == other._is_absolute
            )
        if isinstance(other, str):
            return self == XtcePath(other)
        return False

    def __hash__(self) -> int:
        """Return a hash consistent with path equality.

        Returns:
            int: Hash of the path components and absolute status.

        """
        return hash((self._parts, self._is_absolute))

    def __fspath__(self) -> str:
        """Return the path string for the ``os.PathLike`` protocol.

        Returns:
            str: Normalized path string.

        """
        return str(self)

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: Any,
    ) -> core_schema.CoreSchema:
        """Provide Pydantic validation and serialization for XtcePath."""

        def validate(value: Any) -> "XtcePath":
            if isinstance(value, XtcePath):
                return value
            if isinstance(value, PathNode):
                return XtcePath(value)
            if isinstance(value, str):
                return XtcePath(value)

            raise ValueError("XtcePath must be a string, PathNode, or XtcePath")

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
        """Describe XtcePath as a string in generated JSON Schema."""
        return {"type": "string"}
