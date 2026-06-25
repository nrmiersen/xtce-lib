"""Comprehensive unit tests for XtceRegistry."""

from dataclasses import dataclass
from typing import cast

import pytest

from xtce_lib import ResolvedReference, XtcePath, XtceRegistry
from xtce_lib.xtce._type_aliases import ReferenceableXtceObject


@dataclass
class DummyXtceObject:
    """Stand-in object for registry tests."""

    name: str


def as_referenceable(obj: DummyXtceObject) -> ReferenceableXtceObject:
    """Return a test double cast to the registry's referenceable union."""
    return cast(ReferenceableXtceObject, obj)


def test_register_and_get_by_path_round_trip() -> None:
    """Registered objects should be retrievable by their absolute path."""
    registry = XtceRegistry()
    path = XtcePath("/A/B")
    target = DummyXtceObject(name="B")

    registry.register(path, as_referenceable(target))

    assert registry.get_by_path(path) is target


def test_register_rejects_relative_paths() -> None:
    """Register should reject non-absolute paths."""
    registry = XtceRegistry()

    with pytest.raises(ValueError, match=r"cannot register non-absolute path 'A/B'"):
        registry.register(XtcePath("A/B"), as_referenceable(DummyXtceObject(name="B")))


def test_register_overwrite_logs_warning_and_replaces_definition(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Registering a second object at the same path should overwrite it."""
    registry = XtceRegistry()
    path = XtcePath("/A/B")
    first = DummyXtceObject(name="first")
    second = DummyXtceObject(name="second")

    registry.register(path, as_referenceable(first))

    with caplog.at_level("WARNING"):
        registry.register(path, as_referenceable(second))

    assert registry.get_by_path(path) is second
    assert "Overwriting definition for '/A/B'" in caplog.text


def test_get_by_path_rejects_relative_paths() -> None:
    """get_by_path should only accept absolute paths."""
    registry = XtceRegistry()

    with pytest.raises(
        ValueError, match=r"cannot get object from non-absolute path 'A/B'"
    ):
        registry.get_by_path(XtcePath("A/B"))


def test_get_by_path_raises_for_unknown_absolute_path() -> None:
    """get_by_path should raise when no object is registered at the path."""
    registry = XtceRegistry()

    with pytest.raises(KeyError, match=r"no object registered at path '/A/B'"):
        registry.get_by_path(XtcePath("/A/B"))


def test_get_path_returns_registered_absolute_path() -> None:
    """get_path should return the original registered absolute path."""
    registry = XtceRegistry()
    path = XtcePath("/A/B")
    target = DummyXtceObject(name="B")

    registry.register(path, as_referenceable(target))

    assert registry.get_path(as_referenceable(target)) == path


def test_get_path_raises_for_unregistered_object() -> None:
    """get_path should raise for objects that were never registered."""
    registry = XtceRegistry()
    target = DummyXtceObject(name="B")

    with pytest.raises(KeyError, match="object not registered: DummyXtceObject"):
        registry.get_path(as_referenceable(target))


def test_resolve_absolute_path_returns_matching_definition() -> None:
    """Resolve should return absolute paths directly when present."""
    registry = XtceRegistry()
    path = XtcePath("/A/B")
    target = DummyXtceObject(name="B")
    scope = XtcePath("/IGNORED/SCOPE")

    registry.register(path, as_referenceable(target))

    result = registry.resolve(path, scope)

    assert result == ResolvedReference(path=path, target=as_referenceable(target))


def test_resolve_absolute_path_raises_when_missing() -> None:
    """Resolve should raise for absolute paths that are not registered."""
    registry = XtceRegistry()

    with pytest.raises(KeyError, match=r"failed to resolve absolute path '/A/B'"):
        registry.resolve(XtcePath("/A/B"), XtcePath("/SCOPE"))


def test_resolve_rejects_relative_scope() -> None:
    """Resolve should require an absolute scope for relative references."""
    registry = XtceRegistry()

    with pytest.raises(ValueError, match=r"scope must be absolute, got 'A/B'"):
        registry.resolve(XtcePath("C"), XtcePath("A/B"))


def test_resolve_relative_path_in_current_scope() -> None:
    """Resolve should find relative references within the provided scope."""
    registry = XtceRegistry()
    target = DummyXtceObject(name="C")

    registry.register(XtcePath("/A/B/C"), as_referenceable(target))

    result = registry.resolve(XtcePath("C"), XtcePath("/A/B"))

    assert result == ResolvedReference(
        path=XtcePath("/A/B/C"),
        target=as_referenceable(target),
    )


def test_resolve_relative_path_walks_up_parent_scopes() -> None:
    """Resolve should search parent scopes until it finds a matching path."""
    registry = XtceRegistry()
    target = DummyXtceObject(name="SharedType")

    registry.register(XtcePath("/A/SharedType"), as_referenceable(target))

    result = registry.resolve(XtcePath("SharedType"), XtcePath("/A/B/C"))

    assert result == ResolvedReference(
        path=XtcePath("/A/SharedType"),
        target=as_referenceable(target),
    )


def test_resolve_relative_path_prefers_nearest_scope_match() -> None:
    """Resolve should return the closest matching definition in the scope chain."""
    registry = XtceRegistry()
    parent_target = DummyXtceObject(name="SharedType-parent")
    child_target = DummyXtceObject(name="SharedType-child")

    registry.register(XtcePath("/A/SharedType"), as_referenceable(parent_target))
    registry.register(XtcePath("/A/B/SharedType"), as_referenceable(child_target))

    result = registry.resolve(XtcePath("SharedType"), XtcePath("/A/B/C"))

    assert result == ResolvedReference(
        path=XtcePath("/A/B/SharedType"),
        target=as_referenceable(child_target),
    )


def test_resolve_normalizes_relative_navigation_segments() -> None:
    """Resolve should normalize '..' segments while forming candidate paths."""
    registry = XtceRegistry()
    target = DummyXtceObject(name="SharedType")

    registry.register(XtcePath("/A/B/SharedType"), as_referenceable(target))

    result = registry.resolve(XtcePath("../SharedType"), XtcePath("/A/B/C"))

    assert result == ResolvedReference(
        path=XtcePath("/A/B/SharedType"),
        target=as_referenceable(target),
    )


def test_resolve_raises_after_exhausting_scope_chain() -> None:
    """Resolve should raise when no matching definition exists in any scope."""
    registry = XtceRegistry()

    with pytest.raises(
        KeyError,
        match=r"failed to resolve reference 'Missing' from scope '/A/B'",
    ):
        registry.resolve(XtcePath("Missing"), XtcePath("/A/B"))
