"""Defines the XtcePath class, a pathlib-like object for handling XTCE SpaceSystem hierarchies."""


class XtcePath:
    """A pathlib-like object specifically for XTCE SpaceSystem hierarchies."""

    def __init__(self, path: "str | XtcePath"):
        """Initialize a normalized XTCE path from a string or another XtcePath."""
        if isinstance(path, XtcePath):
            self._parts = path.parts
            self._is_absolute = path.is_absolute()
        else:
            self._is_absolute = path.startswith("/")
            clean_path = path.strip("/")
            self._parts = tuple(p for p in clean_path.split("/") if p)

    @staticmethod
    def _to_parts(path: "str | XtcePath") -> tuple[str, ...]:
        """Normalize input into path parts."""
        return path.parts if isinstance(path, XtcePath) else XtcePath(path).parts

    @property
    def parts(self) -> tuple[str, ...]:
        """Returns the rigid tuple of path components."""
        return self._parts

    @property
    def name(self) -> str:
        """The final component (e.g., the Command name or Type name)."""
        return self._parts[-1] if self._parts else ""

    @property
    def parent(self) -> "XtcePath":
        """Returns a new XtcePath representing the parent SpaceSystem (directory)."""
        if not self._parts:
            return XtcePath("/" if self._is_absolute else ".")

        if len(self._parts) == 1:
            return XtcePath("/" if self._is_absolute else ".")

        prefix = "/" if self._is_absolute else ""
        return XtcePath(prefix + "/".join(self._parts[:-1]))

    @property
    def parents(self) -> tuple["XtcePath", ...]:
        """Returns all ancestors, from closest parent up to root."""
        if not self._parts:
            return ()

        prefix = "/" if self._is_absolute else ""
        ancestors = [
            XtcePath(prefix + "/".join(self._parts[:i]))
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

    def joinpath(self, *other: "str | XtcePath") -> "XtcePath":
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
        path_str = prefix + "/".join(parts)
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
        return XtcePath(prefix + "/".join((*self._parts[:-1], clean_name)))

    def is_absolute(self) -> bool:
        """Return True if this path is absolute (i.e., starts with a slash)."""
        return self._is_absolute

    def relative_to(self, other: "str | XtcePath") -> "XtcePath":
        """Return this path relative to other, or raise ValueError."""
        base_path = XtcePath(other)
        base_parts = base_path.parts
        if self._is_absolute != base_path.is_absolute():
            msg = f"{self} is not in the subpath of {base_path}"
            raise ValueError(msg)
        if self._parts[: len(base_parts)] != base_parts:
            msg = f"{self} is not in the subpath of {base_path}"
            raise ValueError(msg)
        suffix = "/".join(self._parts[len(base_parts) :])
        return XtcePath(suffix or ".")

    def is_relative_to(self, other: "str | XtcePath") -> bool:
        """Return True if this path is relative to other."""
        base_path = XtcePath(other)
        if self._is_absolute != base_path.is_absolute():
            return False
        base_parts = base_path.parts
        return self._parts[: len(base_parts)] == base_parts

    def as_posix(self) -> str:
        """Return the POSIX-style path string."""
        return str(self)

    def __str__(self) -> str:
        """Return the normalized XTCE path string."""
        if self._is_absolute:
            return "/" + "/".join(self._parts) if self._parts else "/"
        return "/".join(self._parts) if self._parts else "."

    def __repr__(self) -> str:
        """Return a debug-friendly representation of this path."""
        return f"XtcePath('{self.__str__()}')"

    def __truediv__(self, other: "str | XtcePath") -> "XtcePath":
        """Support path composition with the / operator."""
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
